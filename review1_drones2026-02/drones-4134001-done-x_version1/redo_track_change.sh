#!/bin/bash
#arguments are hard coded to be run from inside the version1 subfolder

#the name of the file(s) containing the track change
FILE=track_change

#creating the tex file with the differences highlighted
latexdiff ../drones-4134001-done-x_version0/drones-4134001-done.tex drones-4134001-done.tex > $FILE.tex

#cleaning all LaTeX clutter
rm -f $FILE.aux $FILE.dvi $FILE.log $FILE.idx $FILE.ind $FILE.toc $FILE.ilg $FILE.out $FILE.bbl $FILE.blg $FILE.nav $FILE.snm $FILE.ps $FILE.pdf

#doing the usual latex routine
pdflatex $FILE
bibtex $FILE
pdflatex $FILE
pdflatex $FILE
