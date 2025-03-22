import openai
import os
from dotenv import load_dotenv
from backend.config import config

load_dotenv()

openai.api_key = config.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key is missing. Please set it in the environment or config.")

def get_ai_response(question: str) -> str:
    try:

        client = openai.OpenAI()

        response = client.chat.completions.create( 
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert legal advisor providing general legal guidance. "
                                              "Do not provide personal legal representation or definitive legal conclusions."},
                {"role": "user", "content": question}
            ]
        )

        return response.choices[0].message.content.strip()
    except openai.OpenAIError as e:
        return f"An error occurred while fetching the response: {str(e)}"
