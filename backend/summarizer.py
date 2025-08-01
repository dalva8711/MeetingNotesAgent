import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_transcript(transcript_text):
    prompt = f"""
    Here's a meeting transcript with speaker labels. Summarize the discussion and extract:
    1. Main points discussed
    2. Decisions made
    3. Action items (with names if mentioned)

    Transcript:
    {transcript_text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000,
    )

    return response["choices"][0]["message"]["content"]