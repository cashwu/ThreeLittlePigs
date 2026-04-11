## MODIFIED Requirements

### Requirement: Generate English audio files

The system SHALL provide a Python script (`generate_audio.py`) that uses the `edge-tts` library to generate MP3 audio files for each English line from `lines.json`. During generation, the script SHALL use `edge_tts.Communicate.stream()` to capture `WordBoundary` events and record each word's text and start time offset (in seconds, converted from the 100-nanosecond unit provided by edge-tts).

Each entry SHALL produce one MP3 file saved to the `audio/` directory with a sequential naming convention (e.g., `en_01.mp3`, `en_02.mp3`).

#### Scenario: Generate all English audio files with word timing

- **WHEN** the user runs `python generate_audio.py`
- **THEN** the script SHALL generate one MP3 per entry and collect word boundary timing data for each English line

#### Scenario: Audio directory creation

- **WHEN** the `audio/` directory does not exist
- **THEN** the script SHALL create the `audio/` directory before generating files

### Requirement: Single source of truth for lines and translations

The system SHALL use a single JSON file (`lines.json`) as the authoritative data source for both English lines and Chinese translations. The file SHALL be an array of objects, each with `en` and `zh` fields. The audio generation script SHALL write this file, and `generate_audio.py` SHALL also generate `index.html` with the line data AND word boundary timing data embedded inline as JavaScript variables, so the webpage works when opened directly via `file://` without a server.

#### Scenario: lines.json structure

- **WHEN** `lines.json` is read by any component
- **THEN** it SHALL contain an array where each element has `"en"` (English line) and `"zh"` (Chinese translation), and the array order defines the line numbering (index 0 → 01, index 1 → 02, etc.)
