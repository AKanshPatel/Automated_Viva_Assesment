import json
from pathlib import Path

class PromptGenerator:
    def __init__(self):
        pass
        
        
    def old_generate_first_question_prompt(self, filtered_qb):
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
    
    def generate_first_question_prompt(self, filtered_qb):
        """
        Generates a prompt to select an easy-level first viva question.
        """
        prompt_first = f"""
        You are the Viva Question Selector for an oral examination system. From the question bank below, 
        choose **one single** introductory-level question that is suitable as the **first question** in the viva. This question must be simple, clear, foundational, and designed to ease the candidate 
        into the session, typically requiring a straightforward, brief answer.

        Return **only the selected question**. Do not include any additional explanation, context, 
        or introductory phrases (e.g., do not say "Here is the question:").

        Question Bank:
        {filtered_qb}
        
        """
        return prompt_first

    def old_generate_subsequent_question_prompt(self, filtered_qb, previous_question, answer_text, feedback):
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
        - Do not repeat the previous question
        Select the next appropriate question **exactly as it appears in the question bank**. Do not modify or rephrase.  
        Return **only** the selected question. Do not add explanations or context.

        Question Bank:
        {filtered_qb}
        """
        return prompt_second
     
    
    def generate_subsequent_question_prompt(self, filtered_qb, previous_question, answer_text, feedback, prev_questions):
        """
        Generates a prompt for the next viva question based on previous answer and feedback.
        """
        prompt_second = f"""
        You are the Viva Question Selector for an oral examination. Your task is to choose **one single, most appropriate next question** for the candidate from the provided "Question Bank".
        And you can also generate new questions but the question should be relevant to the current discussion 

        Here's the context from the previous round:
        * **Previous Question:** "{previous_question}"
        * **Candidate's Answer:** "{answer_text}"
        * **Evaluation Feedback:** {feedback} 
        * **Previously Asked Questions: {prev_questions}
        
        **Based on the Evaluation Feedback, follow these strict rules:**
        1.  Choose the next question from the given question bank that is **most relevant to the ongoing discussion and syllabus topic**.
        3.  If feedback is positive (e.g., good, excellent, satisfactory), continue with the same topic, exploring a related sub-topic, or **increase the complexity slightly** (e.g., from definitions to applications).
        4.  If feedback is negative (e.g., incorrect, poor, needs improvement), either simplify the next question to reinforce foundational concepts or switch to a different, related topic in the syllabus.umerical score is 1 to 6 (areas for improvement):** Select a question that is **relevant to the previous topic or addresses identified weaknesses** mentioned in the feedback, maintaining a similar or slightly adjusted (e.g., slightly easier or rephrased) difficulty level.
        2.  **Avoid Repetition:** **DO NOT** under any circumstances select the "Previous Question" ("{previous_question}").
        3.  **Exact Match:** Select the next question **exactly as it appears in the "Question Bank"**. Do not modify, rephrase, or abbreviate it.
        5.  Always ensure **logical connection with the previous question**, building upon previous concepts or exploring contrasting ideas.
            **Your output MUST be ONLY the selected question.** Do not include any introductory phrases (e.g., "The next question is:"), explanations, context, or any other text.

        ---
        **Question Bank:**
        {filtered_qb}
        """
        return prompt_second
    
    
    def old_generate_feedback_prompt(self, question, answer_text):
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
        4. If the answer is null/ empty assign than 0.
        
        Assign a score from 1 to 10 based on these criteria.
        Provide brief feedback explaining the score.

        return me in following format:
        x; "Nice answer" 

        """
        return prompt_feedback
    
    def generate_feedback_prompt(self, question, answer_text):
        """
        Generates the evaluation feedback prompt.
        The model evaluates the candidate's answer and provides a score and feedback.
        """
        prompt_feedback = f"""
        You are an AI assistant tasked with evaluating candidate answers in an oral examination setting.
        
        The candidate was asked the following question:
        **"{question}"**
        
        Their provided answer is:
        **"{answer_text}"**

        Please evaluate this answer based on the following criteria:
        1.  **Relevance:** How well does the answer directly address the question? Is it on topic?
        2.  **Completeness:** Does the answer cover all necessary aspects of the question? Is it sufficiently detailed without being overly verbose?
        3.  **Clarity and Correctness:** Is the answer easy to understand, well-articulated, and factually accurate? Are there any significant misconceptions or errors?
        
        **Scoring Guidelines:**
        * Assign a score from **1 to 10**.
        * If the provided answer is **null, empty, or essentially silent/non-responsive**, assign a score of **0**. Otherwise, the minimum score is 1.

        Provide a **brief, concise feedback statement** explaining the assigned score, focusing on the strengths and weaknesses of the answer.

        **Return your response in the following strict format: SCORE; "FEEDBACK_STATEMENT"**
        
        Example: 7; "Good effort, but could have elaborated more on X."
        Example: 0; "No answer provided."
        """
        return prompt_feedback
    
    def generate_rephrase_question_prompt(self, question):
        """
        Generates a prompt to rephrase a given question while maintaining its original meaning.
        """
        prompt_rephrase = f"""
        You are an AI assistant specialized in simplifying and clarifying questions for oral examinations.
        Your task is to rephrase the following original question into one and only one alternative wordings.
        
        **Crucial Rules:**
        1.  **Preserve Meaning:** The rephrased question(s) MUST convey the **exact same meaning** as the original question. Do not add new concepts, remove existing ones, or change the scope.
        2.  **Vary Wording:** Use different vocabulary, sentence structures, and phrasing to make the question potentially easier to understand or to offer an alternative perspective without altering its core.
        3.  **Offer Options (Optional but Recommended):** You may provide up to 2-3 different rephrased versions if multiple good alternatives exist.
        4.  **Clarity First:** The rephrased questions should be clear, concise, and easy to grasp.
        5.  **No Explanations:** Do NOT include any introductory phrases (e.g., "Here's a rephrased version:"), explanations, or conversational text. Return only the rephrased question(s).

        **Original Question to Rephrase:**
        "{question}"

        **Return Format Examples:** 
       "What is the capital of France?"
        """
        return prompt_rephrase

    def generate_hint_for_question(self, question):
        """
        Generates a helpful, concise hint for a given question without revealing the answer.
        """
        prompt_hint = f"""
        You are an AI assistant designed to provide supportive hints for oral examination questions.
        Your goal is to guide the candidate towards the answer without directly stating it.

        **Crucial Rules for Hint Generation:**
        1.  **Indirect Guidance:** The hint should gently steer the candidate in the right direction. It must NOT give away the direct answer or any key parts of it.
        2.  **Concise:** Keep the hint **brief and to the point**, ideally one short sentence or a very short phrase.
        3.  **Focus on Key Concepts/Areas:** The hint should point to a specific concept, principle, or area of knowledge relevant to answering the question.
        4.  **No Explanations/Context:** Do NOT include any introductory phrases (e.g., "Here's a hint:"), explanations, or conversational text. Return only the hint itself.
        5.  **Question-Specific:** The hint must be directly relevant to the provided question.

        **Original Question:**
        "{question}"

        **Return ONLY the hint.**

        **Examples of desired output:**
        * "Consider the definition of recursion."
        * "Think about the main components of a CPU."
        * "What is the primary purpose of a database index?"
        * "Recall the difference between compiled and interpreted languages."
        """
        return prompt_hint

    def generate_topic_context_for_question(self, question, session_id):
        """
        Generates the Unit and Topic name for a given question from the structured question bank.
        """
        path_of_filter_qb = Path("data/sessions") / f"{session_id}_filtered_qb.json"
        if not path_of_filter_qb.exists():
            print(f"Error: Question bank file not found at {path_of_filter_qb}")
            return {} # Return an empty dictionary or handle the error as appropriate

        with open(path_of_filter_qb, 'r', encoding='utf-8') as f:
            filtered_qb = json.load(f) 
        prompt_topic_context = f"""
        You are an AI assistant tasked with identifying the precise location (Unit and Topic) of a given question within a structured Question Bank.

        Here's the Question Bank, organized by Units and then by Topics, with questions listed under each:
        ```json
        {filtered_qb}
        ```

        Your goal is to find the **exact Unit Name** and **exact Topic Name** under which the "Target Question" is listed.

        **Crucial Rules:**
        1.  **Exact Match:** You must find the question in the Question Bank that is an **exact, character-for-character match** to the "Target Question."
        2.  **Identify Hierarchy:** Once the question is found, identify its immediate parent (the **Topic Name**) and that topic's parent (the **Unit Name**).
        3.  **Return Format:** Your output MUST be in the format: `Unit Name; Topic Name`.
        4.  **No Explanations/Context:** Do NOT include any introductory phrases, explanations, conversational text, or anything other than the exact specified output format.
        5.  **Handle Not Found:** If the "Target Question" is not found in the provided Question Bank, return: `Not Found; Not Found`.

        **Target Question:**
        "{question}"

        **Examples of desired output:**
        * `Introduction; Machine Learning Categories`
        * `Machine Learning Perspective of Data; Handling Categorical Data`
        * `Not Found; Not Found`
        """
        return prompt_topic_context