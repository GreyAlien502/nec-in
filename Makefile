.PHONY: all clean
$(info $(shell mkdir -p build))
DIST=~/.local/share/fonts/

all: $(DIST)/nec-in.ttf build/nec-in.psf build/nec-in.pf2 build/nec-in.bdf

$(DIST)/nec-in.ttf: build/nec-in.ttf
	cp $< $@

build/nec-in.bdf: nec-in.sfd
	fontforge -c 'fontforge.open("$<").generate("build/nec-in.bdf")'
	cp `ls build/nec-in-*.bdf -t | head -n1` $@

build/nec-in.psf: build/nec-in.bdf
	bdf2psf --fb $< \
		/usr/share/bdf2psf/standard.equivalents \
		/usr/share/bdf2psf/ascii.set+:/usr/share/bdf2psf/useful.set \
		512 \
		$@

build/nec-in.pf2: build/nec-in.bdf
	grub-mkfont -s 6 -o $@ $<

build/without-diacritics.ttf: build/nec-in.bdf
	bdf2ttf -o $@ $<

build/nec-in.ttf: build/without-diacritics.ttf add_diacritics.py
	python add_diacritics.py $< $@

build/nec-in.c: build/nec-in.psf psf2c.sh
	bash psf2c.sh $< > $@

clean:
	rm -rf build/
