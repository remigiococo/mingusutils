#from mingus.midi.MidiFileOut import *
#from mingus.midi import MidiTrack, MidiFileIn, MidiEvents, Sequencer, SequencerObserver
#from mingus.containers.Note import Note
#from mingus.containers.NoteContainer import NoteContainer
#from mingus.containers.Bar import Bar
#from mingus.containers.Track import Track
#from mingus.containers.Composition import Composition
#from mingus.containers.Instrument import MidiInstrument
from mingusutils import *
import random

penta1 = [0, 2, 5, 7, 9]
lpenta1 = len(penta1)

def test01():
	tk1 = Track()
	tk2 = Track()
	n_bars = 32
	quant = 32
	dummy = Note('C-0')
	dummy.velocity = 0
	dummy.channel = 0
	for i in xrange(n_bars):
		offset = 24
		if i in range(8,15):
			offset = 27
		b = Bar('C', (4,4))
		b2 = Bar('C', (4,4))
		for j in xrange(4):
			n = Note('C', 4)
			n.channel = 0
			n.velocity = 100
			x = penta1[ random.randint(0, lpenta1-1) ] + 12 * random.randint(0,2) + offset
			#n.from_int( random.randint(24, 60) )
			n.from_int(x)
			b + n
		for j in xrange(quant):
			b2.place_notes(dummy, quant)
		for j in xrange(8):	
			n2 = Note('G', 6)
			n2.channel = 0
			n2.velocity = 100
			x = penta1[ random.randint(0, lpenta1-1) ] + 12 * random.randint(0,2) + offset
			#n2.from_int( random.randint(24, 60) )
			n2.from_int(x)
			b2.place_notes_at(n2, j*1.0/8.0, 8)
		tk1 + b
		tk2 + b2
	# print repr(tk2) # debug		
	m = MidiInstrument()
	#m.instrument_nr = 12 # 12 - marimba
	m.instrument_nr = 0
	m.channel = 0
	tk1.instrument = m	
	m2 = MidiInstrument()
	#m2.instrument_nr = 12 # 12 - marimba
	m2.instrument_nr = 0
	m2.channel = 0
	tk2.instrument = m2
	comp = Composition()
	comp + tk1
	comp + tk2
	#write_Track("testx.mid", t, 128)
	write_Composition("testp.mid", comp, 128)
	
def test02():
	b = Bar('C', (4,4))
	durs = [8, 16]
	for i in xrange(10):	
		n = Note('C', 4)
		b.place_notes(n, durs[ random.randint(0,1) ])
	write_Bar("testb.mid", b, 120)
	
test01()	
