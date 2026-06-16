#!/usr/bin/env python3
"""Génère une page web statique (GitHub Pages) pour réviser les réponses Tâche 3.

Lit ``examples/_index.json`` + les fichiers ``examples/NNN-*.md`` et produit un
``index.html`` autonome (données JSON intégrées) à la racine du dépôt : liste des
sujets triés par priorité, recherche, filtre par thème, texte de la réponse modèle
repliable, et un lecteur audio par sujet (``audio/tache3/NNN-slug.mp3``).

Servi tel quel par GitHub Pages (source = branche `main`, dossier `/`) :
    https://<user>.github.io/<repo>/

Exécuter depuis ``src/production-orale/tache3/`` :  ``python3 build_site.py``
"""
from __future__ import annotations

import json
import re
from pathlib import Path

__all__ = ["build_site"]

HERE = Path(__file__).resolve().parent
EXAMPLES_DIR = HERE / "examples"
INDEX_JSON = EXAMPLES_DIR / "_index.json"
REPO_ROOT = HERE.parents[2]
OUT_HTML = REPO_ROOT / "index.html"
AUDIO_REL = "src/production-orale/tache3/examples/audio"

_AUDIO_RE = re.compile(r"<!--\s*AUDIO:START\s*-->(.*?)<!--\s*AUDIO:END\s*-->", re.S)


def _answer_paragraphs(example_path: Path) -> list[str]:
    match = _AUDIO_RE.search(example_path.read_text(encoding="utf-8"))
    if not match:
        return []
    return [p.strip() for p in re.split(r"\n\s*\n", match.group(1).strip()) if p.strip()]


def _collect() -> list[dict[str, object]]:
    entries = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    items: list[dict[str, object]] = []
    for entry in entries:
        path = EXAMPLES_DIR / str(entry["filename"])
        if not path.exists():
            continue
        items.append(
            {
                "rank": entry["rank"],
                "freq": entry["frequency"],
                "sujet": entry["subject"],
                "themes": entry["themes"],
                "audio": f"{AUDIO_REL}/{path.stem}.mp3",
                "answer": _answer_paragraphs(path),
            }
        )
    return items


def build_site() -> Path:
    items = _collect()
    themes = sorted({t for it in items for t in it["themes"]})  # type: ignore[union-attr]
    payload = json.dumps(items, ensure_ascii=False)
    OUT_HTML.write_text(
        _TEMPLATE.replace("__DATA__", payload).replace(
            "__THEMES__", json.dumps(themes, ensure_ascii=False)
        ).replace("__COUNT__", str(len(items))),
        encoding="utf-8",
    )
    return OUT_HTML


_TEMPLATE = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TCF Canada — Tâche 3 : réponses modèles & audios</title>
<style>
  :root { --bg:#0f1220; --card:#1a1f33; --ink:#e8ebf5; --mut:#9aa3c0; --acc:#6ea8fe; --bd:#2a3150; }
  * { box-sizing:border-box; }
  body { margin:0; font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
         background:var(--bg); color:var(--ink); }
  header { padding:28px 20px 12px; max-width:920px; margin:0 auto; }
  h1 { margin:0 0 6px; font-size:1.5rem; }
  .sub { color:var(--mut); margin:0 0 16px; }
  .controls { position:sticky; top:0; z-index:5; background:var(--bg);
              padding:12px 20px; max-width:920px; margin:0 auto;
              display:flex; gap:10px; flex-wrap:wrap; border-bottom:1px solid var(--bd); }
  input,select { background:var(--card); color:var(--ink); border:1px solid var(--bd);
                 border-radius:8px; padding:9px 12px; font-size:.95rem; }
  input#q { flex:1 1 220px; }
  label.chk { color:var(--mut); display:flex; align-items:center; gap:6px; font-size:.9rem; }
  main { max-width:920px; margin:0 auto; padding:14px 20px 60px; }
  .count { color:var(--mut); font-size:.85rem; margin:10px 2px; }
  .card { background:var(--card); border:1px solid var(--bd); border-radius:12px;
          padding:16px 18px; margin:12px 0; }
  .top { display:flex; gap:10px; align-items:baseline; flex-wrap:wrap; }
  .rank { color:var(--mut); font-size:.8rem; }
  .badge { background:#243; color:#9f9; border-radius:20px; padding:2px 9px; font-size:.72rem; }
  .badge.hot { background:#3a2740; color:#f6a; }
  h2 { font-size:1.05rem; margin:6px 0 8px; }
  .themes { color:var(--acc); font-size:.78rem; margin-bottom:10px; }
  audio { width:100%; margin:4px 0 8px; }
  details { border-top:1px solid var(--bd); padding-top:8px; }
  summary { cursor:pointer; color:var(--mut); font-size:.85rem; }
  details p { margin:.7em 0; }
  .empty { color:var(--mut); text-align:center; padding:40px; }
  footer { color:var(--mut); text-align:center; font-size:.8rem; padding:20px; }
  a { color:var(--acc); }
</style>
</head>
<body>
<header>
  <h1>TCF Canada — Tâche 3 · réponses modèles</h1>
  <p class="sub"><strong>__COUNT__</strong> sujets de 2026, dédupliqués et triés par
     <strong>priorité</strong> (fréquence d'apparition). Texte modèle B2 + audio à écouter
     (voix humaine clonée). Astuce&nbsp;: écoutez puis faites du <em>shadowing</em>.</p>
</header>
<div class="controls">
  <input id="q" type="search" placeholder="Rechercher un sujet…" autocomplete="off">
  <select id="theme"><option value="">Tous les thèmes</option></select>
  <label class="chk"><input id="prio" type="checkbox"> Sujets récurrents seulement</label>
</div>
<main>
  <div class="count" id="count"></div>
  <div id="list"></div>
  <div class="empty" id="empty" hidden>Aucun sujet ne correspond.</div>
</main>
<footer>Généré par <code>build_site.py</code> · audios via <code>make speak</code> ·
  les lecteurs restent muets tant que le mp3 n'est pas encore généré.</footer>
<script>
const DATA = __DATA__;
const THEMES = __THEMES__;
const $ = s => document.querySelector(s);
const norm = s => s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
const sel = $('#theme');
for (const t of THEMES) { const o=document.createElement('option'); o.value=t; o.textContent=t; sel.appendChild(o); }
function esc(s){ const d=document.createElement('div'); d.textContent=s; return d.innerHTML; }
function card(it){
  const hot = it.freq>1 ? `<span class="badge hot">${it.freq}× récurrent</span>` : '';
  const ans = it.answer.map(p=>`<p>${esc(p)}</p>`).join('');
  return `<article class="card">
    <div class="top"><span class="rank">#${it.rank}</span>${hot}</div>
    <h2>${esc(it.sujet)}</h2>
    <div class="themes">${it.themes.map(esc).join(' · ')}</div>
    <audio controls preload="none" src="${it.audio}"></audio>
    <details><summary>Voir la réponse modèle</summary>${ans}</details>
  </article>`;
}
function render(){
  const q = norm($('#q').value.trim());
  const th = sel.value;
  const prio = $('#prio').checked;
  const out = DATA.filter(it =>
    (!q || norm(it.sujet).includes(q)) &&
    (!th || it.themes.includes(th)) &&
    (!prio || it.freq>1));
  $('#list').innerHTML = out.map(card).join('');
  $('#count').textContent = `${out.length} sujet(s)`;
  $('#empty').hidden = out.length>0;
}
$('#q').addEventListener('input', render);
sel.addEventListener('change', render);
$('#prio').addEventListener('change', render);
render();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    out = build_site()
    print(f"Page générée : {out}")
    print(f"  Activez GitHub Pages (Settings → Pages → branche main, dossier /) :")
    print(f"  puis ouvrez https://<user>.github.io/<repo>/")
