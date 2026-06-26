#!/usr/bin/env python3
"""Génère content/themes.json (page « Thèmes & arguments ») et content/argbank.json
à partir des fichiers source Markdown :
  - 5-sujets-par-frequence.md      → tableau des thèmes + stats
  - 6-top-sujets-par-theme.md      → top 5 des sujets par thème
  - 7-arguments-pour-contre-par-theme.md → 5 arguments pour / 5 contre par thème

Les trois fichiers listent les 26 thèmes dans le même ordre (fréquence décroissante) ;
l'association se fait donc par rang. Relancer ensuite `python3 build_site.py`.
"""
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CONTENT = BASE / "content"


def md_inline(s: str) -> str:
    s = s.strip().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)


def parse_theme_table() -> list[list[str]]:
    rows, mode = [], False
    for ln in (BASE / "5-sujets-par-frequence.md").read_text(encoding="utf-8").splitlines():
        if "| Rang | Thème" in ln:
            mode = True
            continue
        if mode:
            if not ln.lstrip().startswith("|"):
                break
            if set(ln.strip()) <= set("|-: "):
                continue
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) == 4 and cells[0].isdigit():
                rows.append([cells[0], md_inline(cells[1]), cells[2], cells[3]])
    if not any("Valeurs" in r[1] for r in rows):
        rows.append(["26", "<strong>Valeurs / savoir-vivre</strong>", "2", "0 %"])
    return rows


def parse_top5() -> list[dict]:
    themes, cur = [], None
    for ln in (BASE / "6-top-sujets-par-theme.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+\d+\.\s+(.+?)\s+—\s+\d+\s+sujets\s*$", ln)
        if m:
            cur = {"theme": m.group(1).strip(), "top5": []}
            themes.append(cur)
            continue
        im = re.match(r"^\d+\.\s+\*\*\[(\d+)×\]\*\*\s+(.+?)\s*$", ln)
        if im and cur:
            text = re.sub(r"\s*\*\([^)]*\)\*\s*$", "", im.group(2)).strip()
            cur["top5"].append({"c": int(im.group(1)), "s": text})
    return themes


def parse_args() -> list[dict]:
    themes, cur, mode = [], None, None
    for ln in (BASE / "7-arguments-pour-contre-par-theme.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+\d+\.\s+(.+?)\s*$", ln)
        if m:
            cur = {"theme": m.group(1).strip(), "pour": [], "contre": []}
            themes.append(cur)
            mode = None
            continue
        if ln.startswith("**✅ POUR"):
            mode = "pour"
            continue
        if ln.startswith("**❌ CONTRE"):
            mode = "contre"
            continue
        im = re.match(r"^\d+\.\s+\*\*(.+?)\*\*\s+—\s+(.*\S)\s*$", ln)
        if im and cur and mode:
            cur[mode].append({"k": im.group(1).strip(), "t": im.group(2).strip()})
    return themes


# barres top 10 : libellés courts + couleurs (catégories du design system)
BARS = [
    ("Immigration / intégration", 20, "var(--cat-immigration)"),
    ("Travail / carrière", 19, "var(--cat-travail)"),
    ("Éducation / études", 11, "var(--cat-education)"),
    ("Technologie / Internet", 9, "var(--cat-techno)"),
    ("Santé / mode de vie", 7, "var(--cat-sante)"),
    ("Tourisme / voyage", 6, "var(--cat-societe)"),
    ("Environnement / transports", 6, "var(--cat-environ)"),
    ("Famille / relations", 6, "var(--cat-medias)"),
    ("Téléphone / écrans", 5, "var(--cat-techno)"),
    ("Argent / réussite", 4, "var(--cat-societe)"),
]


def main() -> None:
    theme_rows = parse_theme_table()
    arg_themes = parse_args()
    top5_themes = parse_top5()
    assert len(arg_themes) == len(top5_themes) == 26, (len(arg_themes), len(top5_themes))
    for a, t in zip(arg_themes, top5_themes):
        a["top5"] = t["top5"]

    themes_page = {
        "eyebrow": "Stratégie · Tâche 3",
        "crumb": "Stratégie",
        "title": "Thèmes & arguments",
        "lede": "Quels sujets reviennent le plus, et quels arguments préparer. 723 sujets de la Tâche 3 relevés de 2022 à 2026, classés par thème, et une banque de 260 arguments prêts à l'emploi.",
        "sections": [
            {
                "id": "themes-frequence",
                "title": "Les thèmes les plus fréquents",
                "blocks": [
                    {"type": "prose", "html": "<p>Les sujets de la Tâche 3 sont reformulés d'un mois à l'autre, mais ils tournent autour d'un nombre limité de <strong>thèmes</strong>. En classant les 723 sujets relevés de janvier 2022 à juin 2026, on voit nettement lesquels reviennent le plus — et donc lesquels réviser en priorité.</p>"},
                    {"type": "stats", "items": [
                        {"value": "723", "label": "sujets analysés", "hint": "janv. 2022 → juin 2026"},
                        {"value": "26", "label": "thèmes", "hint": "identifiés et comptés"},
                        {"value": "260", "label": "arguments", "hint": "pour & contre", "color": "var(--accent)"},
                    ]},
                    {"type": "frequency", "bars": [{"label": l, "pct": p, "color": c} for (l, p, c) in BARS]},
                    {"type": "callout", "variant": "accent", "html": "Les <strong>6 premiers thèmes</strong> — Immigration, Travail, Éducation, Technologie, Santé et Tourisme — couvrent à eux seuls <strong>près de 72 %</strong> des sujets. Si vous les préparez solidement, vous êtes prêt(e) pour la grande majorité des tirages."},
                    {"type": "prose", "html": "<p>Le classement complet des 26 thèmes, du plus au moins fréquent :</p>"},
                    {"type": "table", "headers": ["Rang", "Thème", "Sujets", "%"], "rows": theme_rows},
                ],
            },
            {
                "id": "themes-arguments",
                "title": "Arguments pour et contre, par thème",
                "blocks": [
                    {"type": "prose", "html": "<p>Pour chaque thème : ses <strong>sujets les plus fréquents</strong>, puis <strong>5 arguments « pour »</strong> et <strong>5 « contre »</strong>, en français simple (niveau B2) et faciles à mémoriser. Les arguments sont volontairement <strong>généraux</strong> : un même argument peut servir pour la plupart des sujets du thème.</p>"},
                    {"type": "callout", "variant": "info", "html": "Les sujets listés sont des <strong>formulations générales</strong> qui regroupent toutes les variantes d'une même idée — ce n'est pas le libellé exact tiré le jour du test, mais le fond du sujet. Le chiffre (ex. « 9× ») indique le nombre d'apparitions relevées depuis 2022."},
                    {"type": "argbank"},
                ],
            },
        ],
    }

    CONTENT.mkdir(exist_ok=True)
    (CONTENT / "themes.json").write_text(json.dumps(themes_page, ensure_ascii=False, indent=2), encoding="utf-8")
    (CONTENT / "argbank.json").write_text(json.dumps({"themes": arg_themes}, ensure_ascii=False, indent=2), encoding="utf-8")

    tot = sum(len(t["pour"]) + len(t["contre"]) for t in arg_themes)
    print(f"themes.json : {len(theme_rows)} thèmes au tableau")
    print(f"argbank.json : {len(arg_themes)} thèmes · {tot} arguments · "
          f"{sum(len(t['top5']) for t in arg_themes)} sujets (top 5)")


if __name__ == "__main__":
    main()
