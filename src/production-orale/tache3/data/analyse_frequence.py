#!/usr/bin/env python3
"""Compte la fréquence des thèmes dans le corpus de sujets Tâche 3 (TCF Canada 2022-2026).

Chaque sujet est classé dans un ou plusieurs thèmes via des mots-clés.
Un même sujet peut compter pour plusieurs thèmes (ex. « téléphone à l'école » = numérique + éducation).
"""
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

def strip(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

# theme -> liste de motifs (sous-chaînes, déjà sans accents)
THEMES = {
    "Immigration / vivre à l'étranger / intégration": [
        "etranger", "immigr", "immigre", "pays d'accueil", "s'integrer", "s'integ",
        "integration", "expatri", "emigrer", "quitter son pays", "s'installer",
        "s'adapter", "s'habituer", "vivre au canada", "pays natal", "vivre dans un pays",
        "changer de pays", "demarches d'immigration", "renoncer a ses traditions",
        "preserver sa culture", "culture d'origine", "communaute de son pays",
        "vivre dans un autre pays", "s'installe", "nouveau pays", "d'opportunites",
        "adapter son mode de vie", "changer ses habitudes de vie", "faire connaitre son pays",
        "aller vivre ailleurs", "enjeux actuels", "cause la plus prioritaire",
    ],
    "Technologie / Internet / réseaux sociaux": [
        "internet", "reseaux sociaux", "en ligne", "numerique", "technologie",
        "le web", "applications", "outils digitaux", "achats sur internet",
        "monde est devenu un village", "informatique",
    ],
    "Téléphone portable / smartphone / écrans": [
        "telephone", "portable", "smartphone", "ecrans", "tablette", "appareils electroniques",
    ],
    "Travail / emploi / salaire / carrière": [
        "travail", "emploi", "salaire", "metier", "carriere", "entreprise", "employe",
        "employeur", "telework", "teletravail", "professionnel", "70 ans", "sieste",
        "hierarchie", "responsable", "productif", "monde du travail", "bien-etre de ses",
        "motiver les salaries", "perspectives professionnelles",
    ],
    "Éducation / école / études / diplômes": [
        "ecole", "etudes", "diplome", "scolaire", "universite", "matiere", "apprendre",
        "apprentissage", "programme scolaire", "cours prefere", "bons resultats",
        "enseigne", "education a la maison", "classe a la maison", "eleves", "formations",
        "longues etudes", "niveau d'etudes",
    ],
    "Éducation des enfants / parentalité / autorité": [
        "autorite", "eduquer", "education d'un enfant", "elever", "dire la verite aux enfants",
        "frequentations de leurs enfants", "filles et garcons", "filles ou garcons",
        "filles et leurs garcons", "forcer les enfants", "obliger les enfants",
        "surveillent les amis", "parents devraient", "donner un telephone a un enfant",
        "argent a leurs enfants", "recompensent", "autoritaire avec ses enfants",
        "education differente", "verite aux enfants",
    ],
    "Télévision / médias / information": [
        "televis", "la tele", "journaux televises", "actualites", "s'informer", "s'instruire",
        "medias", "media", "vous informer", "images violentes", "journaux", "tele-realite",
        "etre informe", "mieux informe", "diffuser",
    ],
    "Environnement / pollution / transports / écologie": [
        "pollution", "environnement", "dechets", "transports en commun", "transports publics",
        "voiture", "ecologie", "ecologique", "energies renouvelable", "planete", "tri des dechets",
        "recyclage", "voyages en avion", "deplacements en avion", "circulation des voitures",
        "agriculture biologique", "consommation d'eau", "centres-villes", "centres villes",
    ],
    "Santé / alimentation / mode de vie": [
        "sante", "se nourrir", "viande", "vegetarien", "produits bio", "produit bio",
        "le bio", "medicaments", "stress", "chirurgie esthetique", "perdre du poids",
        "habitudes alimentaires", "coutumes alimentaires", "regime", "cuisiner", "alimentation",
        "soins medicaux", "soins", "rendez-vous medicaux",
        "du sport", "de sport", "activite sportive", "commencer un sport",
    ],
    "Tourisme / voyage": [
        "tourisme", "tourist", "voyage", "voyager", "visite", "sorties",
    ],
    "Ville / campagne / logement": [
        "en ville", "a la campagne", "vie rurale", "vie urbaine", "chez leurs parents",
        "chez ses parents", "apres l'age de 25 ans", "vivre en ville",
    ],
    "Famille / amitié / relations / célibat": [
        "famille", "amis", "amitie", "ami(e)s", "celibataire", "vivre seul", "solitaire",
        "se sentir seules", "relations a distance", "relations directes", "ne pas avoir d'enfant",
        "membres de la famille", "se faire des amis", "se socialiser", "proches",
    ],
    "Argent / bonheur / réussite": [
        "argent fait", "argent fait-il le bonheur", "heureux", "bonheur", "riche",
        "profiter de la vie", "reussir dans la vie", "beaucoup d'argent", "gagner sa vie",
    ],
    "Égalité hommes-femmes / droits des femmes": [
        "parite", "hommes-femmes", "homme-femme", "droits des femmes", "egalite",
        "homme ou d'une femme", "50% d'hommes", "feministe",
    ],
    "Citoyenneté / solidarité / bénévolat / État": [
        "solidaire", "benevol", "associations", "citoyen", "l'etat", "ong",
        "action humanitaire", "humanitaire", "personnes en difficulte", "aider les plus pauvres",
        "aider les personnes", "engagement",
    ],
    "Jeux vidéo / enfants et écrans": [
        "jeux video",
    ],
    "Sport / sportifs": [
        "sportif", "salaires des sportifs", "competitions sportives", "faire du sport",
        "activite sportive",
    ],
    "Célébrités / apparence / beauté": [
        "celebrites", "celebrite", "stars", "vie des celebrites", "paraitre", "apparence",
        "beau", "belle", "beaute", "rester jeune", "vetements", "habillement", "vetement",
        "rester toujours jeunes", "vieillir",
    ],
    "Animaux": [
        "animaux", "animal de compagnie", "animaux de compagnie", "zoo", "parcs zoologiques",
        "animaux domestiques",
    ],
    "Lecture / livres / culture": [
        "livre", "lire", "lecture", "musee", "culturel", "matieres culturelles",
        "activites artistiques", "metiers artistiques", "metiers lies a l'art", "theatre",
        "cinema", "artistes", "profiter de la culture",
    ],
    "Langues étrangères": [
        "langue etrangere", "langue du pays", "parler la langue", "langues etrangeres",
        "anglais", "maitriser la langue", "langue maternelle", "sans parler sa langue",
        "connaitre sa langue", "parler sa langue", "savoir sa langue", "nouvelle langue",
        "comprendre la culture d'un pays", "plusieurs langues",
    ],
    "Générations / jeunes / personnes âgées": [
        "personnes agees", "les vieux", "les aines", "que leurs aines", "polis", "respectueux",
        "percoivent les jeunes", "regard pessimiste", "vision pessimiste", "plus optimistes",
        "conseils utiles", "bons conseils", "s'impliquent moins",
    ],
    "Valeurs / savoir-vivre": [
        "gentillesse", "respect des autres", "etre entendu et respecte",
    ],
    "Tâches ménagères": [
        "taches menageres", "menage",
    ],
    "Jeux de hasard / tabac / alcool / espace / liberté": [
        "jeux du hasard", "jeux d'argent", "tabac", "alcool", "espace", "liberte d'expression",
        "frontieres", "passeport", "visa", "caméras", "cameras", "surveillance", "securite",
    ],
    "Politique / engagement des jeunes": [
        "politique", "interet pour la politique", "suivent pas la politique",
        "ne suivent pas la politique", "place en politique",
    ],
}

def _boundary(p: str) -> "re.Pattern":
    # frontière gauche : un mot-clé ne doit pas matcher collé dans un mot plus long
    # (sinon « tele » matche « téléphone », « sport » matche « transports », « proches » matche « rapprochés »…)
    return re.compile(r"(?<![a-z0-9])" + re.escape(p))

THEMES_N = {t: [_boundary(strip(p)) for p in pats] for t, pats in THEMES.items()}

lines = [l.strip() for l in Path("data/corpus.txt").read_text(encoding="utf-8").splitlines()]
subjects = [l for l in lines if l and not l.startswith("#")]

counts = defaultdict(int)
examples = defaultdict(list)
matched = [False] * len(subjects)

for i, subj in enumerate(subjects):
    ns = strip(subj)
    for theme, pats in THEMES_N.items():
        if any(rx.search(ns) for rx in pats):
            counts[theme] += 1
            matched[i] = True
            if len(examples[theme]) < 4:
                examples[theme].append(subj)

total = len(subjects)
print(f"TOTAL sujets analysés : {total}\n")
print(f"{'#':>4}  {'THÈME':52}  occurrences   % du corpus")
print("-" * 88)
for theme, n in sorted(counts.items(), key=lambda kv: -kv[1]):
    print(f"{n:>4}  {theme:52}  {n:>5}        {100*n/total:5.1f}%")

unmatched = [s for s, m in zip(subjects, matched) if not m]
print(f"\nSujets non classés : {len(unmatched)}")
for s in unmatched:
    print("   -", s)
