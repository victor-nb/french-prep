# Préparation TCF Canada — Oral (Compréhension + Production)

Projet personnel de préparation aux épreuves **orales** du **TCF Canada** : la **Compréhension Orale** (écoute) et la **Production / Expression Orale** (les 3 tâches). Objectif : **niveau B2** (NCLC 7+).

> 🌐 **Site en ligne → https://victor-nb.github.io/french-prep**

## 📁 Structure

```
french/
├── src/                                ← toutes les sources Markdown
│   ├── comprehension-orale/
│   │   └── comprehension-orale.md      → le test d'écoute + conseils + site d'entraînement
│   └── production-orale/               (= Expression Orale, 3 tâches)
│       ├── vocabulaire/                (ressource partagée)
│       │   ├── vocabulaire-par-theme.md          → lexique bilingue, 16 thèmes
│       │   └── connecteurs-et-expressions.md     → connecteurs, opinion, concession…
│       ├── tache1/  tache1.md          → Présentation (se présenter)
│       ├── tache2/  tache2.md          → Exercice en interaction (obtenir des infos)
│       └── tache3/                     → Expression d'un point de vue
│           ├── 0-tache3.md             → index du dossier (commencez ici)
│           ├── 1-structure-type.md     → la structure passe-partout en 5 parties
│           ├── 2-guide-pas-a-pas.md    → déroulé jour J + critères de notation (EN)
│           ├── 3-exemples.md           → 6 réponses modèles annotées
│           ├── 4-banque-sujets-arguments.md → 10 thèmes × 10 sujets, ~1 300 arguments
│           ├── 5-sujets-par-frequence.md → thèmes classés par fréquence (703 sujets)
│           ├── examples/               → 214 réponses modèles B2 (tous les sujets 2026)
│           │   ├── 0-index.md          → index trié par priorité (fréquence d'apparition)
│           │   ├── NNN-slug.md         → 1 sujet = 1 réponse rédigée + bloc audio
│           │   └── audio/              → MP3 générés par `make speak` (NNN-slug.mp3)
│           ├── tts.py                  → synthèse vocale des réponses (voix humaine clonée)
│           ├── build_site.py           → génère index.html (le manuel, site GitHub Pages)
│           ├── content/                → contenu des chapitres T2/T3 + annexes (JSON lu par build_site.py)
│           └── data/                   → corpus brut + scripts d'analyse + voix de référence
├── index.html                          ← site statique (make site) — GitHub Pages
├── pdf/                                ← PDF générés (make build) — même arborescence que src/
├── Makefile
└── README.md
```

## 🎧 Compréhension Orale

→ **[`src/comprehension-orale/comprehension-orale.md`](src/comprehension-orale/comprehension-orale.md)**

35 min · 39 questions · QCM (4 options) · **chaque audio passe une seule fois**. Le fichier explique le format, le barème (échelle 100–699, **B2 = 400–499**, NCLC 7 dès 458) et donne les conseils B2. Entraînement avec audios + transcriptions : **[fuck-tcf.xyz](https://fuck-tcf.xyz/)**.

## 🗣️ Production Orale (Expression Orale)

Un **entretien individuel enregistré** d'environ **12 minutes**, en **3 tâches** enchaînées avec le même examinateur :

| Tâche | Intitulé | Durée | Préparation | Ce que vous faites |
|---|---|---|---|---|
| **[1](src/production-orale/tache1/tache1.md)** | Entretien dirigé | 2 min | ❌ aucune | Vous **répondez** aux questions personnelles de l'examinateur |
| **[2](src/production-orale/tache2/tache2.md)** | Exercice en interaction | 5 min 30 | ✅ 2 min | Vous **posez des questions** pour obtenir une information |
| **[3](src/production-orale/tache3/0-tache3.md)** | Expression d'un point de vue | 4 min 30 | ❌ aucune | Vous **défendez un avis** structuré (monologue) |

> 💡 La **Tâche 3** est la plus exigeante et la plus travaillée ici : voir le dossier [`src/production-orale/tache3/`](src/production-orale/tache3/) (structure, exemples, sujets, corpus).

## 🎯 Plan de révision conseillé

1. **Compréhension Orale** : entraînement régulier en conditions réelles (un audio = une écoute), puis lecture des transcriptions pour combler le vocabulaire manquant.
2. **Tâches 1 & 2** : mémoriser les réflexes (développer ses réponses ; poser des questions variées et polies) et le bon registre `tu`/`vous`.
3. **Tâche 3** : mémoriser la **structure passe-partout** ([`1-structure-type.md`](src/production-orale/tache3/1-structure-type.md)), réviser les **6 thèmes prioritaires** (~78 % des sujets : Immigration, Travail, Éducation, Santé, Médias, Technologie), puis s'entraîner **chronomètre en main** (~4 min 30 sans préparation).

## 🗣️ S'entraîner avec Claude (professeur de français)

**Le plus simple : la commande `/tcf-pratique`** (skill du projet, dans `.claude/skills/`).
Claude joue un **professeur** bienveillant — il enseigne, explique et corrige en donnant la règle, **sans jamais vous noter**.

- `/tcf-pratique` → il vous demande ce que vous voulez travailler, ou propose un sujet guidé.
- `/tcf-pratique travail` (ou `immigration`, `santé`, `technologie`…) → un sujet du thème.
- `/tcf-pratique vocabulaire` → mini-leçon de lexique + petits exercices.
- `/tcf-pratique méthode` → leçon sur la structure d'une réponse.
- `/tcf-pratique idées` → on brainstorme ensemble des arguments et des exemples.
- `/tcf-pratique examen` → entraînement réaliste à la Tâche 3 (aucune prépa + 4 min 30 + retour bienveillant).

> Le skill est centré sur la **Tâche 3** ; il pioche de vrais sujets dans [`src/production-orale/tache3/data/corpus.txt`](src/production-orale/tache3/data/corpus.txt).

## 📊 Synthèse de l'analyse (Tâche 3)

Les **6 thèmes les plus fréquents** couvrent ~78 % de tous les sujets posés depuis 2022 :

1. Immigration / vivre à l'étranger / intégration — **20 %**
2. Travail / emploi / salaire / carrière — **19 %**
3. Éducation / école / études / diplômes — **12 %**
4. Santé / alimentation / mode de vie — **10 %**
5. Télévision / médias / information — **9 %**
6. Technologie / Internet / réseaux sociaux — **9 %**

*Source : [reussir-tcfcanada.com](https://reussir-tcfcanada.com/expression-orale/), sessions de janvier 2022 à juin 2026. Détail : [`src/production-orale/tache3/5-sujets-par-frequence.md`](src/production-orale/tache3/5-sujets-par-frequence.md).*

## 🎙️ Réponses modèles & audios (Tâche 3)

Le dossier [`src/production-orale/tache3/examples/`](src/production-orale/tache3/examples/) contient **une réponse modèle B2 rédigée pour chacun des 214 sujets de 2026** (structure passe-partout en 5 parties, ~390 mots ≈ 4 min de parole). Les sujets sont **dédupliqués** (les reformulations quasi identiques sont fusionnées) et **classés par priorité** : plus un sujet est revenu souvent, plus il risque de retomber — voir [`examples/0-index.md`](src/production-orale/tache3/examples/0-index.md).

Chaque réponse peut être **lue à voix haute par une IA**, pour s'entraîner à la **compréhension** et au **shadowing** :

| Commande | Effet |
|---|---|
| `make voice` | Télécharge la **voix de référence humaine** (extrait FLEURS, CC-BY) qui sera clonée |
| `make speak-test` | Génère **3 audios** (test rapide de la voix) |
| `make speak` | Génère **tous** les audios manquants → `examples/audio/*.mp3` (reprend où il s'est arrêté) |
| `make speak ARGS="--ranks 1-20"` | Génère seulement une plage de sujets |
| `make speak ARGS="--speed 0.85"` | Change la vitesse de lecture (défaut `0.9`, plus lent < 1) |
| `make clean-audio` | Supprime les audios générés |

> 🔊 **Voix « la moins synthétique possible » :** on utilise **Higgs Audio v3** (modèle ~4B, tourne en local sur Apple Silicon via MLX) en **clonant une vraie voix humaine** (`data/voix-reference.wav`) plutôt que la voix par défaut. Pour changer de voix, remplacez simplement `data/voix-reference.wav` + `data/voix-reference.txt` par votre propre extrait (~8-15 s) et sa transcription. Installation : `pip install mlx-audio soundfile datasets scipy`.
>
> ⚙️ **Régénérer l'index des sujets** (après une mise à jour du corpus) : `make examples`.

## 🌐 Site web (GitHub Pages)

`make site` génère un **`index.html`** autonome : un **manuel complet de l'Expression orale**, en HTML/CSS/JS pur (sans build). Il contient :

- **un chapitre par tâche** (1, 2, 3), chacun structuré en **Comprendre → Voir → S'entraîner** : format, méthode, simulations, réflexes, et banques de phrases **copiables** ;
- la **Banque des 214 réponses** (recherche, filtre par thème, lecteur audio) ;
- un **trouveur d'arguments** à la demande (10 thèmes × 10 sujets : *pour / contre / nuances*) ;
- les annexes **Vocabulaire** (16 thèmes, FR→EN) et **Connecteurs** (par fonction, concession en vedette) ;
- une page **« Avant d'entrer »** : l'essentiel à relire la veille de l'examen.

Aperçu local : `open index.html`. Mis en ligne via **GitHub Pages** (*Settings → Pages → branche `main`, dossier `/`*) → **https://victor-nb.github.io/french-prep**. Le contenu rédactionnel des chapitres vit dans `src/production-orale/tache3/content/*.json` (lu par `build_site.py`) ; les audios (`examples/audio/`) sont **versionnés** pour que Pages puisse les jouer.

## 🖨️ Générer les PDF

`make build` convertit tous les `.md` en `.pdf` dans le dossier **`pdf/`** (qui reprend la même arborescence que les sources ; nécessite `pandoc` + `weasyprint`). `make clean` supprime le dossier `pdf/`.
