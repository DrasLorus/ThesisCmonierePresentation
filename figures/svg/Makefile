MAKE = make
SOURCES = $(wildcard *_stdl.tex) $(wildcard *.svg)
RESULTS = $(patsubst %.svg,%.pdf,$(patsubst %_stdl.tex,%_stdl.pdf,$(SOURCES)))


all: echoing $(RESULTS) $(SOURCES)
	@echo
	@echo done
	@echo

%_stdl.pdf : %_stdl.tex
	latexmk $<

%.pdf : %.svg
	cairosvg $< -o $@

clean:
	latexmk -c
 
clear:
	latexmk -C

echoing:
	@echo
	@echo Calling latexmk to compile $(SOURCES)
	@echo

.PHONY: clean clear echoing
