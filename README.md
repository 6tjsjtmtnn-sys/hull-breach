# Hull Breach

A 2D platformer built with Python and Pygame. You play an astronaut escaping
a derelict, failing space station — running and jumping across collapsing
corridors, dodging malfunctioning drone sentries, and surviving sections
where gravity itself reverses on you, all before your oxygen supply runs out.

This is my Boot.dev capstone project.

## What makes it different from a typical platformer

- **Low-gravity movement.** Jumps are floatier than a standard platformer,
  matching the station setting.
- **Player-controlled gravity flip.** Collect a green gravity diamond to
  gain a flip charge, then press `G` any time to flip which way is "down."
  Charges carry over between levels — spend them whenever you want, and
  find more diamonds to keep the ability topped up.
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

The main menu has `[C] Controls` and `[R] Rules` screens in-game. Quick
reference:

| Action                | Keys                  |
|------------------------|-----------------------|
| Move left / right       | `A` / `D` or arrow keys |
| Jump                     | `Space`, `W`, or Up arrow |
| Pause / resume           | `Esc` or `P`          |
| Flip gravity (needs a charge) | `G`             |

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
through a level headlessly (hold right, jump over walls/gaps) caught real
level-design mistakes that would have been invisible from reading the
code alone — things like a trigger placed in the normal walking path's
head-space that launched the player into an unbounded fall, since the
level had no top boundary either. That's the kind of bug that's obvious
the moment you watch it happen and easy to miss otherwise. (The original
switch-tile version of the gravity flip that story refers to was later
replaced with the player-controlled charge system described above.)

## Credits

Sprites are from Kenney's "Platformer Pack Remastered" (CC0 license, no
attribution required — see `assets/ATTRIBUTION.md` for details). Sound
effects are synthesized at runtime, not sourced from any external pack.
