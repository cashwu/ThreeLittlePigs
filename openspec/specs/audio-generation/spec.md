# audio-generation Specification

## Purpose

TBD - created by archiving change 'english-lines-practice'. Update Purpose after archive.

## Requirements

### Requirement: Single source of truth for lines and translations

The system SHALL use a single JSON file (`lines.json`) as the authoritative data source for both English lines and Chinese translations. The file SHALL be an array of objects, each with `en` and `zh` fields. The audio generation script SHALL write this file, and `generate_audio.py` SHALL also generate `index.html` with the line data AND word boundary timing data embedded inline as JavaScript variables, so the webpage works when opened directly via `file://` without a server.

#### Scenario: lines.json structure

- **WHEN** `lines.json` is read by any component
- **THEN** it SHALL contain an array where each element has `"en"` (English line) and `"zh"` (Chinese translation), and the array order defines the line numbering (index 0 → 01, index 1 → 02, etc.)


<!-- @trace
source: playback-karaoke
updated: 2026-04-11
code:
  - index.html
  - .DS_Store
  - generate_audio.py
-->

---
### Requirement: Parse eng.md into lines.json

The script SHALL parse `eng.md` to extract English lines. Every non-empty line SHALL be treated as one dialogue entry. If a line starts with `- `, the `- ` prefix SHALL be stripped. Leading and trailing whitespace SHALL be stripped from each line. Empty lines SHALL be ignored. No line merging or continuation logic SHALL be applied.

The script SHALL pair each extracted English line with its corresponding Chinese translation (hardcoded in the script) and write the result to `lines.json`.

#### Scenario: Parse all non-empty lines as individual entries

- **WHEN** `eng.md` contains 9 non-empty lines, some with `- ` prefix and some without
- **THEN** the script SHALL produce 9 entries, one per non-empty line, with `- ` prefixes stripped where present

#### Scenario: Write lines.json

- **WHEN** the script parses `eng.md` successfully
- **THEN** it SHALL write `lines.json` with the paired English and Chinese data before generating any audio


<!-- @trace
source: english-lines-practice
updated: 2026-04-11
code:
  - generate_audio.py
  - index.html
-->

---
### Requirement: Fail-fast on count mismatch

The script SHALL verify that the number of English lines parsed from `eng.md` matches the number of hardcoded Chinese translations. If the counts differ, the script SHALL exit with a non-zero status and print an error message showing both counts. No audio files SHALL be generated in this case.

#### Scenario: Count mismatch aborts generation

- **WHEN** `eng.md` has 9 lines but the script contains 8 Chinese translations
- **THEN** the script SHALL exit with an error like "Mismatch: 9 English lines but 8 Chinese translations" and generate no files


<!-- @trace
source: english-lines-practice
updated: 2026-04-11
code:
  - generate_audio.py
  - index.html
-->

---
### Requirement: Generate English audio files

The system SHALL provide a Python script (`generate_audio.py`) that uses the `edge-tts` library to generate MP3 audio files for each English line from `lines.json`. During generation, the script SHALL use `edge_tts.Communicate.stream()` to capture `WordBoundary` events and record each word's text and start time offset (in seconds, converted from the 100-nanosecond unit provided by edge-tts).

Each entry SHALL produce one MP3 file saved to the `audio/` directory with a sequential naming convention (e.g., `en_01.mp3`, `en_02.mp3`).

#### Scenario: Generate all English audio files with word timing

- **WHEN** the user runs `python generate_audio.py`
- **THEN** the script SHALL generate one MP3 per entry and collect word boundary timing data for each English line

#### Scenario: Audio directory creation

- **WHEN** the `audio/` directory does not exist
- **THEN** the script SHALL create the `audio/` directory before generating files


<!-- @trace
source: playback-karaoke
updated: 2026-04-11
code:
  - index.html
  - .DS_Store
  - generate_audio.py
-->

---
### Requirement: Generate Chinese audio files

The system SHALL generate Chinese MP3 audio files for the Chinese translation of each line from `lines.json`.

Each Chinese translation SHALL produce one MP3 file saved to `audio/` with naming convention `zh_01.mp3`, `zh_02.mp3`, etc.

#### Scenario: Generate all Chinese audio files

- **WHEN** the user runs `python generate_audio.py`
- **THEN** the script SHALL generate Chinese MP3 files for all translated lines using edge-tts with a Chinese (zh-TW) voice, saved as `audio/zh_01.mp3` through `audio/zh_09.mp3`

<!-- @trace
source: english-lines-practice
updated: 2026-04-11
code:
  - generate_audio.py
  - index.html
-->