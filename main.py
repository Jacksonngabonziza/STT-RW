from fastapi import FastAPI, UploadFile, File, status
import aiofiles
import wave
import nemo
import nemo.collections.asr as nemo_asr
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import torchaudio
import pyaudioconvert as pac
from pydub import AudioSegment
import ffmpeg
import logging
import timeit
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

    return ("Welcome to kinyarwanda Speech To Text Model API")
asr_model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained(
                model_name="stt_rw_conformer_transducer_large")

def resampler(audio_path):
    resampler = torchaudio.transforms.Resample(16000) # 
    speech_array, sampling_rate = torchaudio.load(audio_path)
    print("current sample rate is:",sampling_rate)
    #audio = resampler(speech_array)
    audio = resampler(speech_array).squeeze()
    torchaudio.save(audio_path,audio,16000)
def resample_ffmpg(input_file_path):
    stream = ffmpeg.input(input_file_path)
    audio = stream.audio
#     stream = ffmpeg.output(audio, output_file_path)
    stream = ffmpeg.output(audio, input_file_path, **{'ar': '16000','acodec':'flac'})

    #torchaudio.save("out.wav",audio,16000) # 16000 ni sampling rate
        
@app.post("/transcribe/", response_description="", response_model = "")
async def create_file(file: bytes = File(...)):
     try:
         with open("audio.wav", "wb") as f:
            f.write(file)
         
         with wave.open("audio.wav", "rb") as audio_file:
            audio_data = audio_file.readframes(audio_file.getnframes())
         with wave.open("new_audio.wav", "wb") as output_file:
            output_file.setnchannels(audio_file.getnchannels())
            output_file.setsampwidth(audio_file.getsampwidth())
            output_file.setframerate(16000)
            output_file.writeframes(audio_data)
         file_name="new_audio.wav"
         if file_name.endswith("mp3") or file_name.endswith("wav") or file_name.endswith("ogg"):
        #     if file_name.endswith("mp3"):
        #         sound = AudioSegment.from_mp3(file_name)
        #         sound.export(file_name, format="wav")
        #         logging.info("#############mp3 detected#################")
#             if file_name.endswith("ogg"):
#                 sound = AudioSegment.from_ogg(file_name)
#                 sound.export("audio.ogg", format="wav")
#                 logging.info("#############ogg detected#################")
            print("#################### converted before")
#             resampler('audio.wav')
#             pac.convert_wav_to_16bit_mono('audio.wav','audio.wav')
            print("#################### converted successfully")
            files = [file_name]
            print("#################### file loaded successfully")
            # speech_array, sampling_rate = torchaudio.load(file_name)
            # print("updated sample rate is:",sampling_rate)
            # print("file loaded is **************",file.file)
            start = timeit.default_timer()
            for fname, transcription in zip(files, asr_model.transcribe(paths2audio_files=files)):
                logging.info(f"Audio in {fname} was recognized as: {transcription}")
                stop = timeit.default_timer()
                logging.info(transcription[0])
                return {"message": transcription[0], "filename": file_name,"TrancriptionTime":stop-start}
         else:
                return JSONResponse(
                   status_code=status.HTTP_400_BAD_REQUEST, 
                   content={"message": "unsupported audio format please use .wav or mp3 file only", "filename": file_name}
                ) 

     except Exception as e:
        logging.info("The application has returned the error {}".format(e))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(e)}
        )
     else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": transcription[0]}
        )
