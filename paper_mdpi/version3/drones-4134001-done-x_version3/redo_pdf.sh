#!/bin/bash
#READING FROM COMMAND LINE
FILE="$1"

#cleaning all LaTeX clutter
rm -f $FILE.aux $FILE.dvi $FILE.log $FILE.idx $FILE.ind $FILE.toc $FILE.ilg $FILE.out $FILE.bbl $FILE.blg $FILE.nav $FILE.snm $FILE.ps $FILE.pdf

#doing the usual latex routine
pdflatex $FILE
#bibtex $FILE
pdflatex $FILE
pdflatex $FILE
