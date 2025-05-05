from groq import Groq
from dotenv import load_dotenv
import os

class GroqApi:
    def __init__(self):
        """Initialize the Groq client and load API key from environment variables."""
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key)
        self.response = None
    
    def api_calls(self, prompt):
        """
        Calls the Groq API with a given prompt and returns the generated response.
        
        Args:
            prompt (str): The prompt to send to the Groq API.
        
        Returns:
            str: The generated response from the Groq API.
        """
        try:
            # Call the Groq API with the provided prompt
            completion = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=True,
                stop=None,
            )
            # Extract and return the response
            response = self._stream_response(completion)
            self.response = response
            return response
        
        except Exception as e:
            print(f"Error during API call: {e}")
            return None
    
    def _stream_response(self, completion):
        """
        Helper function to handle streaming responses from the Groq API.
        
        Args:
            completion: The streaming response object from the Groq API.
        
        Returns:
            str: The complete response as a single string.
        """
        response = ""
        try:
            for chunk in completion:
                response += chunk.choices[0].delta.content or ""
        except Exception as e:
            print(f"Error while streaming response: {e}")
        return response


# Example usage
if __name__ == "__main__":
    g = GroqApi()
    prompt = "Who are you"
    result = g.api_calls(prompt)
    if result:
        print("Generated Response:", result)
