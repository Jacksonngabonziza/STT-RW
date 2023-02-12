from fastapi import FastAPI, UploadFile, File, status
from fastapi.responses import StreamingResponse,JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import tempfile
from typing import Optional
import numpy as np
from TTS.utils.synthesizer import Synthesizer

app = FastAPI()
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%d-%b-%y %H:%M:%S',level=logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    allow_origins=['*'])

@app.get("/")
async def read_root():
    return ("Welcome to kinyarwanda Text To Text Model API")
MAX_TXT_LEN=3000

@app.post("/generate_audio/", response_description="", response_model = "")
async def generate_audio(text: str):
    if len(text) > MAX_TXT_LEN:
        text = text[:MAX_TXT_LEN]
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': f"Error:Input text was cutoff since it went over the {MAX_TXT_LEN} character limit."}
        )
    synthesizer = Synthesizer("./Kinyarwanda_YourTTS/model.pth",
            "./Kinyarwanda_YourTTS/config.json",
            tts_speakers_file="./Kinyarwanda_YourTTS/speakers.pth",
            encoder_checkpoint="./Kinyarwanda_YourTTS/SE_checkpoint.pth.tar",
            encoder_config="./Kinyarwanda_YourTTS/config_se.json",)
    wav = synthesizer.tts(text, speaker_wav="Kinyarwanda_YourTTS/conditioning_audio.wav")
    headers = {
        "Content-Disposition": "attachment; filename=" + str(text[:10]) + ".wav"
    }
    return StreamingResponse(
        wav, media_type="application/octet-stream", headers=headers
    )
    # with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fp:
    #     synthesizer.save_wav(wav, fp)
    #     return fp.name