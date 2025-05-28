import os
from models.deepgram_stt_tts import DeepgramAPI
from models.groq_api_llm import GroqApi
from utils.prompt import PromptGenerator
import json
# from database.crud import viva_answer_crud 
# from database.schemas.viva_answer_schema import VivaAnswerBase
from database.connection import SessionLocal



class EvaluationManager:
    def __init__(self, session_id, question_no, question_text):
        self.session_id = session_id
        self.question_no = question_no
        self.question_text = question_text
        self.answer_path = f"data/audio/{session_id}_answer_{question_no}.mp3"
        # "data/audio/6ff5d2d9-7f7e-4dfb-86d9-955d640e3074_answer_1.mp3"
        self.answer_text = None
        self.score = None
        self.feedback = None
        self.student_id = None
        
    def transcribe(self):
        deepgram_api = DeepgramAPI(self.session_id, self.question_no)
        print("self.answer_path", self.answer_path)
        self.answer_text = deepgram_api.transcribe_audio(self.answer_path)
        print(f"Transcribed answer: {self.answer_text}")
        return self.answer_text
    
    def prompt_evaluation(self): 
        self.prompt_generator = PromptGenerator()
        self.evaluate_prompt = self.prompt_generator.generate_feedback_prompt(self.question_text, self.answer_text)
        
    # def evaluate_answer(self):
    #     groq_api = GroqApi()
    #     response = groq_api.api_calls(self.evaluate_prompt)
    #     print(f"Response from Groq API: {response}")
    #     if type(response) != list:
    #         self.score, self.feedback = 6, "Greate understanding of the topic. Good job!"
    #     else:
    #         self.score, self.feedback = int(response[0]), response[1]
    #     print(f"Score: {self.score}, Feedback: {self.feedback}")
    #     return self.score, self.feedback
    
    def evaluate_answer(self):
        groq_api = GroqApi()
        response = groq_api.api_calls(self.evaluate_prompt)
        print(f"Response from Groq API: {response}")
        if isinstance(response, str) and ";" in response:
            try:
                parts = response.split(";", 1)
                self.score = int(parts[0].strip())
                self.feedback = parts[1].strip().strip('"')
            except ValueError:
                print(f"Warning: Could not parse score from response: {response}. Setting default score and feedback.")
                self.score, self.feedback = 0, "Could not parse feedback."
        elif type(response) != list:
            self.score, self.feedback = 6, "Great understanding of the topic. Good job!"
        else:
            try:
                self.score, self.feedback = int(response[0]), response[1]
            except (IndexError, ValueError):
                print(f"Warning: Unexpected list format in response: {response}. Setting default score and feedback.")
                self.score, self.feedback = 0, "Could not parse score and feedback from list."
        print(f"Score: {self.score}, Feedback: {self.feedback}")
        return self.score, self.feedback
    
    
    def get_student_id(self): 
        session_json_path = os.path.join("data", "sessions", f"{self.session_id}.json")    
        if os.path.exists(session_json_path):
            with open(session_json_path, 'r') as f:
                session_data = json.load(f)
                student_id = session_data.get("student_id")
                if student_id:
                    self.student_id = student_id
                    return student_id
                else:
                    raise ValueError(f"Student ID not found in session data for session {self.session_id}")
    
    # def save_everything(self):
    #     db = SessionLocal()
    #     try:
    #         viva_data = VivaAnswerSchema(
    #             student_id=self.student_id,
    #             session_id=self.session_id,
    #             question_no=str(self.question_no),
    #             question_text=self.question_text,
    #             answer_text=self.answer_text,
    #             score=self.score,
    #             feedback=self.feedback
    #         )

    #         db_viva_answer = viva_answer_crud.add_viva_answer(db, viva_data)
    #         return db_viva_answer
    #     finally:
    #         db.close()


    def save_everything_to_json(self):
        viva_data = {
            "student_id": self.student_id,
            "question_no": str(self.question_no),
            "question_text": self.question_text,
            "answer_text": self.answer_text,
            "score": self.score,
            "feedback": self.feedback
        }

        os.makedirs(os.path.join("data", "answers"), exist_ok=True)
        json_path = os.path.join("data", "answers", f"{self.session_id}_full.json")

        try:
            with open(json_path, 'r') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = {"student_id": self.student_id, "session_id": self.session_id, "answers": []}

        existing_data["answers"].append(viva_data)

        with open(json_path, 'w') as f:
            json.dump(existing_data, f, indent=4)

        print(f"Saved evaluation data to {json_path}")
        return json_path   

    def run(self):
        self.get_student_id()
        self.transcribe()
        self.prompt_evaluation()  
        self.evaluate_answer()
        self.save_everything_to_json()
         
        

if __name__ == "__main__":
    evaluation_manager = EvaluationManager("2e6c3b98-0732-454a-be80-1df3084ae2a0", "1", "What is your name?")
    evaluation_manager.transcribe()