
import gensound
import music21

### SIGNALS STUFF ##########################
############################################

def get_overtones(freq_list, n):
   return [freq * (n+1) for freq in freq_list]

def stringify(freq_list):
   return " ".join([str(f) for f in freq_list])

def normalize(l):
   return [e / sum(l) for e in l]

def note_to_freq(note):
    return music21.note.Note(note).pitch.frequency

def CoolSynth(note_list, duration=0.5e3):
  # Get frequencies
  freq_list = [note_to_freq(note) for note in note_list]
  print("Extracted frequencies: {}".format(freq_list))
  # Get overtones
  overtones = []
  overtone_amplitudes = normalize([1, 0.6, 0.1, 0.1, 0.03, 0.01, 0.01, 0.01, 0.01, 0.005, 0.001])
  
  for n in range(len(overtone_amplitudes)):
     overtone_n_list = get_overtones(freq_list, n)
     overtones.append(overtone_n_list)

  overtones = [stringify(ot) for ot in overtones]
  signals = [a * gensound.Sine(ot, duration) for (a, ot) in zip(overtone_amplitudes, overtones)]

  return sum(signals)

### NOTES STUFF #################################
#################################################

def generate_notes():
   # Start at a low C
   pitches = [music21.pitch.Pitch('c3')]

   # Go up by a semi-tone each time
   for i in range(10):
      pitches.append(pitches[-1].transpose(1))

   return [p.name for p in pitches]

### MAIN ########################################
#################################################

if __name__ == '__main__':

  VOLUME_CONTROL = 0.03

  notes = generate_notes()
  s = CoolSynth(notes) * VOLUME_CONTROL
  s.play()