import speech_recognition as sr
import pygame
import logging
import pydub
from io import BytesIO
from pydub import AudioSegment
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@lru_cache(maxsize=None)
def get_recognizer():
    """
    Return a cached speech recognizer instance
    """
    return sr.Recognizer()

def record_audio(file_path, timeout=None, phrase_time_limit=30, retries=3, energy_threshold=1700, 
                 pause_threshold=2, phrase_threshold=0.15, dynamic_energy_threshold=True, 
                 calibration_duration=2):
    """
    Record audio from the microphone and save it as an MP3 file.
    """
    recognizer = get_recognizer()
    recognizer.energy_threshold = energy_threshold
    recognizer.pause_threshold = pause_threshold
    recognizer.phrase_threshold = phrase_threshold
    recognizer.dynamic_energy_threshold = dynamic_energy_threshold
    
    for attempt in range(retries):
        try:
            with sr.Microphone() as source:
                logging.info("Calibrating for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=calibration_duration)
                logging.info("Recording started")
                audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                logging.info("Recording complete")

                # Convert the recorded audio data to an MP3 file
                wav_data = audio_data.get_wav_data()
                audio_segment = pydub.AudioSegment.from_wav(BytesIO(wav_data))
                audio_segment.export(file_path, format="mp3", bitrate="128k", parameters=["-ar", "22050", "-ac", "1"])
                return
        except sr.WaitTimeoutError:
            logging.warning(f"Listening timed out, retrying... ({attempt + 1}/{retries})")
        except Exception as e:
            logging.error(f"Failed to record audio: {e}")
            if attempt == retries - 1:
                raise
        
    logging.error("Recording failed after all retries")

def play_audio(file_path):
    """
    Play an audio file using pygame.
    """
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
    except pygame.error as e:
        logging.error(f"Failed to play audio: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while playing audio: {e}")
    finally:
        pygame.mixer.quit()
