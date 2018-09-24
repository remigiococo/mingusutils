import random
#from mingus.midi.MidiFileOut import *
from mingus.midi.midi_file_out import *
#from mingus.midi import MidiTrack, MidiFileIn, MidiEvents, Sequencer, SequencerObserver
from mingus.midi.midi_track import MidiTrack
#from mingus.midi.midi_file_in import MidiFileIn
from mingus.midi.midi_events import *
from mingus.midi.sequencer import Sequencer 
from mingus.midi.sequencer_observer import SequencerObserver
from mingus.containers.note import Note
from mingus.containers.note_container import NoteContainer, Note
from mingus.containers.bar import Bar
from mingus.containers.track import Track
from mingus.containers.composition import Composition
from mingus.containers.instrument import MidiInstrument
from mingus.core import progressions, intervals
from mingus.core import chords as ch

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
	if len(a) == 16:
		return "{0:016b}".format(x) # N.B.: solo per stringhe lunghe 16
	elif len(a) == 32:	
		return "{0:032b}".format(x)
	else:
		return "{0:064b}".format(x)

def or_str(a, b):
	x1 = int(a,2)
	x2 = int(b,2)
	x = x1 | x2
	if len(a) == 16:
		return "{0:016b}".format(x) # N.B.: solo per stringhe lunghe 16
	elif len(a) == 32:	
		return "{0:032b}".format(x)
	else:
		return "{0:064b}".format(x)

def xor_str(a, b):
	x1 = int(a,2)
	x2 = int(b,2)
	x = x1 ^ x2
	if len(a) == 16:
		return "{0:016b}".format(x) # N.B.: solo per stringhe lunghe 16
	elif len(a) == 32:	
		return "{0:032b}".format(x)
	else:
		return "{0:064b}".format(x)
	
def place_at(bar, note, pos, dur=16):
	bar.place_notes_at(note, pos, dur)

def bin_to_bar(bar, note, str, dur=16):
	ls = len(str)
	dt = 1.0 / float(ls)
	for i in xrange(ls):
		if str[i] == '1':
			place_at(bar, note, i*dt, dur)

def init_bar(b, quantiz=16):
	# Note ha i seguenti campi: name, octave, velocity, channel, dynamics 
	dummy = Note('C-0')
	dummy.velocity = 0
	dummy.channel = 0
	for j in xrange(quantiz):
		b.place_notes(dummy, quantiz)
		
def clean_bar(b):
	# Bar.bar e' una lista di triple [beat, duration, notes] (notes e' un NoteContainer)
	for x in b.bar:
		x[2].remove_note('C', 0)
	it = iter(b.bar)
	try:	
		x = it.next()	
	except:
		return
	while x:
		if len(x[2]) == 0:
			b.bar.remove(x)
		try:
			x = it.next()
		except:
			break
		
def setup_composition(nbars=64, ntracks=2, quant=16):
	comp = Composition()
	tks =[Track() for i in xrange(ntracks)]
	for i in xrange(ntracks):
		bars = [Bar() for j in xrange(nbars)]
		for j in xrange(nbars):
			init_bar(bars[j], quant)
			tks[i] + bars[j]	
		comp + tks[i]
	return comp
	
def set_track_instrument(track, instr, channel=0):
	m = MidiInstrument()
	m.channel = channel
	m.instrument_nr = instr
	track.instrument = m
		
	
class randmel:	
	def __init__(self):
		self.stato = 0
		
	def extract_note(self, scala, ottave=3):
		ls = len(scala)
		x = random.randint(-1, 1)
		y = self.stato + x
		if y < 0:
			y = 0
		if y > ls*ottave-1:
			y = ls*ottave-1
		self.stato = y	
		return scala[ y % ls ] + 12 * (y/ls)

	def extract_note2(self, scala, ottave=3):
		ls = len(scala)
		x = 0
		while x == 0:
			x = random.randint(-1, 1)
		y = self.stato + x
		if y < 0:
			y = 0
		if y > ls*ottave-1:
			y = ls*ottave-1
		self.stato = y	
		return scala[ y % ls ] + 12 * (y/ls)
	
	def extract_note_tri(self, scala, ottave=3, interval=2):
		ls = len(scala)
		x = 0
		while x == 0:
			x1 = random.randint(-interval, interval)
			x2 = random.randint(-interval, interval)
			x = (x1+x2)/2
		y = self.stato + x
		if y < 0:
			y = 0
		if y > ls*ottave-1:
			y = ls*ottave-1
		self.stato = y
		# print self.stato # debug	
		return scala[ y % ls ] + 12 * (y/ls)
	
class randdrum:
	_OR_VAR_=0
	_XOR_VAR_=1
	def __init__(self, nsteps=16, nbars=16, tempo=120, duration=16):
		# self.bd = Note('C', 2) # bass drum
		self.bd = Note('B', 1) # bass drum
		self.bd.channel = 9
		self.lt = Note('F', 2) # lo tom
		self.lt.channel = 9
		self.ht = Note('B', 2) # hi tom
		self.ht.channel = 9
		self.lb = Note('C#', 4) # lo bongo
		self.lb.channel = 9
		self.hb = Note('C', 4) # hi bongo
		self.hb.channel = 9
		self.ch = Note('F#', 2) # closed hat
		self.ch.channel = 9
		self.oh = Note('A#', 2) # open hat
		self.oh.channel = 9
		self.sn = Note('D', 2) # snare
		self.sn.channel = 9
		self.DRMAP={"bd":self.bd, "sn":self.sn, "ch":self.ch, "oh":self.oh, 
			"lt":self.lt, "ht":self.ht, "hb":self.hb, "lb":self.lb}
		for x in self.DRMAP.keys():
			self.DRMAP[x].velocity = 100
			self.DRMAP[x].duration = duration
		self.tk = Track()
		self.bds=""	
		self.sns=""	
		self.hts=""	
		self.lts=""	
		self.chs=""	
		self.ohs=""	
		self.lbs=""	
		self.hbs=""	
		self.bdv=[]	
		self.snv=[]	
		self.htv=[]	
		self.ltv=[]	
		self.chv=[]	
		self.ohv=[]	
		self.lbv=[]	
		self.hbv=[]	
		self.m = MidiInstrument()
		# TR-808 kit = 25 (26 but zero-based!)
		# self.m.instrument_nr = 25
		self.m.instrument_nr = 0
		self.m.channel = 9
		self.tk.instrument = self.m
		self.nsteps = nsteps
		self.dur = duration
		self.n_bars = nbars
		self.tempo = tempo
		self.STRMAP={"bd":self.bds, "sn":self.sns, "ch":self.chs, "oh":self.ohs, 
			"lt":self.lts, "ht":self.hts, "hb":self.hbs, "lb":self.lbs}
		self.VARMAP={"bd":self.bdv, "sn":self.snv, "ch":self.chv, "oh":self.ohv, 
			"lt":self.ltv, "ht":self.htv, "hb":self.hbv, "lb":self.lbv}
		self.vartype = self._OR_VAR_	
		
	def base_str(self, instr, s):
		if len(s) != self.nsteps:
			print "error: pattern length not corresponding to num. of steps !!!"
			return
		self.STRMAP[instr] = s
		
	def set_var(self, instr, v):
		if len(v) != self.n_bars:
			print "error: variation length not corresponding to num. of bars !!!"
			return
		self.VARMAP[instr] = v
		
	def set_kit(self, prog):
		set_track_instrument(self.tk, prog)
		
	def gen(self, midifilename):
		dummy = Note('C-0')
		dummy.velocity = 0
		dummy.channel = 9
		dummy.duration = self.dur
		for nb in xrange( self.n_bars ):
			b = Bar('C', (4,4))
			# note "dummy" posizionate su una "griglia di quantizzazione"	
			for i in xrange(self.nsteps):
				b.place_notes(dummy, self.dur)
			# print repr(b) # debug
			# note "vere"	
			for x in self.STRMAP.keys():
				ys = self.STRMAP[x]
				y = self.DRMAP[x]
				if len(ys) > 0:
					if len(self.VARMAP[x]) > 0:
						var = self.VARMAP[x][nb]
					else:
						var = 0
					if self.vartype == self._OR_VAR_: # or = variazione aggiunge !? xor = toggle
						tmps = or_str( ys, gen_bin_str(self.nsteps, var) ) 
					elif self.vartype == self._XOR_VAR_:
						tmps = xor_str( ys, gen_bin_str(self.nsteps, var) )
					else:
						tmps = ys # no var.
					bin_to_bar(b, y, tmps, self.dur)
			# cleanup - tolgo le note "dummy"
			for x in b.bar :
				x[2].remove_note('C', 0)
			# print repr(b) # debug
			self.tk + b
		# "dummy bar"
		db = Bar('C', (4,4))
		db.place_notes(dummy,1)
		self.tk + db
		comp = Composition()
		comp + self.tk
		write_Composition(midifilename, comp, self.tempo)
	