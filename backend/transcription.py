import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

AUDIO_UPLOAD_ENDPOINT = "https://api.assemblyai.com/v2/upload"
TRANSCRIPTION_ENDPOINT = "https://api.assemblyai.com/v2/transcript"
headers = {"authorization": os.getenv("ASSEMBLYAI_API_KEY")}

async def upload_audio(file_path):
    with open(file_path, "rb") as f:
        response = httpx.post(AUDIO_UPLOAD_ENDPOINT, headers=headers, files={"file": f})
    return response.json()["upload_url"]

async def transcribe_audio(upload_url):
    json_data = {
        "audio_url": upload_url,
        "speaker_labels": True,
        "auto_chapters": True,
        "language_model": "latest_conversational"
    }

    response = httpx.post(TRANSCRIPTION_ENDPOINT, headers=headers, json=json_data)
    transcript_id = response.json()["id"]

    while True:
        res = httpx.get(f"{TRANSCRIPTION_ENDPOINT}/{transcript_id}", headers=headers).json()
        if res["status"] == "completed":
            return res
        elif res["status"] == "error":
            raise Exception(res["error"])