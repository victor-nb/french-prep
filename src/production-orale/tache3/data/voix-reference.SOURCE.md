# Voix de référence — provenance & licence

`voix-reference.wav` (+ `.txt`) est un extrait du jeu de données **FLEURS**
(*Few-shot Learning Evaluation of Universal Representations of Speech*), sous-ensemble
`fr_fr`, publié par Google.

- **Licence : CC-BY 4.0** — réutilisation autorisée avec attribution.
- Source : https://huggingface.co/datasets/google/fleurs
- Récupéré automatiquement par [`fetch_reference_voice.py`](fetch_reference_voice.py).

Cet extrait sert uniquement de **voix de référence** clonée par Higgs Audio v3
([`../tts.py`](../tts.py)) pour donner un rendu humain et cohérent aux réponses modèles.

Pour utiliser une autre voix (par ex. la vôtre), remplacez `voix-reference.wav`
(extrait .wav de ~8-15 s) et `voix-reference.txt` (sa transcription exacte).
