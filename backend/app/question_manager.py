import os
from utils.filter_qb import FilterQuestionBank
from utils.prompt import PromptGenerator
from models.deepgram_stt_tts import DeepgramAPI
from models.groq_api_llm import GroqApi
from database.connection import SessionLocal
from database.crud import viva_answer_crud
import json

class QuestionManager:
    def __init__(self, session_id, question_no):
        self.question_no = question_no
        self.session_id = session_id
        self.question_text = None
        self.question_audio_path = f"data/audio/{session_id}_question_{question_no}_audio.mp3"
        self.create_audio_directory()
        self.prompt_generator = PromptGenerator()
        self.groq_api = GroqApi()
        self.filtered_qb = self._load_filtered_qb()
        self.question_prompt = None
        self.rephrased_question_text = None
        self.question_text_prev = None
        self.answer_text = None
        self.feedback = None
        self.hint = None

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

    # def load_previous_answer_feedback(self):
    #     db = SessionLocal()
    #     try:
    #         prev_qno = self.question_no - 1
    #         result = viva_answer_crud.get_score_feedback_by_question(db, self.session_id, prev_qno)
    #         if result:
    #             self.question_text_prev = result["question_text"]
    #             self.answer_text = result["answer_text"]  # Ensure it's added in your fetch function
    #             self.feedback = result["feedback"]
    #         else:
    #             print("Previous answer data not found.")
    #     finally:
    #         db.close()

    def load_previous_answer_feedback(self):
        """
        Fetches the latest previous question and answer details from the session's JSON file.

        Returns:
            dict: A dictionary containing the question text, answer text and feedback of the latest previous question,
                or None if no previous question is found.
                The dictionary will have keys 'question_text_prev', 'answer_text', and 'feedback'.
        """
        json_path = os.path.join("data", "answers", f"{self.session_id}_full.json")

        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"File not found: {json_path}")
            return None

        if "answers" in data and data["answers"]:
            latest_answer = data["answers"][-1]
            self.question_text_prev = latest_answer.get("question_text")
            self.answer_text = latest_answer.get("answer_text")
            self.feedback = latest_answer.get("feedback")
            
        else:
            print(f"No previous answers found in {json_path}")
            return None
    
    def question_prompt_fetch(self):
        if self.question_no == 1:
            self.question_prompt = self.prompt_generator.generate_first_question_prompt(self.filtered_qb)
        else:
            self.load_previous_answer_feedback()
            prev_questions =  self.get_prev_question_json()
            self.question_prompt = self.prompt_generator.generate_subsequent_question_prompt(
                self.filtered_qb, self.question_text_prev, self.answer_text, self.feedback, prev_questions
            )
            print(self.question_prompt)

    def question_text_fetch(self):
        self.question_text = self.groq_api.api_calls(self.question_prompt)
        print(f"Generated Question Text: {self.question_text}")

    def get_prev_question_json(self): 
        file_path = f"data/questions/{self.session_id}.json"

        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No question file found for session ID: {self.session_id}")

        # Read and parse the file
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                questions_data = json.load(file)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON in file: {file_path}")

        # Extract question_texts
        question_texts = [item["question_text"] for item in questions_data if "question_text" in item]

        return question_texts
    
    def question_audio(self):
        print("Generating audio...")
        deepgram_api = DeepgramAPI(self.session_id, self.question_no)
        deepgram_api.text_to_speech(self.question_text)

    def run(self):
        self.question_prompt_fetch()
        self.question_text_fetch()
        self.question_audio()
        print("Audio generated successfully.")
        self.save_question_to_json()
        return self.question_text, self.question_audio_path

    def save_question_to_json(self):
        # Ensure the "data/questions" directory exists
        questions_dir = os.path.join("data", "questions")
        os.makedirs(questions_dir, exist_ok=True)

        # Construct the path to the session-specific JSON file (without question number)
        file_path = os.path.join(questions_dir, f"{self.session_id}.json")

        # Prepare the new question entry
        question_entry = {
            "question_no": self.question_no,
            "question_text": self.question_text
        }

        # Load existing data if the file exists
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []

        # Append the new question
        data.append(question_entry)

        # Save updated data back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def get_question_from_json(self):
        # Construct the file path
        file_path = os.path.join("data", "questions", f"{self.session_id}.json")

        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No question file found for session ID: {self.session_id}")

        # Load the questions from the file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Search for the question with the matching question_no
        for question in data:
            if question.get("question_no") == self.question_no:
                return question.get("question_text")

        # If the question is not found
        raise ValueError(f"Question number {self.question_no} not found in session {self.session_id}")


    # Intent handling Code: 
    def handle_intent_rephrase(self):
        question_ = self.get_question_from_json()
        prompt = self.prompt_generator.generate_rephrase_question_prompt(question_)
        self.rephrased_question_text = self.groq_api.api_calls(prompt)
        return self.rephrased_question_text
    
    
    def handle_intent_hint(self): 
        question_ = self.get_question_from_json()
        prompt = self.prompt_generator.generate_hint_for_question(question_)
        self.hint = self.groq_api.api_calls(prompt)
        return self.hint 

    def handle_intent_context(self, session_id): 
        question_ = self.get_question_from_json()
        prompt = self.prompt_generator.generate_topic_context_for_question(question_, session_id)
        self.context = self.groq_api.api_calls(prompt)
        return self.context

if __name__ == "__main__":
    question_manager = QuestionManager("9b71e9c3-4e6b-4253-9f88-4752cfeca143", 2)
    question_manager.run()
