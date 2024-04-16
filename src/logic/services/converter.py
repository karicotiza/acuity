from io import BytesIO
from pydub import AudioSegment  # type: ignore


class Convertor:

    def __init__(
        self,
        format: str = 'mp3',
        bitrate: str = '48k',
        mono: bool = True,
    ) -> None:
        self.__format: str = format
        self.__bitrate: str = bitrate
        self.__mono: bool = mono

    def convert(
        self,
        data: BytesIO
    ) -> BytesIO:
        processed_audio: AudioSegment = AudioSegment.from_file(data)

        memory = BytesIO()

        if self.__mono:
            processed_audio = processed_audio.set_channels(1)

        processed_audio.export(
            memory, format=self.__format, bitrate=self.__bitrate
        )

        memory.seek(0)

        return memory
