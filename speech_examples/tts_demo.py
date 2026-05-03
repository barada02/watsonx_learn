import os
from pathlib import Path

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import TextToSpeechV1


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


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    load_env_file(repo_root / ".env")

    tts_apikey = os.environ.get("TTS_APIKEY")
    tts_url = os.environ.get("TTS_URL")
    if not tts_apikey or not tts_url:
        raise SystemExit("Missing TTS_APIKEY or TTS_URL in environment or .env")

    text = "Hello, this is Watson Text to Speech. how are you doing ? all good ?"
    voice = "en-US_AllisonV3Voice"
    accept = "audio/wav"
    output_path = repo_root / "hello_world.wav"

    authenticator = IAMAuthenticator(tts_apikey)
    tts = TextToSpeechV1(authenticator=authenticator)
    tts.set_service_url(tts_url)

    audio = tts.synthesize(
        text,
        voice=voice,
        accept=accept,
    ).get_result().content

    output_path.write_bytes(audio)
    print(f"Wrote audio to {output_path}")


if __name__ == "__main__":
    main()
