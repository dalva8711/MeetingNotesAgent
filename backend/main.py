from fastapi import FastAPI, File, UploadFile
from transcription import upload_audio, transcribe_audio
from summarizer import summarize_transcript
import shutil

app = FastAPI()

@app.post("/upload/")
async def upload_and_process(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    audio_url = await upload_audio(temp_path)
    transcript_data = await transcribe_audio(audio_url)
    speaker_text = transcript_data["utterances"]
    full_text = "\n".join([f'{seg["speaker"]}: {seg["text"]}' for seg in speaker_text])
    summary = summarize_transcript(full_text)

    return {"summary": summary, "transcript": full_text}