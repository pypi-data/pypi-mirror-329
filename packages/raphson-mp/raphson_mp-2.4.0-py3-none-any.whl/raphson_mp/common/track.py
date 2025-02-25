from enum import Enum

TrackDict = dict[str, str | int | bool | list[str] | None]


class AudioFormat(Enum):
    """
    Opus audio in WebM container, for music player streaming.
    """

    WEBM_OPUS_HIGH = "webm_opus_high"

    """
    Opus audio in WebM container, for music player streaming with lower data
    usage.
    """
    WEBM_OPUS_LOW = "webm_opus_low"

    """
    MP3 files with metadata (including cover art), for use with external
    music player applications and devices Uses the MP3 format for broadest
    compatibility.
    """
    MP3_WITH_METADATA = "mp3_with_metadata"

    @property
    def content_type(self):
        if self is AudioFormat.WEBM_OPUS_HIGH:
            return "audio/webm"
        elif self is AudioFormat.WEBM_OPUS_LOW:
            return "audio/webm"
        elif self is AudioFormat.MP3_WITH_METADATA:
            return "audio/mp3"
        else:
            raise ValueError

    @property
    def legacy_id(self) -> int:
        if self is AudioFormat.WEBM_OPUS_HIGH:
            return 0
        elif self is AudioFormat.WEBM_OPUS_LOW:
            return 1
        elif self is AudioFormat.MP3_WITH_METADATA:
            return 3
        else:
            return 0
