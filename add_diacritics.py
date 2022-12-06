import fontforge, subprocess, sys, unicodedata

def p(e):
	print(e)
	return(e)


nec_in = fontforge.open(sys.argv[1])
#handmade = [glyph for glyph in nec_in.glyphs()]
custom_chars = {chr(glyph.unicode) for glyph in nec_in.glyphs() if glyph.unicode>0}

#copy combining characters
unifont = fontforge.open(subprocess.check_output('fc-match --format=%{file} Unifont'.split()).decode())
to_transfer = [glyph for glyph in unifont.glyphs() if glyph.width == 0]
for glyph in unifont.glyphs():
	if glyph.width != 0:
		print('',glyph.unicode,end='\r')
		unifont.removeGlyph(glyph)
nec_in.mergeFonts(unifont)


#build composite glyphs
for glyph in nec_in.glyphs():
	if 'GREEK' in fontforge.UnicodeNameFromLib(glyph.unicode):
		decomp = unicodedata.normalize('NFD',chr(glyph.unicode))
		if len(decomp) > 1:
			print(fontforge.UnicodeNameFromLib(glyph.unicode))
			glyph.user_decomp = decomp
nec_in.selection.select(*(glyph for glyph in nec_in))
nec_in.selection.invert()
nec_in.build()

#remov any unwanted glyphs
for glyph in nec_in.glyphs():
	if (
		glyph.width not in [0,680]
		or
		glyph.unicode > 0
		and
		not all(
			unicodedata.category(component)[0] == 'M' or component in custom_chars
			for component in unicodedata.normalize('NFD',chr(glyph.unicode))
		)
	):
		print(glyph.width,fontforge.UnicodeNameFromLib(glyph.unicode))#,end='\r')
		nec_in.removeGlyph(glyph)

#save the script
nec_in.generate(sys.argv[2])
