# Préparation TCF Canada — Oral (Compréhension + Production)

Projet personnel de préparation aux épreuves **orales** du **TCF Canada** : la **Compréhension Orale** (écoute) et la **Production / Expression Orale** (les 3 tâches). Objectif : **niveau B2** (NCLC 7+).

## 📁 Structure

```
french/
├── comprehension-orale/
│   └── comprehension-orale.md      → le test d'écoute + conseils + site d'entraînement
│
├── production-orale/               (= Expression Orale, 3 tâches)
│   ├── vocabulaire/                (ressource partagée)
│   │   ├── vocabulaire-par-theme.md          → lexique bilingue, 16 thèmes
│   │   └── connecteurs-et-expressions.md     → connecteurs, opinion, concession, proverbes
│   ├── tache1/  tache1.md          → Entretien dirigé (se présenter)
│   ├── tache2/  tache2.md          → Exercice en interaction (obtenir des infos)
│   └── tache3/                     → Expression d'un point de vue
│       ├── tache3.md               → vue d'ensemble + conseils + index du dossier
│       ├── structure-type.md       → la structure passe-partout en 5 parties
│       ├── guide-pas-a-pas.md      → déroulé jour J + critères de notation (EN)
│       ├── exemples.md             → 5 réponses modèles annotées
│       ├── sujets-par-frequence.md → thèmes classés par fréquence (703 sujets)
│       └── data/                   → corpus brut + scripts d'analyse
│
└── AMELIORATIONS.md                → feuille de route (recherche, pistes d'amélioration)
```

## 🎧 Compréhension Orale

→ **[`comprehension-orale/comprehension-orale.md`](comprehension-orale/comprehension-orale.md)**

35 min · 39 questions · QCM (4 options) · **chaque audio passe une seule fois**. Le fichier explique le format, le barème (échelle 100–699, **B2 = 400–499**, NCLC 7 dès 458) et donne les conseils B2. Entraînement avec audios + transcriptions : **[fuck-tcf.xyz](https://fuck-tcf.xyz/)**.

## 🗣️ Production Orale (Expression Orale)

Un **entretien individuel enregistré** d'environ **12 minutes**, en **3 tâches** enchaînées avec le même examinateur :

| Tâche | Intitulé | Durée | Préparation | Ce que vous faites |
|---|---|---|---|---|
| **[1](production-orale/tache1/tache1.md)** | Entretien dirigé | 2 min | ❌ aucune | Vous **répondez** aux questions personnelles de l'examinateur |
| **[2](production-orale/tache2/tache2.md)** | Exercice en interaction | 5 min 30 | ✅ 2 min | Vous **posez des questions** pour obtenir une information |
| **[3](production-orale/tache3/tache3.md)** | Expression d'un point de vue | 4 min 30 | ❌ aucune | Vous **défendez un avis** structuré (monologue) |

> 💡 La **Tâche 3** est la plus exigeante et la plus travaillée ici : voir le dossier [`production-orale/tache3/`](production-orale/tache3/) (structure, exemples, sujets, corpus).

## 🎯 Plan de révision conseillé

1. **Compréhension Orale** : entraînement régulier en conditions réelles (un audio = une écoute), puis lecture des transcriptions pour combler le vocabulaire manquant.
2. **Tâches 1 & 2** : mémoriser les réflexes (développer ses réponses ; poser des questions variées et polies) et le bon registre `tu`/`vous`.
3. **Tâche 3** : mémoriser la **structure passe-partout** ([`structure-type.md`](production-orale/tache3/structure-type.md)), réviser les **6 thèmes prioritaires** (~78 % des sujets : Immigration, Travail, Éducation, Santé, Médias, Technologie), puis s'entraîner **chronomètre en main** (~4 min 30 sans préparation).

## 🗣️ S'entraîner avec Claude (professeur de français)

**Le plus simple : la commande `/tcf-pratique`** (skill du projet, dans `.claude/skills/`).
Claude joue un **professeur** bienveillant — il enseigne, explique et corrige en donnant la règle, **sans jamais vous noter**.

- `/tcf-pratique` → il vous demande ce que vous voulez travailler, ou propose un sujet guidé.
- `/tcf-pratique travail` (ou `immigration`, `santé`, `technologie`…) → un sujet du thème.
- `/tcf-pratique vocabulaire` → mini-leçon de lexique + petits exercices.
- `/tcf-pratique méthode` → leçon sur la structure d'une réponse.
- `/tcf-pratique idées` → on brainstorme ensemble des arguments et des exemples.
- `/tcf-pratique examen` → entraînement réaliste à la Tâche 3 (aucune prépa + 4 min 30 + retour bienveillant).

> Le skill est centré sur la **Tâche 3** ; il pioche de vrais sujets dans [`production-orale/tache3/data/corpus.txt`](production-orale/tache3/data/corpus.txt).

## 📊 Synthèse de l'analyse (Tâche 3)

Les **6 thèmes les plus fréquents** couvrent ~78 % de tous les sujets posés depuis 2022 :

1. Immigration / vivre à l'étranger / intégration — **20 %**
2. Travail / emploi / salaire / carrière — **19 %**
3. Éducation / école / études / diplômes — **12 %**
4. Santé / alimentation / mode de vie — **10 %**
5. Télévision / médias / information — **9 %**
6. Technologie / Internet / réseaux sociaux — **9 %**

*Source : [reussir-tcfcanada.com](https://reussir-tcfcanada.com/expression-orale/), sessions de janvier 2022 à juin 2026. Détail : [`production-orale/tache3/sujets-par-frequence.md`](production-orale/tache3/sujets-par-frequence.md).*

## 🖨️ Générer les PDF

`make build` convertit tous les `.md` en `.pdf` (nécessite `pandoc` + `weasyprint`). `make clean` supprime les PDF générés.
