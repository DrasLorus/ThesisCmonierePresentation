
MAKE = make

.PHONY: all clean clear
all: main
	@echo
	@echo Main file generated.
	@echo

subfiles: algorithm implementation system experimentations introduction conclusion
	@echo
	@echo Subfiles generated
	@echo

main: figures main.pdf main.gls main.acr
	makeglossaries main
	latexmk main.tex

main.pdf main.ist main.acn: main.tex figures
	latexmk main.tex

main.gls main.acr: main.ist main.glo main.acn
	makeglossaries main

figures: svg tikzpictures pgfplots
	@echo
	@echo Figures generated.
	@echo

svg: figures/svg/.latexmkrc figures/svg/Makefile
	cd figures/svg && $(MAKE) -B

tikzpictures: figures/tikzpicture/.latexmkrc figures/tikzpicture/Makefile
	cd figures/tikzpicture && $(MAKE) -B

pgfplots: figures/pgfplots/.latexmkrc figures/pgfplots/Makefile
	cd figures/pgfplots && $(MAKE) -B

clean:
	cd figures/tikzpicture && $(MAKE) clean
	cd figures/pgfplots && $(MAKE) clean

clear:
	cd figures/tikzpicture && $(MAKE) clear
	cd figures/pgfplots && $(MAKE) clear


introduction: sections/introduction.pdf sections/introduction.bbl
	cd sections; lualatex -interaction=nonstopmode -file-line-error -synctex=1 introduction.tex

sections/introduction.pdf: sections/introduction.tex figures
	cd sections; lualatex -interaction=nonstopmode -file-line-error -synctex=1 introduction.tex

sections/introduction.bbl: sections/introduction.pdf
	biber --output-directory sections introduction.bcf

conclusion: sections/conclusion.pdf sections/conclusion.bbl
	cd sections; lualatex -interaction=nonstopmode -file-line-error -synctex=1 conclusion.tex

sections/conclusion.pdf: sections/conclusion.tex figures
	cd sections; lualatex -interaction=nonstopmode -file-line-error -synctex=1 conclusion.tex

sections/conclusion.bbl: sections/conclusion.pdf
	biber --output-directory sections conclusion.bcf

qcsp_summary: sections/qcsp_summary.pdf sections/qcsp_summary.bbl
	cd sections; lualatex -interaction=nonstopmode -file-line-error -synctex=1 qcsp_summary.tex

sections/qcsp_summary.pdf: sections/qcsp_summary.tex figures
	cd sections; lualatex -interaction=nonstopmode -file-line-error -synctex=1 qcsp_summary.tex

sections/qcsp_summary.bbl: sections/qcsp_summary.pdf
	biber --output-directory sections qcsp_summary.bcf


algorithm: sections/algorithm.pdf sections/algorithm.bbl
	cd sections; lualatex -interaction=nonstopmode -file-line-error -synctex=1 algorithm.tex

sections/algorithm.pdf: sections/algorithm.tex figures
	cd sections; lualatex -interaction=nonstopmode -file-line-error -synctex=1 algorithm.tex

sections/algorithm.bbl: sections/algorithm.pdf
	biber --output-directory sections algorithm.bcf

implementation: sections/implementations.pdf sections/implementations.bbl
	cd sections; lualatex -interaction=nonstopmode -file-line-error -synctex=1 implementations.tex

sections/implementations.pdf: sections/implementations.tex figures
	cd sections; lualatex -interaction=nonstopmode -file-line-error -synctex=1 implementations.tex

sections/implementations.bbl: sections/implementations.pdf
	biber --output-directory sections implementations.bcf

experimentations: sections/real-time-exp.pdf sections/real-time-exp.bbl
	cd sections; lualatex -interaction=nonstopmode -file-line-error -synctex=1 real-time-exp.tex

sections/real-time-exp.pdf: sections/real-time-exp.tex figures
	cd sections; lualatex -interaction=nonstopmode -file-line-error -synctex=1 real-time-exp.tex

sections/real-time-exp.bbl: sections/real-time-exp.pdf
	biber --output-directory sections real-time-exp.bcf
