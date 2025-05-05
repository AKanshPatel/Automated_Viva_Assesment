import json
from pathlib import Path

class PromptGenerator:
    def __init__(self,filtered_qb: str, question_no: int):
        self.filtered_qb = filtered_qb
        self.question_no = question_no
        # self.previous_question = None
        # self.answer = None
        # self.feedback = None
        
        
        
    def generate_first_question_prompt(self):
        """
        Generates a prompt to select an easy-level first viva question.
        """
        prompt_first = f"""
        You are the Viva Question Selector for an oral examination system. From the question bank below, 
        choose **one** introductory-level question that is suitable as the **first question** 
        in the viva. It should be simple, clear, and help ease the candidate into the session.

        Return **only** the selected question. Do not include any additional explanation or context.

        Question Bank:
        {self.filtered_qb}
        
        """
        return prompt_first

    # def generate_subsequent_question_prompt(self, filtered_qb, previous_question, candidate_answer, feedback):
    #     """
    #     Generates a prompt for the next viva question based on previous answer and feedback.
    #     """
    #     prompt_second = f"""
    #     You are the Viva Question Selector. The candidate just responded to the following:

    #     Previous Question: "{previous_question}"  
    #     Candidate's Answer: "{candidate_answer}"  
    #     Feedback: {feedback}

    #     Based on the feedback:
    #     - If the feedback indicates strong performance (high score or positive comments), increase the difficulty of the next question.
    #     - If the feedback suggests areas for improvement (low score or constructive comments), ask a relevant question that reinforces those areas while remaining aligned with the candidate’s level.

    #     Select the next appropriate question **exactly as it appears in the question bank**. Do not modify or rephrase.  
    #     Return **only** the selected question. Do not add explanations or context.

    #     Question Bank:
    #     {filtered_qb}
    #     """
    #     return prompt_second

    def generate_prompt_question(self, previous_question=None, candidate_answer=None, feedback=None):
        """
        Wrapper to generate appropriate prompt based on the question number.
        """
        if self.question_no == 1:
            return self.generate_first_question_prompt()
        # else:
        #     if not all([previous_question, candidate_answer, feedback]):
        #         raise ValueError("Previous question, candidate answer, and feedback must be provided for question number > 1.")
        #     return self.generate_subsequent_question_prompt(filtered_qb, previous_question, candidate_answer, feedback)
