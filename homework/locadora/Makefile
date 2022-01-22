
all: locadora lmt.pdf

locadora.o: locadora.c
	gcc -g -c -o locadora.o locadora.c

locadora: locadora.o
	gcc -g -o locadora locadora.o


view: lmt.pdf
	evince lmt.pdf

lmt.pdf: lmt.tex
	pdflatex -enc lmt
	pdflatex -enc lmt

clean:
	rm *.aux *.log lmt.pdf *~
