from dataclasses import dataclass


@dataclass
class Album:
    name: str
    artist: str | None
    track: str
