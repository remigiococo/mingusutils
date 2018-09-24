from mingusutils import *
import random

progression = ["I", "vidom7", "ii", "bIIdom7",
               "I7", "vidom7", "ii", "V7"]
key = 'C'

def test_misc():
	print int( Note('C', 4) )							 
	chords = progressions.to_chords(progression, key)
	print chords # debug
	for c in chords:
		nc = NoteContainer(c)
		print nc # debug
		for n in nc:
			y = int(n) # note to midi note number
			print "---", y # debug
		
penta = [0, 2, 5, 7, 9]
lpenta = len(penta)
penta2 = [0, 3, 5, 7, 10]
lpenta2 = len(penta2)
		
def test_poly():
	global penta, lpenta, penta2, lpenta2
	c = setup_composition(ntracks=2)
	rm = randmel()
	offset = [ int(Note('C',3)), int(Note('C',5)) ]
	pause_prob = 20
	i = 0
	inst = [0, 20]
	quant = 8
	for t in c.tracks:
		set_track_instrument(t, inst[i], i)
		for b in t.bars:
			for k in xrange(quant):
				#x = rm.extract_note2(penta2) + offset
				x = rm.extract_note_tri(penta2, interval=4) + offset[i]
				n = Note('C',4)
				n.channel = i
				n.velocity = 100
				n.from_int(x)
				if random.randint(0,100) > pause_prob:
					place_at(b, n, k*1.0/float(quant))
			clean_bar(b)
		i = i+1	
	write_Composition("test_j.mid", c, 120)

def test_poly2():
	global penta, lpenta, penta2, lpenta2
	c = setup_composition(nbars=16, ntracks=2,quant=16)
	rm = randmel()
	offset = [ int(Note('C',3)), int(Note('C',5)) ]
	pause_prob = 20
	i = 0
	inst = [0, 20]
	quant = 16
	for t in c.tracks:
		set_track_instrument(t, inst[i], i)
		for b in t.bars:
			k = 0
			while k < quant:
				#x = rm.extract_note2(penta2) + offset
				x = rm.extract_note_tri(penta2, interval=4) + offset[i]
				dur = random.choice( [1, 2, 4] )
				n = Note('C',4)
				n.channel = i
				n.velocity = 100
				n.duration = quant/dur
				n.from_int(x)
				# if random.randint(0,100) > pause_prob:
				place_at(b, n, k*1.0/float(quant), quant/dur)
				k = k + dur	
			clean_bar(b)
			print b
		i = i+1	
	write_Composition("test_j.mid", c, 120)
	
	
test_poly2()		