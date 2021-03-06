.PHONY: all clean
$(info $(shell mkdir -p build))
DIST=~/.local/share/fonts/

all: $(DIST)/nec-in.ttf build/nec-in.psf build/nec-in.pf2 build/nec-in.bdf

$(DIST)/nec-in.ttf: build/nec-in.ttf
	cp $< $@

build/nec-in.bdf: nec-in.sfd
	python -c 'import fontforge; fontforge.open("nec-in.sfd").generate("build/nec-in.bdf");'
	cp `ls build/nec-in-*.bdf -t | head -n1` build/nec-in.bdf

build/nec-in.psf: build/nec-in.bdf
	bdf2psf --fb build/nec-in.bdf \
		/usr/share/bdf2psf/standard.equivalents \
		/usr/share/bdf2psf/ascii.set+:/usr/share/bdf2psf/useful.set \
		512 \
		build/nec-in.psf
build/nec-in.pf2: build/nec-in.bdf
	grub-mkfont -s 6 -o build/nec-in.pf2 build/nec-in.bdf


build/nec-in.ttf: build/nec-in.bdf
	bdf2ttf -o build/nec-in.ttf build/nec-in.bdf

clean:
	rm -rf build/
