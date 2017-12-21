from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def transcribe_audio(audio_bytes, framerate, language, context):
    client = speech.SpeechClient()
    config = types.RecognitionConfig(
                        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                        sample_rate_hertz=framerate,
                        profanity_filter=True,
                        speech_contexts=[speech.types.SpeechContext(phrases=context)],
                        language_code=language)

    audio = types.RecognitionAudio(content=audio_bytes)
    response = client.recognize(config, audio)
    string = []
    # Convert the data into a string
    for result in response.results:
        string.append(result.alternatives[0].transcript.encode("utf-8"))
    return "\n".join(string)
