import json
import logging
from colorama import Fore
from deepgram import DeepgramClient, PrerecordedOptions, SpeakOptions
from dotenv import load_dotenv
import os
class DeepgramAPI:
    """
    A class to handle interactions with the Deepgram API for speech-to-text (STT) and text-to-speech (TTS) functionalities.

    Attributes:
        api_key (str): The API key for accessing Deepgram services.
        transcription_model (str): The model to use for transcription (default: 'nova-2').
        tts_model (str): The model to use for TTS (default: 'aura-arcas-en').
    """

    def __init__(self, session_id, question_no):

        """
        Initialize the DeepgramAPI instance with API key and model configurations.

        Args:
            api_key (str): The API key for accessing Deepgram services.
            transcription_model (str): The model to use for transcription (default: 'nova-2').
            tts_model (str): The model to use for TTS (default: 'aura-arcas-en').
        """
        self.session_id = session_id
        self.question_no = question_no
        self.audio_path = f"data/audio/{session_id}_question_{question_no}_audio.mp3"
        load_dotenv()
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        self.transcription_model = "nova-2"
        self.tts_model = "aura-asteria-en"
        self.deepgram_client = DeepgramClient(self.api_key)

    def transcribe_audio(self, audio_file_path):
        """
        Transcribe an audio file to text using Deepgram's Speech-to-Text API.

        Args:
            audio_file_path (str): The path to the audio file to transcribe.

        Returns:
            str: The transcribed text.
        """
        try:
            with open(audio_file_path, "rb") as file:
                buffer_data = file.read()

            payload = {"buffer": buffer_data}
            options = PrerecordedOptions(model=self.transcription_model, smart_format=True)
            response = self.deepgram_client.listen.prerecorded.v("1").transcribe_file(payload, options)
            data = json.loads(response.to_json())

            transcript = data['results']['channels'][0]['alternatives'][0]['transcript']
            return transcript
        except Exception as e:
            # logging.error(f"{Fore.RED}Deepgram transcription error: {e}{Fore.RESET}")
            raise Exception("Error in transcribing audio")

    def text_to_speech(self, text):
        """
        Convert text to speech and save the output audio file using Deepgram's Text-to-Speech API.

        Args:
            text (str): The text to convert to speech.
            self.audio_path (str): The path to save the generated speech audio file.

        Returns:
            None
        """
        try:
            options = SpeakOptions(
                model=self.tts_model,
                encoding="linear16",
                container="wav"
            )

            self.deepgram_client.speak.v("1").save(
                self.audio_path,
                {"text": text},
                options
            )
            print(f"Speech successfully saved to {self.audio_path}")
        except Exception as e:
            raise Exception("Error in text-to-speech conversion")
