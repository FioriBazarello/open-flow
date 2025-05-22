import whisper

_MODEL_CACHE: dict[str, whisper.Whisper] = {}


class SpeechToText:
    def __init__(self, model_name: str = "medium"):
        if model_name not in _MODEL_CACHE:
            _MODEL_CACHE[model_name] = whisper.load_model(model_name)
        self.model = _MODEL_CACHE[model_name]

    def transcribe(self, audio_path: str, language: str = "pt", **kwargs) -> str:
        """
        Return the recognised text for the given audio file.
        Raises:
            RuntimeError: if the underlying Whisper call fails.
        """
        try:
            result = self.model.transcribe(audio_path, language=language, **kwargs)
            return result["text"]
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"Transcription failed for {audio_path!r}") from exc