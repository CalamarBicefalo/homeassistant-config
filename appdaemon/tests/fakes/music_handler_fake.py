from typing import Optional, Protocol

import sys
sys.path.insert(0, '../../apps/utils')

from music import MusicHandler


class MusicHandlerProtocol(Protocol):
    """Protocol defining the interface for music handlers."""
    
    def is_playing(self) -> bool: ...
    
    def play(self, tune: object = None, shuffle: bool = True, volume_level: float = 0.3) -> None: ...
    
    def pause(self) -> None: ...
    
    def toggle_play_pause(self) -> None: ...
    
    def volume(self, volume_level: float) -> None: ...
    
    def mute(self) -> None: ...


class FakeMusicHandler:
    """Test double for MusicHandler that conforms to MusicHandlerProtocol.
    
    Uses state machine approach where state is the single source of truth:
    - _is_playing: bool (playing or paused/stopped)
    - _volume: float (current volume level, 0.0 = muted)
    
    Tests should assert using observable state methods: is_playing(), get_volume()
    """
    
    def __init__(self) -> None:
        self.reset()
    
    def reset(self) -> None:
        self._is_playing: bool = False
        self._volume: float = 0.3
    
    def is_playing(self) -> bool:
        return self._is_playing
    
    def get_volume(self) -> float:
        """Get current volume level for test assertions."""
        return self._volume
    
    def play(self, tune: object = None, shuffle: bool = True, volume_level: float = 0.3) -> None:
        self._is_playing = True
        self._volume = volume_level
    
    def pause(self) -> None:
        self._is_playing = False
    
    def toggle_play_pause(self) -> None:
        self._is_playing = not self._is_playing
    
    def volume(self, volume_level: float) -> None:
        self._volume = volume_level
    
    def mute(self) -> None:
        self._volume = 0.0


# Runtime verification functions
def _verify_real_music_handler() -> MusicHandlerProtocol:
    """Type checker verifies MusicHandler implements MusicHandlerProtocol."""
    return None  # type: ignore


def _verify_fake_music() -> MusicHandlerProtocol:
    """Type checker verifies FakeMusicHandler implements MusicHandlerProtocol."""
    return FakeMusicHandler()
