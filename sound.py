import array
import math

import pygame

SAMPLE_RATE = 44100
_cache = {}


def _generate_tone(frequency, duration, volume, wave, sweep_to=None):
    n_samples = int(SAMPLE_RATE * duration)
    buf = array.array("h")
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        freq = frequency if sweep_to is None else frequency + (sweep_to - frequency) * (i / n_samples)
        raw = math.sin(2 * math.pi * freq * t)
        if wave == "square":
            raw = 1.0 if raw >= 0 else -1.0
        fade = 1.0 - (i / n_samples)
        buf.append(int(raw * volume * fade * 32767))
    return buf.tobytes()


def _generate_melody(notes, volume, wave):
    """notes is a list of (frequency_or_chord, duration) — a chord is a
    list of frequencies summed together, for a fuller final note."""
    buf = array.array("h")
    for freqs, duration in notes:
        if isinstance(freqs, (int, float)):
            freqs = [freqs]
        n_samples = int(SAMPLE_RATE * duration)
        for i in range(n_samples):
            t = i / SAMPLE_RATE
            raw = sum(math.sin(2 * math.pi * f * t) for f in freqs) / len(freqs)
            if wave == "square":
                raw = 1.0 if raw >= 0 else -1.0
            fade = 1.0 - (i / n_samples) * 0.8
            buf.append(int(max(-1.0, min(1.0, raw)) * volume * fade * 32767))
    return buf.tobytes()


def _play(name, frequency, duration, volume, wave, sweep_to=None):
    if name not in _cache:
        try:
            _cache[name] = pygame.mixer.Sound(
                buffer=_generate_tone(frequency, duration, volume, wave, sweep_to)
            )
        except pygame.error:
            _cache[name] = None

    sound = _cache[name]
    if sound is not None:
        sound.play()


def _play_melody(name, notes, volume, wave):
    if name not in _cache:
        try:
            _cache[name] = pygame.mixer.Sound(buffer=_generate_melody(notes, volume, wave))
        except pygame.error:
            _cache[name] = None

    sound = _cache[name]
    if sound is not None:
        sound.play()


def play_jump():
    _play("jump", 600, 0.08, volume=0.25, wave="sine")


def play_hit():
    _play("hit", 150, 0.15, volume=0.3, wave="square")


def play_pickup():
    _play("pickup", 900, 0.1, volume=0.25, wave="sine")


def play_success():
    _play("success", 700, 0.3, volume=0.3, wave="sine")


def play_victory():
    """The final-win fanfare — a rising major arpeggio into a held chord,
    distinct from the small per-level completion chime."""
    notes = [
        (523.25, 0.1),  # C5
        (659.25, 0.1),  # E5
        (783.99, 0.1),  # G5
        ([1046.50, 1318.51, 1567.98], 0.45),  # C6 major chord, held
    ]
    _play_melody("victory", notes, volume=0.32, wave="sine")


def play_flip():
    _play("flip", 300, 0.25, volume=0.3, wave="sine", sweep_to=900)


def play_defeat():
    _play("defeat", 500, 0.2, volume=0.3, wave="square", sweep_to=120)


def play_boss_hit():
    _play("boss_hit", 200, 0.2, volume=0.35, wave="square", sweep_to=80)


def play_shoot():
    _play("shoot", 500, 0.07, volume=0.2, wave="square", sweep_to=1000)


def play_lose():
    _play("lose", 400, 0.6, volume=0.3, wave="sine", sweep_to=80)
