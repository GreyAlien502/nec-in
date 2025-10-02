import tempfile,unicodedata,argparse
import numpy as n
import itertools
import fontforge, PIL.Image

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('input')
	parser.add_argument('-s','--size',type=int)
	parser.add_argument('-H','--hardblank',default='.')
	parser.add_argument('-f','--fill',default='8')
	return parser.parse_args()




options = parse_args()

if not all([
	(len(options.hardblank)==1),
	(len(options.fill)==1),
	(options.hardblank != options.fill),
]):
	raise Exception(f"Illegal options: {options}")

font = fontforge.open(options.input)

glyphs = {}
with tempfile.TemporaryDirectory() as tmpdir:
	glyph_path = tmpdir+'/glyph.png'
	for glyph in font.glyphs():
		glyph.export(glyph_path,pixelsize=options.size,bitdepth=1)
		with PIL.Image.open(glyph_path) as img:
			glyphs[glyph.unicode] = n.array(img)[1:,:-1]



comment = '''
	test comment
'''
hardblank = options.hardblank
fill = options.fill
endmark = '@'

def header():
	return ' '.join((str(x) for x in (
		(
			"flf2a" # Signature
			+
			hardblank # Hardblank
		),
		6, # Height
		5, # Baseline
		4 + 2, # Max_Length = usually the width of the widest FIGcharacter, plus 2
		sum(( # Old_Layout
		    -1,   # Full-width layout by default
		    # 0,  # Horizontal fitting (kerning) layout by default*
		    # 1,  # Apply horizontal smushing rule 1 by default
		    # 2,  # Apply horizontal smushing rule 2 by default
		    # 4,  # Apply horizontal smushing rule 3 by default
		    # 8,  # Apply horizontal smushing rule 4 by default
		    #16,  # Apply horizontal smushing rule 5 by default
		    #32,  # Apply horizontal smushing rule 6 by default

		)),
                len(comment.split('\n')), # Comment_Lines
                0, # Print_Direction
		sum((  # Full_Layout:
			#1<<0 , # Apply horizontal smushing rule 1 when smushing
			#1<<1 , # Apply horizontal smushing rule 2 when smushing
			#1<<2 , # Apply horizontal smushing rule 3 when smushing
			#1<<3 , # Apply horizontal smushing rule 4 when smushing
			#1<<4 , # Apply horizontal smushing rule 5 when smushing
			#1<<5 , # Apply horizontal smushing rule 6 when smushing
			1<<6 , # Horizontal fitting (kerning) by default
			#1<<7 , # Horizontal smushing by default (Overrides 64)
			#1<<8 , # Apply vertical smushing rule 1 when smushing
			#1<<9 , # Apply vertical smushing rule 2 when smushing
			#1<<10, # Apply vertical smushing rule 3 when smushing
			#1<<11, # Apply vertical smushing rule 4 when smushing
			#1<<12, # Apply vertical smushing rule 5 when smushing
			1<<13, # Vertical fitting by default
			#1<<14, # Vertical smushing by default (Overrides 8192)
		)),
                   # Codetag_Count = the total number of FIGcharacters in the font minus 102
	)))



def glyph_str(glyph):
	return (endmark+'\n').join(
		''.join(
			{1:hardblank,0:fill}[e]
			for e in row
		)
		for row in glyph
	)+ endmark*2

def figcharacter_data():
	required = [
		*range(0x20,0x7f), # ASCII
		196, 214, 220, 228, 246, 252, 223 # German
	]
	return itertools.chain(
		(
			glyph_str(
				glyphs.get(char, n.zeros((options.size,0)) )
			)
			for char in required
		),
		(
			#str( int.from_bytes(chr(glyph.unicode).encode('utf-8'), 'big') )
			f'0x{glyph.unicode:X} '+unicodedata.name(chr(glyph.unicode))[:80]+'\n'
			+ glyph_str(glyphs[glyph.unicode])
			for glyph in font.glyphs()
			if glyph.unicode not in required
			and glyph.unicode in range(0x110000)
			and unicodedata.category(chr(glyph.unicode)) != 'Cc'
		)
	)

for section in itertools.chain(
	[
		header(),
		'\n'.join(comment.split('\n'))
	],
	figcharacter_data()
):
	print( section )
