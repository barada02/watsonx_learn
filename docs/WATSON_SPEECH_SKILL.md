# Watson Speech (STT/TTS) quick start

Portable quick start for IBM Watson Speech to Text (STT) and Text to Speech (TTS).

## Prereqs

- Python 3.9+ recommended
- Package installed: ibm-watson >= 7.0.0

## Environment variables

Set these in your environment (or in a .env file your app loads):

- STT_APIKEY
- STT_URL
- TTS_APIKEY
- TTS_URL

## Run STT demo

Use your own script to call STT. At minimum you need:

- IAM API key and service URL for Speech to Text
- An audio file in a supported format (wav, flac, mp3, ogg)
- Correct Content-Type matching the file format

Example (Python, file transcription):

```python
import json
import os
from pathlib import Path

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import SpeechToTextV1

audio_path = Path("audio-file.wav")

authenticator = IAMAuthenticator(os.environ["STT_APIKEY"])
stt = SpeechToTextV1(authenticator=authenticator)
stt.set_service_url(os.environ["STT_URL"])

with audio_path.open("rb") as audio_file:
	result = stt.recognize(
		audio=audio_file,
		content_type="audio/wav",
		model="en-US_BroadbandModel",
	).get_result()

print(json.dumps(result, indent=2))
```

## Run TTS demo

Use your own script to call TTS. At minimum you need:

- IAM API key and service URL for Text to Speech
- A text string to synthesize
- An output audio format (for example audio/wav)

Example (Python, synthesize to WAV):

```python
import os
from pathlib import Path

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import TextToSpeechV1

output_path = Path("hello_world.wav")

authenticator = IAMAuthenticator(os.environ["TTS_APIKEY"])
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(os.environ["TTS_URL"])

audio = tts.synthesize(
	"Hello, this is Watson Text to Speech.",
	voice="en-US_AllisonV3Voice",
	accept="audio/wav",
).get_result().content

output_path.write_bytes(audio)
```

## Outputs

- STT: JSON transcription response
- TTS: audio bytes saved to a file you choose

## Notes

- Ensure the service URL matches the region of your IBM Cloud instance.
- Use the correct audio content type for STT requests.
- TTS default voice is `en-US_MichaelV3Voice` if you do not specify one.
