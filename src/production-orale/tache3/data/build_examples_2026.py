#!/usr/bin/env python3
"""Construit la liste dédupliquée et priorisée des sujets Tâche 3 de l'année 2026.

Pipeline :
1. Extraire du corpus tous les sujets datés 2026 (avec leur mois).
2. Regrouper les reformulations quasi identiques (même méthode que
   ``cluster_sujets.py`` : normalisation + similarité difflib). Chaque groupe = une
   « question canonique » ; sa taille = sa fréquence d'apparition = sa priorité
   (un sujet reformulé plusieurs fois retombe probablement le jour J).
3. Classer chaque groupe par thème (mots-clés).
4. Émettre ``examples/_index.json`` (pilote la génération + la synthèse vocale) et
   ``examples/0-index.md`` (index lisible, trié par priorité).

Exécuter depuis ``src/production-orale/tache3/`` :  ``python3 data/build_examples_2026.py``
"""
from __future__ import annotations

import json
import re
import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path

__all__ = ["build", "Cluster"]

YEAR = "2026"
SIMILARITY_THRESHOLD = 0.78

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "corpus.txt"
OUT_DIR = HERE.parent / "examples"

# tournures rhétoriques retirées avant comparaison (reprises de cluster_sujets.py)
_BOILER = [
    r"qu'?en pensez[- ]vous", r"etes[- ]vous d'?accord( avec cette affirmation)?",
    r"qu'?en dites[- ]vous", r"que pensez[- ]vous( de cette affirmation)?",
    r"selon vous", r"a votre avis", r"d'?apres vous", r"pensez[- ]vous que",
    r"croyez[- ]vous que", r"pourquoi", r"justifiez( votre reponse| votre point de vue)?",
    r"expliquez( pourquoi)?", r"argumentez", r"partagez[- ]vous cet avis",
    r"partagez[- ]vous cette opinion", r"quel est votre avis( sur)?",
    r"donnez votre (avis|opinion|point de vue)", r"de cette affirmation",
    r"avec cette affirmation", r"est-?ce une bonne idee", r"selon certains",
    r"de nos jours", r"aujourd'?hui", r"actuellement",
]
_BOILER_RE = re.compile("|".join(_BOILER))
_STOP = frozenset(
    "est il elle le la les un une des de du que qui ce cette ces vous on ou et a en "
    "est-ce pour plus moins dans sur au aux avec ne pas se son sa ses leur leurs nos "
    "notre y".split()
)

# thème -> motifs (sous-chaînes sans accents). Repris de analyse_frequence.py.
THEMES: dict[str, list[str]] = {
    "Immigration / vivre à l'étranger / intégration": [
        "etranger", "immigr", "pays d'accueil", "s'integ", "integration", "expatri",
        "emigrer", "quitter son pays", "s'installe", "s'adapter", "s'habituer",
        "vivre au canada", "pays natal", "vivre dans un pays", "changer de pays",
        "renoncer a ses traditions", "preserver sa culture", "culture d'origine",
        "vivre dans un autre pays", "nouveau pays", "adapter son mode de vie",
        "changer ses habitudes de vie", "faire connaitre son pays", "aller vivre ailleurs",
    ],
    "Travail / emploi / salaire / carrière": [
        "travail", "emploi", "salaire", "metier", "carriere", "entreprise", "employe",
        "employeur", "teletravail", "professionnel", "hierarchie", "responsable",
        "productif", "monde du travail", "bien-etre de ses", "perspectives professionnelles",
        "trouver un travail", "trouver du travail",
    ],
    "Éducation / école / études / diplômes": [
        "ecole", "etudes", "diplome", "scolaire", "universite", "matiere", "apprendre",
        "apprentissage", "programme scolaire", "bons resultats", "enseigne",
        "education a la maison", "classe a la maison", "eleves", "formations",
        "longues etudes", "niveau d'etudes", "etudiant", "selection",
    ],
    "Éducation des enfants / parentalité / autorité": [
        "autorite", "eduquer", "education d'un enfant", "elever", "verite aux enfants",
        "filles et garcons", "forcer les enfants", "obliger les enfants", "parents devraient",
        "donner un telephone a un enfant", "argent a leurs enfants", "recompens",
        "education differente", "bien eduquer", "education des enfants",
    ],
    "Télévision / médias / information": [
        "television", "tele", "journaux televises", "actualites", "s'informer",
        "s'instruire", "medias", "media", "vous informer", "images violentes", "journaux",
        "tele-realite", "etre informe", "diffuser", "informations consultees",
    ],
    "Technologie / Internet / réseaux sociaux": [
        "internet", "reseaux sociaux", "en ligne", "numerique", "technologie", "le web",
        "applications", "outils digitaux", "achats sur internet", "informatique",
        "nouvelles technologies", "remplacer le travail humain", "magasins physiques",
    ],
    "Téléphone portable / smartphone / écrans": [
        "telephone", "portable", "smartphone", "ecrans", "tablette",
        "appareils electroniques", "ordinateurs",
    ],
    "Environnement / pollution / écologie": [
        "pollution", "environnement", "dechets", "transports en commun", "voiture",
        "ecologie", "ecologique", "energies renouvelable", "planete", "tri des dechets",
        "recyclage", "avion", "circulation des voitures", "agriculture biologique",
        "preservant l'environnement", "proteger la planete",
    ],
    "Santé / alimentation / mode de vie": [
        "sante", "se nourrir", "viande", "vegetarien", "produit bio", "le bio",
        "medicaments", "stress", "chirurgie esthetique", "perdre du poids",
        "habitudes alimentaires", "regime", "cuisiner", "alimentation", "soins medicaux",
        "soins", "consommation",
    ],
    "Tourisme / voyage": ["tourisme", "tourist", "voyage", "voyager", "visite", "sorties"],
    "Ville / campagne / logement": [
        "en ville", "a la campagne", "vie rurale", "vie urbaine", "chez leurs parents",
        "chez ses parents", "vivre en ville", "logement",
    ],
    "Famille / amitié / relations / célibat": [
        "famille", "amis", "amitie", "celibataire", "vivre seul", "solitaire",
        "se sentir seul", "relations a distance", "ne pas avoir d'enfant",
        "membres de la famille", "se faire des amis", "proches", "solidarite entre",
    ],
    "Argent / bonheur / réussite": [
        "argent fait", "heureux", "bonheur", "riche", "profiter de la vie",
        "reussir dans la vie", "beaucoup d'argent", "gagner sa vie", "reussir dans sa vie",
    ],
    "Égalité hommes-femmes / droits des femmes": [
        "parite", "hommes-femmes", "homme-femme", "droits des femmes", "egalite",
        "meme education", "feministe",
    ],
    "Citoyenneté / solidarité / bénévolat / État": [
        "benevol", "associations", "citoyen", "l'etat", "ong", "humanitaire",
        "personnes en difficulte", "aider les plus pauvres", "engagement", "prestations sociales",
    ],
    "Jeux vidéo": ["jeux video"],
    "Sport / sportifs": [
        "sportif", "salaires des sportifs", "competitions sportives", "faire du sport",
        "activite sportive",
    ],
    "Apparence / beauté / célébrités": [
        "celebrite", "stars", "paraitre", "apparence", "beaute", "rester jeune", "vetements",
        "habillement", "vieillir", "plus jeunes que leur age",
    ],
    "Animaux": [
        "animaux", "animal de compagnie", "zoo", "parcs zoologiques", "animaux domestiques",
    ],
    "Lecture / livres / culture / art": [
        "livre", "lire", "lecture", "musee", "culturel", "activites artistiques",
        "metiers lies a l'art", "theatre", "cinema", "artistes", "art",
    ],
    "Langues étrangères": [
        "langue etrangere", "langue du pays", "parler la langue", "langues etrangeres",
        "anglais", "maitriser la langue", "langue maternelle", "nouvelle langue",
        "comprendre la culture d'un pays", "comprendre sa culture",
    ],
    "Générations / jeunes / personnes âgées": [
        "personnes agees", "les aines", "polis", "respectueux", "les jeunes",
        "s'impliquent moins", "independants", "devenir independant",
    ],
    "Sécurité / surveillance / libertés": [
        "cameras", "surveillance", "securite", "liberte d'expression", "frontieres",
        "passeport", "visa", "lieux publics",
    ],
    "Politique / engagement des jeunes": [
        "politique", "interet pour la politique", "place en politique",
    ],
}
def strip_accents(s: str) -> str:
    """Minuscule + suppression des accents (pour comparer le fond des sujets)."""
    decomposed = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")


_THEMES_N = {t: [strip_accents(p) for p in pats] for t, pats in THEMES.items()}


def normalize(subject: str) -> str:
    """Réduit un sujet à ses mots porteurs de sens pour le clustering."""
    s = strip_accents(subject)
    s = _BOILER_RE.sub(" ", s)
    s = re.sub(r"[^a-z ]", " ", s)
    return " ".join(w for w in s.split() if w and w not in _STOP)


def classify(subject: str) -> list[str]:
    """Renvoie les thèmes dont au moins un motif apparaît dans le sujet."""
    ns = strip_accents(subject)
    return [theme for theme, pats in _THEMES_N.items() if any(p in ns for p in pats)]


def slugify(subject: str, max_words: int = 7) -> str:
    """Slug court et stable pour les noms de fichiers."""
    s = strip_accents(subject)
    s = _BOILER_RE.sub(" ", s)
    words = [w for w in re.sub(r"[^a-z ]", " ", s).split() if w and w not in _STOP]
    return "-".join(words[:max_words]) or "sujet"


@dataclass(slots=True)
class Cluster:
    """Une question canonique 2026 et toutes ses reformulations."""

    key: str
    subjects: list[str] = field(default_factory=list)
    months: list[str] = field(default_factory=list)

    @property
    def frequency(self) -> int:
        return len(self.subjects)

    @property
    def representative(self) -> str:
        # la variante la plus courte est en général la plus « canonique »
        return min(self.subjects, key=len)

    @property
    def variants(self) -> list[str]:
        rep = self.representative
        return sorted({s for s in self.subjects if s != rep}, key=len)


def parse_year(corpus: Path, year: str) -> list[tuple[str, str]]:
    """Renvoie [(sujet, mois)] pour l'année demandée (mois au format ``2026-06``)."""
    pairs: list[tuple[str, str]] = []
    month: str | None = None
    for raw in corpus.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            tokens = line.lstrip("# ").split()
            month = tokens[0] if tokens and tokens[0].startswith(year) else None
            continue
        if month is not None:
            pairs.append((line, month))
    return pairs


def cluster(pairs: Iterable[tuple[str, str]], threshold: float) -> list[Cluster]:
    """Regroupe les sujets par similarité difflib (premier match au-dessus du seuil)."""
    clusters: list[Cluster] = []
    for subject, month in pairs:
        norm = normalize(subject)
        best: Cluster | None = None
        best_ratio = 0.0
        for c in clusters:
            ratio = SequenceMatcher(None, norm, c.key).ratio()
            if ratio > best_ratio:
                best, best_ratio = c, ratio
        if best is not None and best_ratio >= threshold:
            best.subjects.append(subject)
            best.months.append(month)
        else:
            clusters.append(Cluster(key=norm, subjects=[subject], months=[month]))
    # priorité = fréquence décroissante, puis mois le plus récent
    clusters.sort(key=lambda c: (-c.frequency, max(c.months)), reverse=False)
    clusters.sort(key=lambda c: -c.frequency)
    return clusters


def build() -> list[dict[str, object]]:
    """Construit l'index, l'écrit sur disque et renvoie les entrées."""
    pairs = parse_year(CORPUS, YEAR)
    clusters = cluster(pairs, SIMILARITY_THRESHOLD)

    entries: list[dict[str, object]] = []
    used_slugs: set[str] = set()
    for rank, c in enumerate(clusters, start=1):
        slug = slugify(c.representative)
        unique_slug = slug
        suffix = 2
        while unique_slug in used_slugs:
            unique_slug = f"{slug}-{suffix}"
            suffix += 1
        used_slugs.add(unique_slug)
        entries.append(
            {
                "rank": rank,
                "id": f"{rank:03d}",
                "slug": unique_slug,
                "filename": f"{rank:03d}-{unique_slug}.md",
                "frequency": c.frequency,
                "subject": c.representative,
                "themes": classify(c.representative) or ["Divers"],
                "months": sorted(set(c.months), reverse=True),
                "variants": c.variants,
            }
        )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    index_path = OUT_DIR / "_index.json"
    index_path.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    _write_markdown_index(entries, len(pairs), len(clusters))
    return entries


def _write_markdown_index(
    entries: list[dict[str, object]], total: int, distinct: int
) -> None:
    lines = [
        "# Tâche 3 — Sujets 2026, dédupliqués et classés par priorité",
        "",
        f"**{total} sujets** relevés en 2026 (jan.–juin), regroupés en **{distinct} questions "
        "canoniques** (les reformulations quasi identiques sont fusionnées). La **fréquence** "
        "est le nombre de fois où la question — ou une variante très proche — est apparue : "
        "**plus elle est élevée, plus le sujet est susceptible de retomber**.",
        "",
        "Chaque sujet a une réponse modèle B2 rédigée dans ce dossier (`examples/`) et un audio "
        "généré par `make speak`.",
        "",
        "| # | Fréq. | Sujet | Thème(s) | Fichier |",
        "|---|---|---|---|---|",
    ]
    for e in entries:
        themes = " · ".join(e["themes"])  # type: ignore[arg-type]
        subject = str(e["subject"]).replace("|", "\\|")
        lines.append(
            f"| {e['rank']} | {e['frequency']}× | {subject} | {themes} | "
            f"[`{e['filename']}`]({e['filename']}) |"
        )
    (OUT_DIR / "0-index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    rows = build()
    multi = sum(1 for r in rows if r["frequency"] > 1)  # type: ignore[operator]
    print(f"{len(rows)} questions canoniques écrites dans {OUT_DIR}/_index.json")
    print(f"  dont {multi} apparues au moins 2 fois (sujets prioritaires)")
    for r in rows[:12]:
        print(f"  {r['rank']:>3}. [{r['frequency']}×] {r['subject']}")
