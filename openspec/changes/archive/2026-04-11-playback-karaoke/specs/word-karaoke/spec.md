## ADDED Requirements

### Requirement: Capture word boundary timing

During English audio generation, the script SHALL capture word boundary events from edge-tts for each English line. Each word boundary event SHALL include the word text and its start time offset (in seconds). The timing data SHALL be embedded in `index.html` alongside the line data as a JavaScript variable.

#### Scenario: Word timing data structure

- **WHEN** `index.html` is generated
- **THEN** each English line's timing data SHALL be an array of objects with `word` (string) and `offset` (number, in seconds) fields, embedded in a JavaScript variable

#### Scenario: Timing offsets are monotonically non-decreasing

- **WHEN** the timing data for an English line is examined
- **THEN** each entry's `offset` SHALL be greater than or equal to the previous entry's `offset`

### Requirement: Canonical tokenization and alignment

The webpage SHALL render each English line's text as individual `<span>` elements. The tokenization rule SHALL be: split the English text on whitespace (equivalent to `text.split(/\s+/)`). Each resulting token becomes one `<span>`.

The number of `<span>` elements SHALL equal the number of word boundary entries in the timing data for that line. If the counts do not match, the webpage SHALL fall back to displaying the line as a single unsplit block with no karaoke highlighting for that line. No error SHALL be thrown; playback SHALL still work normally without highlighting.

#### Scenario: Tokenization matches timing data

- **WHEN** an English line "Hi dear friends" has 3 whitespace-split tokens and 3 word boundary entries
- **THEN** the webpage SHALL render 3 `<span>` elements and map each to its corresponding timing entry by index

#### Scenario: Token count mismatch falls back gracefully

- **WHEN** an English line has 5 whitespace-split tokens but the timing data contains 4 word boundary entries
- **THEN** the webpage SHALL render the line as a single text block without `<span>` splitting, and no karaoke highlighting SHALL occur for that line

### Requirement: Word-by-word karaoke highlighting

During English audio playback, the webpage SHALL highlight the current word being spoken. The word whose timing offset has been reached (but whose next word's offset has not yet been reached) SHALL be visually highlighted with a distinct color. Only one word SHALL be highlighted at a time. Only English lines SHALL have karaoke highlighting; Chinese lines SHALL NOT.

The highlighting SHALL be driven by the `timeupdate` event on the Audio element, using `audio.currentTime` to determine which word to highlight. This inherently tracks the correct position regardless of playback speed, since `currentTime` reflects actual playback position.

#### Scenario: Words highlight in sequence during playback

- **WHEN** an English audio is playing and `audio.currentTime` crosses a word's offset
- **THEN** that word's `<span>` SHALL be highlighted and the previous word's highlight SHALL be removed

#### Scenario: Highlight resets on new playback

- **WHEN** the user starts playing a line (or replays the same line)
- **THEN** all word highlights for that line SHALL be reset before playback begins

#### Scenario: Highlight resets on stop

- **WHEN** audio stops (by clicking a different line or reaching the end)
- **THEN** all word highlights SHALL be cleared

#### Scenario: Highlight persists on pause

- **WHEN** audio is paused
- **THEN** the currently highlighted word SHALL remain highlighted until playback resumes or the audio is stopped

#### Scenario: Karaoke works with speed control

- **WHEN** the user changes playback speed
- **THEN** the word highlighting SHALL still track the correct word because it uses `audio.currentTime` which reflects actual playback position
