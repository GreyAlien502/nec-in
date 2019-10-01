.PHONY: all bdf clean
all: bdf build/nec-in.psf build/nec-in.pf2 build/nec-in.bdf
$(info $(shell mkdir -p build))


DIST=~/.local/share/fonts/nec-in.bdf
bdf: $(DIST)
$(DIST): build/nec-in.bdf
	cp build/nec-in.bdf $(DIST)
build/nec-in.bdf: nec-in.sfd
	python -c "import fontforge as f;  f.open('nec-in.sfd').generate('build/nec-in.bdf');"
	cp `ls build/nec-in-*.bdf -t | head -n1` build/nec-in.bdf


build/nec-in.psf: build/nec-in.bdf
	bdf2psf --fb build/nec-in.bdf \
		/usr/share/bdf2psf/standard.equivalents \
		/usr/share/bdf2psf/ascii.set+:/usr/share/bdf2psf/useful.set \
		512 \
		build/nec-in.psf
build/nec-in.pf2:
	grub-mkfont -s 6 -o build/nec-in.pf2 build/nec-in.bdf

build/nec-in.ttf: nec-in.sfd
	python -c "import fontforge as f;  f.open('nec-in.sfd').generate('build/nec-in.ttf');"
	cp `ls build/nec-in-*.ttf -t | head -n1` build/nec-in.ttf




clean:
	rm build/*
