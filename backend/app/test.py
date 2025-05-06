import os
from models.deepgram_stt_tts import DeepgramAPI

class Test:
    def __init__(self, session_id, question_no):
        self.session_id = session_id
        self.question_no = question_no
        self.answer_path = os.path.abspath(
            os.path.join("backend","data", "audio", f"{session_id}_answer_{question_no}_audio.mp3")
        )
        self.transcribe()

    def transcribe(self):
        deepgram_api = DeepgramAPI(self.session_id, self.question_no)
        print("Answer path:", self.answer_path)
        self.answer_text = deepgram_api.transcribe_audio("backend/data/audio/6ff5d2d9-7f7e-4dfb-86d9-955d640e3074_answer_1.mp3")
        print(f"Transcribed answer: {self.answer_text}")
        return self.answer_text

# Run test
test1 = Test("6ff5d2d9-7f7e-4dfb-86d9-955d640e3074", 1)
