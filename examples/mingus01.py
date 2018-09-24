# from mingus.midi.MidiFileOut import *
# from mingus.midi import MidiTrack, MidiFileIn, MidiEvents, Sequencer, SequencerObserver
# from mingus.containers.Note import Note
# from mingus.containers.NoteContainer import NoteContainer
# from mingus.containers.Bar import Bar
# from mingus.containers.Track import Track
# from mingus.containers.Composition import Composition
# from mingus.containers.Instrument import MidiInstrument
from mingusutils import *
import random

'''
-----------------------------------------------------------------------------
   Key / Perc. sound            Key / Perc. sound            Key / Perc. sound
  -----------------------------------------------------------------------------
   35. Acoustic Bass Drum       51. Ride Cymbal 1            67. High Agogo
   36. Bass Drum 1              52. Chinese Cymbal           68. Low Agogo
   37. Side Stick               53. Ride Bell                69. Cabasa
   38. Acoustic Snare           54. Tambourine               70. Maracas
   39. Hand Clap                55. Splash Cymbal            71. Short Whistle
   40. Electric Snare           56. Cowbell                  72. Long Whistle
   41. Low Floor Tom            57. Crash Cymbal 2           73. Short Guiro
   42. Closed Hi-Hat            58. Vibraslap                74. Long Guiro
   43. High Floor Tom           59. Ride Cymbal 2            75. Claves
   44. Pedal Hi-Hat             60. High Bongo               76. Hi Woodblock
   45. Low Tom                  61. Low Bongo                77. Low Woodblock
   46. Open Hi-Hat              62. Mute Hi Conga            78. Mute Cuica
   47. Low-Mid Tom              63. Open Hi Conga            79. Open Cuica
   48. High-Mid Tom             64. Low Conga                80. Mute Triangle
   49. Crash Cymbal 1           65. High Timbale             81. Open Triangle
   50. High Tom                 66. Low Timbale
'''	 
	 
def gen_bin_str(len, n_ones):
	no = 0
	s = set()
	for i in xrange(n_ones):
		f = 0
		while f == 0:
			x = random.randint(0, len-1)
			# print x # debug
			if x not in s:
				s.add(x)
				f = 1
	rs = ''			
	# print s # debug
	for i in xrange(len):
		if i in s:
			rs += '1'
		else:
			rs += '0'
	return rs			

def and_str(a, b):
	x1 = int(a,2)
	x2 = int(b,2)
	x = x1 & x2
	return "{0:016b}".format(x) # N.B.: solo per stringhe lunghe 16

def or_str(a, b):
	x1 = int(a,2)
	x2 = int(b,2)
	x = x1 | x2
	return "{0:016b}".format(x)

def xor_str(a, b):
	x1 = int(a,2)
	x2 = int(b,2)
	x = x1 ^ x2
	return "{0:016b}".format(x)
	
def place_at(bar, note, pos):
	bar.place_notes_at(note, pos, 16)

def bin_to_bar(bar, note, str):
	ls = len(str)
	dt = 1.0 / float(ls)
	for i in xrange(ls):
		if str[i] == '1':
			place_at(bar, note, i*dt)
			
def gen01() :
	tk1 = Track()
	tk2 = Track()
	# channel = 9 (10 but zero-based!)
	bd = Note('C', 2)
	bd.channel = 9
	lt = Note('F', 2)
	lt.channel = 9
	ht = Note('B', 2)
	ht.channel = 9
	lb = Note('C#', 4)
	lb.channel = 9
	hb = Note('C', 4)
	hb.channel = 9
	bd.velocity = lt.velocity = ht.velocity = lb.velocity = hb.velocity = 100
	# t1 = Note('E', 5)
	# t1.channel = 9
	# t2 = Note('F', 5)
	# t2.channel = 9
	# temple blocks
	t1 = Note('C', 2)
	t1.channel = 0
	t2 = Note('A#', 2)
	t2.channel = 0
	t3 = Note('G#', 3)
	t3.channel = 0
	t4 = Note('F#', 4)
	t4.channel = 0
	t5 = Note('E', 5)
	t5.channel = 0
	t1.velocity = t2.velocity = t3.velocity = t4.velocity = t5.velocity = 100
	dummy = Note('C-0')
	dummy.velocity = 0
	dummy.channel = 9
	nsteps = 16
	dur = 16
	n_bars = 32
	emptys = "0000000000000000"
	bds0 = lts0 = hts0 = lbs0 = hbs0 = emptys
	t1s0 = "0000000000100000"
	t2s0 = "0010000000000000"
	t3s0 = "1001000000010000"
	t4s0 = "0000100000001010"
	t5s0 = "0000000000000100"
	# n. di variazioni
	nvar = [0, 0, 1, 1, 1, 1, 2, 2,
					3, 3, 3, 3, 3, 3, 3, 3,
					4, 4, 5, 5, 0, 0, 1, 1,
					2, 2, 1, 1, 1, 1, 0, 0]
	for nb in xrange( n_bars ):
		b = Bar('C', (4,4))
		b2 = Bar('C', (4,4))
		# note "dummy" posizionate su una "griglia di quantizzazione"	
		for i in xrange(nsteps):
			b.place_notes(dummy, dur)
			b2.place_notes(dummy, dur)
		# print repr(b) # debug
		# note "vere"	
		bds = xor_str( bds0, gen_bin_str(16, nvar[nb]) )
		bin_to_bar(b, bd, bds)
		lts = xor_str( lts0, gen_bin_str(16, nvar[nb]) )
		bin_to_bar(b, lt, lts)
		hts = xor_str( hts0, gen_bin_str(16, nvar[nb]) )
		bin_to_bar(b, ht, hts)
		lbs = xor_str( lbs0, gen_bin_str(16, nvar[nb]) )
		bin_to_bar(b, lb, lbs)
		hbs = xor_str( hbs0, gen_bin_str(16, nvar[nb]) )
		bin_to_bar(b, hb, hbs)
		t1s = xor_str( t1s0, gen_bin_str(16, nvar[nb]) )
		bin_to_bar(b2, t1, t1s)
		t2s = xor_str( t2s0, gen_bin_str(16, nvar[nb]) )
		bin_to_bar(b2, t2, t2s)
		t3s = xor_str( t3s0, gen_bin_str(16, nvar[nb]) )
		bin_to_bar(b2, t3, t3s)
		t4s = xor_str( t4s0, gen_bin_str(16, nvar[nb]) )
		bin_to_bar(b2, t4, t4s)
		t5s = xor_str( t5s0, gen_bin_str(16, nvar[nb]) )
		bin_to_bar(b2, t5, t5s)
		# cleanup - tolgo le note "dummy"
		for x in b.bar :
			x[2].remove_note('C', 0)
		for x in b2.bar :
			x[2].remove_note('C', 0)
		# print repr(b) # debug
		tk1 + b
		tk2 + b2
	# "dummy bar"
	db = Bar('C', (4,4))
	db.place_notes(dummy,1)
	tk1 + db
	tk2 + db	
	m = MidiInstrument()
	# TR-808 kit = 25 (26 but zero-based!)
	# m.instrument_nr = 25
	m.instrument_nr = 0
	m.channel = 9
	tk1.instrument = m	
	m2 = MidiInstrument()
	m2.instrument_nr = 115
	m2.channel = 0
	tk2.instrument = m2
	comp = Composition()
	comp + tk1
	comp + tk2
	#write_Track("testx.mid", t, 128)
	write_Composition("testx.mid", comp, 128)
	
	
gen01()	