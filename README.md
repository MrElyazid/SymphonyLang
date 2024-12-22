﻿# SymphonyLang

SymphonyLang is a simplified language for creating piano music that compiles to MIDI files. It provides an intuitive syntax for writing musical compositions with support for tempo control, notes, scales, chords, rests, comments.

## Language Features

### Basic Syntax

A SymphonyLang program consists of:
1. A tempo setting
2. A sequence of musical elements (notes, scales, chords, rests)
3. can also handles comments with the syntax `# comment`

Example:
```
tempo=120
C4 qn
D4 hn
E4 qn
F4 wn
```

### Tempo:

the tempo declaration at the start of a SymphonyLang program represents the number of Beats per minute ( BPM ), its like the number of *pulses* during one minute for music programs.

note that the duration for notes in SymphonyLang needs to be translated to *TICKS* because we're using midi files as output, see the code 
in `midi_generator.py` to understand the mapping between note durations and ticks.

### Notes

Notes are written in the format: `[Note][Accidental?][Octave] [Duration]`

- **Note**: A through G (e.g., C, D, E, F, G, A, B)
- **Accidental** (optional): 
  - `#` for sharp
  - `b` for flat
- **Octave**: Number representing the octave (e.g., 4 for middle C)
- **Duration**:
  - `wn` = whole note
  - `hn` = half note
  - `qn` = quarter note
  - `en` = eighth note
  - `sn` = sixteenth note

the duration of a note is related to the tempo setting, a whole note ( wn ) is 4 beats.

Examples:
```
C4 qn    # Middle C quarter note
F#4 hn   # F sharp half note
Bb3 wn   # B flat whole note
```

### Rests

Rests use similar duration notation:
- `wr` = whole rest
- `hr` = half rest
- `qr` = quarter rest
- `er` = eighth rest
- `sr` = sixteenth rest

Example:
```
C4 qn
qr      # Quarter rest
E4 hn
```

### Scales

Scales are written in the format: `[Root Note] [Scale Type] [Extension?]`

Scale Types:
- `maj` = Major scale
- `min` = Minor scale

Extensions (optional):
- `pent` = Pentatonic
- `chrom` = Chromatic

Examples:
```
C4 maj           # C major scale
A4 min pent      # A minor pentatonic scale
F#4 maj chrom    # F sharp chromatic scale
```

When a scale is played, it will:
1. Play ascending from the root note
2. Play descending back to the root
3. Use quarter notes for each note in the scale

### Comments

Use `#` for single-line comments:
```
# This is a comment
tempo=120    # Set the tempo to 120 BPM
C4 qn       # Play middle C
```



### Chords

play multiple notes simultaneiously

syntax : [note1 note2 note3] duration

example : 

```
# This is a comment
tempo=120    # Set the tempo to 120 BPM
C4 qn       # Play middle C
[C4 D4 B#6] wn
```


## GUI Application

SymphonyLang includes a graphical interface for writing and playing music:

### Features
- Text editor for writing SymphonyLang code
- Compile button to convert code to MIDI
- Upload button to load existing .txt files
- MIDI player with playback controls
- Real-time music visualization
- Status messages for errors and success

### Music Player
The application includes a built-in MIDI player with:
- Play button to start playback
- Stop button to end playback
- Current file display
- Playback status indicators

### Music Visualization
The application features a real-time music visualizer that:
- Displays a bar chart representation of the music
- Updates in real-time during playback
- Shows note durations with different bar heights:
  - Whole notes: Tallest bars
  - Half notes: Tall bars
  - Quarter notes: Medium bars
  - Eighth notes: Short bars
  - Sixteenth notes: Shortest bars
- Uses pastel colors to distinguish different notes

### File Management

- Upload existing .txt files to edit or play
- Automatically generates output.mid when compiling
- Provides clear status messages for file operations

### Usage
1. Write your SymphonyLang code in the text editor
2. Click "Compile" to generate a MIDI file
3. Use the player controls to play, pause, or stop the music
4. Watch the visualizer display the music in real-time
5. Save your work as a .txt file for later use

## Technical Details

### MIDI Generation
- Notes are converted to MIDI note numbers (middle C = 60)
- Durations are converted to MIDI ticks:
  - Whole note = 1920 ticks
  - Half note = 960 ticks
  - Quarter note = 480 ticks
  - Eighth note = 240 ticks
  - Sixteenth note = 120 ticks

### Scale Patterns
The following scale patterns are supported (numbers represent semitones from root):
- Major: [0, 2, 4, 5, 7, 9, 11, 12]
- Minor: [0, 2, 3, 5, 7, 8, 10, 12]
- Major Pentatonic: [0, 2, 4, 7, 9, 12]
- Minor Pentatonic: [0, 3, 5, 7, 10, 12]
- Chromatic: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

## Example Composition

Here's an example SymphonyLang composition:
```
tempo=120

# Play a simple melody
C4 qn
E4 qn
G4 hn
C5 wn

# Add a scale
C4 maj

F4 qn
G4 qn
A4 hn

# End with a pentatonic scale
G4 min pent
```

## Error Handling

SymphonyLang provides clear error messages for:
- Invalid note names or octaves
- Incorrect duration specifications
- Unknown scale types or extensions
- Invalid tempo values
- Syntax errors in the code
- MIDI generation issues
- File loading/saving problems

The GUI displays these errors in red text below the editor, making it easy to identify and fix issues in your composition. Success messages are shown in green, and warnings in orange.

## Libraries and tools :

Just see requirements.txt :)

## Screenshots :

!(pic1)[./assets/main.png]
!(pic2)[./assets/text_editor.png]
!(pic3)[./assets/visualization.png]