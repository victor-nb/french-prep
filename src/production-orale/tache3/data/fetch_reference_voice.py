#!/usr/bin/env python3
"""Récupère une voix de référence française (humaine, libre) pour le clonage TTS.

On extrait un court extrait de parole lue, clair et naturel, du jeu de données
**FLEURS** (``google/fleurs``, sous-ensemble ``fr_fr``, licence CC-BY 4.0) avec sa
transcription. Higgs Audio v3 clone ensuite ce timbre humain pour TOUTES les réponses
(``tts.py``) — c'est le principal levier pour un rendu « le moins synthétique possible »
et pour garder la même voix d'un fichier à l'autre.

Sortie : ``data/voix-reference.wav`` (mono 24 kHz) + ``data/voix-reference.txt``.

Pour utiliser une autre voix (par ex. la vôtre), remplacez simplement ces deux fichiers :
un extrait .wav de ~8-15 s et sa transcription exacte en .txt.
"""
from __future__ import annotations

import io
from pathlib import Path

import soundfile as sf
from datasets import Audio, load_dataset
from scipy.signal import resample_poly

HERE = Path(__file__).resolve().parent
WAV_OUT = HERE / "voix-reference.wav"
TXT_OUT = HERE / "voix-reference.txt"
TARGET_SR = 24_000
MIN_S, MAX_S = 8.0, 15.0


def fetch() -> None:
    ds = load_dataset(
        "google/fleurs", "fr_fr", split="validation", streaming=True
    ).cast_column("audio", Audio(decode=False))
    for sample in ds:
        raw = sample["audio"]["bytes"]
        wave, sr = sf.read(io.BytesIO(raw), dtype="float32")
        if wave.ndim > 1:
            wave = wave.mean(axis=1)
        duration = len(wave) / sr
        transcript = sample["transcription"].strip()
        if MIN_S <= duration <= MAX_S and transcript:
            if sr != TARGET_SR:
                wave = resample_poly(wave, TARGET_SR, sr)
            sf.write(WAV_OUT, wave, TARGET_SR)
            TXT_OUT.write_text(transcript + "\n", encoding="utf-8")
            print(f"Référence : {duration:.1f}s — « {transcript} »")
            print(f"  -> {WAV_OUT.name} + {TXT_OUT.name}")
            return
    raise RuntimeError("Aucun extrait FLEURS entre 8 et 15 s trouvé.")


if __name__ == "__main__":
    fetch()
