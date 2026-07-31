import array
import math

import pygame

SAMPLE_RATE = 44100
_cache = {}


def _generate_tone(frequency, duration, volume, wave):
    n_samples = int(SAMPLE_RATE * duration)
    buf = array.array("h")
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        raw = math.sin(2 * math.pi * frequency * t)
        if wave == "square":
            raw = 1.0 if raw >= 0 else -1.0
        fade = 1.0 - (i / n_samples)
        buf.append(int(raw * volume * fade * 32767))
    return buf.tobytes()


def _play(name, frequency, duration, volume, wave):
    if name not in _cache:
        try:
            _cache[name] = pygame.mixer.Sound(buffer=_generate_tone(frequency, duration, volume, wave))
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
