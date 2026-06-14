PANDOC := pandoc
PDF_ENGINE := weasyprint
SRC_DIR := src
PDF_DIR := pdf

MD_FILES := $(shell find $(SRC_DIR) -name '*.md')
PDF_FILES := $(patsubst $(SRC_DIR)/%.md,$(PDF_DIR)/%.pdf,$(MD_FILES))

.PHONY: build clean

build: $(PDF_FILES)

$(PDF_DIR)/%.pdf: $(SRC_DIR)/%.md
	@command -v $(PANDOC) >/dev/null || { echo "pandoc not found. Install with: brew install pandoc weasyprint"; exit 1; }
	@mkdir -p $(dir $@)
	@echo "Building $@"
	@$(PANDOC) "$<" -o "$@" --pdf-engine=$(PDF_ENGINE) 2>/dev/null

clean:
	@rm -rf $(PDF_DIR)
	@echo "Removed $(PDF_DIR)/"
