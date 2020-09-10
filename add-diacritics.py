import fontforge, subprocess, sys

nec_in = fontforge.open(sys.argv[1])
#handmade = [glyph for glyph in nec_in.glyphs()]

#copy combining characters
unifont = fontforge.open(subprocess.check_output('fc-match --format=%{file} Unifont.ttf'.split()).decode())
to_transfer = [glyph for glyph in unifont.glyphs() if glyph.width == 0]
for glyph in unifont.glyphs():
	if glyph.width != 0:
		print('',glyph.unicode,end='\r')
		unifont.removeGlyph(glyph)
nec_in.mergeFonts(unifont)

#build composite glyphs
nec_in.selection.select(*(glyph for glyph in nec_in))
nec_in.selection.invert()
nec_in.build()

#remov any unwanted glyphs
for glyph in nec_in.glyphs():
	if glyph.width not in [0,512]:
		#print('',glyph.unicode,end='\r')
		print(glyph.width,fontforge.UnicodeNameFromLib(glyph.unicode))

#save the script
nec_in.generate(sys.argv[2])
