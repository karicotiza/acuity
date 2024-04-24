from celery import shared_task  # type: ignore
from logic.models import AudioData, StringHexdigest, Logs


@shared_task
def start_recognition(
    audio_bytes: bytes,
    audio_bytes_hexdigest: str,
    ip: str,
) -> None:
    audio_data: AudioData = AudioData(audio_bytes, audio_bytes_hexdigest)
    audio_data_text: str = audio_data.text

    if audio_data_text:
        text_hexdigest: StringHexdigest = StringHexdigest(audio_data_text)

        new_log: Logs = Logs(ip=ip, hash=text_hexdigest.value)
        new_log.save()
