.DELETE_ON_ERROR:
.PHONY: all dist clean
$(info $(shell mkdir -p build))
DIST=~/.local/share/fonts/

all: $(shell echo build/nec-in.{ttf,woff2,psf,pf2,bdf,flf})
dist: $(DIST)/nec-in.ttf

$(DIST)/nec-in.ttf: build/nec-in.ttf
	cp $< $@

build/nec-in.bdf: nec-in.sfd
	fontforge -c 'fontforge.open("$<").generate("build/nec-in.bdf")'
	sed -r 's/(POINT_SIZE ).*/\16/' `ls build/nec-in-*.bdf -t | head -n1` > $@

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

build/merged.ttf build/unicode_to_keep: build/without-diacritics.ttf add_diacritics.py
	python add_diacritics.py $< build/merged.ttf build/unicode_to_keep

build/nec-in.woff build/nec-in.woff2: build/merged.ttf build/unicode_to_keep
	pyftsubset build/merged.ttf --unicodes-file=build/unicode_to_keep --no-ignore-missing-unicodes --output-file=$@ --recommended-glyphs --flavor=`cut -d. -f2 <<<$@`

build/nec-in.ttf: build/nec-in.woff
	python -c "from fontTools.ttLib import woff2; woff2.decompress('$<', '$@')"

build/nec-in.c: build/nec-in.psf psf2c.sh
	bash psf2c.sh $< > $@

build/uncompressed.flf: build/without-diacritics.ttf
	python ttf2flf.py -s 6 $<  > $@

build/nec-in.flf: build/uncompressed.flf
	zip $@ $<



clean:
	rm -rf build/
