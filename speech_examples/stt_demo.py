import json
import os
from pathlib import Path

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import SpeechToTextV1


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        if key and key not in os.environ:
            os.environ[key] = value


def get_content_type(audio_path: Path) -> str:
    ext = audio_path.suffix.lower()
    mapping = {
        ".wav": "audio/wav",
        ".flac": "audio/flac",
        ".mp3": "audio/mp3",
        ".ogg": "audio/ogg",
    }
    return mapping.get(ext, "audio/wav")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    load_env_file(repo_root / ".env")

    stt_apikey = os.environ.get("STT_APIKEY")
    stt_url = os.environ.get("STT_URL")
    if not stt_apikey or not stt_url:
        raise SystemExit("Missing STT_APIKEY or STT_URL in environment or .env")

    audio_path = repo_root / "audio-file.wav"
    if not audio_path.exists():
        audio_path = Path(__file__).resolve().parent / "audio-file.wav"
    if not audio_path.exists():
        raise SystemExit(f"Audio file not found: {audio_path}")

    authenticator = IAMAuthenticator(stt_apikey)
    stt = SpeechToTextV1(authenticator=authenticator)
    stt.set_service_url(stt_url)

    content_type = get_content_type(audio_path)
    with audio_path.open("rb") as audio_file:
        result = stt.recognize(
            audio=audio_file,
            content_type=content_type,
            model="en-US_BroadbandModel",
        ).get_result()

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
