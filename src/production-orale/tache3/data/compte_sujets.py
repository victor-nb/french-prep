#!/usr/bin/env python3
"""Compte des QUESTIONS CANONIQUES récurrentes via des signatures de mots-clés.

Chaque question canonique = une liste de conditions ; une condition est satisfaite si
l'un de ses synonymes (sans accents) apparaît dans le sujet. Toutes les conditions
doivent être réunies (ET). Un sujet peut compter pour plusieurs questions canoniques
distinctes (ce sont des questions différentes), mais chaque signature est conçue pour
cibler une idée précise. Comptage accent-insensible sur data/corpus.txt.
"""
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

def strip(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

# (libellé canonique, [condition1, condition2, ...]) ; condition = (synonyme, ...)
CANON = [
    ("Vivre / s'intégrer dans un pays étranger est difficile",
        [("etranger", "nouveau pays", "pays d'accueil", "s'integrer", "s'adapter", "s'habituer", "immigr"),
         ("difficile", "compliqu", "pas facile", "jamais facile", "defi", "courage", "surpassent ses inconvenients")]),
    ("Il est facile de travailler / trouver un emploi à l'étranger",
        [("travailler", "travail", "emploi", "exercer un emploi"),
         ("etranger", "autre pays"),
         ("facile",)]),
    ("Faut-il connaître la langue / vivre dans un pays pour connaître sa culture",
        [("culture", "comprendre sa culture", "connaitre sa culture", "connaitre un pays"),
         ("langue", "vivre dans un pays", "vivre dans le pays", "y vivre", "lisant des livres", "parler sa langue")]),
    ("Faut-il maîtriser la langue du pays d'accueil pour s'intégrer",
        [("langue",),
         ("integr", "s'integrer", "pays d'accueil", "pays ou l'on")]),
    ("Apprendre une langue étrangère (difficulté / dès l'enfance)",
        [("langue etrangere", "langue", "nouvelle langue"),
         ("apprendre", "apprennent", "maitriser", "enfance", "jeune age", "difficile")]),
    ("S'intégrer : faut-il renoncer à ses traditions / sa culture",
        [("tradition", "preserver sa culture", "renoncer", "abandonner", "preserver sa propre culture")]),
    ("Connaître le pays / s'y préparer avant d'immigrer",
        [("immigr", "pays d'accueil", "avant d'y immigrer"),
         ("connaitre", "bien connaitre", "se preparer")]),
    ("L'immigration est-elle bénéfique / une richesse pour le pays d'accueil",
        [("immigr",),
         ("benefique", "richesse", "valeur ajoutee", "apportent", "apporte", "utile", "contribuent")]),
    ("Quel âge idéal / est-ce plus facile jeune pour émigrer-s'intégrer",
        [("emigrer", "s'expatrier", "etranger", "immigr", "nouveau pays", "s'integrer", "s'adapter"),
         ("age ideal", "quel age", "meilleur age", "a quel age", "quand on est jeune",
          "plus facile pour les jeunes", "plus simple pour les jeunes", "plus facile quand on est jeune",
          "facile de s'adapter a un nouveau pays quand on est jeune", "prefer")]),
    ("Une expérience à l'étranger est-elle nécessaire pour la carrière",
        [("experience",),
         ("etranger",),
         ("carriere", "professionnel", "reussir", "avantages", "atout")]),

    ("Faut-il des études / diplômes pour réussir / gagner sa vie",
        [("etudes", "diplome"),
         ("reussir", "gagner", "argent", "carriere", "vie professionnelle", "professionnelle")]),
    ("Les bons résultats scolaires permettent-ils de réussir dans la vie",
        [("resultats", "notes", "reussite scolaire", "performance a l'ecole"),
         ("reussir", "reussite", "vie", "succes")]),
    ("Faut-il aimer son travail pour être productif / réussir",
        [("aimer son travail", "aimer son metier", "apprecier son metier", "aime ce que", "aimer ce que"),
         ("productif", "reussir", "professionnel", "bonnes conditions", "carriere")]),
    ("Travailler jusqu'à 70 ans",
        [("70 ans",)]),
    ("Le salaire est-il le plus important / la motivation au travail",
        [("salaire",),
         ("important", "principal", "motiv", "facteur")]),
    ("Le télétravail (avantages / équilibre vie pro-perso)",
        [("teletravail", "travail a distance", "travailler depuis chez", "travail a la maison")]),
    ("Est-il bon de faire plusieurs métiers / changer de métier",
        [("plusieurs metiers", "changer de metier", "changer de carriere", "reconversion", "plusieurs fois de metier")]),
    ("Le travail des personnes âgées / seniors est-il utile à la société",
        [("personnes agees", "seniors", "ages"),
         ("travail", "actives dans le monde du travail")]),
    ("Faut-il éviter de travailler avec sa famille / ses proches",
        [("travailler avec", "ne pas travailler avec"),
         ("famille", "proches", "amis", "membre de sa famille")]),
    ("Tout le monde devrait-il avoir le même salaire",
        [("meme salaire",)]),

    ("Peut-on vivre sans téléphone portable / il est indispensable",
        [("telephone", "portable"),
         ("sans", "indispensable", "se passer", "vivre sans")]),
    ("Faut-il interdire le téléphone aux enfants / à l'école / au travail",
        [("telephone", "portable"),
         ("interdi", "empecher", "ne pas conseille", "offrir")]),
    ("Les réseaux sociaux : perte de temps / isolement",
        [("reseaux sociaux",),
         ("perte de temps", "solitaire", "isol", "concentr", "perdre un temps", "moins dynamiques")]),
    ("Peut-on vivre sans Internet / Internet rend la vie meilleure",
        [("internet",),
         ("sans internet", "vit mieux", "vie plus facile", "rend heureux", "impact positif sur le bonheur", "village")]),
    ("Internet et l'éducation des enfants / l'information",
        [("internet",),
         ("enfants", "education", "enseignement", "informe", "information")]),
    ("La technologie va-t-elle remplacer le travail humain",
        [("technologie", "nouvelles technologies"),
         ("remplace", "plus besoin de travailler", "detruire les emplois", "remplacer le travail")]),

    ("Certaines personnes ne regardent jamais la télévision",
        [("television", "tele", "actualites"),
         ("jamais", "ne pas regarder", "refusent", "moins en moins", "se passer")]),
    ("Regarder la télévision permet de s'instruire / éduque les enfants",
        [("television", "tele"),
         ("s'instruire", "instruire", "developpement de l'enfant", "education des enfants", "connaissances", "developpement des enfants")]),
    ("La télévision / le temps d'écran est-il du temps perdu",
        [("television", "tele", "ecrans"),
         ("temps perdu", "trop de temps", "trop longtemps")]),
    ("Les journaux télévisés et les images violentes",
        [("images violentes",)]),
    ("Quel média préférez-vous pour vous informer",
        [("medias", "media"),
         ("prefer", "informer")]),

    ("Pour la santé, faut-il arrêter la viande / devenir végétarien",
        [("viande", "vegetarien", "vegetarienne")]),
    ("Les produits bio (santé / réservés aux riches)",
        [("bio", "biologique")]),
    ("Le stress est-il un bon stimulant",
        [("stress",)]),
    ("La chirurgie esthétique / vouloir paraître jeune",
        [("chirurgie esthetique", "paraitre", "rester jeune", "apparence", "plus jeunes", "rester toujours jeunes", "vieillir", "beaute")]),
    ("Peut-on vivre sans médicaments",
        [("medicaments",)]),

    ("Les transports en commun devraient être gratuits",
        [("transports en commun", "transports publics"),
         ("gratuit",)]),
    ("Peut-on vivre sans voiture / interdire les voitures en ville",
        [("voiture",),
         ("sans voiture", "interdire", "limiter", "circulation", "centres")]),
    ("Chacun peut-il agir pour l'environnement (déchets, gestes)",
        [("dechets", "tri", "recycl", "pollution", "planete", "gestes"),
         ("reduire", "trier", "tout le monde", "chacun", "actions", "proteger", "diminuer", "lutter")]),
    ("Développer l'économie en préservant l'environnement",
        [("economie", "economique"),
         ("environnement", "nature", "planete")]),
    ("Le tourisme : bon pour l'économie / nuisible à l'environnement",
        [("tourisme", "touristes"),
         ("environnement", "detrui", "deterior", "nature", "developpement", "croissance", "economie", "regions")]),

    ("L'argent fait-il le bonheur / faut-il être riche pour être heureux",
        [("argent", "riche", "salaire"),
         ("bonheur", "heureux", "profiter de la vie")]),
    ("Peut-on être heureux célibataire / sans amis",
        [("celibataire", "vivre seul", "sans avoir d'amis", "sans amis"),
         ("heureux", "epanoui", "epanouir", "bonheur")]),
    ("La famille est-elle la chose la plus importante / nos meilleurs amis",
        [("famille",),
         ("meilleurs amis", "plus importante", "place la plus")]),
    ("Les amitiés sur Internet valent-elles les liens familiaux",
        [("amitie", "amities", "relations", "liens"),
         ("internet", "a distance", "virtuel"),]),

    ("Faut-il de l'autorité pour éduquer les enfants",
        [("autorite", "autoritaire"),
         ("enfant", "eduquer", "education", "elever")]),
    ("Faut-il toujours dire la vérité aux enfants",
        [("verite",), ("enfants",)]),
    ("Les parents doivent-ils contrôler / surveiller leurs enfants",
        [("parents", "controler", "surveillent"),
         ("frequentations", "surveillent", "controler", "amis de leurs enfants")]),
    ("Éduquer filles et garçons de la même manière",
        [("filles", "garcons"),
         ("meme", "differente", "egale")]),
    ("Faut-il forcer / obliger les enfants à faire du sport",
        [("enfants",),
         ("sport",),
         ("forcer", "obliger", "encourager", "competitions")]),
    ("L'éducation à la maison (école à la maison)",
        [("a la maison", "a domicile", "classe a la maison"),
         ("enfants", "enseigner", "education", "ecole")]),

    ("Les salaires des sportifs sont-ils excessifs",
        [("sportif",), ("salaire", "gagnent", "argent", "merit")]),
    ("Les célébrités ont-elles leur place en politique / vie publique",
        [("celebrites", "celebrite"),
         ("politique", "vie publique")]),
    ("Pourquoi s'intéresse-t-on à la vie des célébrités / stars",
        [("celebrites", "stars", "vie des celebrites"),
         ("interess", "attir", "pourquoi", "attrait")]),
    ("Les jeux vidéo : dangereux ou utiles au développement de l'enfant",
        [("jeux video",)]),
    ("Voyager seul ou accompagné",
        [("voyager seul", "voyage seul", "voyagent seul", "voyager seules", "seul ou accompagne", "voyager accompagne")]),
    ("Voyager rend-il meilleur / change-t-il la personne",
        [("voyage", "voyager", "voyageant"),
         ("meilleure personne", "transforme", "influence", "devient une autre", "personnalite", "forme")]),
    ("Le voyage est-il réservé aux personnes riches",
        [("voyage",), ("riche",)]),
    ("Les livres sont-ils inutiles / faut-il lire pour être cultivé",
        [("livre", "lire", "lecture"),
         ("inutile", "cultive", "perdu", "importance")]),
    ("Les musées / la culture devraient-ils être gratuits",
        [("musee", "culture", "theatre", "sites culturels"),
         ("gratuit", "sans frais")]),
    ("Vivre en ville ou à la campagne (stress, qualité de vie)",
        [("ville",), ("campagne",)]),
    ("Les jeunes adultes qui restent vivre chez leurs parents",
        [("chez leurs parents", "chez ses parents", "avec ses parents"),
         ("rester", "habiter", "vivre", "25 ans")]),
    ("Les jeunes sont-ils moins polis / les vieux pessimistes sur les jeunes",
        [("jeunes", "vieux", "aines", "adultes"),
         ("polis", "respectueux", "pessimiste", "optimistes", "regard", "percoivent")]),
    ("La parité hommes-femmes / les droits des femmes",
        [("parite", "droits des femmes", "hommes-femmes", "homme-femme", "50% d'hommes", "egalite")]),
    ("Le bénévolat / l'engagement citoyen / actions solidaires",
        [("benevol", "solidaire", "action solidaire", "actions citoyennes", "associations pour aider", "engagement")]),
    ("Qui doit aider les plus démunis : l'État ou les citoyens",
        [("aider",),
         ("etat", "citoyens", "ong", "associations", "personnes en difficulte", "plus pauvres")]),
]

raw = [l.strip() for l in Path("data/corpus.txt").read_text(encoding="utf-8").splitlines()]
subjects = [strip(l) for l in raw if l and not l.startswith("#")]

@lru_cache(maxsize=None)
def _syn(syn):
    # frontière gauche : « tele » ne doit pas matcher « téléphone », « ong » ne doit pas matcher « longtemps »…
    return re.compile(r"(?<![a-z0-9])" + re.escape(syn))

def matches(subj, conds):
    return all(any(_syn(syn).search(subj) for syn in cond) for cond in conds)

rows = []
for label, conds in CANON:
    n = sum(1 for s in subjects if matches(s, conds))
    rows.append((n, label))

rows.sort(key=lambda r: -r[0])
print(f"TOTAL sujets : {len(subjects)}\n")
print(f"{'occ.':>4}  question canonique")
print("-" * 80)
for n, label in rows:
    print(f"{n:>4}  {label}")
