import os
from models.deepgram_stt_tts import DeepgramAPI
from models.groq_api_llm import GroqApi
from utils.prompt import PromptGenerator



class EvaluationManager:
    def __init__(self, session_id, question_no, question_text):
        self.session_id = session_id
        self.question_no = question_no
        self.question_text = question_text
        self.answer_path = f"data/audio/{session_id}_answer_{question_no}_audio.mp3"
        
    def transcribe(self):
        deepgram_api = DeepgramAPI(self.session_id, self.question_no)
        answer_text = deepgram_api.transcribe_audio(self.answer_path)
        print(f"Transcribed answer: {answer_text}")
        return answer_text
    
    def prompt_evaluation(self): 
        self.prompt_generator = PromptGenerator(self.filtered_qb, self.question_no)
    
    def evaluate_answer(self, answer_text):
        groq_api = GroqApi()
        
        score, feedback = groq_api.evaluate_answer(question_text, answer_text)
        print(f"Score: {score}, Feedback: {feedback}")
        return score, feedback
    
    
    def save_everything(self,session_id, question_no, question_text, answer_text, score, feedback):
        # Save the session_id, question text, answer text, question index, score, feedback
        # This could be a database operation or saving to a file
        
        
        print(f"Saving evaluation data for session {session_id}:")
        print(f"- Question No: {question_no}")
        print(f"- Question Text: {question_text}")
        print(f"- Answer Text: {answer_text}")
        print(f"- Score: {score}")
        print(f"- Feedback: {feedback}")
if __name__ == "__main__":
    evaluation_manager = EvaluationManager("2e6c3b98-0732-454a-be80-1df3084ae2a0", "1", "What is your name?")
    evaluation_manager.transcribe()