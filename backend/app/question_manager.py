import os
from utils.filter_qb import FilterQuestionBank
from utils.prompt import PromptGenerator
from models.deepgram_stt_tts import DeepgramAPI
from models.groq_api_llm import GroqApi
from database.connection import SessionLocal
from database.crud import viva_answer_crud

class QuestionManager:
    def __init__(self, session_id, question_no):
        self.question_no = question_no
        self.session_id = session_id
        self.question_text = None
        self.question_audio_path = f"data/audio/{session_id}_question_{question_no}_audio.mp3"
        self.create_audio_directory()

        self.filtered_qb = self._load_filtered_qb()
        self.question_prompt = None
        self.question_text_prev = None
        self.answer_text = None
        self.feedback = None

    def create_audio_directory(self):
        audio_dir = os.path.dirname(self.question_audio_path)
        if not os.path.exists(audio_dir):
            print(f"Audio directory '{audio_dir}' does not exist. Creating it.")
            os.makedirs(audio_dir)
        else:
            print(f"Audio directory '{audio_dir}' already exists.")

    def _load_filtered_qb(self):
        qb_filter = FilterQuestionBank(self.session_id)
        return qb_filter.run()

    def load_previous_answer_feedback(self):
        db = SessionLocal()
        try:
            prev_qno = self.question_no - 1
            result = viva_answer_crud.get_score_feedback_by_question(db, self.session_id, prev_qno)
            if result:
                self.question_text_prev = result["question_text"]
                self.answer_text = result["answer_text"]  # Ensure it's added in your fetch function
                self.feedback = result["feedback"]
            else:
                print("Previous answer data not found.")
        finally:
            db.close()

    def question_prompt_fetch(self):
        self.prompt_generator = PromptGenerator()
        if self.question_no == 1:
            self.question_prompt = self.prompt_generator.generate_first_question_prompt(self.filtered_qb)
        else:
            self.load_previous_answer_feedback()
            self.question_prompt = self.prompt_generator.generate_subsequent_question_prompt(
                self.filtered_qb, self.question_text_prev, self.answer_text, self.feedback
            )

    def question_text_fetch(self):
        groq_api = GroqApi()
        self.question_text = groq_api.api_calls(self.question_prompt)
        print(f"Generated Question Text: {self.question_text}")

    def question_audio(self):
        print("Generating audio...")
        deepgram_api = DeepgramAPI(self.session_id, self.question_no)
        deepgram_api.text_to_speech(self.question_text)

    def run(self):
        self.question_prompt_fetch()
        self.question_text_fetch()
        self.question_audio()
        print("Audio generated successfully.")
        return self.question_text, self.question_audio_path

if __name__ == "__main__":
    question_manager = QuestionManager("9b71e9c3-4e6b-4253-9f88-4752cfeca143", 2)
    question_manager.run()
