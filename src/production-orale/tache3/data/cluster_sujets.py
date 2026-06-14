#!/usr/bin/env python3
"""Regroupe les sujets quasi identiques (reformulés d'un mois à l'autre) et les compte.

Méthode : on normalise chaque sujet (minuscules, sans accents, sans la « queue »
rhétorique du type « qu'en pensez-vous ? / êtes-vous d'accord ? / selon vous »),
puis on regroupe par similarité (difflib) au-dessus d'un seuil. Chaque groupe = une
« question canonique » ; sa taille = le nombre de fois où elle (ou une variante très
proche) apparaît dans le corpus 2022-2026.
"""
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

def strip_accents(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

# tournures rhétoriques à retirer pour comparer le fond
BOILER = [
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
BOILER_RE = re.compile("|".join(BOILER))

def normalize(s: str) -> str:
    s = strip_accents(s)
    s = BOILER_RE.sub(" ", s)
    s = re.sub(r"[^a-z ]", " ", s)       # ponctuation -> espace
    # mots vides courts qui n'aident pas la comparaison
    stop = {"est","il","elle","le","la","les","un","une","des","de","du","que","qui",
            "ce","cette","ces","vous","on","ou","et","a","en","est-ce","pour","plus",
            "moins","dans","sur","au","aux","avec","ne","pas","se","son","sa","ses",
            "leur","leurs","nos","notre","y","il-est"}
    words = [w for w in s.split() if w and w not in stop]
    return " ".join(words)  # garde l'ordre des mots (clusters plus purs)

raw = [l.strip() for l in Path("data/corpus.txt").read_text(encoding="utf-8").splitlines()]
subjects = [l for l in raw if l and not l.startswith("#")]
norms = [normalize(s) for s in subjects]

THRESHOLD = 0.62
clusters = []  # chaque cluster : {"key": norm_repr, "items": [indices]}

for i, n in enumerate(norms):
    best, best_r = None, 0.0
    for c in clusters:
        r = SequenceMatcher(None, n, c["key"]).ratio()
        if r > best_r:
            best, best_r = c, r
    if best is not None and best_r >= THRESHOLD:
        best["items"].append(i)
    else:
        clusters.append({"key": n, "items": [i]})

clusters.sort(key=lambda c: -len(c["items"]))

print(f"TOTAL sujets : {len(subjects)} — groupes : {len(clusters)} (seuil {THRESHOLD})\n")
print("Sujets apparaissant AU MOINS 3 fois (question canonique → nombre d'occurrences) :\n")
rank = 0
for c in clusters:
    n = len(c["items"])
    if n < 3:
        break
    rank += 1
    # représentant = la variante la plus courte (souvent la plus « canonique »)
    rep = min((subjects[i] for i in c["items"]), key=len)
    print(f"{rank:>2}. [{n}×] {rep}")
    variants = sorted({subjects[i] for i in c["items"] if subjects[i] != rep}, key=len)
    for v in variants[:3]:
        print(f"        ~ {v}")
    if len(variants) > 3:
        print(f"        … (+{len(variants)-3} autres variantes)")
