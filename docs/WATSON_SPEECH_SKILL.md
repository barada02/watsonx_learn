# Watson Speech (STT/TTS) quick start

This note captures the working setup for IBM Watson Speech to Text (STT) and Text to Speech (TTS) in this repo.

## Prereqs

- Python venv active (bobenv)
- Package installed: ibm-watson >= 7.0.0

## Environment variables (.env)

Set these in the repo .env file:

- STT_APIKEY
- STT_URL
- TTS_APIKEY
- TTS_URL

## Files

- speech_examples/stt_demo.py
- speech_examples/tts_demo.py

## Run STT demo

Place an audio file named audio-file.wav in one of these locations:

- repo root (watsonx_learn/audio-file.wav)
- speech_examples/audio-file.wav

Then run:

python speech_examples/stt_demo.py

## Run TTS demo

python speech_examples/tts_demo.py

## Outputs

- STT: prints JSON transcription to stdout
- TTS: writes hello_world.wav to repo root

## Notes

- If you change the audio file extension, update it in stt_demo.py or add a new mapping in get_content_type.
- Make sure the service URL matches the region of your IBM Cloud instance.
