import os
from utils.filter_qb import FilterQuestionBank
from utils.prompt import PromptGenerator
from models.deepgram_stt_tts import DeepgramAPI
from models.groq_api_llm import GroqApi

# fetch_filtered_qb, prompt_generator, question_text, question_audio
class QuestionManager:
    def __init__(self, session_id, question_no):
        self.question_no = question_no
        self.session_id = session_id
        self.question_text = None
        self.question_audio_path = "data/audio/question_audio.mp3"
        self.create_audio_directory()
       
        # Load the filtered question bank
        self.filtered_qb = self._load_filtered_qb()
        self.question_prompt = None
    
    def _load_filtered_qb(self):
        qb_filter = FilterQuestionBank(self.session_id)
        return qb_filter.run() # Update, Save, Return filtered_qb 

    def create_audio_directory(self):
        audio_dir = os.path.dirname(self.question_audio_path)  # Get the directory of the audio path
        
        if not os.path.exists(audio_dir):
            print(f"Audio directory '{audio_dir}' does not exist. Creating it.")
            os.makedirs(audio_dir)
        else:
            print(f"Audio directory '{audio_dir}' already exists.")
    
    def question_prompt_fetch(self): 
        self.prompt_generator = PromptGenerator(self.filtered_qb, self.question_no)
        self.question_prompt = self.prompt_generator.generate_prompt_question() 
        
    def question_text_fetch(self): 
        groq_api = GroqApi()
        self.question_text = groq_api.api_calls(self.question_prompt)
        print(self.question_text) 
    
    def question_audio(self):
        print("Generating audio...")
        print(self.question_text)
        deepgram_api = DeepgramAPI()
        deepgram_api.text_to_speech(self.question_text, self.question_audio_path)
    
    
    def subset_question(self, question_no,):
        pass
     
    
    
    def run(self):
        self.question_prompt_fetch()
        self.question_text_fetch()
        self.question_audio()
        print("Audio generated successfully.")
        return self.question_text, self.question_audio_path
    
if __name__ == "__main__":
    question_manager = QuestionManager("9b71e9c3-4e6b-4253-9f88-4752cfeca143", 1)
    question_manager.question_prompt_fetch()
    question_manager.question_text_fetch() 
    question_manager.question_audio()