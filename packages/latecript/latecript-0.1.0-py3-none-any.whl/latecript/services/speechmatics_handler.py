import os
import speechmatics


if os.getenv("SSL_CERT_FILE") is None:
    os.environ["SSL_CERT_FILE"] = "certificate.pem"

SPEECHMATICS_CONNECTION_URL = "wss://eu2.rt.speechmatics.com/v2/"
CHUNK_SIZE = 1024


def get_speechmatics_client(
    speechmatics_api_key: str, transcript_language: str
) -> speechmatics.client.WebsocketClient:
    connection_parameters = speechmatics.models.ConnectionSettings(
        url=f"{SPEECHMATICS_CONNECTION_URL}{transcript_language}",
        auth_token=speechmatics_api_key,
    )
    speechmatics_websocket = speechmatics.client.WebsocketClient(connection_parameters)
    return speechmatics_websocket


def get_transcription_config(
    transcript_language: str, translation_language: str | None, max_delay: float = 3
) -> speechmatics.models.TranscriptionConfig:
    return speechmatics.models.TranscriptionConfig(
        language=transcript_language,
        max_delay=max_delay,
        diarization="speaker",
        translation_config=speechmatics.models.TranslationConfig(
            target_languages=[translation_language]
        )
        if translation_language is not None
        else None,
    )


def get_audio_config(
    sample_rate: int,
    chunk_size: int = CHUNK_SIZE,
    encoding: str = "pcm_f32le",
):
    settings = speechmatics.models.AudioSettings()
    settings.encoding = encoding
    settings.sample_rate = sample_rate
    settings.chunk_size = chunk_size

    return settings
