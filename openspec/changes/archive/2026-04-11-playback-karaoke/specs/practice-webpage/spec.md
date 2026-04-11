## MODIFIED Requirements

### Requirement: Play English audio per line

Each English line SHALL have a play/pause toggle button that plays or pauses the corresponding English MP3 audio file. During playback, the English text SHALL display word-by-word karaoke highlighting.

#### Scenario: User clicks English play button

- **WHEN** the user clicks the play button next to an English line
- **THEN** the browser SHALL play the corresponding `audio/en_XX.mp3` file, the button SHALL show a pause symbol, and word highlighting SHALL begin

### Requirement: Play Chinese audio per line

Each Chinese translation SHALL have a play/pause toggle button that plays or pauses the corresponding Chinese MP3 audio file.

#### Scenario: User clicks Chinese play button

- **WHEN** the user clicks the play button next to a Chinese translation
- **THEN** the browser SHALL play the corresponding `audio/zh_XX.mp3` file and the button SHALL show a pause symbol

### Requirement: Single active playback

Any new audio playback SHALL stop the currently playing (or paused) audio, regardless of whether the current and new audio are English or Chinese. At most one audio file SHALL be active (playing or paused) at any time. When a line's audio is stopped by another line, its button SHALL reset to play (▶) and any karaoke highlighting SHALL be cleared.

#### Scenario: Playing English then clicking Chinese stops English

- **WHEN** an English audio is playing and the user clicks any Chinese play button
- **THEN** the English audio SHALL stop, its button SHALL reset to play (▶), karaoke highlighting SHALL clear, and the Chinese audio SHALL start

#### Scenario: Playing Chinese then clicking different English stops Chinese

- **WHEN** a Chinese audio is playing and the user clicks any English play button
- **THEN** the Chinese audio SHALL stop, its button SHALL reset to play (▶), and the English audio SHALL start with karaoke

#### Scenario: Playing English then clicking different English

- **WHEN** an English audio is playing and the user clicks a different English play button
- **THEN** the first audio SHALL stop with highlight cleared, and the second SHALL start with fresh highlighting
