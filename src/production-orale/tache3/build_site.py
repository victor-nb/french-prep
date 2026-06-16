#!/usr/bin/env python3
"""Génère le site statique « Préparation TCF Canada » (GitHub Pages).

Le site est un *manuel* de l'Expression orale : un chapitre par tâche (1, 2, 3),
chacun suivant le même rythme Comprendre → Voir → S'entraîner, plus la Banque des
214 réponses modèles (Tâche 3, audio) et les annexes Vocabulaire / Connecteurs.

Recréation fidèle, en HTML/CSS/JS pur (sans build), du design system exporté depuis
Claude Design : papier crème, encre marine, serif Spectral pour les titres et les
sujets, Hanken Grotesk pour l'UI, IBM Plex Mono pour les métadonnées.

Le contenu rédactionnel des chapitres est un modèle de *blocs* (``_content()``),
injecté en JSON et rendu par des fonctions de rendu côté client. La Banque lit
``examples/_index.json`` + les fichiers ``examples/NNN-*.md``.

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


# --------------------------------------------------------------------------- #
# Contenu rédactionnel des chapitres (modèle de blocs).
# Chaque tâche : {id,num,title,eyebrow,duree,prep,desc,lede,sections:[...]}.
# Une section : {band: Comprendre|Voir|S'entraîner, id, title, blocks:[...]}.
# Un bloc : {type, ...} rendu par BLK[type] côté client.
# Les annexes (vocab/connecteurs/cram/args) sont remplies dans une 2ᵉ étape.
# --------------------------------------------------------------------------- #

_T1 = {
    "id": "t1",
    "num": 1,
    "title": "Entretien dirigé",
    "eyebrow": "Tâche 1 · Présentation",
    "duree": "2 min",
    "prep": "Sans préparation",
    "desc": "Vous vous présentez : parcours, vie actuelle, projets — un monologue, mais l'examinateur peut vous interrompre.",
    "lede": "La première tâche : vous vous présentez pendant environ deux minutes — un véritable monologue de présentation (parcours, vie actuelle, projets), pas une simple série de questions-réponses.",
    "sections": [
        {
            "band": "Comprendre",
            "id": "t1-format",
            "title": "Le format",
            "blocks": [
                {
                    "type": "format",
                    "rows": [
                        ["Durée", "<strong>2 minutes</strong>"],
                        ["Préparation", "<strong>Aucune</strong> — entretien dirigé sans préparation"],
                        ["Ce que vous faites", "Vous vous présentez : votre parcours, votre vie actuelle, vos projets"],
                        ["Objectif officiel", "« Échanger avec une personne qu'il ne connaît pas »"],
                    ],
                    "badges": [
                        {"icon": "clock", "label": "2 min", "cls": "badge-brand"},
                        {"label": "Sans préparation", "cls": "badge-neutral"},
                    ],
                },
                {
                    "type": "callout",
                    "variant": "warn",
                    "title": "On vous interrompt souvent.",
                    "html": "C'est une présentation, mais il est très courant que l'examinateur vous coupe pour poser une question pendant que vous parlez. Ce n'est pas un piège : <strong>répondez brièvement, puis reprenez</strong> votre présentation là où vous vous étiez arrêté(e).",
                },
            ],
        },
        {
            "band": "Comprendre",
            "id": "t1-structure",
            "title": "La structure : passé → présent → futur",
            "blocks": [
                {
                    "type": "prose",
                    "html": "<p>Couvrez les <strong>trois temps</strong> : c'est exactement ce que l'examinateur vérifie ici — votre maîtrise des temps.</p>",
                },
                {
                    "type": "steps",
                    "items": [
                        {"n": "P", "titre": "Passé", "color": "var(--cat-immigration)", "desc": "<strong>Passé composé, imparfait, plus-que-parfait.</strong> D'où vous venez, votre enfance, vos études, votre arrivée au Canada."},
                        {"n": "R", "titre": "Présent", "color": "var(--cat-sante)", "desc": "<strong>Présent de l'indicatif.</strong> Votre vie actuelle, votre travail, vos loisirs."},
                        {"n": "F", "titre": "Futur", "color": "var(--cat-travail)", "desc": "<strong>Futur simple.</strong> Vos projets — visez au moins <strong>3 phrases au futur simple</strong>."},
                    ],
                },
                {
                    "type": "callout",
                    "variant": "accent",
                    "html": "Astuce notation : glissez au moins <strong>3 phrases au futur simple</strong> dans vos projets (« je passerai », « je ferai », « je parlerai », « je serai »). C'est explicitement attendu.",
                },
            ],
        },
        {
            "band": "Comprendre",
            "id": "t1-themes",
            "title": "Les thèmes à couvrir",
            "blocks": [
                {
                    "type": "tags",
                    "items": ["Nom, prénom", "Nationalité", "État civil", "Âge", "Origine", "Où vous avez habité", "Formation / études", "Pourquoi le Canada", "Arrivée au Canada", "Où vous habitez", "Travail", "Loisirs (été & hiver)", "Projets futurs"],
                },
                {
                    "type": "prose",
                    "html": "<p>Déroulez votre présentation en piochant dans cette liste. Et surtout, <strong>donnez des détails</strong> : ce sont eux qui font la différence. L'examinateur peut aussi rebondir sur la famille, vos goûts, vos conditions de vie, un événement passé ou vos voyages.</p>",
                },
            ],
        },
        {
            "band": "Comprendre",
            "id": "t1-reflexes",
            "title": "Réflexes & erreurs fréquentes",
            "blocks": [
                {
                    "type": "reflexes",
                    "items": [
                        "Présentez-vous de façon fluide et structurée : passé → présent → futur.",
                        "Donnez des détails — « je m'appelle X, j'ai Y ans » ne suffit pas.",
                        "Préparez vos projets : au moins 3 phrases au futur simple.",
                        "Si on vous interrompt, répondez court puis reprenez.",
                        "Variez les temps : passé composé, imparfait, présent, futur.",
                        "Restez naturel et souriez : c'est un échange, pas une récitation.",
                    ],
                },
                {
                    "type": "reflexes",
                    "variant": "danger",
                    "items": [
                        "Réciter une liste plate, sans détails ni connecteurs.",
                        "Se figer quand l'examinateur interrompt — c'est normal, rebondissez.",
                        "N'utiliser que le présent : on passe à côté du passé et du futur attendus.",
                        "Parler trop peu — visez les 2 minutes, occupez le temps.",
                        "Oublier les projets au futur simple.",
                    ],
                },
            ],
        },
        {
            "band": "Voir",
            "id": "t1-fiche",
            "title": "Fiche de présentation modèle",
            "blocks": [
                {
                    "type": "prose",
                    "html": "<p>Une présentation complète et <strong>fictive</strong> (Sofia), à utiliser comme modèle : remplacez les informations par les vôtres. Remarquez l'enchaînement passé → présent → futur ; le passage en gras regroupe les <strong>projets au futur simple</strong>.</p>",
                },
                {
                    "type": "fiche",
                    "html": "<p>Bonjour, je m'appelle Sofia. J'ai 29 ans et je suis colombienne.</p>"
                    "<p>Je suis née et j'ai grandi à Medellín, une grande ville de montagne qu'on surnomme « la ville de l'éternel printemps », car le climat y est doux toute l'année.</p>"
                    "<p>Quand j'étais plus jeune, je rêvais déjà de travailler dans la santé. J'ai donc étudié les soins infirmiers et, après mon diplôme, j'ai travaillé cinq ans dans un hôpital de ma ville.</p>"
                    "<p>C'est pour cette raison que mon mari et moi avons décidé de nous installer au Canada, pour découvrir un autre pays et de meilleures opportunités.</p>"
                    "<p>Aujourd'hui, j'habite à Québec et je suis des cours de français pour faire reconnaître mon diplôme. Pendant mon temps libre, j'adore cuisiner ; en hiver, j'ai appris à patiner, et en été je fais du vélo dans le Vieux-Québec.</p>"
                    "<p><strong>À l'avenir, j'aimerais exercer de nouveau comme infirmière. Je passerai bientôt mon examen de français, puis je ferai les démarches nécessaires ; dans quelques années, j'espère que je parlerai couramment et que je serai parfaitement intégrée.</strong></p>",
                },
            ],
        },
        {
            "band": "Voir",
            "id": "t1-simulation",
            "title": "Simulation (≈ 2 min, avec interruptions)",
            "blocks": [
                {
                    "type": "prose",
                    "html": "<p>Voici comment ça se passe réellement : vous présentez, l'examinateur vous coupe une ou deux fois, vous répondez court, puis vous <strong>reprenez</strong>.</p>",
                },
                {
                    "type": "dialogue",
                    "turns": [
                        {"who": "Examinateur", "html": "Bonjour, installez-vous. Présentez-vous, je vous en prie."},
                        {"who": "Vous", "html": "Bonjour ! Avec plaisir. Je m'appelle Sofia, j'ai 29 ans et je suis colombienne, de Medellín, une ville de montagne au climat très doux. J'ai grandi là-bas, et depuis toujours je m'intéresse au domaine de la santé…"},
                        {"who": "Examinateur", "html": "<em>(vous interrompt)</em> Vous travailliez déjà dans ce domaine en Colombie ?"},
                        {"who": "Vous", "html": "Oui, tout à fait : j'ai étudié les soins infirmiers, puis j'ai travaillé cinq ans dans un hôpital de ma ville. <strong>Pour revenir à mon parcours</strong>, mon mari et moi avons ensuite décidé de nous installer au Canada."},
                        {"who": "Examinateur", "html": "Et pourquoi Québec en particulier ?"},
                        {"who": "Vous", "html": "Parce que c'est une ville calme et sécuritaire, où l'on vit en français. <strong>Aujourd'hui</strong>, j'y suis des cours de français pour faire reconnaître mon diplôme. <strong>À l'avenir</strong>, j'aimerais redevenir infirmière ici : je passerai bientôt mon examen, puis je ferai les démarches nécessaires, et j'espère que je serai vite intégrée."},
                        {"who": "Examinateur", "html": "Très bien, merci."},
                    ],
                },
            ],
        },
        {
            "band": "S'entraîner",
            "id": "t1-phrases",
            "title": "Banque de phrases prêtes à l'emploi",
            "blocks": [
                {
                    "type": "prose",
                    "html": "<p>Touchez une phrase pour la copier. Apprenez-en quelques-unes par cœur pour démarrer sans hésiter et rebondir après une interruption.</p>",
                },
                {
                    "type": "phrasebank",
                    "groups": [
                        {"label": "Pour démarrer", "phrases": ["Bonjour ! Je m'appelle… et je viens de…", "Avec plaisir, je vais me présenter."]},
                        {"label": "Pour le passé", "phrases": ["J'ai grandi à…", "Quand j'étais plus jeune, je…", "Après mes études, j'ai commencé à…"]},
                        {"label": "Pour le présent", "phrases": ["Aujourd'hui, je travaille comme…", "Actuellement, je vis à…", "En ce moment, j'apprends…"]},
                        {"label": "Pour le futur", "phrases": ["À l'avenir, j'aimerais…", "Dans quelques années, je + futur simple", "Mon projet, c'est de…"]},
                        {"label": "Pour gérer une interruption", "phrases": ["Pour revenir à ce que je disais…", "Comme je le mentionnais…", "J'y reviens : …"]},
                    ],
                },
            ],
        },
        {
            "band": "S'entraîner",
            "id": "t1-pratique",
            "title": "S'entraîner à l'oral",
            "blocks": [
                {
                    "type": "callout",
                    "variant": "accent",
                    "title": "Entraînez-vous en conditions réelles.",
                    "html": "Demandez à la commande <strong>/tcf-pratique</strong> de jouer l'examinateur : il vous laisse vous présenter, vous interrompt parfois avec une question, puis corrige gentiment (temps, détails, fluidité).",
                },
            ],
        },
    ],
}

_T2 = {
    "id": "t2",
    "num": 2,
    "title": "Exercice en interaction",
    "eyebrow": "Tâche 2 · Interaction",
    "duree": "5 min 30",
    "prep": "2 min de préparation",
    "desc": "Vous posez des questions à l'examinateur pour obtenir une information précise dans une situation courante.",
    "lede": "La seule tâche avec préparation. On vous donne un rôle et une situation : vous menez l'échange en posant beaucoup de questions pour obtenir l'information dont vous avez besoin.",
    "sections": [],
}

_T3 = {
    "id": "t3",
    "num": 3,
    "title": "Expression d'un point de vue",
    "eyebrow": "Tâche 3 · Point de vue",
    "duree": "4 min 30",
    "prep": "Sans préparation",
    "desc": "Vous défendez un avis structuré, en continu, pendant 4 min 30. La tâche la plus exigeante — et la plus travaillée ici.",
    "lede": "La dernière et la plus exigeante : on vous lit une affirmation ou une question, et vous tenez un discours organisé et fluide pendant environ 4 min 30, sans préparation.",
    "sections": [],
}

CONTENT_DIR = HERE / "content"


def _load(name: str) -> dict[str, object] | None:
    path = CONTENT_DIR / f"{name}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _content() -> dict[str, object]:
    return {
        "taches": [_T1, _load("t2") or _T2, _load("t3") or _T3],
        "vocab": _load("vocab"),
        "connecteurs": _load("connecteurs"),
        "cram": _load("cram"),
        "args": _load("args"),
    }


def build_site() -> Path:
    items = _collect()
    payload = json.dumps(items, ensure_ascii=False, separators=(",", ":"))
    content = json.dumps(_content(), ensure_ascii=False, separators=(",", ":"))
    html = (
        _TEMPLATE
        .replace("/*__DATA__*/null", payload)
        .replace("/*__CONTENT__*/null", content)
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
<meta name="description" content="Le manuel complet de l'Expression orale du TCF Canada : les 3 tâches en détail + 214 réponses modèles B2 avec audio. Méthode, simulations, vocabulaire et connecteurs.">
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
.card-interactive{transition:box-shadow var(--t-base),transform var(--t-base),border-color var(--t-base);cursor:pointer}
.card-interactive:hover{box-shadow:var(--shadow-md);transform:translateY(-2px);border-color:var(--border-strong)}

/* ---- header ---- */
.site-header{position:sticky;top:0;z-index:50;background:rgba(251,248,242,.86);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid var(--border-default)}
.site-header .inner{max-width:var(--container);margin:0 auto;height:68px;padding:0 var(--space-5);display:flex;align-items:center;gap:var(--space-6)}
.site-nav{display:flex;gap:4px;margin-left:8px}
.nav-link{font-family:var(--font-sans);font-size:var(--text-sm);font-weight:600;padding:8px 13px;border-radius:var(--radius-sm);border:none;cursor:pointer;background:transparent;color:var(--text-secondary);transition:background var(--t-fast),color var(--t-fast)}
.nav-link:hover{background:var(--surface-sunken)}
.nav-link.active{background:var(--brand-tint);color:var(--bleu-800)}
.nav-annexe{display:inline-flex}
.header-right{margin-left:auto;display:flex;align-items:center;gap:10px}
.header-cram{font-family:var(--font-sans);font-size:var(--text-xs);font-weight:600;color:var(--text-secondary);background:none;border:none;cursor:pointer;padding:6px 4px}
.header-cram:hover{color:var(--text-link)}
.objectif-pill{display:inline-flex;align-items:center;gap:7px;font-family:var(--font-mono);font-size:var(--text-2xs);letter-spacing:.04em;color:var(--vert-700);background:var(--vert-050);padding:5px 11px;border-radius:var(--radius-pill);border:1px solid var(--vert-100)}
.objectif-pill .dot{width:7px;height:7px;border-radius:50%;background:var(--success)}
.site-mobnav{display:none}

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
.task-toc{display:flex;gap:6px;flex-wrap:wrap;margin:14px 0 0}
.task-toc span{font-family:var(--font-mono);font-size:var(--text-3xs);letter-spacing:.04em;text-transform:uppercase;color:var(--text-faint)}

/* ---- theme bars ---- */
.theme-row .top{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px}
.theme-row .name{display:inline-flex;align-items:center;gap:9px;font-size:var(--text-sm);font-weight:600;color:var(--text-strong)}
.theme-row .name .dot{width:11px;height:11px;border-radius:50%}
.theme-row .pct{font-family:var(--font-mono);font-size:var(--text-sm);font-weight:600;color:var(--text-muted)}
.theme-row .track{height:9px;border-radius:var(--radius-pill);background:var(--paper-2);overflow:hidden}
.theme-row .fill{display:block;height:100%;border-radius:var(--radius-pill)}

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
.card-grid{display:grid;grid-template-columns:1fr;gap:var(--space-5);align-items:start}
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

/* ---- chapitre : fil d'ariane ---- */
.crumb{display:flex;align-items:center;gap:7px;font-family:var(--font-mono);font-size:var(--text-2xs);color:var(--text-muted);letter-spacing:.03em;margin-bottom:14px;flex-wrap:wrap}
.crumb button{background:none;border:none;cursor:pointer;color:var(--text-muted);font:inherit;padding:0}
.crumb button:hover{color:var(--text-link)}
.crumb .sep{color:var(--text-faint)}

/* ---- chapitre : mise en page ---- */
.chapter{max-width:var(--container);margin:0 auto;padding:var(--space-7) var(--space-5) var(--space-9)}
.ch-head{margin-bottom:18px}
.ch-head h1{font-size:var(--text-3xl);margin:0 0 12px}
.ch-head .lede{font-size:var(--text-md);color:var(--text-secondary);line-height:1.6;margin:0 0 14px;max-width:64ch}
.ch-badges{display:inline-flex;gap:8px;flex-wrap:wrap}
.ch-layout{display:grid;grid-template-columns:204px 1fr;gap:var(--space-7);align-items:start}
.ch-toc{position:sticky;top:88px;align-self:start}
.ch-toc .toc-band{font-family:var(--font-mono);font-size:var(--text-3xs);font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--text-faint);margin:18px 0 7px;padding-left:12px}
.ch-toc .toc-band:first-child{margin-top:0}
.toc-link{display:block;width:100%;text-align:left;background:none;border:none;border-left:2px solid var(--border-default);cursor:pointer;font-family:var(--font-sans);font-size:var(--text-xs);color:var(--text-muted);padding:5px 12px;line-height:1.35;transition:color var(--t-fast),border-color var(--t-fast)}
.toc-link:hover{color:var(--text-link)}
.toc-link.active{color:var(--bleu-800);border-left-color:var(--brand);font-weight:600}
.ch-main{min-width:0}
.ch-band-label{display:inline-flex;align-items:center;gap:8px;font-family:var(--font-mono);font-size:var(--text-2xs);font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin:30px 0 2px}
.ch-band:first-child .ch-band-label{margin-top:0}
.ch-band-label::before{content:"";width:18px;height:1.5px;background:var(--accent)}
.ch-section{padding:16px 0 6px;scroll-margin-top:130px}
.ch-section>h2{font-size:var(--text-xl);margin:0 0 14px}
.block{margin:0 0 18px}.block:last-child{margin-bottom:0}

/* ---- callout ---- */
.callout{display:flex;gap:12px;border:1px solid var(--border-default);border-radius:var(--radius-md);padding:14px 16px;background:var(--surface-card)}
.callout .ic{flex:0 0 auto;margin-top:1px}
.callout .ct{font-size:var(--text-sm);line-height:1.55;color:var(--text-secondary)}
.callout .ct strong{color:var(--text-strong)}
.callout-warn{background:var(--ochre-050);border-color:var(--ochre-100)}.callout-warn .ic{color:var(--ochre-600)}
.callout-accent{background:var(--bleu-050);border-color:var(--bleu-200)}.callout-accent .ic{color:var(--brand)}
.callout-danger{background:var(--rouge-100);border-color:#EEC9C6}.callout-danger .ic{color:var(--danger)}
.callout-info{background:var(--surface-sunken)}.callout-info .ic{color:var(--text-muted)}

/* ---- format band ---- */
.fmt{display:flex;flex-direction:column;border:1px solid var(--border-default);border-radius:var(--radius-md);overflow:hidden;background:var(--surface-card)}
.fmt .fr{display:grid;grid-template-columns:170px 1fr;gap:14px;padding:11px 16px;border-bottom:1px solid var(--border-soft);font-size:var(--text-sm)}
.fmt .fr:last-child{border-bottom:none}
.fmt .fk{font-family:var(--font-mono);font-size:var(--text-2xs);letter-spacing:.04em;text-transform:uppercase;color:var(--text-muted);align-self:center}
.fmt .fv{color:var(--text-body)}.fmt .fv strong{color:var(--text-strong)}

/* ---- generic table ---- */
.tbl{width:100%;border-collapse:collapse;font-size:var(--text-sm)}
.tbl-wrap{border:1px solid var(--border-default);border-radius:var(--radius-md);overflow:hidden;overflow-x:auto}
.tbl thead th{background:var(--surface-sunken);text-align:left;font-family:var(--font-mono);font-size:var(--text-2xs);letter-spacing:.04em;text-transform:uppercase;color:var(--text-muted);font-weight:600;padding:9px 13px}
.tbl td{padding:10px 13px;border-top:1px solid var(--border-soft);color:var(--text-secondary);vertical-align:top;line-height:1.5}
.tbl td strong{color:var(--text-strong)}

/* ---- copy chip ---- */
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{display:inline-flex;align-items:center;gap:8px;max-width:100%;text-align:left;background:var(--surface-card);border:1px solid var(--border-default);border-radius:var(--radius-md);padding:7px 12px;font-family:var(--font-sans);font-size:var(--text-sm);color:var(--text-body);cursor:pointer;line-height:1.4;transition:border-color var(--t-fast),background var(--t-fast)}
.chip:hover{border-color:var(--brand);background:var(--bleu-050)}
.chip .ci{flex:0 0 auto;color:var(--text-faint)}
.chip.copied{border-color:var(--success);background:var(--vert-050);color:var(--vert-700)}
.chip.copied .ci{color:var(--success)}
.phrasebank{display:flex;flex-direction:column;gap:14px}
.pb-group .pb-label{font-family:var(--font-mono);font-size:var(--text-2xs);letter-spacing:.05em;text-transform:uppercase;color:var(--text-muted);margin-bottom:8px}

/* ---- dialogue ---- */
.dialogue{border:1px solid var(--border-default);border-radius:var(--radius-lg);overflow:hidden;background:var(--surface-card)}
.dialogue .dlg-consigne{background:var(--surface-sunken);border-bottom:1px solid var(--border-default);padding:12px 16px;font-family:var(--font-display);font-style:italic;font-size:var(--text-sm);color:var(--text-secondary)}
.dialogue .turns{padding:6px 0}
.turn{display:grid;grid-template-columns:104px 1fr;gap:14px;padding:9px 16px}
.turn .who{font-family:var(--font-mono);font-size:var(--text-2xs);font-weight:600;letter-spacing:.04em;text-transform:uppercase;padding-top:3px}
.turn.ex .who{color:var(--text-muted)}
.turn.vous .who{color:var(--brand)}
.turn .say{font-size:var(--text-sm);line-height:1.6;color:var(--text-body)}
.turn .say strong{color:var(--text-strong)}
.turn .say em{color:var(--text-muted)}
.turn.vous{background:var(--bleu-050)}
.turn.narr{grid-template-columns:1fr}.turn.narr .say{font-style:italic;color:var(--text-muted);font-size:var(--text-xs)}

/* ---- model fiche / answer ---- */
.fiche{font-family:var(--font-display);font-size:var(--text-md);line-height:var(--lh-relaxed);color:var(--text-body);border-left:3px solid var(--brand);padding:4px 0 4px 18px;max-width:66ch}
.fiche p{margin:0 0 1em}.fiche p:last-child{margin:0}
.model-answer .ma-part{margin-bottom:14px}.model-answer .ma-part:last-child{margin-bottom:0}
.ma-label{display:inline-block;font-family:var(--font-mono);font-size:var(--text-2xs);font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--accent);margin-bottom:5px}
.ma-part .ma-txt{font-family:var(--font-display);font-size:var(--text-base);line-height:1.7;color:var(--text-body)}
.ma-part .ma-txt strong{color:var(--bleu-800)}

/* ---- template (mono) card ---- */
.tpl-card{background:var(--ink-900);color:#E7E3D7;border-radius:var(--radius-md);padding:18px;font-family:var(--font-mono);font-size:var(--text-sm);line-height:1.75;white-space:pre-wrap}
.tpl-card .blk,.tpl-card strong,.tpl-card b{color:var(--ochre-500);font-weight:var(--fw-semibold)}
.tpl-card p{margin:0 0 .9em}.tpl-card p:last-child{margin:0}

/* ---- arguments finder (Tâche 3, à la demande) ---- */
.argfinder .arg-list{display:flex;flex-direction:column;gap:8px;margin-top:14px}
.arg-item{border:1px solid var(--border-default);border-radius:var(--radius-md);overflow:hidden;background:var(--surface-card)}
.arg-toggle{display:flex;align-items:center;gap:9px;width:100%;text-align:left;background:none;border:none;cursor:pointer;padding:12px 14px;font-family:var(--font-display);font-size:var(--text-base);color:var(--text-strong)}
.arg-toggle .chev{transition:transform var(--t-fast);color:var(--text-muted);flex:0 0 auto}
.arg-item.open .arg-toggle .chev{transform:rotate(90deg)}
.arg-body{padding:0 14px 14px;border-top:1px solid var(--border-soft)}
.arg-cols{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:12px}
.arg-col-h{font-family:var(--font-mono);font-size:var(--text-2xs);font-weight:600;letter-spacing:.05em;text-transform:uppercase;margin-bottom:7px}
.arg-col-h.pour{color:var(--success)} .arg-col-h.contre{color:var(--danger)} .arg-col-h.nuance{color:var(--accent)}
.arg-col ul{margin:0;padding-left:16px} .arg-col li{font-size:var(--text-sm);color:var(--text-secondary);line-height:1.5;margin-bottom:6px}
@media(max-width:880px){.arg-cols{grid-template-columns:1fr;gap:12px}}

/* ---- methode steps (réutilisé) ---- */
.steps{display:flex;flex-direction:column;gap:14px}
.step{display:flex;gap:18px;align-items:stretch}
.step .rail{display:flex;flex-direction:column;align-items:center;flex:0 0 auto}
.step .num{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;border-radius:50%;color:#fff;font-family:var(--font-display);font-weight:700;font-size:var(--text-md);flex:0 0 auto}
.step .line{flex:1;width:2px;background:var(--border-default);margin-top:4px}
.step .phrase{font-family:var(--font-display);font-style:italic;font-size:var(--text-md);line-height:1.5;color:var(--text-body);margin:0;padding-left:14px}
.reflexes{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
.reflexe{display:flex;gap:11px;align-items:flex-start}
.reflexe .chk{color:var(--vert-600);flex:0 0 auto;margin-top:1px}
.reflexe span{font-size:var(--text-sm);color:var(--text-secondary);line-height:1.5}

/* ---- pager ---- */
.pager{display:flex;justify-content:space-between;gap:14px;margin-top:36px;border-top:1px solid var(--border-default);padding-top:18px}
.pager button{display:inline-flex;flex-direction:column;gap:2px;background:none;border:none;cursor:pointer;text-align:left;padding:0}
.pager .pg-r{text-align:right;margin-left:auto;align-items:flex-end}
.pager .pg-k{font-family:var(--font-mono);font-size:var(--text-3xs);letter-spacing:.06em;text-transform:uppercase;color:var(--text-faint)}
.pager .pg-t{font-family:var(--font-display);font-size:var(--text-md);color:var(--text-strong)}
.pager button:hover .pg-t{color:var(--text-link)}

/* ---- table des matières (accueil) ---- */
.toc-book{border:1px solid var(--border-default);border-radius:var(--radius-lg);background:var(--surface-card);overflow:hidden;box-shadow:var(--shadow-sm)}
.tb-row{display:grid;grid-template-columns:auto 1fr auto;gap:16px;align-items:center;padding:15px 18px;border-bottom:1px solid var(--border-soft);cursor:pointer;background:none;border-left:none;border-right:none;border-top:none;width:100%;text-align:left;font:inherit;transition:background var(--t-fast)}
.tb-row:last-child{border-bottom:none}
.tb-row:hover{background:var(--surface-sunken)}
.tb-n{font-family:var(--font-mono);font-size:var(--text-sm);color:var(--text-faint);font-weight:600;min-width:34px}
.tb-t{display:block;font-family:var(--font-display);font-size:var(--text-md);color:var(--text-strong)}
.tb-s{display:block;font-size:var(--text-xs);color:var(--text-muted);margin-top:2px;line-height:1.4}
.tb-go{color:var(--text-faint)}
.tb-row:hover .tb-go{color:var(--text-link)}

/* ---- placeholder ---- */
.placeholder{text-align:center;padding:var(--space-8);color:var(--text-muted);border:1px dashed var(--border-strong);border-radius:var(--radius-lg);background:var(--surface-card)}

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

@media (max-width:1024px){.nav-annexe{display:none}}
@media (max-width:880px){
  .hero .grid{grid-template-columns:1fr;gap:var(--space-6)}
  .hero h1{font-size:var(--text-3xl)}
  .synth-grid{grid-template-columns:1fr!important}
  .task-grid{grid-template-columns:1fr}
  .card-grid{grid-template-columns:1fr}
  .reflexes{grid-template-columns:1fr}
  .site-nav{display:none}
  .header-cram{display:none}
  .objectif-pill{display:none}
  .sec-head{flex-direction:column;gap:8px}
  .sec-head p{text-align:left!important}
  .ch-layout{grid-template-columns:1fr}
  .ch-toc{display:none}
  .fmt .fr{grid-template-columns:1fr;gap:3px}
  .turn{grid-template-columns:74px 1fr;gap:10px}
  .site-mobnav{display:block;border-top:1px solid var(--border-soft);background:rgba(251,248,242,.92);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
  .site-mobnav .scroller{display:flex;gap:7px;overflow-x:auto;-webkit-overflow-scrolling:touch;padding:9px var(--space-5)}
  .site-mobnav .toc-link{border:1px solid var(--border-default);border-radius:var(--radius-pill);white-space:nowrap;padding:6px 12px;flex:0 0 auto}
  .site-mobnav .toc-link.active{background:var(--brand-tint);border-color:var(--bleu-200);color:var(--bleu-800)}
}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.001ms!important;transition-duration:.001ms!important}}
</style>
</head>
<body>
<div id="app"></div>
<script>
const DATA = /*__DATA__*/null;
const CONTENT = /*__CONTENT__*/null;
const SUBJECT_COUNT = __COUNT__;

/* ---------- icons ---------- */
const ICONS = {
  search:'<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
  mic:'<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/>',
  'messages-square':'<path d="M14 9a2 2 0 0 1-2 2H6l-4 4V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2Z"/><path d="M18 9h2a2 2 0 0 1 2 2v11l-4-4h-6a2 2 0 0 1-2-2v-1"/>',
  'help-circle':'<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>',
  clock:'<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
  sparkles:'<path d="m12 3-1.9 5.8a2 2 0 0 1-1.287 1.288L3 12l5.8 1.9a2 2 0 0 1 1.288 1.287L12 21l1.9-5.8a2 2 0 0 1 1.287-1.288L21 12l-5.8-1.9a2 2 0 0 1-1.288-1.287Z"/><path d="M5 3v4"/><path d="M19 17v4"/><path d="M3 5h4"/><path d="M17 19h4"/>',
  'arrow-right':'<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
  'arrow-left':'<path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>',
  'check-circle-2':'<path d="M21.801 10A10 10 0 1 1 17 3.335"/><path d="m9 11 3 3L22 4"/>',
  x:'<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
  'search-x':'<path d="m13.5 8.5-5 5"/><path d="m8.5 8.5 5 5"/><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
  chevron:'<path d="m9 18 6-6-6-6"/>',
  'chevron-down':'<path d="m6 9 6 6 6-6"/>',
  check:'<path d="M20 6 9 17l-5-5"/>',
  copy:'<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
  list:'<line x1="8" x2="21" y1="6" y2="6"/><line x1="8" x2="21" y1="12" y2="12"/><line x1="8" x2="21" y1="18" y2="18"/><line x1="3" x2="3.01" y1="6" y2="6"/><line x1="3" x2="3.01" y1="12" y2="12"/><line x1="3" x2="3.01" y1="18" y2="18"/>',
  'book-open':'<path d="M12 7v14"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/>',
  'alert-triangle':'<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
  'external-link':'<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
};
const FILLED = {};
function ic(n,size){size=size||18;const filled=FILLED[n];return '<svg width="'+size+'" height="'+size+'" viewBox="0 0 24 24" fill="'+(filled?'currentColor':'none')+'" stroke="'+(filled?'none':'currentColor')+'" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+(ICONS[n]||'')+'</svg>';}

const esc=(s)=>{const d=document.createElement('div');d.textContent=s==null?'':String(s);return d.innerHTML;};
const norm=(s)=>s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');
const stripTags=(h)=>{const d=document.createElement('div');d.innerHTML=h==null?'':String(h);return (d.textContent||'').trim();};

/* theme -> category hue */
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
const PALETTE=['var(--cat-immigration)','var(--cat-travail)','var(--cat-education)','var(--cat-medias)','var(--cat-sante)','var(--cat-techno)'];

const LOGO=(cls)=>'<span class="logo '+(cls||'')+'"><span class="mark">é</span><span class="wm"><span class="t">Préparation TCF</span>'+(cls==='sm'?'':'<span class="s">Canada · Oral</span>')+'</span></span>';
const themeTag=(t)=>'<span class="theme-tag"><span class="dot" style="background:'+themeColor(t)+'"></span>'+esc(t)+'</span>';
const chip=(text)=>'<button class="chip" data-copy="'+esc(text)+'">'+esc(text)+'<span class="ci">'+ic('copy',13)+'</span></button>';

/* ---------- block renderers ---------- */
const BLK={
  prose:(b)=>'<div class="block prose">'+b.html+'</div>',
  callout:(b)=>{const v=b.variant||'info';const i=v==='warn'?'alert-triangle':v==='accent'?'sparkles':v==='danger'?'alert-triangle':'help-circle';
    return '<div class="block callout callout-'+v+'"><span class="ic">'+ic(i,18)+'</span><div class="ct">'+(b.title?'<strong>'+esc(b.title)+'</strong> ':'')+b.html+'</div></div>';},
  format:(b)=>'<div class="block fmt">'+b.rows.map(r=>'<div class="fr"><span class="fk">'+esc(r[0])+'</span><span class="fv">'+r[1]+'</span></div>').join('')+'</div>'
    +(b.badges&&b.badges.length?'<div class="block" style="display:flex;gap:8px;flex-wrap:wrap">'+b.badges.map(bd=>'<span class="badge '+(bd.cls||'badge-brand')+'">'+(bd.icon?ic(bd.icon,12):'')+esc(bd.label)+'</span>').join('')+'</div>':''),
  steps:(b)=>'<div class="block steps">'+b.items.map((s,i)=>{const c=s.color||PALETTE[i%PALETTE.length];const last=i===b.items.length-1;
    return '<div class="step"><div class="rail"><span class="num" style="background:'+c+'">'+(s.n||(i+1))+'</span>'+(last?'':'<span class="line"></span>')+'</div>'
      +'<div class="card card-pad-md" style="flex:1"><div style="display:flex;align-items:baseline;gap:10px;margin-bottom:'+(s.desc||s.phrase?'6px':'0')+';flex-wrap:wrap"><h3 style="font-size:var(--text-lg);margin:0">'+esc(s.titre)+'</h3>'+(s.duree?'<span style="font-family:var(--font-mono);font-size:var(--text-2xs);color:var(--text-faint);white-space:nowrap">'+esc(s.duree)+'</span>':'')+'</div>'
      +(s.desc?'<p style="font-size:var(--text-sm);color:var(--text-muted);margin:0 0 '+(s.phrase?'12px':'0')+';line-height:1.5">'+s.desc+'</p>':'')
      +(s.phrase?'<p class="phrase" style="border-left:3px solid '+c+';margin:0">'+s.phrase+'</p>':'')
    +'</div></div>';}).join('')+'</div>',
  reflexes:(b)=>{const d=b.variant==='danger';return '<div class="block reflexes">'+b.items.map(t=>'<div class="reflexe"><span class="chk"'+(d?' style="color:var(--danger)"':'')+'>'+ic(d?'x':'check-circle-2',18)+'</span><span>'+t+'</span></div>').join('')+'</div>';},
  table:(b)=>'<div class="block tbl-wrap"><table class="tbl">'+(b.headers?'<thead><tr>'+b.headers.map(h=>'<th>'+esc(h)+'</th>').join('')+'</tr></thead>':'')
    +'<tbody>'+b.rows.map(r=>'<tr>'+r.map((c,ci)=>'<td>'+(b.copyCol===ci?'<button class="chip" data-copy="'+esc(stripTags(c))+'">'+c+'<span class="ci">'+ic('copy',13)+'</span></button>':c)+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>',
  dialogue:(b)=>'<div class="block dialogue">'+(b.consigne?'<div class="dlg-consigne">'+b.consigne+'</div>':'')
    +'<div class="turns">'+b.turns.map(t=>{const cls=t.who==='Vous'?'vous':t.who==='Examinateur'?'ex':'narr';
      return '<div class="turn '+cls+'">'+(cls!=='narr'?'<span class="who">'+esc(t.who)+'</span>':'')+'<span class="say">'+t.html+'</span></div>';}).join('')+'</div></div>',
  phrasebank:(b)=>'<div class="block phrasebank">'+b.groups.map(g=>'<div class="pb-group"><div class="pb-label">'+esc(g.label)+'</div><div class="chips">'+g.phrases.map(chip).join('')+'</div></div>').join('')+'</div>',
  tags:(b)=>'<div class="block"><div style="display:flex;flex-wrap:wrap;gap:7px">'+b.items.map(themeTag).join('')+'</div></div>',
  fiche:(b)=>'<div class="block fiche">'+b.html+'</div>',
  modelAnswer:(b)=>'<div class="block model-answer card card-pad-md">'+(b.title?'<h3 style="font-size:var(--text-md);margin:0 0 14px">'+esc(b.title)+'</h3>':'')+b.parts.map(p=>'<div class="ma-part"><span class="ma-label">'+esc(p.label)+'</span><div class="ma-txt">'+p.html+'</div></div>').join('')+'</div>',
  frequency:(b)=>'<div class="block" style="display:flex;flex-direction:column;gap:12px">'+b.bars.map(t=>'<div class="theme-row"><div class="top"><span class="name"><span class="dot" style="background:'+(t.color||'var(--brand)')+'"></span>'+esc(t.label)+'</span><span class="pct">'+t.pct+'&nbsp;%</span></div><div class="track"><span class="fill" style="width:'+Math.min(100,t.pct*4)+'%;background:'+(t.color||'var(--brand)')+'"></span></div></div>').join('')+'</div>',
  template:(b)=>'<div class="block"><div class="tpl-card">'+b.html+'</div><div style="margin-top:10px"><button class="chip" data-copy="'+esc(b.copy||stripTags(b.html))+'">Copier la trame<span class="ci">'+ic('copy',13)+'</span></button></div></div>',
  stats:(b)=>'<div class="block" style="display:flex;gap:14px;flex-wrap:wrap">'+b.items.map(s=>'<div class="stat-card" style="flex:1;min-width:150px"><span class="val"'+(s.color?' style="color:'+s.color+'"':'')+'>'+esc(s.value)+'</span><span class="lab">'+esc(s.label)+'</span>'+(s.hint?'<span class="hint">'+esc(s.hint)+'</span>':'')+'</div>').join('')+'</div>',
  consignes:(b)=>'<div class="block card-grid">'+b.items.map((c,i)=>'<article class="subject-card"><span class="edge" style="background:'+(c.registre==='tu'?'var(--cat-sante)':'var(--cat-immigration)')+'"></span><div class="meta"><span class="rk">#'+String(c.n||i+1).padStart(2,'0')+'</span>'+(c.registre?'<span class="badge badge-neutral badge-sm">'+(c.registre==='tu'?'tutoiement':'vouvoiement')+'</span>':'')+(c.type?themeTag(c.type):'')+'</div><p class="q" style="font-size:var(--text-base);margin:0">'+esc(c.text)+'</p></article>').join('')+'</div>',
};
const renderBlocks=(arr)=>(arr||[]).map(b=>(BLK[b.type]||(()=>''))(b)).join('');

/* ---------- arguments finder (Tâche 3, à la demande) ---------- */
let argTheme=null;
const argThemes=()=>(CONTENT&&CONTENT.args&&CONTENT.args.themes)||[];
const argSubjects=(t)=>{const x=argThemes().find(z=>z.theme===t);return x?x.subjects:[];};
function argCols(s){
  const col=(label,items,cls)=>'<div class="arg-col"><div class="arg-col-h '+cls+'">'+label+'</div><ul>'+(items||[]).map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul></div>';
  return '<div class="arg-cols">'+col('Pour',s.pour,'pour')+col('Contre',s.contre,'contre')+col('Nuances',s.nuances,'nuance')+'</div>';
}
const argListHtml=(t)=>argSubjects(t).map(s=>'<div class="arg-item"><button class="arg-toggle" data-arg-toggle><span class="chev">'+ic('chevron',14)+'</span>'+esc(s.subject)+'</button><div class="arg-body" hidden>'+argCols(s)+'</div></div>').join('');
BLK.argfinder=()=>{
  const themes=argThemes();
  if(!themes.length)return '';
  if(!argTheme||!themes.some(t=>t.theme===argTheme))argTheme=themes[0].theme;
  const opts=themes.map(t=>'<option value="'+esc(t.theme)+'"'+(t.theme===argTheme?' selected':'')+'>'+esc(t.theme)+'</option>').join('');
  return '<div class="block argfinder"><p style="font-size:var(--text-sm);color:var(--text-muted);margin:0 0 12px">Besoin d\'idées ? Choisissez un thème, puis dépliez un sujet pour voir des arguments <strong>pour</strong>, <strong>contre</strong> et des <strong>nuances</strong>.</p>'
    +'<span class="select" style="width:100%;max-width:360px"><select data-arg-theme>'+opts+'</select><span class="chev chevron">'+ic('chevron-down',13)+'</span></span>'
    +'<div class="arg-list" data-arg-list>'+argListHtml(argTheme)+'</div></div>';
};

/* ---------- chapter view ---------- */
const BANDS=['Comprendre','Voir',"S'entraîner"];
const taches=()=>(CONTENT&&CONTENT.taches)||[];
const tacheById=(id)=>taches().find(c=>c.id===id);

function chapterToc(ch){
  let out='';
  for(const band of BANDS){
    const secs=ch.sections.filter(s=>s.band===band);
    if(!secs.length)continue;
    out+='<div class="toc-band">'+esc(band)+'</div>'+secs.map(s=>'<button class="toc-link" data-scroll="'+s.id+'">'+esc(s.title)+'</button>').join('');
  }
  return out;
}
function chapterBody(ch){
  let out='';
  for(const band of BANDS){
    const secs=ch.sections.filter(s=>s.band===band);
    if(!secs.length)continue;
    out+='<div class="ch-band"><div class="ch-band-label">'+esc(band)+'</div>'
      +secs.map(s=>'<section class="ch-section" id="'+s.id+'"><h2>'+esc(s.title)+'</h2>'+renderBlocks(s.blocks)+'</section>').join('')+'</div>';
  }
  return out;
}
function chapterPager(ch){
  const list=taches();const i=list.findIndex(c=>c.id===ch.id);
  const prev=i>0?list[i-1]:null, next=i<list.length-1?list[i+1]:null;
  return '<div class="pager">'
    +(prev?'<button data-nav="'+prev.id+'"><span class="pg-k">'+ic('arrow-left',13)+' Chapitre précédent</span><span class="pg-t">Tâche '+prev.num+' · '+esc(prev.title)+'</span></button>':'<span></span>')
    +(next?'<button class="pg-r" data-nav="'+next.id+'"><span class="pg-k">Chapitre suivant '+ic('arrow-right',13)+'</span><span class="pg-t">Tâche '+next.num+' · '+esc(next.title)+'</span></button>':'')
  +'</div>';
}
function viewTache(id){
  const ch=tacheById(id);
  if(!ch)return '<div class="view"><main class="chapter"><div class="placeholder">Chapitre introuvable.</div></main></div>';
  const crumb='<nav class="crumb"><button data-nav="accueil">Manuel</button><span class="sep">/</span><span>Tâche '+ch.num+'</span></nav>';
  const head='<div class="ch-head">'+crumb
    +'<span class="eyebrow" style="display:block;margin-bottom:10px">'+esc(ch.eyebrow)+'</span>'
    +'<h1>'+esc(ch.title)+'</h1>'
    +(ch.lede?'<p class="lede">'+esc(ch.lede)+'</p>':'')
    +'<div class="ch-badges"><span class="badge badge-brand">'+ic('clock',12)+' '+esc(ch.duree)+'</span><span class="badge badge-neutral">'+esc(ch.prep)+'</span></div>'
  +'</div>';
  if(!ch.sections.length){
    return '<div class="view"><main class="chapter">'+head
      +'<div class="placeholder">'+ic('book-open',26)+'<p style="margin-top:12px">Ce chapitre est en cours de rédaction.</p></div>'
      +chapterPager(ch)+'</main></div>';
  }
  const mob='<div class="site-mobnav"><div class="scroller">'+ch.sections.map(s=>'<button class="toc-link" data-scroll="'+s.id+'">'+esc(s.title)+'</button>').join('')+'</div></div>';
  return '<div class="view"><main class="chapter">'+head+mob
    +'<div class="ch-layout"><aside class="ch-toc">'+chapterToc(ch)+'</aside>'
    +'<div class="ch-main">'+chapterBody(ch)+chapterPager(ch)+'</div></div>'
  +'</main></div>';
}

/* ---------- annexes ---------- */
function annexePlaceholder(eyebrow,title,lede){
  return '<div class="view"><main class="chapter">'
    +'<nav class="crumb"><button data-nav="accueil">Manuel</button><span class="sep">/</span><span>Annexe</span></nav>'
    +'<div class="ch-head"><span class="eyebrow" style="display:block;margin-bottom:10px">'+esc(eyebrow)+'</span><h1>'+esc(title)+'</h1><p class="lede">'+esc(lede)+'</p></div>'
    +'<div class="placeholder">'+ic('book-open',26)+'<p style="margin-top:12px">Annexe en cours de rédaction.</p></div>'
  +'</main></div>';
}
function annexeHead(a){
  return '<div class="ch-head"><nav class="crumb"><button data-nav="accueil">Manuel</button><span class="sep">/</span><span>Annexe</span></nav>'
    +'<span class="eyebrow" style="display:block;margin-bottom:10px">'+esc(a.eyebrow)+'</span><h1>'+esc(a.title)+'</h1>'+(a.lede?'<p class="lede">'+esc(a.lede)+'</p>':'')+'</div>';
}
function viewAnnexe(a){
  const toc=a.sections.map(s=>'<button class="toc-link" data-scroll="'+s.id+'">'+esc(s.title)+'</button>').join('');
  const body=a.sections.map(s=>'<section class="ch-section" id="'+s.id+'"><h2>'+esc(s.title)+'</h2>'+renderBlocks(s.blocks)+'</section>').join('');
  const mob='<div class="site-mobnav"><div class="scroller">'+a.sections.map(s=>'<button class="toc-link" data-scroll="'+s.id+'">'+esc(s.title)+'</button>').join('')+'</div></div>';
  return '<div class="view"><main class="chapter">'+annexeHead(a)+mob
    +'<div class="ch-layout"><aside class="ch-toc">'+toc+'</aside><div class="ch-main">'+body+'</div></div></main></div>';
}
const viewVocab=()=>CONTENT&&CONTENT.vocab?viewAnnexe(CONTENT.vocab):annexePlaceholder('Annexe A · Lexique','Vocabulaire par thème','Le lexique bilingue, thème par thème — à venir.');
const viewConnecteurs=()=>CONTENT&&CONTENT.connecteurs?viewAnnexe(CONTENT.connecteurs):annexePlaceholder('Annexe B · Discours','Connecteurs & expressions','Les connecteurs classés par fonction, la concession en vedette — à venir.');
function viewCram(){
  const a=CONTENT&&CONTENT.cram;
  if(!a)return annexePlaceholder("Veille d'examen","Avant d'entrer","L'essentiel des 3 tâches, sur une seule page — à venir.");
  const body=a.sections.map(s=>'<section class="ch-section" id="'+s.id+'"><h2>'+esc(s.title)+'</h2>'+renderBlocks(s.blocks)+'</section>').join('');
  return '<div class="view"><main class="chapter" style="max-width:var(--container-narrow)">'+annexeHead(a)+body+'</main></div>';
}

/* ---------- accueil ---------- */
function viewAccueil(){
  const list=taches();
  const tasks=list.map(c=>({id:c.id,n:String(c.num),titre:c.title,duree:c.duree,prep:c.prep,desc:c.desc,ico:c.num===1?'messages-square':c.num===2?'help-circle':'mic',focus:c.num===3}));
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

  const tocRows=[
    ...list.map(c=>({nav:c.id,n:String(c.num),t:'Tâche '+c.num+' · '+c.title,s:c.duree+' · '+c.prep})),
    {nav:'banque',n:'★',t:'Banque des '+SUBJECT_COUNT+' réponses',s:'Tâche 3 · sujets 2026 triés par fréquence, avec audio'},
    {nav:'vocabulaire',n:'A',t:'Vocabulaire par thème',s:'Annexe · lexique bilingue'},
    {nav:'connecteurs',n:'B',t:'Connecteurs & expressions',s:'Annexe · discours, concession'},
    {nav:'avant',n:'⚑',t:"Avant d'entrer",s:"L'essentiel, la veille de l'examen"},
  ];
  const tocBook='<div class="toc-book">'+tocRows.map(r=>'<button class="tb-row" data-nav="'+r.nav+'"><span class="tb-n">'+r.n+'</span><span><span class="tb-t">'+esc(r.t)+'</span><span class="tb-s">'+esc(r.s)+'</span></span><span class="tb-go">'+ic('arrow-right',16)+'</span></button>').join('')+'</div>';

  return '<div class="view">'
  +'<section class="hero"><div class="grid">'
    +'<div>'
      +'<span class="eyebrow" style="display:block;margin-bottom:16px">TCF Canada · Expression orale</span>'
      +'<h1>Le manuel complet de&nbsp;l\'<em>expression orale.</em></h1>'
      +'<p class="lede">Les trois tâches expliquées en détail — méthode, simulations, phrases prêtes à l\'emploi — plus '+SUBJECT_COUNT+' réponses modèles B2 avec audio pour la Tâche 3.</p>'
      +'<div style="display:flex;gap:12px;flex-wrap:wrap">'
        +'<button class="btn btn-primary btn-lg" data-nav="t1">Commencer par la Tâche 1 '+ic('arrow-right',17)+'</button>'
        +'<button class="btn btn-outline btn-lg" data-nav="banque">Banque des '+SUBJECT_COUNT+' sujets</button>'
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
    +'<div class="task-grid">'+tasks.map(t=>'<div class="card card-interactive '+(t.focus?'card-floating':'')+' card-pad-lg task'+(t.focus?' focus':'')+'" data-nav="'+t.id+'">'
      +'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px"><span class="task-icon">'+ic(t.ico,19)+'</span><span class="task-num">'+t.n+'</span></div>'
      +'<h3 style="font-size:var(--text-lg);margin:0 0 8px">'+esc(t.titre)+'</h3>'
      +'<p style="font-size:var(--text-sm);color:var(--text-muted);line-height:1.55;margin:0 0 14px;min-height:62px">'+esc(t.desc)+'</p>'
      +'<div style="display:flex;gap:8px;flex-wrap:wrap"><span class="badge badge-brand badge-sm">'+ic('clock',12)+' '+esc(t.duree)+'</span><span class="badge badge-neutral badge-sm">'+esc(t.prep)+'</span>'+(t.focus?'<span class="badge badge-accent badge-sm">'+SUBJECT_COUNT+' modèles</span>':'')+'</div>'
      +'<div class="task-toc"><span>Comprendre</span><span>·</span><span>Voir</span><span>·</span><span>S\'entraîner</span></div>'
    +'</div>').join('')+'</div>'
  +'</section>'

  +'<section class="section-band"><div class="section"><span class="eyebrow" style="display:block;margin-bottom:10px">Le sommaire</span>'
    +'<h2 style="margin:0 0 6px">Table des matières</h2>'
    +'<p style="color:var(--text-secondary);margin:0 0 22px;max-width:54ch">Tout le manuel, à plat. Touchez une entrée pour y aller directement.</p>'
    +tocBook
  +'</div></section>'

  +'<section class="section synth-grid" style="display:grid;grid-template-columns:.9fr 1.1fr;gap:var(--space-8);align-items:center">'
    +'<div><span class="eyebrow" style="display:block;margin-bottom:10px">Synthèse du corpus · Tâche 3</span>'
      +'<h2 style="margin:0 0 14px">Six thèmes couvrent 78&nbsp;% des sujets</h2>'
      +'<p style="color:var(--text-secondary);line-height:1.6;margin:0 0 24px;max-width:40ch">703 sujets relevés de janvier 2022 à juin 2026, classés par thème. Révisez ces six familles et vous êtes prêt(e) pour la grande majorité des tirages.</p>'
      +'<div style="display:flex;gap:14px"><div class="stat-card" style="flex:1"><span class="val">703</span><span class="lab">sujets analysés</span><span class="hint">2022 → 2026</span></div>'
      +'<div class="stat-card" style="flex:1"><span class="val" style="color:var(--accent)">'+SUBJECT_COUNT+'</span><span class="lab">réponses modèles B2</span><span class="hint">dédupliquées, audio</span></div></div>'
    +'</div>'
    +'<div style="display:flex;flex-direction:column;gap:13px">'+themes.map(t=>'<div class="theme-row"><div class="top"><span class="name"><span class="dot" style="background:'+t.color+'"></span>'+t.label+'</span><span class="pct">'+t.pct+'&nbsp;%</span></div><div class="track"><span class="fill" style="width:'+(t.pct*4)+'%;background:'+t.color+'"></span></div></div>').join('')+'</div>'
  +'</section>'

  +'<section class="section" style="padding-top:0"><p style="font-size:var(--text-sm);color:var(--text-muted);margin:0;text-align:center">La <strong>Compréhension orale</strong> est une épreuve distincte, hors de ce manuel.</p></section>'
  +'</div>';
}

/* ---------- banque (Tâche 3) ---------- */
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
    +'<nav class="crumb"><button data-nav="accueil">Manuel</button><span class="sep">/</span><button data-nav="t3">Tâche 3</button><span class="sep">/</span><span>Banque</span></nav>'
    +'<div style="margin-bottom:22px"><span class="eyebrow" style="display:block;margin-bottom:10px">Tâche 3 · Expression d\'un point de vue</span>'
    +'<h1 style="margin:0 0 10px">Banque des '+SUBJECT_COUNT+' réponses</h1>'
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

/* ---------- footer ---------- */
function viewFooter(){
  return '<footer class="site-footer"><div class="top">'
    +'<div style="max-width:34ch">'+LOGO('sm')+'<p style="margin-top:14px;font-size:var(--text-sm);color:var(--text-muted);line-height:1.55">Le manuel de l\'Expression orale du TCF Canada. Objectif&nbsp;: B2 / NCLC&nbsp;7.</p></div>'
    +'<div class="cols">'
      +'<div><div class="eyebrow" style="margin-bottom:12px">Les tâches</div>'
        +'<button class="foot-link" data-nav="t1">Tâche 1 · Présentation</button><button class="foot-link" data-nav="t2">Tâche 2 · Interaction</button><button class="foot-link" data-nav="t3">Tâche 3 · Point de vue</button></div>'
      +'<div><div class="eyebrow" style="margin-bottom:12px">Ressources</div>'
        +'<button class="foot-link" data-nav="banque">Banque des '+SUBJECT_COUNT+' réponses</button><button class="foot-link" data-nav="vocabulaire">Vocabulaire</button><button class="foot-link" data-nav="connecteurs">Connecteurs</button><button class="foot-link" data-nav="avant">Avant d\'entrer</button></div>'
    +'</div></div>'
    +'<div class="bottom"><div class="inner">Projet personnel · Données : reussir-tcfcanada.com (2022–2026) · Design system — recréation</div></div>'
  +'</footer>';
}

/* ---------- shell + routing ---------- */
let view='accueil';
const VIEWS={
  accueil:viewAccueil, banque:renderBanque,
  vocabulaire:viewVocab, connecteurs:viewConnecteurs, avant:viewCram,
  t1:()=>viewTache('t1'), t2:()=>viewTache('t2'), t3:()=>viewTache('t3'), methode:()=>viewTache('t3'),
};
function header(){
  const links=[['accueil','Accueil'],['t1','Tâche 1'],['t2','Tâche 2'],['t3','Tâche 3'],['vocabulaire','Vocabulaire'],['connecteurs','Connecteurs']];
  const cur=view==='methode'?'t3':view;
  const mob=[['accueil','Accueil'],['t1','Tâche 1'],['t2','Tâche 2'],['t3','Tâche 3'],['banque','Banque'],['vocabulaire','Vocab.'],['connecteurs','Conn.'],['avant','Avant']];
  return '<header class="site-header"><div class="inner">'
    +'<button data-nav="accueil" style="background:none;border:none;cursor:pointer;padding:0">'+LOGO('')+'</button>'
    +'<nav class="site-nav">'+links.map(l=>'<button class="nav-link'+(['vocabulaire','connecteurs'].includes(l[0])?' nav-annexe':'')+(cur===l[0]?' active':'')+'" data-nav="'+l[0]+'">'+l[1]+'</button>').join('')+'</nav>'
    +'<div class="header-right">'
      +'<button class="header-cram" data-nav="avant">Avant d\'entrer</button>'
      +'<span class="objectif-pill"><span class="dot"></span>Objectif&nbsp;B2 · NCLC&nbsp;7</span>'
      +'<button class="btn btn-accent btn-sm" data-nav="banque">'+ic('book-open',15)+' Banque ('+SUBJECT_COUNT+')</button>'
    +'</div></div>'
    +'<div class="site-mobnav"><div class="scroller">'+mob.map(l=>'<button class="toc-link'+(cur===l[0]?' active':'')+'" data-nav="'+l[0]+'">'+l[1]+'</button>').join('')+'</div></div>'
  +'</header>';
}
function render(){
  const fn=VIEWS[view]||viewAccueil;
  document.getElementById('app').innerHTML=header()+'<div>'+fn()+'</div>'+viewFooter();
  document.querySelectorAll('[data-audio]').forEach(bindAudio);
  setupSpy();
}
function route(){
  const raw=(location.hash||'').replace(/^#/,'');
  const [v,a]=raw.split('/');
  view=VIEWS[v]?v:'accueil';
  render();
  if(a){const el=document.getElementById(a);if(el){el.scrollIntoView();return;}}
  window.scrollTo({top:0});
}
function nav(v,a){const h='#'+v+(a?'/'+a:'');if(location.hash===h){route();}else{location.hash=h;}}
window.addEventListener('hashchange',route);

/* scroll-spy for the chapter TOC */
let _spyObs=null;
function setupSpy(){
  if(_spyObs){_spyObs.disconnect();_spyObs=null;}
  const links=Array.from(document.querySelectorAll('.toc-link[data-scroll]'));
  if(!links.length)return;
  const byId=new Map();links.forEach(a=>{const id=a.getAttribute('data-scroll');if(!byId.has(id))byId.set(id,[]);byId.get(id).push(a);});
  _spyObs=new IntersectionObserver((entries)=>{
    entries.forEach(e=>{if(e.isIntersecting){
      links.forEach(x=>x.classList.remove('active'));
      (byId.get(e.target.id)||[]).forEach(x=>x.classList.add('active'));
    }});
  },{rootMargin:'-45% 0px -50% 0px'});
  document.querySelectorAll('.ch-section').forEach(s=>_spyObs.observe(s));
}

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
  const cp=e.target.closest('[data-copy]'); if(cp){const txt=cp.getAttribute('data-copy')||cp.textContent;if(navigator.clipboard){navigator.clipboard.writeText(txt).then(()=>{cp.classList.add('copied');setTimeout(()=>cp.classList.remove('copied'),1100);}).catch(()=>{});}return;}
  const navEl=e.target.closest('[data-nav]'); if(navEl){nav(navEl.getAttribute('data-nav'));return;}
  const sc=e.target.closest('[data-scroll]'); if(sc){const el=document.getElementById(sc.getAttribute('data-scroll'));if(el)el.scrollIntoView({behavior:'smooth'});return;}
  const reset=e.target.closest('[data-reset]'); if(reset){filt.q='';filt.theme='';filt.prio=false;render();return;}
  const tog=e.target.closest('[data-toggle]'); if(tog){const dis=tog.closest('.disclosure');const body=dis.querySelector('.body');const open=dis.classList.toggle('open');body.hidden=!open;tog.querySelector('.lbl').textContent=open?'Masquer la réponse':'Voir la réponse modèle';return;}
  const at=e.target.closest('[data-arg-toggle]'); if(at){const it=at.closest('.arg-item');const body=it.querySelector('.arg-body');const open=it.classList.toggle('open');body.hidden=!open;return;}
});
document.addEventListener('input',(e)=>{
  if(e.target.matches('[data-q]')){filt.q=e.target.value;renderCards();}
});
document.addEventListener('change',(e)=>{
  if(e.target.matches('[data-theme]')){filt.theme=e.target.value;render();}
  if(e.target.matches('[data-prio]')){filt.prio=e.target.checked;render();}
  if(e.target.matches('[data-arg-theme]')){argTheme=e.target.value;const l=document.querySelector('[data-arg-list]');if(l)l.innerHTML=argListHtml(argTheme);}
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

route();
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
