
### A Simplified Language for Classical Music

#### **Basic Idea:**
SymphonyLang is a language designed to simplify the process of writing and compiling classical music. The project aims to map complex classical music notation (notes, durations, rests, tempo, etc.) into a simplified, keyboard-friendly language, which can then be compiled into a **MIDI file** for playback. Essentially, Symphony Lang will allow users to write music using a custom syntax and then "compile" it into a song, making it easier to compose instrumental music like piano.

#### **Tools We Will Use:**
1. **Python** for the entire development process.
2. **PLY (Python Lex-Yacc)** to define the lexer and parser, creating a compiler for Symphony Lang.
3. **MIDI Libraries**:
   - **mido** for generating and handling MIDI files.
   - Optional: **pretty_midi** for more advanced MIDI manipulation.
4. **ttk Bootstrap** for a modern and clean GUI, allowing users to input their music code, compile it, and potentially play it back directly within the application.
5. **pygame.mixer** (optional) to handle MIDI playback directly from the GUI.
   
#### **Steps to Build Symphony Lang**:

1. **Define the Language Syntax**:
   - Create a simplified syntax for notes, durations, rests, and tempo.
   - Examples: `C4` for middle C in octave 4, `q` for quarter note, `R` for rest, `tempo 120` for tempo in BPM.
   - Plan mappings between classical music symbols and easier keyboard notations.

2. **Create the Lexical Analyzer (Lex)**:
   - Use **PLY** to tokenize the input, converting the simplified language into tokens (e.g., `C4`, `tempo`, `q`).
   - Token types: `NOTE`, `DURATION`, `REST`, `TEMPO`, `NUMBER`.

3. **Write the Grammar Rules (Yacc)**:
   - Define how tokens can be combined into valid musical expressions (e.g., `NOTE DURATION` to represent a note played for a specific length).
   - The parser will interpret the musical notation and generate corresponding MIDI events.

4. **MIDI Generation**:
   - Use **mido** to convert the parsed music into MIDI events (notes, rests, tempo changes).
   - Implement functions like `play_note`, `play_rest`, and `set_tempo` to generate MIDI messages for playback.
   - Map notes (e.g., `C4`, `G5`) to MIDI numbers and durations (e.g., quarter, half notes) to MIDI ticks.

5. **Integrate GUI with ttk Bootstrap**:
   - Build a user-friendly interface using **ttk bootstrap** where users can enter their music code.
   - Add buttons for "Compile to MIDI" and (optionally) "Play MIDI" functionality.

6. **Compile and Save the MIDI File**:
   - Parse the user input, generate the corresponding MIDI file, and save it for playback.
   
7. **(Optional) Add MIDI Playback**:
   - Use **pygame.mixer** or other libraries to allow users to play the compiled MIDI file directly from the GUI.

8. **Future Features (Optional)**:
   - Add support for more advanced musical concepts like sharps (`#`), flats (`b`), dynamics (`pp`, `ff`), and instrument changes (e.g., switching from piano to violin).
   - Improve error handling for invalid input.

---

### Example Workflow:
1. User inputs the following in the GUI:
   ```
   tempo 120
   C4 q D4 q E4 h
   R q F4 q G4 w
   ```
2. **Lex** tokenizes the input: `TEMPO`, `NUMBER`, `NOTE`, `DURATION`, etc.
3. **Yacc** parses the tokens and converts them into MIDI messages.
4. **mido** generates the MIDI file.
5. User can either save the file or (optionally) play it back directly from the GUI.

### App design : 

![[assets\SymphonyLang.excalidraw.svg]]

### Mapping for Symphony :

### 1. **Core Elements to Map in SymphonyLang**

#### **Notes**:
For piano music, we'll map the basic notes (A-G) along with sharps and flats.

- **Notes**: `A`, `B`, `C`, `D`, `E`, `F`, `G`
- **Accidentals**: `#` for sharp, `b` for flat
- **Octaves**: Use a number to represent the octave, where **C4** is **middle C**.
  
Example keywords:
```
C4, D#4, Bb3
```

#### **Durations**:
We’ll map standard note durations to simple, intuitive symbols.

| Duration    | Keyword   |
|-------------|-----------|
| Whole note  | `wn`      |
| Half note   | `hn`      |
| Quarter note| `qn`      |
| Eighth note | `en`      |
| Sixteenth note | `sn`   |

Example usage:
```
C4 qn, D4 en, E4 hn
```

#### **Rests**:
For rests, you’ll want to map durations similarly.

| Rest Symbol    | Keyword  |
|----------------|----------|
| Whole rest     | `wr`     |
| Half rest      | `hr`     |
| Quarter rest   | `qr`     |
| Eighth rest    | `er`     |
| Sixteenth rest | `sr`     |

Example usage:
```
qr, hr, wr
```

#### **Chords**:
Chords can be represented by enclosing multiple notes in square brackets.

```
[C4 E4 G4] qn   # C major chord with quarter note duration
```

#### **Dynamics**:
Use standard piano dynamics as keywords for loudness.

| Dynamic       | Keyword   |
|---------------|-----------|
| Pianissimo    | `pp`      |
| Piano         | `p`       |
| Mezzo-piano   | `mp`      |
| Mezzo-forte   | `mf`      |
| Forte         | `f`       |
| Fortissimo    | `ff`      |

Example usage:
```
p C4 qn, f G4 hn
```

#### **Articulation**:
Map basic articulation symbols.

| Articulation | Keyword   |
|--------------|-----------|
| Staccato     | `stacc`   |
| Legato       | `legato`  |
| Accent       | `accent`  |
| Slur         | `slur`    |

Example usage:
```
C4 qn stacc, E4 hn legato
```

#### **Tempo**:
Define a tempo with a simple keyword like `tempo=120` for 120 BPM.

Example usage:
```
tempo=90
```

### 2. **Suggested Core Syntax for SymphonyLang**

Let’s put everything together into a simple, readable language:

```plaintext
tempo=120        # Set the tempo to 120 BPM

f                # Set dynamic to forte
C4 qn            # Play C4 for a quarter note
D4 en            # Play D4 for an eighth note
E4 hn            # Play E4 for a half note

[C4 E4 G4] qn    # Play C major chord for a quarter note

qr               # Quarter rest

p                # Switch to piano dynamic
F4 qn stacc      # Play F4 with staccato for a quarter note
```

### 3. **Full Keyword Summary**

| Type             | Keyword Examples                    | Description                                   |
| ---------------- | ----------------------------------- | --------------------------------------------- |
| **Notes**        | `A4`, `C#5`, `Bb3`                  | Notes with octave and accidentals             |
| **Durations**    | `wn`, `hn`, `qn`, `en`, `sn`        | Whole, half, quarter, eighth, sixteenth notes |
| **Rests**        | `wr`, `hr`, `qr`, `er`, `sr`        | Corresponding rests                           |
| **Chords**       | `[C4 E4 G4] qn`                     | Chords in square brackets                     |
| **Dynamics**     | `pp`, `p`, `mp`, `mf`, `f`, `ff`    | Dynamics for volume control                   |
| **Articulation** | `stacc`, `legato`, `accent`, `slur` | Playing style of notes                        |
| **Tempo**        | `tempo=120`                         | Sets the tempo in BPM                         |

---

#### You can test the main.py script via the following input :

```
C4 qn
E4 qn
G4 qn
C5 hn
D4 en
E4 en
F4 en
G4 hn
A4 qn
B4 qn
C5 qn
D5 hn
E5 en
F5 en
G5 en
A5 hn
C5 qn
B4 qn
A4 qn
G4 hn
F4 en
E4 en
D4 en
C4 hn
C4 wn
G4 qn
C5 qn
E5 hn
D5 qn
C5 qn
B4 hn
A4 en
G4 en
F4 en
E4 hn
D4 qn
C4 qn
C4 qn
D4 hn
E4 qn
F4 qn
G4 hn
A4 en
B4 en
C5 en
D5 hn
C5 qn
B4 qn
A4 qn
G4 hn
C4 qn
D4 qn
E4 qn
F4 hn
G4 qn
A4 qn
B4 hn
C5 qn
D5 qn
E5 qn
F5 hn
G5 qn
A5 qn
B5 hn
C5 wn
exit

```
