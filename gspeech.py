from google.cloud import speech

def transcribe_audio(audio_bytes, framerate, language, context):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
                        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                        sample_rate_hertz=framerate,
                        profanity_filter=True,
                        speech_contexts=[speech.SpeechContext(phrases=context)],
                        language_code=language)

    audio = speech.RecognitionAudio(content=audio_bytes)
    response = client.recognize(config=config, audio=audio)
    string = []
    # Convert the data into a string
    for result in response.results:
        string.append(result.alternatives[0].transcript)
    return "\n".join(string)
