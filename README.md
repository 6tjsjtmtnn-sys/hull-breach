# Hull Breach

A 2D platformer built with Python and Pygame. You play an astronaut escaping
a derelict, failing space station — running and jumping across collapsing
corridors, dodging malfunctioning drone sentries, and surviving sections
where gravity itself reverses on you, all before your oxygen supply runs out.

This is my Boot.dev capstone project.

## What makes it different from a typical platformer

- **Low-gravity movement.** Jumps are floatier than a standard platformer,
  matching the station setting.
- **Gravity-flip mechanic.** Certain switches flip which way is "down,"
  turning the ceiling into the floor for a section of the level. It's
  scoped to a discoverable optional puzzle pocket in level 1 — you don't
  have to find it to finish the game, but it's there to explore.
- **Oxygen as both a timer and a health bar.** It drains continuously (the
  "get out before you run out of air" pressure) and drops further on
  contact with drones or hazards. Oxygen pickups scattered through the
  levels buy you more time.

## How to run it

Requires Python 3.13 and [uv](https://docs.astral.sh/uv/).

```
git clone <this-repo-url>
cd hull-breach
uv run main.py
```

`uv run` takes care of creating the virtual environment and installing
dependencies (pinned to `pygame==2.6.1`) automatically — no separate
install step needed.

## Controls

| Action                | Keys                  |
|------------------------|-----------------------|
| Move left / right       | `A` / `D` or arrow keys |
| Jump                     | `Space`, `W`, or Up arrow |
| Pause / resume           | `Esc` or `P`          |
| Flip gravity             | Walk into a blue switch tile |

## Running the tests

A small `pytest` suite covers the parts that are meaningfully testable
without a display — tile collision resolution, level-grid parsing, and the
gravity-flip ground-check logic. Rendering, camera feel, and jump tuning
were verified through manual playtesting and scripted bot walkthroughs
during development instead, since those aren't the kind of thing a unit
test can meaningfully assert on.

```
uv run pytest
```

## Project structure

```
hull-breach/
├── main.py              # entry point
├── game.py               # Game class: owns the screen/clock and the state machine
├── constants.py          # all tuning values (physics, colors, screen size, ...)
├── hud.py                 # oxygen bar rendering
├── sound.py                # procedurally-generated SFX (no audio assets needed)
├── states/                 # menu / play / pause / game-over states
├── entities/                # player, drone, particle, and the shared Entity base class
├── levels/                  # level parsing, tile collision, camera, and level data
└── tests/                    # pytest suite
```

## What I built / what I learned

The core technical challenge was the platformer physics: two-pass axis-
separated collision resolution (move X, resolve; move Y, resolve) to avoid
tunneling through corners, plus a signed `gravity_dir` that the collision,
jump, and animation code all key off of so the gravity-flip mechanic didn't
turn into duplicated code paths.

Level design turned out to be its own source of bugs, independent of the
physics code being correct. Writing a small scripted "bot" that plays
through a level headlessly (hold right, jump over walls/gaps) caught two
real level-design mistakes that would have been invisible from reading the
code: a switch placed in the normal walking path's head-space that
launched the player into an unbounded fall, and a return switch positioned
outside the footprint the player actually lands in after a jump. Both are
the kind of bug that's obvious the moment you watch it happen and easy to
miss otherwise.

## Credits

Sprites are from Kenney's "Platformer Pack Remastered" (CC0 license, no
attribution required — see `assets/ATTRIBUTION.md` for details). Sound
effects are synthesized at runtime, not sourced from any external pack.
