import fontforge, subprocess, sys, unicodedata

p=type('',(),{'__pow__':lambda _,x:print(x)or x})()

TONOS=ord(unicodedata.lookup('GREEK TONOS'))

nec_in = fontforge.open(sys.argv[1])
#handmade = [glyph for glyph in nec_in.glyphs()]
custom_chars = {chr(glyph.unicode) for glyph in nec_in.glyphs() if glyph.unicode>0}

#copy combining characters
unifont = fontforge.open(subprocess.check_output('fc-match --format=%{file} Unifont'.split()).decode())
for glyph in unifont.glyphs():
       if glyph.unicode == TONOS:
               print('found tonos')
               glyph.width = 680
               custom_chars.add(chr(glyph.unicode))
       elif glyph.width != 0:
               print('',glyph.unicode,end='\r')
               unifont.removeGlyph(glyph)
nec_in.mergeFonts(unifont)

#build composite glyphs
nec_in.selection.select(*(glyph for glyph in nec_in))
nec_in.selection.invert()
nec_in.build()

#save the font
nec_in.generate(sys.argv[2])
with open(sys.argv[3],'w') as unicodes_file:
	unicodes_file.write( '\n'.join(
		f'{glyph.unicode:x}'
		for glyph in nec_in.glyphs()
		if (
			glyph.unicode > 0
			and
			glyph.width in [0,680]
			and
			all(
				unicodedata.category(component)[0] == 'M' or component in custom_chars
				for component in unicodedata.normalize('NFD',chr(glyph.unicode))
			)
		)
	) )
