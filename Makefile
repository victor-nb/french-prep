PANDOC := pandoc
PDF_ENGINE := weasyprint
PY := python3
SRC_DIR := src
PDF_DIR := pdf

T3_DIR := $(SRC_DIR)/production-orale/tache3
TTS := $(T3_DIR)/tts.py
VOICE_REF := $(T3_DIR)/data/voix-reference.wav

ANKI_SRC := ../epub-translation/anki/final
DOWNLOADS := downloads

MD_FILES := $(shell find $(SRC_DIR) -name '*.md')
PDF_FILES := $(patsubst $(SRC_DIR)/%.md,$(PDF_DIR)/%.pdf,$(MD_FILES))

.PHONY: build clean examples voice speak speak-test clean-audio decks site

build: $(PDF_FILES)

$(PDF_DIR)/%.pdf: $(SRC_DIR)/%.md
	@command -v $(PANDOC) >/dev/null || { echo "pandoc not found. Install with: brew install pandoc weasyprint"; exit 1; }
	@mkdir -p $(dir $@)
	@echo "Building $@"
	@$(PANDOC) "$<" -o "$@" --pdf-engine=$(PDF_ENGINE) 2>/dev/null

clean:
	@rm -rf $(PDF_DIR)
	@echo "Removed $(PDF_DIR)/"

## examples : (re)construit l'index dédupliqué des sujets 2026 (examples/_index.json + 0-index.md)
examples:
	@cd $(T3_DIR) && $(PY) data/build_examples_2026.py

$(VOICE_REF):
	@echo "Récupération de la voix de référence humaine (FLEURS, CC-BY)…"
	@cd $(T3_DIR) && $(PY) data/fetch_reference_voice.py

## voice : télécharge/prépare la voix de référence pour le clonage TTS
voice: $(VOICE_REF)

## speak : synthétise toutes les réponses manquantes en audio (voix humaine clonée, Higgs v3)
##         options : make speak ARGS="--ranks 1-20"  |  make speak ARGS="--force --format wav"
speak: $(VOICE_REF)
	@$(PY) $(TTS) $(ARGS)

## speak-test : génère seulement les 3 premières réponses (test rapide de la voix)
speak-test: $(VOICE_REF)
	@$(PY) $(TTS) --limit 3 $(ARGS)

## clean-audio : supprime tous les audios générés
clean-audio:
	@rm -rf $(T3_DIR)/examples/audio
	@echo "Removed $(T3_DIR)/examples/audio"

## decks : synchronise les paquets Anki (.apkg) depuis $(ANKI_SRC) vers downloads/
decks:
	@mkdir -p $(DOWNLOADS)
	@rm -f $(DOWNLOADS)/*.apkg
	@if ls $(ANKI_SRC)/*.apkg >/dev/null 2>&1; then \
		cp -f $(ANKI_SRC)/*.apkg $(DOWNLOADS)/; \
		echo "Paquets Anki synchronisés : $$(ls $(DOWNLOADS)/*.apkg 2>/dev/null | wc -l | tr -d ' ')"; \
	else echo "Aucun .apkg trouvé dans $(ANKI_SRC)"; fi

## site : (re)génère index.html (GitHub Pages) à partir des réponses + audios + paquets Anki
site: decks
	@cd $(T3_DIR) && $(PY) build_site.py
