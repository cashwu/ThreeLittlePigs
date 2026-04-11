## ADDED Requirements

### Requirement: Play/pause toggle button

Each play button SHALL act as a toggle between play and pause states. When audio is stopped, the button SHALL display a play symbol (▶). When audio is playing, the button SHALL display a pause symbol (⏸). Clicking the button while playing SHALL pause the audio. Clicking again SHALL resume from where it was paused.

#### Scenario: User clicks play then pause

- **WHEN** the user clicks a play button (▶) on a line
- **THEN** the audio SHALL start playing and the button SHALL change to pause (⏸)

#### Scenario: User clicks pause then resume

- **WHEN** the user clicks the pause button (⏸) on a currently playing line
- **THEN** the audio SHALL pause at its current position and the button SHALL change back to play (▶)

#### Scenario: User clicks resume after pause

- **WHEN** the user clicks the play button (▶) on a paused line
- **THEN** the audio SHALL resume from the paused position

#### Scenario: User clicks a different line while one is playing

- **WHEN** audio is playing on line A and the user clicks play on line B
- **THEN** line A's audio SHALL stop and its button SHALL reset to play (▶), and line B's audio SHALL start with its button showing pause (⏸)

#### Scenario: User clicks a different line while one is paused

- **WHEN** audio is paused on line A and the user clicks play on line B
- **THEN** line A's audio SHALL stop and its button SHALL reset to play (▶), and line B's audio SHALL start with its button showing pause (⏸)
