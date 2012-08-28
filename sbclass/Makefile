DOC ?= songbook.tex
OUTDIR ?= .

TARGET = $(subst .tex,,$(DOC))

CLASS=songbook.cls
SONGS=songs.tex
INDICES=fwidx.ind titidx.ind
INDEXSTYLE=index.ist

EXT_CLASS_DIR = sty

LATEX=TEXINPUTS='.:$(EXT_CLASS_DIR);' pdflatex

all: $(TARGET)

$(TARGET): $(DOC) $(SONGS) $(CLASS) $(INDICES)
	$(LATEX) -jobname $(TARGET) -output-directory $(OUTDIR) $(DOC)

%.ind : %.idx
	makeindex -s $(INDEXSTYLE) $<

%.idx: $(DOC)
	$(LATEX) $(DOC)

clean:
	rm -fr *.dvi *.pdf *.log *.aux *.idx *.ind *.ilg *.mtc *.mtc0 *.maf comment.cut
