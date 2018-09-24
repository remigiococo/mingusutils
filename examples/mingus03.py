from mingusutils import *
import random

#penta = [0, 2, 5, 7, 9]
penta = [0, 2, 4, 5, 7, 9, 11]
lpenta = len(penta)
#penta2 = [0, 3, 5, 7, 10]
penta2 = [0, 2, 4, 5, 7, 9, 11]
lpenta2 = len(penta2)

def test01():
	global penta, lpenta
	c = setup_composition(nbars=16)
	print "N. tracks", len(c.tracks)
	i = 0
	pause_prob = 20
	for t in c.tracks:
		print "N. bars", len(t.bars)
		j = 0
		m = MidiInstrument()
		m.channel = i
		i += 1
		m.instrument_nr = random.randint(0, 30)
		print "instrument:", m.instrument_nr
		t.instrument = m
		for b in t.bars:
			offset = 24
			if j >= 32:
				offset = 27
			j += 1
			nn = 4
			if i == 1:
				nn = 16
			for k in xrange(nn):	
				x = penta[ random.randint(0, lpenta-1) ] + 12 * random.randint(0,2) + offset
				n = Note('C',4)
				n.channel = i
				n.velocity = 100
				n.from_int(x)
				pl = k*1.0/nn
				if random.randint(0,100) > pause_prob:
					place_at(b, n, pl)
			clean_bar(b)	
	write_Composition("test_i.mid", c, 120)
	
		
def test02():
	global penta, lpenta
	c = setup_composition(ntracks=1)
	rm = randmel()
	offset = 36
	for t in c.tracks:
		set_track_instrument(t, 81)
		for b in t.bars:
			for k in xrange(16):
				x = rm.extract_note2(penta2) + offset
				n = Note('C',4)
				n.channel = 0
				n.velocity = 100
				n.from_int(x)
				place_at(b, n, k*1.0/16.0)
			clean_bar(b)
	write_Composition("test_j.mid", c, 120)
	
def test03():
	b = Bar()
	init_bar(b)
	print b
	clean_bar(b)
	print b

def test04():
	global penta, lpenta, penta2, lpenta2
	c = setup_composition(ntracks=1)
	rm = randmel()
	offset = 36
	pause_prob = 20
	for t in c.tracks:
		set_track_instrument(t, 81)
		for b in t.bars:
			for k in xrange(16):
				#x = rm.extract_note2(penta2) + offset
				x = rm.extract_note_tri(penta2) + offset
				n = Note('C',4)
				n.channel = 0
				n.velocity = 100
				n.from_int(x)
				if random.randint(0,100) > pause_prob:
					place_at(b, n, k*1.0/16.0)
			clean_bar(b)
	write_Composition("test_j.mid", c, 120)

def test_poly():
	global penta, lpenta, penta2, lpenta2
	c = setup_composition(ntracks=2)
	rm = randmel()
	offset = [ int(Note('C',3)), int(Note('C',5)) ]
	pause_prob = 20
	i = 0
	inst = [0, 10]
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
	
drumnotes = [0,2,6,7]	
def test_drum():
	global penta, lpenta
	c = setup_composition(ntracks=1)
	rm = randmel()
	offset = 24
	pause_prob = 20
	for t in c.tracks:
		set_track_instrument(t, 0)
		for b in t.bars:
			for k in xrange(16):
				x = rm.extract_note2(drumnotes,ottave=1) + offset
				n = Note('C',4)
				n.channel = 9
				n.velocity = 100
				n.from_int(x)
				#print x, int(n) # debug
				if random.randint(0,100) > pause_prob:
					place_at(b, n, k*1.0/16.0)
			clean_bar(b)
	write_Composition("test_dr.mid", c, 120)
	
test_poly()	
#test_drum()