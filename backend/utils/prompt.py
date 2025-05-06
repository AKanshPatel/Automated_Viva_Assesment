import json
from pathlib import Path

class PromptGenerator:
    def __init__(self):
        pass
        
        
    def generate_first_question_prompt(self, filtered_qb):
        """
        Generates a prompt to select an easy-level first viva question.
        """
        prompt_first = f"""
        You are the Viva Question Selector for an oral examination system. From the question bank below, 
        choose **one** introductory-level question that is suitable as the **first question** 
        in the viva. It should be simple, clear, and help ease the candidate into the session.

        Return **only** the selected question. Do not include any additional explanation or context.

        Question Bank:
        {filtered_qb}
        
        """
        return prompt_first

    def generate_subsequent_question_prompt(self, filtered_qb, previous_question, answer_text, feedback):
        """
        Generates a prompt for the next viva question based on previous answer and feedback.
        """
        prompt_second = f"""
        You are the Viva Question Selector. The candidate just responded to the following:

        Previous Question: "{previous_question}"  
        Candidate's Answer: "{answer_text}"  
        Feedback: {feedback}

        Based on the feedback:
        - If the feedback indicates strong performance (high score or positive comments), increase the difficulty of the next question.
        - If the feedback suggests areas for improvement (low score or constructive comments), ask a relevant question that reinforces those areas while remaining aligned with the candidate’s level.

        Select the next appropriate question **exactly as it appears in the question bank**. Do not modify or rephrase.  
        Return **only** the selected question. Do not add explanations or context.

        Question Bank:
        {filtered_qb}
        """
        return prompt_second


    def generate_feedback_prompt(self, question, answer_text):
        """
        Generates the evaluation feedback prompt.
        The model evaluates the candidate's answer and provides a score and feedback.
        """
        prompt_feedback = f"""
        The candidate answered the following question:
        "{question}"
        Their answer: "{answer_text}"

        Please evaluate the answer based on the following criteria:
        1. Relevance to the question
        2. Completeness of the answer
        3. Clarity and correctness

        Assign a score from 1 to 10 based on these criteria.
        Provide brief feedback explaining the score.

        Return the result in plain text using the following key-value pair format:
            Score: <score>  
            Feedback: <your_feedback>
            
        Example:
        Score: 7  
        Feedback: Good explanation, but lacks clarity in the example.

        """
        return prompt_feedback