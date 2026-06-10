"""Hardware abstraction protocols for start signal and audio playback."""

from typing import Protocol


class StartSignal(Protocol):
    def on(self) -> None: ...
    def off(self) -> None: ...


class AudioPlayer(Protocol):
    def play(self, sound_name: str) -> None: ...
