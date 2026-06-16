#!/usr/bin/env python3
"""Synthèse vocale des réponses modèles de la Tâche 3 (Higgs Audio v3, voix clonée).

Pour rendre la voix « le moins synthétique possible », on n'utilise PAS la voix par
défaut du modèle (timbre aléatoire à chaque appel) : on **clone une vraie voix humaine**
à partir de ``data/voix-reference.wav`` (+ sa transcription ``.txt``). Le même timbre est
réutilisé pour tous les fichiers. On découpe aussi chaque réponse en phrases courtes
(générations plus stables, prosodie plus naturelle) recollées avec de brèves pauses.

Usage :
    python3 tts.py                 # toutes les réponses manquantes -> audio/tache3/*.mp3
    python3 tts.py --ranks 1-20    # seulement les rangs 1 à 20
    python3 tts.py --limit 5       # les 5 premières (test)
    python3 tts.py --force         # régénère même si l'audio existe déjà

Le modèle (~4B) tourne en local sur Apple Silicon (MLX). La voix de référence est
remplaçable : déposez votre propre extrait .wav (~8-15 s) + .txt pour cloner une autre voix.
"""
from __future__ import annotations

import argparse
import gc
import re
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

import mlx.core as mx
import numpy as np
import soundfile as sf

HERE = Path(__file__).resolve().parent
EXAMPLES_DIR = HERE / "examples"
REF_WAV = HERE / "data" / "voix-reference.wav"
REF_TXT = HERE / "data" / "voix-reference.txt"
OUT_DIR = EXAMPLES_DIR / "audio"
MODEL_REPO = "bosonai/higgs-audio-v3-tts-4b"

_AUDIO_RE = re.compile(r"<!--\s*AUDIO:START\s*-->(.*?)<!--\s*AUDIO:END\s*-->", re.S)
_SUJET_RE = re.compile(r'^sujet:\s*"?(.*?)"?\s*$', re.M)
_SENTENCE_RE = re.compile(r"[^.!?…]+[.!?…]+(?:\s|$)|\S[^.!?…]*$")

MAX_CHUNK_CHARS = 240
PAUSE_SENTENCE_S = 0.28
PAUSE_PARAGRAPH_S = 0.55


def parse_example(path: Path) -> tuple[str, str] | None:
    """Renvoie (sujet, texte_audio) depuis un fichier exemple, ou None si absent."""
    text = path.read_text(encoding="utf-8")
    audio_match = _AUDIO_RE.search(text)
    sujet_match = _SUJET_RE.search(text)
    if not audio_match or not sujet_match:
        return None
    return sujet_match.group(1).strip(), audio_match.group(1).strip()


def chunk_paragraph(paragraph: str) -> list[str]:
    """Découpe un paragraphe en groupes de phrases <= MAX_CHUNK_CHARS."""
    sentences = [s.strip() for s in _SENTENCE_RE.findall(paragraph) if s.strip()]
    chunks: list[str] = []
    current = ""
    for sentence in sentences:
        if current and len(current) + len(sentence) + 1 > MAX_CHUNK_CHARS:
            chunks.append(current)
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
    if current:
        chunks.append(current)
    return chunks


def build_chunks(sujet: str, audio_text: str, *, say_sujet: bool) -> list[tuple[str, bool]]:
    """Liste (texte, pause_paragraphe_après) prête pour la synthèse."""
    chunks: list[tuple[str, bool]] = []
    if say_sujet:
        chunks.append((f"Sujet : {sujet}.", True))
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", audio_text) if p.strip()]
    for paragraph in paragraphs:
        pieces = chunk_paragraph(paragraph)
        for i, piece in enumerate(pieces):
            chunks.append((piece, i == len(pieces) - 1))
    return chunks


class Synthesizer:
    """Charge le modèle une fois et synthétise du texte avec la voix clonée."""

    def __init__(self, *, temperature: float, top_p: float, top_k: int, seed: int) -> None:
        from mlx_audio.tts.utils import load_model

        if not REF_WAV.exists() or not REF_TXT.exists():
            raise FileNotFoundError(
                f"Voix de référence absente. Lancez d'abord :\n"
                f"  python3 data/fetch_reference_voice.py\n"
                f"(attendu : {REF_WAV} + {REF_TXT})"
            )
        self.model = load_model(MODEL_REPO)
        self.sample_rate: int = self.model.sample_rate
        self.ref_audio = str(REF_WAV)
        self.ref_text = REF_TXT.read_text(encoding="utf-8").strip()
        self.seed = seed
        self._params = dict(temperature=temperature, top_p=top_p, top_k=top_k)

    def _generate(self, text: str, *, seed: int, max_frames: int) -> np.ndarray:
        segments = [
            np.asarray(result.audio, dtype=np.float32)
            for result in self.model.generate(
                text=text,
                ref_audio=self.ref_audio,
                ref_text=self.ref_text,
                seed=seed,
                max_new_tokens=max_frames,
                **self._params,
            )
        ]
        return np.concatenate(segments) if segments else np.zeros(0, dtype=np.float32)

    def say(self, text: str) -> np.ndarray:
        # 25 fps ; on borne la durée d'un segment à ~2.2 frames/caractère (+marge),
        # ce qui évite l'emballement (« runaway ») d'un segment qui n'émet pas son
        # token de fin et générerait des secondes de babillage répété.
        max_frames = min(1024, int(len(text) * 2.2) + 60)
        tolerated_s = max(7.0, len(text) / 11.0)  # durée plausible pour ce texte
        best = self._generate(text, seed=self.seed, max_frames=max_frames)
        for retry in range(2):
            if len(best) / self.sample_rate <= tolerated_s:
                return best
            candidate = self._generate(
                text, seed=self.seed + 7919 * (retry + 1), max_frames=max_frames
            )
            if len(candidate) < len(best):
                best = candidate
        return best

    def render(self, chunks: list[tuple[str, bool]]) -> np.ndarray:
        sentence_gap = np.zeros(int(PAUSE_SENTENCE_S * self.sample_rate), dtype=np.float32)
        paragraph_gap = np.zeros(int(PAUSE_PARAGRAPH_S * self.sample_rate), dtype=np.float32)
        out: list[np.ndarray] = []
        for text, ends_paragraph in chunks:
            out.append(self.say(text))
            out.append(paragraph_gap if ends_paragraph else sentence_gap)
        return np.concatenate(out) if out else np.zeros(0, dtype=np.float32)


def write_audio(
    wave: np.ndarray, sample_rate: int, dest: Path, audio_format: str, speed: float
) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if audio_format == "wav" and speed == 1.0:
        sf.write(dest, wave, sample_rate)
        return
    # wav temporaire puis ffmpeg : atempo ralentit le débit sans modifier la hauteur
    tmp = dest.with_suffix(".tmp.wav")
    sf.write(tmp, wave, sample_rate)
    tempo = [] if speed == 1.0 else ["-filter:a", f"atempo={speed}"]
    encode = (
        [] if audio_format == "wav"
        else ["-codec:a", "libmp3lame" if audio_format == "mp3" else "aac", "-qscale:a", "2"]
    )
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), *tempo, *encode, str(dest)],
        check=True,
    )
    tmp.unlink(missing_ok=True)


def iter_examples(ranks: range | None, limit: int | None) -> Iterator[Path]:
    files = sorted(EXAMPLES_DIR.glob("[0-9][0-9][0-9]-*.md"))
    count = 0
    for path in files:
        rank = int(path.name[:3])
        if ranks is not None and rank not in ranks:
            continue
        yield path
        count += 1
        if limit is not None and count >= limit:
            return


def parse_ranks(spec: str | None) -> range | None:
    if not spec:
        return None
    start, _, end = spec.partition("-")
    return range(int(start), int(end or start) + 1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ranks", help="plage de rangs, ex. 1-20")
    parser.add_argument("--limit", type=int, help="nombre max de fichiers")
    parser.add_argument("--format", default="mp3", choices=("mp3", "wav", "m4a"))
    parser.add_argument(
        "--speed", type=float, default=0.9,
        help="débit de parole (1.0 = normal, <1 plus lent ; défaut 0.9)",
    )
    parser.add_argument("--force", action="store_true", help="régénère même si présent")
    parser.add_argument("--no-sujet", action="store_true", help="ne pas lire l'intitulé")
    parser.add_argument("--temperature", type=float, default=0.8)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args(argv)

    ranks = parse_ranks(args.ranks)
    todo: list[tuple[Path, Path]] = []
    for path in iter_examples(ranks, args.limit):
        dest = OUT_DIR / f"{path.stem}.{args.format}"
        if dest.exists() and not args.force:
            continue
        todo.append((path, dest))

    if not todo:
        print("Rien à générer (tout est déjà synthétisé — utilisez --force pour refaire).")
        return 0

    print(f"{len(todo)} fichier(s) à synthétiser → {OUT_DIR}")
    synth = Synthesizer(
        temperature=args.temperature, top_p=args.top_p, top_k=args.top_k, seed=args.seed
    )
    for i, (src, dest) in enumerate(todo, start=1):
        parsed = parse_example(src)
        if parsed is None:
            print(f"  [{i}/{len(todo)}] ⏭  {src.name} (bloc AUDIO introuvable)")
            continue
        sujet, audio_text = parsed
        chunks = build_chunks(sujet, audio_text, say_sujet=not args.no_sujet)
        wave = synth.render(chunks)
        write_audio(wave, synth.sample_rate, dest, args.format, args.speed)
        seconds = len(wave) / synth.sample_rate / args.speed
        print(f"  [{i}/{len(todo)}] ✅ {dest.name}  ({seconds:4.0f}s)", flush=True)
        # libère la mémoire MLX entre chaque fichier (batch de 214 stable)
        del wave
        mx.clear_cache()
        gc.collect()
    return 0


if __name__ == "__main__":
    sys.exit(main())
