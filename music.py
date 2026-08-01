from pathlib import Path

import pygame

MUSIC_DIR = Path(__file__).resolve().parent / "assets" / "music"
GAMEPLAY_TRACK = MUSIC_DIR / "gameplay.ogg"
BOSS_TRACK = MUSIC_DIR / "boss.ogg"

VOLUME = 0.4

_current_track = None


def _play(track_path):
    global _current_track
    if _current_track == track_path:
        return
    try:
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.set_volume(VOLUME)
        pygame.mixer.music.play(loops=-1)
        _current_track = track_path
    except pygame.error:
        pass


def play_gameplay():
    _play(GAMEPLAY_TRACK)


def play_boss():
    _play(BOSS_TRACK)


def stop():
    global _current_track
    try:
        pygame.mixer.music.stop()
    except pygame.error:
        pass
    _current_track = None


def pause():
    try:
        pygame.mixer.music.pause()
    except pygame.error:
        pass


def unpause():
    try:
        pygame.mixer.music.unpause()
    except pygame.error:
        pass
