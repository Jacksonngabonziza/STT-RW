from fastapi import FastAPI, UploadFile, File, status
import aiofiles
import nemo
import torch
import torchaudio
import nemo.collections.asr as nemo_asr
from fastapi.responses import JSONResponse
app = FastAPI()

resampler = torchaudio.transforms.Resample(48000, 16000)
def speech_to_array(audio_path):
    speech_array, sampling_rate = torchaudio.load(audio_path)
    audio_length = torch.tensor([speech_array.shape[1]/sampling_rate])
    audio = resampler(speech_array)
    return audio



@app.get("/")
async def read_root():

    return ("Welcome to kinyarwanda Speech To Text Model API")

@app.post("/transcribe/", response_description="", response_model = "")
async def result(file:UploadFile = File(...)):
     try:
        async with aiofiles.open(file.filename, 'wb') as out_file:
            content = await file.read()  # async read
            cleaned_audio=speech_to_array(content)
            await out_file.write(cleaned_audio)  # async write
            print(out_file.name)
            asr_model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained(
            model_name="stt_rw_conformer_transducer_large")
            # speech_to_array(out_file.name)
            files = [out_file.name]
            print("file loaded is **************",out_file.name)
            for fname, transcription in zip(files, asr_model.transcribe(paths2audio_files=files)):
                print(f"Audio in {fname} was recognized as: {transcription}")
                print(transcription[0])
                return {"text": transcription[0], "filename": file.filename}

     except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
     else:
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {"result":transcription[0]}
            )