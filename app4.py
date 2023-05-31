import os
import azure.cognitiveservices.speech as speechsdk
import requests
from flask import Flask, request

app = Flask(__name__)

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# The language of the voice that speaks.
speech_config.speech_synthesis_voice_name = 'en-US-JennyNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

@app.route('/synthesize', methods=['POST'])
def synthesize_text():
    text = request.json.get('text')

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return "Speech synthesized for text [{}]".format(text)
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        error_message = "Speech synthesis canceled: {}".format(cancellation_details.reason)
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                error_message += "\nError details: {}".format(cancellation_details.error_details)
        return error_message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
