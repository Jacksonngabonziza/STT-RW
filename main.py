from fastapi import FastAPI, UploadFile, File, status
import aiofiles
import nemo
import nemo.collections.asr as nemo_asr
from fastapi.responses import JSONResponse
import torchaudio
import pyaudioconvert as pac
app = FastAPI()


@app.get("/")
async def read_root():

    return ("Welcome to kinyarwanda Speech To Text Model API")
asr_model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained(
                model_name="stt_rw_conformer_transducer_large")

def resampler(audio_path):
    resampler = torchaudio.transforms.Resample(16000) # 
    speech_array, sampling_rate = torchaudio.load(audio_path)
    print("current sample rate is:",sampling_rate)
    audio = resampler(speech_array)
    torchaudio.save("out.wav",audio,16000) # 16000 ni sampling rate
        
@app.post("/transcribe/", response_description="", response_model = "")
async def result(file:UploadFile = File(...)):
     try:
         async with aiofiles.open(file.filename, 'wb') as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write
            print(out_file.name)
            #resampler(out_file.name)
            pac.convert_wav_to_16bit_mono(out_file.name,out_file.name)
            files = [out_file.name]
            speech_array, sampling_rate = torchaudio.load("out.wav")
            print("current updated sample rate is:",sampling_rate)
            # print("file loaded is **************",file.file)
            for fname, transcription in zip(files, asr_model.transcribe(paths2audio_files=files)):
                print(f"Audio in {fname} was recognized as: {transcription}")
                print(transcription[0])
                return {"text": transcription[0], "filename": file.filename}

     except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(e)}
        )
     else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"result": transcription[0]}
        )
