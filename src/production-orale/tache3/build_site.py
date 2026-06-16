#!/usr/bin/env python3
"""Génère le site statique « Préparation TCF Canada » (GitHub Pages).

Recréation fidèle, en HTML/CSS/JS pur (sans build), du design system exporté depuis
Claude Design : look éditorial (papier crème, encre marine, bleu encre, serif Spectral
pour les sujets, Hanken Grotesk pour l'UI, IBM Plex Mono pour les métadonnées). Trois
vues — Accueil, Banque de sujets, Méthode — alimentées par les 214 réponses réelles.

Lit ``examples/_index.json`` + les fichiers ``examples/NNN-*.md`` et écrit ``index.html``
à la racine du dépôt. Audios servis depuis ``examples/audio/`` (versionnés).

Exécuter depuis ``src/production-orale/tache3/`` :  ``python3 build_site.py``
"""
from __future__ import annotations

import json
import re
from pathlib import Path

__all__ = ["build_site"]

HERE = Path(__file__).resolve().parent
EXAMPLES_DIR = HERE / "examples"
AUDIO_DIR = EXAMPLES_DIR / "audio"
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
                "frequency": entry["frequency"],
                "subject": entry["subject"],
                "themes": entry["themes"],
                "audio": f"{AUDIO_REL}/{path.stem}.mp3",
                "answer": _answer_paragraphs(path),
            }
        )
    return items


def build_site() -> Path:
    items = _collect()
    payload = json.dumps(items, ensure_ascii=False, separators=(",", ":"))
    html = (
        _TEMPLATE
        .replace("/*__DATA__*/null", payload)
        .replace("__COUNT__", str(len(items)))
    )
    OUT_HTML.write_text(html, encoding="utf-8")
    return OUT_HTML


_TEMPLATE = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Préparation TCF Canada — Expression orale</title>
<meta name="description" content="214 réponses modèles B2 à la Tâche 3 du TCF Canada, classées par fréquence, avec audio et la structure passe-partout pour parler 4 min 30 sans blanc.">
<style>
@import url('https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Hanken+Grotesk:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root{
  --paper-0:#FBF8F2; --paper-1:#FFFFFF; --paper-2:#F4EFE5; --paper-3:#ECE5D6;
  --ink-900:#16203A; --ink-800:#232F4D; --ink-700-s:#344061; --ink-500:#4A5474; --ink-muted:#6B7491; --ink-faint:#99A0B5;
  --line-strong:#D9CFBC; --line:#E6DECE; --line-soft:#F0E9DB;
  --bleu-900:#16235E; --bleu-800:#1D2F7E; --bleu-700:#243C9E; --bleu-600:#2B49C0; --bleu-500:#4863D6; --bleu-200:#C3CDF4; --bleu-100:#E4E9FB; --bleu-050:#F0F3FD;
  --ochre-700:#9C5A1E; --ochre-600:#C0742A; --ochre-500:#D88A3C; --ochre-100:#F8E9D6; --ochre-050:#FCF4E9;
  --vert-700:#1F7A4D; --vert-600:#2A8F5C; --vert-100:#DCEFE3; --vert-050:#EEF7F1;
  --rouge-700:#A8302B; --rouge-600:#C73B34; --rouge-100:#F7DEDC;
  --bg-app:var(--paper-0); --surface-card:var(--paper-1); --surface-sunken:var(--paper-2); --surface-rail:var(--paper-3);
  --text-strong:var(--ink-900); --text-body:var(--ink-800); --text-secondary:var(--ink-700-s); --text-muted:var(--ink-muted); --text-faint:var(--ink-faint);
  --text-on-brand:#FFFFFF; --text-link:var(--bleu-600);
  --border-default:var(--line); --border-strong:var(--line-strong); --border-soft:var(--line-soft);
  --brand:var(--bleu-600); --brand-hover:var(--bleu-700); --brand-active:var(--bleu-800); --brand-tint:var(--bleu-100); --brand-wash:var(--bleu-050);
  --accent:var(--ochre-600); --accent-tint:var(--ochre-100); --accent-wash:var(--ochre-050);
  --success:var(--vert-600); --success-tint:var(--vert-100); --danger:var(--rouge-600);
  --cat-immigration:#2B49C0; --cat-travail:#9C5A1E; --cat-education:#6B3FA0; --cat-sante:#2A8F5C;
  --cat-medias:#B23A48; --cat-techno:#1B7F94; --cat-environ:#4C7A2E; --cat-societe:#735C3A;
  --font-display:'Spectral',Georgia,'Times New Roman',serif;
  --font-sans:'Hanken Grotesk',system-ui,-apple-system,'Segoe UI',sans-serif;
  --font-mono:'IBM Plex Mono',ui-monospace,'SFMono-Regular',Menlo,monospace;
  --text-3xs:.6875rem; --text-2xs:.75rem; --text-xs:.8125rem; --text-sm:.875rem; --text-base:1rem; --text-md:1.125rem; --text-lg:1.3125rem; --text-xl:1.625rem; --text-2xl:2rem; --text-3xl:2.5rem; --text-4xl:3.25rem;
  --fw-regular:400; --fw-medium:500; --fw-semibold:600; --fw-bold:700; --fw-black:800;
  --lh-tight:1.12; --lh-snug:1.28; --lh-normal:1.5; --lh-relaxed:1.68;
  --space-1:.25rem; --space-2:.5rem; --space-3:.75rem; --space-4:1rem; --space-5:1.5rem; --space-6:2rem; --space-7:2.5rem; --space-8:3rem; --space-9:4rem;
  --radius-xs:4px; --radius-sm:7px; --radius-md:11px; --radius-lg:16px; --radius-xl:22px; --radius-pill:999px;
  --container:1120px; --container-narrow:760px;
  --shadow-xs:0 1px 2px rgba(22,32,58,.05);
  --shadow-sm:0 1px 2px rgba(22,32,58,.05),0 2px 6px rgba(22,32,58,.05);
  --shadow-md:0 2px 4px rgba(22,32,58,.05),0 8px 20px rgba(22,32,58,.07);
  --shadow-lg:0 4px 8px rgba(22,32,58,.06),0 18px 40px rgba(22,32,58,.10);
  --shadow-focus:0 0 0 3px rgba(43,73,192,.28);
  --t-fast:120ms cubic-bezier(.22,1,.36,1); --t-base:200ms cubic-bezier(.22,1,.36,1);
}

*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--bg-app);color:var(--text-body);font-family:var(--font-sans);font-size:var(--text-base);line-height:var(--lh-normal);font-weight:var(--fw-regular);-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
h1,h2,h3,h4{font-family:var(--font-display);color:var(--text-strong);font-weight:var(--fw-semibold);line-height:var(--lh-tight);letter-spacing:-.01em;margin:0 0 var(--space-3);text-wrap:balance}
h1{font-size:var(--text-3xl)} h2{font-size:var(--text-2xl)} h3{font-size:var(--text-xl)}
p{margin:0 0 var(--space-4);text-wrap:pretty}
a{color:var(--text-link);text-decoration:none} a:hover{text-decoration:underline;text-underline-offset:2px}
strong,b{font-weight:var(--fw-bold);color:var(--text-strong)}
button{font-family:inherit}
::selection{background:var(--bleu-200);color:var(--ink-900)}
:focus-visible{outline:none;box-shadow:var(--shadow-focus);border-radius:var(--radius-xs)}
svg{display:inline-block;vertical-align:middle;flex:0 0 auto}
.eyebrow{font-family:var(--font-mono);font-size:var(--text-3xs);font-weight:var(--fw-medium);letter-spacing:.12em;text-transform:uppercase;color:var(--text-muted)}
.container{max-width:var(--container);margin:0 auto;padding-left:var(--space-5);padding-right:var(--space-5)}

/* ---- buttons ---- */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:42px;padding:10px 18px;font-family:var(--font-sans);font-size:var(--text-sm);font-weight:var(--fw-semibold);letter-spacing:.005em;line-height:1;border-radius:var(--radius-md);border:1px solid transparent;cursor:pointer;white-space:nowrap;transition:background var(--t-fast),border-color var(--t-fast),color var(--t-fast),transform var(--t-fast),box-shadow var(--t-fast)}
.btn-sm{min-height:34px;padding:7px 13px;gap:6px}
.btn-lg{min-height:50px;padding:13px 24px;gap:9px;font-size:var(--text-base)}
.btn-primary{background:var(--brand);color:var(--text-on-brand);box-shadow:0 1px 2px rgba(22,32,58,.12)}
.btn-primary:hover{background:var(--brand-hover);transform:translateY(-1px)}
.btn-accent{background:var(--accent);color:#fff;box-shadow:0 1px 2px rgba(22,32,58,.12)}
.btn-accent:hover{background:var(--ochre-700);transform:translateY(-1px)}
.btn-outline{background:var(--surface-card);color:var(--text-strong);border-color:var(--border-strong)}
.btn-outline:hover{background:var(--surface-sunken)}

/* ---- badges ---- */
.badge{display:inline-flex;align-items:center;gap:5px;padding:3px 9px;border-radius:var(--radius-pill);font-family:var(--font-mono);font-size:var(--text-2xs);font-weight:var(--fw-medium);letter-spacing:.04em;line-height:1.3;white-space:nowrap}
.badge-sm{font-size:var(--text-3xs);padding:2px 7px;gap:4px}
.badge-neutral{background:var(--paper-2);color:var(--text-secondary)}
.badge-brand{background:var(--bleu-100);color:var(--bleu-800)}
.badge-accent{background:var(--ochre-100);color:var(--ochre-700)}
.badge-success{background:var(--vert-100);color:var(--vert-700)}
.badge-hot{background:var(--ochre-100);color:var(--ochre-700)}

/* ---- card ---- */
.card{position:relative;background:var(--surface-card);border:1px solid var(--border-default);border-radius:var(--radius-lg);box-shadow:var(--shadow-sm);overflow:hidden}
.card-pad-md{padding:var(--space-5)} .card-pad-lg{padding:var(--space-6)}
.card-floating{box-shadow:var(--shadow-md)}
.card-interactive{transition:box-shadow var(--t-base),transform var(--t-base),border-color var(--t-base)}
.card-interactive:hover{box-shadow:var(--shadow-md);transform:translateY(-2px);border-color:var(--border-strong)}

/* ---- header ---- */
.site-header{position:sticky;top:0;z-index:50;background:rgba(251,248,242,.86);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid var(--border-default)}
.site-header .inner{max-width:var(--container);margin:0 auto;height:68px;padding:0 var(--space-5);display:flex;align-items:center;gap:var(--space-6)}
.site-nav{display:flex;gap:4px;margin-left:8px}
.nav-link{font-family:var(--font-sans);font-size:var(--text-sm);font-weight:600;padding:8px 13px;border-radius:var(--radius-sm);border:none;cursor:pointer;background:transparent;color:var(--text-secondary);transition:background var(--t-fast),color var(--t-fast)}
.nav-link:hover{background:var(--surface-sunken)}
.nav-link.active{background:var(--brand-tint);color:var(--bleu-800)}
.header-right{margin-left:auto;display:flex;align-items:center;gap:10px}
.objectif-pill{display:inline-flex;align-items:center;gap:7px;font-family:var(--font-mono);font-size:var(--text-2xs);letter-spacing:.04em;color:var(--vert-700);background:var(--vert-050);padding:5px 11px;border-radius:var(--radius-pill);border:1px solid var(--vert-100)}
.objectif-pill .dot{width:7px;height:7px;border-radius:50%;background:var(--success)}

/* ---- logo ---- */
.logo{display:inline-flex;align-items:center;gap:11px}
.logo .mark{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:9px;background:var(--bleu-600);color:#FBF8F2;font-family:var(--font-display);font-weight:600;font-size:22px;line-height:1;padding-bottom:2px;box-shadow:0 1px 2px rgba(22,32,58,.18),inset 0 1px 0 rgba(255,255,255,.16)}
.logo .wm{display:flex;flex-direction:column;line-height:1}
.logo .wm .t{font-family:var(--font-display);font-weight:600;font-size:19px;letter-spacing:-.01em;color:var(--ink-900)}
.logo .wm .s{font-family:var(--font-mono);font-weight:500;font-size:9.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--text-muted);margin-top:3px}
.logo.sm .mark{width:28px;height:28px;font-size:18px;border-radius:7px}
.logo.sm .wm .t{font-size:16px}

/* ---- hero / sections ---- */
.hero{border-bottom:1px solid var(--border-soft);background:linear-gradient(180deg,var(--paper-1) 0%,var(--paper-0) 100%)}
.hero .grid{max-width:var(--container);margin:0 auto;padding:var(--space-9) var(--space-5);display:grid;grid-template-columns:1.25fr .9fr;gap:var(--space-8);align-items:center}
.hero h1{font-size:var(--text-4xl);line-height:1.04;margin:0 0 18px;letter-spacing:-.025em}
.hero h1 em{font-weight:500;color:var(--bleu-700);font-style:italic}
.hero .lede{font-size:var(--text-md);color:var(--text-secondary);max-width:46ch;margin:0 0 28px;line-height:1.6}
.section{max-width:var(--container);margin:0 auto;padding:var(--space-9) var(--space-5)}
.section-band{background:var(--paper-1);border-top:1px solid var(--border-soft);border-bottom:1px solid var(--border-soft)}
.sec-head{display:flex;align-items:baseline;justify-content:space-between;gap:16px;margin-bottom:28px}

/* ---- score scale ---- */
.score-scale{width:100%}
.score-scale .bands{position:relative;height:30px;display:flex;border-radius:var(--radius-pill);overflow:hidden;border:1px solid var(--border-default)}
.score-scale .band{flex:1;display:flex;align-items:center;justify-content:center;font-family:var(--font-mono);font-size:var(--text-2xs);font-weight:600;letter-spacing:.05em;color:var(--text-muted);border-right:1px solid rgba(255,255,255,.6);position:relative}
.score-scale .band.b2{color:var(--vert-700)}
.score-scale .band.b2::after{content:"";position:absolute;inset:0;border:2px solid var(--success);border-radius:2px}
.score-scale .tick{position:absolute;top:-4px;bottom:-4px;width:2px;background:var(--ink-900);transform:translateX(-1px)}
.score-scale .legend{display:flex;justify-content:space-between;margin-top:7px;font-family:var(--font-mono);font-size:var(--text-3xs);color:var(--text-faint);letter-spacing:.04em}
.score-scale .legend .mid{color:var(--vert-700)}

/* ---- level badge ---- */
.level-badge{display:inline-flex;flex-direction:column;align-items:center;gap:3px}
.level-badge .box{display:inline-flex;align-items:center;justify-content:center;min-width:36px;height:36px;padding:0 10px;border-radius:var(--radius-md);background:var(--success);border:1px solid var(--vert-700);color:#fff;font-family:var(--font-display);font-weight:var(--fw-bold);font-size:var(--text-sm);line-height:1;box-shadow:var(--shadow-sm)}
.level-badge .sub{font-family:var(--font-mono);font-size:var(--text-3xs);letter-spacing:.06em;color:var(--vert-700);font-weight:500}

/* ---- stat card ---- */
.stat-card{display:flex;flex-direction:column;gap:4px;padding:var(--space-5);background:var(--surface-card);border:1px solid var(--border-default);border-radius:var(--radius-lg);box-shadow:var(--shadow-xs)}
.stat-card .val{font-family:var(--font-display);font-weight:var(--fw-bold);font-size:var(--text-3xl);line-height:1;letter-spacing:-.02em;color:var(--brand)}
.stat-card .lab{font-size:var(--text-sm);font-weight:var(--fw-semibold);color:var(--text-strong);margin-top:4px}
.stat-card .hint{font-size:var(--text-xs);color:var(--text-muted);line-height:1.4}

/* ---- tasks ---- */
.task-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--space-5)}
.task-icon{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:var(--radius-md);background:var(--surface-sunken);color:var(--text-secondary)}
.task-num{font-family:var(--font-display);font-size:var(--text-3xl);font-weight:700;color:var(--line-strong);line-height:1}
.task.focus .task-icon{background:var(--brand);color:#fff}
.task.focus .task-num{color:var(--bleu-600)}
.task.focus{border-color:var(--bleu-200)}

/* ---- theme bars ---- */
.theme-row .top{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px}
.theme-row .name{display:inline-flex;align-items:center;gap:9px;font-size:var(--text-sm);font-weight:600;color:var(--text-strong)}
.theme-row .name .dot{width:11px;height:11px;border-radius:50%}
.theme-row .pct{font-family:var(--font-mono);font-size:var(--text-sm);font-weight:600;color:var(--text-muted)}
.theme-row .track{height:9px;border-radius:var(--radius-pill);background:var(--paper-2);overflow:hidden}
.theme-row .fill{display:block;height:100%;border-radius:var(--radius-pill)}

/* ---- CTA band ---- */
.cta-band{background:var(--ink-900);border-radius:var(--radius-xl);padding:var(--space-8);display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap;background-image:radial-gradient(circle at 88% 16%,rgba(67,99,214,.30),transparent 42%)}
.cta-band h2{color:#FBF8F2;margin:0 0 10px}
.cta-band p{color:rgba(251,248,242,.66);margin:0;font-size:var(--text-md);line-height:1.55}

/* ---- banque ---- */
.filter-bar{position:sticky;top:68px;z-index:30;background:rgba(251,248,242,.9);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);padding:14px 0;margin-bottom:6px;border-bottom:1px solid var(--border-default)}
.filter-bar .row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.search{position:relative;display:flex;align-items:center;background:var(--surface-card);border:1px solid var(--border-strong);border-radius:var(--radius-md);height:44px;box-shadow:var(--shadow-xs);flex:1 1 260px;transition:border-color var(--t-fast),box-shadow var(--t-fast)}
.search:focus-within{border-color:var(--brand);box-shadow:var(--shadow-focus)}
.search svg{position:absolute;left:12px;color:var(--text-faint);pointer-events:none}
.search input{flex:1;width:100%;height:100%;border:none;outline:none;background:transparent;font-family:var(--font-sans);font-size:var(--text-sm);color:var(--text-strong);padding:0 14px 0 40px}
.select{position:relative;display:inline-flex;width:230px}
.select select{appearance:none;-webkit-appearance:none;width:100%;height:44px;padding:0 38px 0 14px;background:var(--surface-card);border:1px solid var(--border-strong);border-radius:var(--radius-md);box-shadow:var(--shadow-xs);font-family:var(--font-sans);font-size:var(--text-sm);font-weight:var(--fw-medium);color:var(--text-strong);cursor:pointer;outline:none;transition:border-color var(--t-fast),box-shadow var(--t-fast)}
.select select:focus{border-color:var(--brand);box-shadow:var(--shadow-focus)}
.select .chev{position:absolute;right:13px;top:50%;transform:translateY(-50%);pointer-events:none;color:var(--text-muted)}
.checkbox{display:inline-flex;align-items:center;gap:9px;cursor:pointer;font-family:var(--font-sans);font-size:var(--text-sm);color:var(--text-secondary);user-select:none}
.checkbox .box{display:inline-flex;align-items:center;justify-content:center;width:19px;height:19px;border-radius:6px;border:1.5px solid var(--border-strong);background:var(--surface-card);color:#fff;transition:background var(--t-fast),border-color var(--t-fast)}
.checkbox input{position:absolute;opacity:0;width:0;height:0}
.checkbox input:checked+.box{background:var(--brand);border-color:var(--brand)}
.checkbox .box svg{opacity:0}
.checkbox input:checked+.box svg{opacity:1}
.result-row{display:flex;align-items:center;gap:10px;margin:14px 2px 18px}
.result-count{font-family:var(--font-mono);font-size:var(--text-xs);color:var(--text-muted);letter-spacing:.04em}
.reset-btn{font-family:var(--font-sans);font-size:var(--text-xs);font-weight:600;color:var(--text-link);background:none;border:none;cursor:pointer;display:inline-flex;align-items:center;gap:5px}
.card-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:var(--space-5);align-items:start}
.empty{text-align:center;padding:var(--space-9);color:var(--text-muted)}

/* ---- subject card ---- */
.subject-card{position:relative;background:var(--surface-card);border:1px solid var(--border-default);border-radius:var(--radius-lg);padding:var(--space-5) var(--space-5) var(--space-5) calc(var(--space-5) + 4px);box-shadow:var(--shadow-sm);overflow:hidden}
.subject-card .edge{position:absolute;left:0;top:0;bottom:0;width:4px}
.subject-card .meta{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.subject-card .rk{font-family:var(--font-mono);font-size:var(--text-xs);font-weight:600;color:var(--text-faint);letter-spacing:.04em}
.subject-card .q{font-family:var(--font-display);font-size:var(--text-lg);font-weight:var(--fw-medium);line-height:var(--lh-snug);color:var(--text-strong);margin:0 0 12px;text-wrap:balance}
.subject-card .tags{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px}

/* ---- theme tag ---- */
.theme-tag{display:inline-flex;align-items:center;gap:6px;padding:2px 9px 2px 8px;border-radius:var(--radius-pill);background:var(--surface-card);border:1px solid var(--border-default);font-family:var(--font-sans);font-size:var(--text-2xs);font-weight:var(--fw-medium);color:var(--text-secondary);white-space:nowrap}
.theme-tag .dot{width:6px;height:6px;border-radius:50%;flex:0 0 auto}

/* ---- audio player ---- */
.audio{display:flex;align-items:center;gap:12px;padding:9px 12px;background:var(--surface-sunken);border:1px solid var(--border-default);border-radius:var(--radius-pill);margin-bottom:14px}
.audio.disabled{opacity:.6}
.audio .pp{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;flex:0 0 auto;border-radius:50%;background:var(--brand);color:#fff;border:none;cursor:pointer;box-shadow:var(--shadow-sm);transition:background var(--t-fast)}
.audio .pp:hover{background:var(--brand-hover)}
.audio.disabled .pp{cursor:not-allowed}
.audio .time{font-family:var(--font-mono);font-size:var(--text-2xs);color:var(--text-muted);min-width:34px}
.audio .total{color:var(--text-faint)}
.audio .bar{flex:1;height:6px;border-radius:var(--radius-pill);background:var(--paper-3);cursor:pointer;position:relative;overflow:hidden}
.audio.disabled .bar{cursor:default}
.audio .bar .prog{position:absolute;left:0;top:0;bottom:0;width:0;background:var(--brand);border-radius:var(--radius-pill)}
.audio .rate{font-family:var(--font-mono);font-size:var(--text-2xs);font-weight:600;padding:5px 9px;border-radius:var(--radius-sm);background:var(--surface-card);color:var(--text-secondary);border:1px solid var(--border-default);cursor:pointer;min-width:44px}
.audio.disabled .rate{cursor:not-allowed}

/* ---- answer disclosure ---- */
.disclosure{border-top:1px solid var(--border-soft);padding-top:12px}
.disclosure .toggle{display:inline-flex;align-items:center;gap:7px;background:transparent;border:none;cursor:pointer;font-family:var(--font-sans);font-size:var(--text-sm);font-weight:var(--fw-semibold);color:var(--text-link);padding:0}
.disclosure .toggle .chev{transition:transform var(--t-fast)}
.disclosure.open .toggle .chev{transform:rotate(90deg)}
.disclosure .body{margin-top:14px;font-family:var(--font-display);font-size:var(--text-md);line-height:var(--lh-relaxed);color:var(--text-body);max-width:66ch;text-align:justify;hyphens:auto;-webkit-hyphens:auto;animation:answerIn var(--t-base)}
.disclosure .body p{margin:0 0 1em} .disclosure .body p:last-child{margin-bottom:0}
@keyframes answerIn{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:none}}

/* ---- methode ---- */
.methode{max-width:var(--container-narrow);margin:0 auto;padding:var(--space-7) var(--space-5) var(--space-9)}
.steps{display:flex;flex-direction:column;gap:14px;margin-bottom:40px}
.step{display:flex;gap:18px;align-items:stretch}
.step .rail{display:flex;flex-direction:column;align-items:center;flex:0 0 auto}
.step .num{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;border-radius:50%;color:#fff;font-family:var(--font-display);font-weight:700;font-size:var(--text-md);flex:0 0 auto}
.step .line{flex:1;width:2px;background:var(--border-default);margin-top:4px}
.step .phrase{font-family:var(--font-display);font-style:italic;font-size:var(--text-md);line-height:1.5;color:var(--text-body);margin:0;padding-left:14px}
.reflexes{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-bottom:40px}
.reflexe{display:flex;gap:11px;align-items:flex-start}
.reflexe .chk{color:var(--vert-600);flex:0 0 auto;margin-top:1px}
.reflexe span{font-size:var(--text-sm);color:var(--text-secondary);line-height:1.5}

/* ---- footer ---- */
.site-footer{border-top:1px solid var(--border-default);background:var(--paper-1);margin-top:var(--space-7)}
.site-footer .top{max-width:var(--container);margin:0 auto;padding:var(--space-7) var(--space-5);display:flex;justify-content:space-between;align-items:flex-start;gap:28px;flex-wrap:wrap}
.site-footer .cols{display:flex;gap:56px}
.foot-link{display:block;background:none;border:none;padding:5px 0;cursor:pointer;font-family:var(--font-sans);font-size:var(--text-sm);color:var(--text-secondary);text-align:left}
.foot-link:hover{color:var(--text-link)}
.site-footer .bottom{border-top:1px solid var(--border-soft)}
.site-footer .bottom .inner{max-width:var(--container);margin:0 auto;padding:16px var(--space-5);font-family:var(--font-mono);font-size:var(--text-2xs);color:var(--text-faint);letter-spacing:.03em}

.view{animation:viewIn var(--t-base)}
@keyframes viewIn{from{opacity:0}to{opacity:1}}

@media (max-width:880px){
  .hero .grid{grid-template-columns:1fr;gap:var(--space-6)}
  .hero h1{font-size:var(--text-3xl)}
  .synth-grid{grid-template-columns:1fr!important}
  .task-grid{grid-template-columns:1fr}
  .card-grid{grid-template-columns:1fr}
  .reflexes{grid-template-columns:1fr}
  .site-nav{display:none}
  .objectif-pill{display:none}
  .sec-head{flex-direction:column;gap:8px}
  .sec-head p{text-align:left!important}
}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.001ms!important;transition-duration:.001ms!important}}
</style>
</head>
<body>
<div id="app"></div>
<script>
const DATA = /*__DATA__*/null;
const SUBJECT_COUNT = __COUNT__;

/* ---------- icons (ported from the design's icons.jsx) ---------- */
const ICONS = {
  search:'<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
  mic:'<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/>',
  'messages-square':'<path d="M14 9a2 2 0 0 1-2 2H6l-4 4V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2Z"/><path d="M18 9h2a2 2 0 0 1 2 2v11l-4-4h-6a2 2 0 0 1-2-2v-1"/>',
  'help-circle':'<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>',
  clock:'<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
  sparkles:'<path d="m12 3-1.9 5.8a2 2 0 0 1-1.287 1.288L3 12l5.8 1.9a2 2 0 0 1 1.288 1.287L12 21l1.9-5.8a2 2 0 0 1 1.287-1.288L21 12l-5.8-1.9a2 2 0 0 1-1.288-1.287Z"/><path d="M5 3v4"/><path d="M19 17v4"/><path d="M3 5h4"/><path d="M17 19h4"/>',
  'arrow-right':'<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
  'check-circle-2':'<path d="M21.801 10A10 10 0 1 1 17 3.335"/><path d="m9 11 3 3L22 4"/>',
  x:'<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
  'search-x':'<path d="m13.5 8.5-5 5"/><path d="m8.5 8.5 5 5"/><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
  chevron:'<path d="m9 18 6-6-6-6"/>',
  'chevron-down':'<path d="m6 9 6 6 6-6"/>',
  check:'<path d="M20 6 9 17l-5-5"/>',
};
const FILLED = {};
function ic(n,size){size=size||18;const filled=FILLED[n];return '<svg width="'+size+'" height="'+size+'" viewBox="0 0 24 24" fill="'+(filled?'currentColor':'none')+'" stroke="'+(filled?'none':'currentColor')+'" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+(ICONS[n]||'')+'</svg>';}

const esc=(s)=>{const d=document.createElement('div');d.textContent=s==null?'':String(s);return d.innerHTML;};
const norm=(s)=>s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');

/* theme -> category hue (ported from ThemeTag.jsx) */
const CAT=[
  [/immigr|étranger|etranger|intégr|integr|culture/i,'var(--cat-immigration)'],
  [/travail|emploi|salaire|carrièr|carrier|métier|metier|télétravail|teletravail/i,'var(--cat-travail)'],
  [/éducation|education|école|ecole|étude|etude|diplôm|diplom|enfant|parent/i,'var(--cat-education)'],
  [/santé|sante|aliment|mode de vie|viande|stress|bio/i,'var(--cat-sante)'],
  [/télévision|television|média|media|information|journ|lecture|livre/i,'var(--cat-medias)'],
  [/techno|internet|réseaux|reseaux|téléphone|telephone|écran|ecran|numérique|numerique|jeux vidéo/i,'var(--cat-techno)'],
  [/environn|pollution|écolog|ecolog|transport|voiture|déchet|dechet/i,'var(--cat-environ)'],
];
function themeColor(l){l=l||'';for(const [re,c] of CAT){if(re.test(l))return c;}return 'var(--cat-societe)';}

const LOGO=(cls)=>'<span class="logo '+(cls||'')+'"><span class="mark">é</span><span class="wm"><span class="t">Préparation TCF</span>'+(cls==='sm'?'':'<span class="s">Canada · Oral</span>')+'</span></span>';
const themeTag=(t)=>'<span class="theme-tag"><span class="dot" style="background:'+themeColor(t)+'"></span>'+esc(t)+'</span>';

/* ---------- views ---------- */
function viewAccueil(){
  const tasks=[
    {n:'1',titre:'Entretien dirigé',duree:'2 min',prep:'Sans préparation',desc:"Vous répondez aux questions personnelles de l'examinateur.",ico:'messages-square'},
    {n:'2',titre:'Exercice en interaction',duree:'5 min 30',prep:'2 min de préparation',desc:"Vous posez des questions pour obtenir une information.",ico:'help-circle'},
    {n:'3',titre:"Expression d'un point de vue",duree:'4 min 30',prep:'Sans préparation',desc:"Vous défendez un avis structuré, en continu. La tâche la plus exigeante.",ico:'mic',focus:true},
  ];
  const themes=[
    {label:'Immigration / intégration',pct:20,color:'var(--cat-immigration)'},
    {label:'Travail / emploi / carrière',pct:19,color:'var(--cat-travail)'},
    {label:'Éducation / études',pct:12,color:'var(--cat-education)'},
    {label:'Santé / mode de vie',pct:10,color:'var(--cat-sante)'},
    {label:'Médias / télévision',pct:9,color:'var(--cat-medias)'},
    {label:'Technologie / Internet',pct:9,color:'var(--cat-techno)'},
  ];
  const bands=['A1','A2','B1','B2','C1','C2'];
  const bandColors={A1:'var(--paper-3)',A2:'#E4D9C2',B1:'var(--bleu-200)',B2:'var(--vert-100)',C1:'var(--vert-100)',C2:'var(--ochre-100)'};
  const scoreScale='<div class="score-scale"><div class="bands">'+bands.map(b=>'<div class="band'+(b==='B2'?' b2':'')+'" style="background:'+bandColors[b]+'">'+b+'</div>').join('')+'<span class="tick" style="left:'+(((458-100)/599)*100)+'%"></span></div><div class="legend"><span>100</span><span class="mid">B2 = 400–499 · NCLC 7 dès 458</span><span>699</span></div></div>';

  return '<div class="view">'
  +'<section class="hero"><div class="grid">'
    +'<div>'
      +'<span class="eyebrow" style="display:block;margin-bottom:16px">TCF Canada · Expression orale</span>'
      +'<h1>Préparez l\'oral du&nbsp;TCF&nbsp;Canada,<br><em>sujet par sujet.</em></h1>'
      +'<p class="lede">'+SUBJECT_COUNT+' réponses modèles de niveau B2, classées par fréquence d\'apparition, avec audio à écouter et la structure passe-partout pour parler 4 min 30 sans blanc.</p>'
      +'<div style="display:flex;gap:12px;flex-wrap:wrap">'
        +'<button class="btn btn-primary btn-lg" data-nav="banque">Voir la banque de sujets '+ic('arrow-right',17)+'</button>'
        +'<button class="btn btn-outline btn-lg" data-nav="methode">La méthode</button>'
      +'</div>'
    +'</div>'
    +'<div class="card card-floating card-pad-lg">'
      +'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:18px"><span class="eyebrow">Le barème oral</span>'
      +'<span class="level-badge"><span class="box">B2</span><span class="sub">NCLC 7</span></span></div>'
      +scoreScale
      +'<p style="font-size:var(--text-sm);color:var(--text-muted);margin:18px 0 0;line-height:1.55">Échelle de <strong>100 à 699</strong>. Le niveau <strong style="color:var(--vert-700)">B2</strong> se situe entre 400 et 499 — le seuil <strong>NCLC&nbsp;7</strong> est atteint dès <strong>458</strong>.</p>'
    +'</div>'
  +'</div></section>'

  +'<section class="section"><div class="sec-head"><div>'
    +'<span class="eyebrow" style="display:block;margin-bottom:10px">L\'épreuve · ~12 minutes</span><h2 style="margin:0">Trois tâches enchaînées</h2></div>'
    +'<p style="color:var(--text-muted);font-size:var(--text-sm);max-width:32ch;margin:0;text-align:right">Un entretien individuel enregistré avec le même examinateur.</p></div>'
    +'<div class="task-grid">'+tasks.map(t=>'<div class="card '+(t.focus?'card-floating':'')+' card-pad-lg task'+(t.focus?' focus':'')+'">'
      +'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px"><span class="task-icon">'+ic(t.ico,19)+'</span><span class="task-num">'+t.n+'</span></div>'
      +'<h3 style="font-size:var(--text-lg);margin:0 0 8px">'+t.titre+'</h3>'
      +'<p style="font-size:var(--text-sm);color:var(--text-muted);line-height:1.55;margin:0 0 16px;min-height:62px">'+t.desc+'</p>'
      +'<div style="display:flex;gap:8px;flex-wrap:wrap"><span class="badge badge-brand badge-sm">'+ic('clock',12)+' '+t.duree+'</span><span class="badge badge-neutral badge-sm">'+t.prep+'</span>'+(t.focus?'<span class="badge badge-accent badge-sm">Le plus travaillé ici</span>':'')+'</div>'
    +'</div>').join('')+'</div>'
  +'</section>'

  +'<section class="section-band"><div class="section synth-grid" style="display:grid;grid-template-columns:.9fr 1.1fr;gap:var(--space-8);align-items:center">'
    +'<div><span class="eyebrow" style="display:block;margin-bottom:10px">Synthèse du corpus · Tâche 3</span>'
      +'<h2 style="margin:0 0 14px">Six thèmes couvrent 78&nbsp;% des sujets</h2>'
      +'<p style="color:var(--text-secondary);line-height:1.6;margin:0 0 24px;max-width:40ch">703 sujets relevés de janvier 2022 à juin 2026, classés par thème. Révisez ces six familles et vous êtes prêt(e) pour la grande majorité des tirages.</p>'
      +'<div style="display:flex;gap:14px"><div class="stat-card" style="flex:1"><span class="val">703</span><span class="lab">sujets analysés</span><span class="hint">2022 → 2026</span></div>'
      +'<div class="stat-card" style="flex:1"><span class="val" style="color:var(--accent)">'+SUBJECT_COUNT+'</span><span class="lab">réponses modèles B2</span><span class="hint">dédupliquées, audio</span></div></div>'
    +'</div>'
    +'<div style="display:flex;flex-direction:column;gap:13px">'+themes.map(t=>'<div class="theme-row"><div class="top"><span class="name"><span class="dot" style="background:'+t.color+'"></span>'+t.label+'</span><span class="pct">'+t.pct+'&nbsp;%</span></div><div class="track"><span class="fill" style="width:'+(t.pct*4)+'%;background:'+t.color+'"></span></div></div>').join('')+'</div>'
  +'</div></section>'

  +'<section class="section"><div class="cta-band"><div style="max-width:46ch"><h2>Entraînez-vous avec un professeur</h2>'
    +'<p>Claude joue un professeur bienveillant : il pioche un vrai sujet, vous laisse parler 4 min 30, puis corrige sans jamais vous noter.</p></div>'
    +'<button class="btn btn-accent btn-lg">'+ic('sparkles',17)+' Commencer un entraînement</button></div></section>'
  +'</div>';
}

function viewMethode(){
  const steps=[
    {n:'1',titre:'Introduction',duree:'~30 s',desc:"Accroche, reformulation du sujet, votre opinion, annonce du plan.",phrase:"« À mon avis, c'est un sujet très actuel. Personnellement, je pense que… Pour justifier mon opinion, je vous donnerai quelques arguments. »",color:'var(--cat-immigration)'},
    {n:'2',titre:'Premier argument',desc:"Idée → explication (En effet…) → exemple concret (Par exemple…).",phrase:"« Tout d'abord… En effet… Par exemple… »",color:'var(--cat-travail)'},
    {n:'3',titre:'Deuxième argument',desc:"Un autre point, étoffé de la même manière.",phrase:"« Ensuite… / De plus… Cela permet de… C'est notamment le cas de… »",color:'var(--cat-education)'},
    {n:'4',titre:'Nuance / contre-argument',desc:"Le réflexe B2 : reconnaître l'avis opposé, puis y répondre.",phrase:"« Cependant, certaines personnes pensent que… Je comprends ce point de vue, mais je crois que… »",color:'var(--cat-medias)'},
    {n:'5',titre:'Conclusion',desc:"Bilan clair, avec un « car ». Ouverture facultative.",phrase:"« En conclusion, je pense que…, car… On pourrait même se demander si… »",color:'var(--cat-sante)'},
  ];
  const reflexes=[
    "Choisissez le camp le plus facile à défendre, pas forcément votre vraie opinion.",
    "Toujours un exemple concret par argument — c'est ce qui fait monter la note.",
    "Reliez tout avec des connecteurs : d'abord, ensuite, en effet, cependant…",
    "Glissez une concession (« Certes…, cependant… ») : la marque du B2.",
    "Développez 2 bons arguments plutôt que 4 superficiels.",
    "Parlez jusqu'au bout du temps, calmement. Le silence pénalise plus que l'erreur.",
  ];
  return '<div class="view"><main class="methode">'
    +'<span class="eyebrow" style="display:block;margin-bottom:10px">Tâche 3 · Structure passe-partout</span>'
    +'<h1 style="margin:0 0 12px">Parler 4 min 30, sans blanc</h1>'
    +'<p style="color:var(--text-secondary);font-size:var(--text-md);line-height:1.6;margin:0 0 14px">Il n\'y a <strong>pas de préparation</strong> pour la Tâche 3 : vous répondez spontanément. L\'enjeu n\'est pas de réfléchir longtemps, mais de tenir un discours <strong>organisé et fluide</strong>. Cette structure marche pour presque tous les sujets.</p>'
    +'<div style="display:inline-flex;gap:8px;margin-bottom:32px"><span class="badge badge-brand">'+ic('clock',12)+' ~4 min 30 en continu</span><span class="badge badge-success">Objectif B2</span></div>'
    +'<div class="steps">'+steps.map(s=>'<div class="step"><div class="rail"><span class="num" style="background:'+s.color+'">'+s.n+'</span>'+(s.n!=='5'?'<span class="line"></span>':'')+'</div>'
      +'<div class="card card-pad-md" style="flex:1"><div style="display:flex;align-items:baseline;gap:10px;margin-bottom:6px;flex-wrap:wrap"><h3 style="font-size:var(--text-lg);margin:0">'+s.titre+'</h3>'+(s.duree?'<span style="font-family:var(--font-mono);font-size:var(--text-2xs);color:var(--text-faint);white-space:nowrap">'+s.duree+'</span>':'')+'</div>'
      +'<p style="font-size:var(--text-sm);color:var(--text-muted);margin:0 0 12px;line-height:1.5">'+s.desc+'</p>'
      +'<p class="phrase" style="border-left:3px solid '+s.color+'">'+s.phrase+'</p></div></div>').join('')+'</div>'
    +'<h2 style="margin:0 0 18px">Réflexes pour le jour J</h2>'
    +'<div class="reflexes">'+reflexes.map(r=>'<div class="reflexe"><span class="chk">'+ic('check-circle-2',18)+'</span><span>'+r+'</span></div>').join('')+'</div>'
    +'<div class="card card-pad-lg" style="background:var(--bleu-050);border-color:var(--bleu-200)"><div style="display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap"><div><h3 style="margin:0 0 6px">Mettez la méthode en pratique</h3><p style="margin:0;color:var(--text-secondary);font-size:var(--text-sm)">'+SUBJECT_COUNT+' sujets réels vous attendent, classés par priorité.</p></div>'
    +'<button class="btn btn-primary" data-nav="banque">Voir la banque de sujets '+ic('arrow-right',16)+'</button></div></div>'
  +'</main></div>';
}

const ALL_THEMES=Array.from(new Set(DATA.flatMap(d=>d.themes))).sort((a,b)=>a.localeCompare(b,'fr'));
const filt={q:'',theme:'',prio:false};

function subjectCard(d){
  const edge=d.themes.length?themeColor(d.themes[0]):'var(--border-strong)';
  const rk='#'+String(d.rank).padStart(3,'0');
  const hot=d.frequency>1?'<span class="badge badge-hot badge-sm">'+d.frequency+'× récurrent</span>':'';
  const tags=d.themes.map(themeTag).join('');
  const ans=(d.answer||[]).map(p=>'<p>'+esc(p)+'</p>').join('');
  return '<article class="subject-card" data-rank="'+d.rank+'"><span class="edge" style="background:'+edge+'"></span>'
    +'<div class="meta"><span class="rk">'+rk+'</span>'+hot+'</div>'
    +'<h3 class="q">'+esc(d.subject)+'</h3>'
    +(tags?'<div class="tags">'+tags+'</div>':'')
    +'<div class="audio" data-audio><audio preload="none" src="'+esc(d.audio)+'"></audio>'
      +'<button class="pp" data-pp aria-label="Lecture">'+'<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" style="margin-left:2px"><path d="M8 5v14l11-7z"/></svg>'+'</button>'
      +'<span class="time cur">0:00</span>'
      +'<div class="bar" data-bar><span class="prog"></span></div>'
      +'<span class="time total tot">—:—</span>'
      +'<button class="rate" data-rate aria-label="Vitesse de lecture">1×</button>'
    +'</div>'
    +'<div class="disclosure"><button class="toggle" data-toggle><span class="chev">'+ic('chevron',15)+'</span><span class="lbl">Voir la réponse modèle</span></button>'
      +'<div class="body" hidden lang="fr">'+ans+'</div></div>'
  +'</article>';
}

function renderBanque(){
  const out=DATA.filter(d=>(!filt.q||norm(d.subject).includes(norm(filt.q)))&&(!filt.theme||d.themes.includes(filt.theme))&&(!filt.prio||d.frequency>1));
  const opts='<option value="">Tous les thèmes</option>'+ALL_THEMES.map(t=>'<option value="'+esc(t)+'"'+(filt.theme===t?' selected':'')+'>'+esc(t)+'</option>').join('');
  const active=filt.q||filt.theme||filt.prio;
  const grid=out.length?'<div class="card-grid">'+out.map(subjectCard).join('')+'</div>'
    :'<div class="empty">'+ic('search-x',28)+'<p style="margin-top:12px">Aucun sujet ne correspond à votre recherche.</p></div>';
  return '<div class="view"><main class="section" style="padding-top:var(--space-7)">'
    +'<div style="margin-bottom:22px"><span class="eyebrow" style="display:block;margin-bottom:10px">Tâche 3 · Expression d\'un point de vue</span>'
    +'<h1 style="margin:0 0 10px">Banque de sujets prioritaires</h1>'
    +'<p style="color:var(--text-secondary);font-size:var(--text-md);margin:0;max-width:60ch;line-height:1.55">Les sujets 2026 dédupliqués et triés par <strong>priorité</strong> (fréquence d\'apparition). Texte modèle B2 + audio à écouter — astuce&nbsp;: écoutez, puis faites du <em>shadowing</em>.</p></div>'
    +'<div class="filter-bar"><div class="row">'
      +'<label class="search">'+ic('search',16)+'<input type="search" data-q placeholder="Rechercher un sujet…" value="'+esc(filt.q)+'"></label>'
      +'<span class="select"><select data-theme>'+opts+'</select><span class="chev chevron">'+ic('chevron-down',13)+'</span></span>'
      +'<label class="checkbox"><input type="checkbox" data-prio'+(filt.prio?' checked':'')+'><span class="box">'+ic('check',12)+'</span>Sujets récurrents seulement</label>'
    +'</div></div>'
    +'<div class="result-row"><span class="result-count">'+out.length+' sujet'+(out.length>1?'s':'')+'</span>'
    +(active?'<button class="reset-btn" data-reset>'+ic('x',13)+' Réinitialiser</button>':'')+'</div>'
    +grid
  +'</main></div>';
}

function viewFooter(){
  return '<footer class="site-footer"><div class="top">'
    +'<div style="max-width:34ch">'+LOGO('sm')+'<p style="margin-top:14px;font-size:var(--text-sm);color:var(--text-muted);line-height:1.55">Préparation libre aux épreuves orales du TCF Canada. Objectif&nbsp;: B2 / NCLC&nbsp;7.</p></div>'
    +'<div class="cols">'
      +'<div><div class="eyebrow" style="margin-bottom:12px">Épreuve</div>'
        +'<button class="foot-link" data-nav="accueil">Vue d\'ensemble</button><button class="foot-link" data-nav="banque">Banque de sujets</button><button class="foot-link" data-nav="methode">Méthode Tâche 3</button></div>'
      +'<div><div class="eyebrow" style="margin-bottom:12px">Ressources</div>'
        +'<button class="foot-link" data-nav="banque">Réponses modèles B2</button><button class="foot-link" data-nav="banque">Audios &amp; shadowing</button><button class="foot-link" data-nav="methode">Connecteurs &amp; lexique</button></div>'
    +'</div></div>'
    +'<div class="bottom"><div class="inner">Projet personnel · Données : reussir-tcfcanada.com (2022–2026) · Design system — recréation</div></div>'
  +'</footer>';
}

/* ---------- shell + routing ---------- */
let view='accueil';
function header(){
  const links=[['accueil','Accueil'],['banque','Banque de sujets'],['methode','Méthode']];
  return '<header class="site-header"><div class="inner">'
    +'<button data-nav="accueil" style="background:none;border:none;cursor:pointer;padding:0">'+LOGO('')+'</button>'
    +'<nav class="site-nav">'+links.map(l=>'<button class="nav-link'+(view===l[0]?' active':'')+'" data-nav="'+l[0]+'">'+l[1]+'</button>').join('')+'</nav>'
    +'<div class="header-right"><span class="objectif-pill"><span class="dot"></span>Objectif&nbsp;B2 · NCLC&nbsp;7</span>'
    +'<button class="btn btn-accent btn-sm">'+ic('sparkles',15)+' S\'entraîner</button></div>'
  +'</div></header>';
}
function render(){
  const body=view==='banque'?renderBanque():view==='methode'?viewMethode():viewAccueil();
  document.getElementById('app').innerHTML=header()+'<div>'+body+'</div>'+viewFooter();
}
function nav(v){view=v;window.scrollTo({top:0,behavior:'smooth'});render();}

/* ---------- audio player wiring ---------- */
const fmt=(s)=>{if(!s||!isFinite(s))return '0:00';const m=Math.floor(s/60),r=Math.floor(s%60);return m+':'+String(r).padStart(2,'0');};
const RATES=[0.75,0.9,1];
function bindAudio(el){
  const audio=el.querySelector('audio');
  const pp=el.querySelector('[data-pp]');
  const bar=el.querySelector('[data-bar]');
  const prog=el.querySelector('.prog');
  const cur=el.querySelector('.cur');
  const tot=el.querySelector('.tot');
  const rateBtn=el.querySelector('[data-rate]');
  let rateIdx=2, ok=true;
  const disable=()=>{ok=false;el.classList.add('disabled');tot.textContent='—:—';};
  audio.addEventListener('error',disable);
  audio.addEventListener('loadedmetadata',()=>{tot.textContent=fmt(audio.duration);});
  audio.addEventListener('timeupdate',()=>{cur.textContent=fmt(audio.currentTime);prog.style.width=(audio.duration?(audio.currentTime/audio.duration*100):0)+'%';});
  audio.addEventListener('ended',()=>{pp.innerHTML='<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" style="margin-left:2px"><path d="M8 5v14l11-7z"/></svg>';});
  pp.addEventListener('click',()=>{if(!ok)return;if(audio.paused){audio.play().then(()=>{pp.innerHTML='<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>';}).catch(disable);}else{audio.pause();pp.innerHTML='<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" style="margin-left:2px"><path d="M8 5v14l11-7z"/></svg>';}});
  bar.addEventListener('click',(e)=>{if(!ok||!audio.duration)return;const r=bar.getBoundingClientRect();audio.currentTime=((e.clientX-r.left)/r.width)*audio.duration;});
  rateBtn.addEventListener('click',()=>{if(!ok)return;rateIdx=(rateIdx+1)%RATES.length;audio.playbackRate=RATES[rateIdx];rateBtn.textContent=RATES[rateIdx]+'×';});
}

/* ---------- event delegation ---------- */
document.addEventListener('click',(e)=>{
  const navEl=e.target.closest('[data-nav]'); if(navEl){nav(navEl.getAttribute('data-nav'));return;}
  const reset=e.target.closest('[data-reset]'); if(reset){filt.q='';filt.theme='';filt.prio=false;render();return;}
  const tog=e.target.closest('[data-toggle]'); if(tog){const dis=tog.closest('.disclosure');const body=dis.querySelector('.body');const open=dis.classList.toggle('open');body.hidden=!open;tog.querySelector('.lbl').textContent=open?'Masquer la réponse':'Voir la réponse modèle';return;}
});
document.addEventListener('input',(e)=>{
  if(e.target.matches('[data-q]')){filt.q=e.target.value;renderCards();}
});
document.addEventListener('change',(e)=>{
  if(e.target.matches('[data-theme]')){filt.theme=e.target.value;render();}
  if(e.target.matches('[data-prio]')){filt.prio=e.target.checked;render();}
});

/* live search without losing focus: re-render only the grid + count */
function renderCards(){
  if(view!=='banque')return;
  const out=DATA.filter(d=>(!filt.q||norm(d.subject).includes(norm(filt.q)))&&(!filt.theme||d.themes.includes(filt.theme))&&(!filt.prio||d.frequency>1));
  const grid=document.querySelector('.card-grid')||document.querySelector('.empty');
  const newGrid=out.length?'<div class="card-grid">'+out.map(subjectCard).join('')+'</div>':'<div class="empty">'+ic('search-x',28)+'<p style="margin-top:12px">Aucun sujet ne correspond à votre recherche.</p></div>';
  if(grid)grid.outerHTML=newGrid;
  const rc=document.querySelector('.result-count'); if(rc)rc.textContent=out.length+' sujet'+(out.length>1?'s':'');
  document.querySelectorAll('[data-audio]').forEach(bindAudio);
}

const _origRender=render;
render=function(){_origRender();document.querySelectorAll('[data-audio]').forEach(bindAudio);};

render();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    out = build_site()
    n = len(_collect())
    print(f"Page générée : {out}  ({n} sujets)")
    print("Aperçu local : open index.html")
    print("En ligne : https://victor-nb.github.io/french-prep/")
