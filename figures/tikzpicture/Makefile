MAKE = make
SOURCES = $(wildcard *_stdl.tex)
RESULTS = $(patsubst %.tex,%.pdf,$(SOURCES))


all: echoing $(RESULTS) $(SOURCES)
	@echo
	@echo done
	@echo

%_stdl.pdf : %_stdl.tex
	latexmk $<

clean:
	latexmk -c
 
clear:
	latexmk -C

echoing:
	@echo
	@echo Calling latexmk to compile $(SOURCES)
	@echo

.PHONY: clean clear echoing
