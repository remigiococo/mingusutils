from mingus.extra.musicxml import *
from mingus.midi.midi_file_in import MidiFile, MIDI_to_Composition
from mingus.containers.composition import Composition
import sys

if len(sys.argv) < 2:
	print("missing input file!!!")
	sys.exit(0)
	
nomemid=sys.argv[1]

#mf=MidiFile()
#try:
#	mf.parse_midi_file(nomemid)
#except Exception:
#	pass
# print(mf) # debug

comp,bpm=MIDI_to_Composition(nomemid)
print(type(comp))

# print(comp) # debug

nomexml="test"
write_Composition(comp, nomexml)
