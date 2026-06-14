PANDOC := pandoc
PDF_ENGINE := weasyprint

MD_FILES := $(shell find . -name '*.md' -not -path './.claude/*' -not -name 'README.md')
PDF_FILES := $(MD_FILES:.md=.pdf)

.PHONY: build clean

build: $(PDF_FILES)

%.pdf: %.md
	@command -v $(PANDOC) >/dev/null || { echo "pandoc not found. Install with: brew install pandoc weasyprint"; exit 1; }
	@echo "Building $@"
	@$(PANDOC) "$<" -o "$@" --pdf-engine=$(PDF_ENGINE) 2>/dev/null

clean:
	@rm -f $(PDF_FILES)
	@echo "Removed generated PDFs"
