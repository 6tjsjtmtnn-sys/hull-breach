# Hull Breach

A 2D platformer built with Python and Pygame. You play an astronaut escaping
a derelict, failing space station — running and jumping across collapsing
corridors, dodging malfunctioning drone sentries, and surviving sections
where gravity itself reverses on you, all before your oxygen supply runs
out — capped off by a boss fight against the station's reactor sentinel.

This is my Boot.dev capstone project.

## Motivation

The capstone brief was open-ended — any language, any project — and I'd
already gotten a taste of game dev from an earlier Boot.dev course (a
vector-drawn Asteroids clone). I wanted this one to go further: real sprite
art instead of procedural shapes, a tile-based level format instead of one
hardcoded arena, and at least one mechanic that couldn't be bolted on as an
afterthought. Gravity-flip was that mechanic — it meant the collision,
jump, and animation code all had to key off a signed direction instead of
assuming "down" is always the floor, which touches nearly everything in the
physics layer. Python + Pygame kept the iteration loop fast enough to
actually playtest and tune that mechanic dozens of times rather than fight
a heavier engine's boilerplate.

## Features

- **Low-gravity movement.** Jumps are floatier than a standard platformer,
  matching the station setting.
- **Player-controlled gravity flip.** Collect a green gravity diamond to
  gain a flip charge, then press `G` any time to flip which way is "down."
  Charges carry over between levels. Flipping away from normal gravity
  costs a charge; flipping back to normal is always free, so you can never
  get stranded even at zero charges.
- **Oxygen as both a timer and a health bar.** It drains continuously (the
  "get out before you run out of air" pressure) and drops further on
  contact with drones, hazards, or projectiles. Oxygen pickups scattered
  through the levels buy you more time.
- **Stomp combat.** Land on a drone from above (gravity-relative — this
  still works correctly mid-flip) to defeat it and get a bounce strong
  enough to carry you up onto a nearby platform, not just a hop in place.
  Touch one from the side and it hurts you instead. Ground drones patrol
  platforms; flying drones patrol a fixed path near the ceiling and take
  potshots at you with projectiles when you're in range. Spike hazards
  show up on elevated platforms and hanging from the ceiling too, not
  just the ground — the ceiling ones mainly matter if you flip gravity
  and end up walking up there.
- **9 levels that ramp up**, then a final boss. Oxygen drains faster and
  enemy/hazard density increases each level; the 10th level drops the
  oxygen timer entirely for a 3-heart fight against the station's Reactor
  Sentinel, a scaled-up saw drone that also shoots back — stomp it 10
  times to disable it, its own health bar tracking the fight, different
  music, no clock ticking. Each stomp stuns it briefly, giving you a
  breather before it's back on your tail. A flying drone also sweeps
  across the screen every so often, taking shots of its own along the
  way. Disabling the sentinel doesn't end the fight by itself — you
  still have to reach the exit sign to actually escape. Winning or
  losing (any level) stops the music and plays a distinct win/lose
  sting. Since there's no other way to recover a lost heart during the
  fight, a bonus heart pickup appears at a random spot every so often
  (only while you're missing one) and vanishes again
  if you don't reach it in time.

## Quick Start

Requires Python 3.13 and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/6tjsjtmtnn-sys/hull-breach
cd hull-breach
uv run main.py
```

`uv run` takes care of creating the virtual environment and installing
dependencies (pinned to `pygame==2.6.1`) automatically — no separate
install step needed.

## Usage

From the main menu: `[ENTER]` to start, `[C]` for a controls reference,
`[R]` for the rules, both viewable in-game at any time. Quick reference:

| Action                | Keys                  |
|------------------------|-----------------------|
| Move left / right       | `A` / `D` or arrow keys |
| Jump                     | `Space`, `W`, or Up arrow |
| Pause / resume           | `Esc` or `P`          |
| Flip gravity (needs a charge) | `G`             |
| Flip back to normal (always free) | `G` again  |

Reach each level's exit sign to move on to the next. Watch the oxygen bar
(top left) — it drains on its own and drops further if you get hit; blue
pickups refill it. Green diamonds bank a gravity-flip charge. The 10th
level swaps the oxygen bar for three hearts and drops you into the boss
fight described above.

## Contributing

### Clone the repo

```bash
git clone https://github.com/6tjsjtmtnn-sys/hull-breach
cd hull-breach
```

### Run it

```bash
uv run main.py
```

### Run the test suite

```bash
uv run pytest
```

The `pytest` suite covers the parts that are meaningfully testable without
a display — tile collision resolution, level-grid parsing, and the
gravity-flip ground-check logic. Rendering, camera feel, and jump tuning
were verified through manual playtesting and scripted headless bot
walkthroughs during development instead, since those aren't the kind of
thing a unit test can meaningfully assert on.

### Submit a pull request

If you'd like to contribute, please fork the repository and open a pull
request against the `main` branch.

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

Playtesting after the fact caught a state-machine bug the automated bot
never would have: resuming from pause would bounce right back into the
pause screen. `Game.run()` swaps to `state.next_state` on a transition
but never cleared it — so PauseState's underlying PlayState still had its
old "go to PauseState" transition sitting on it from when it was first
paused, and the very next frame reused that stale value and hopped
straight back. Fixed by clearing `next_state` on the outgoing state right
after consuming it. A good reminder that state reused across transitions
(rather than freshly constructed each time) needs its leftover fields
reset explicitly, and that some bugs only show up when a human plays
naturally back and forth rather than a bot that always moves in one
direction.

## Credits

Sprites are from Kenney's "Platformer Pack Remastered" and music (a
separate intro/gameplay/boss track for each context) is from Kenney's
"Music Loops" (both CC0, no attribution required — see
`assets/ATTRIBUTION.md` for details). Sound effects are synthesized at
runtime, not sourced from any external pack.
