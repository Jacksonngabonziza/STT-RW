from fastapi import FastAPI, UploadFile, File, status
import aiofiles
import nemo
import nemo.collections.asr as nemo_asr
from fastapi.responses import JSONResponse
import torchaudio
import pyaudioconvert as pac
from pydub import AudioSegment
import ffmpeg
import timeit
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

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
async def result(file:UploadFile = File(...)):
     try:
         async with aiofiles.open(file.file, 'wb') as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write
            print("file uploadedd as:",out_file.name)
            speech_array, sampling_rate = torchaudio.load(out_file.name)
            print("sample rate: ",sampling_rate)
            file_name=out_file.name
            print(type(file_name))
            if file_name.endswith("mp3") or file_name.endswith("wav"):
                
                #test
    #             resampler(out_file.name)
    #             resample_ffmpg(out_file.name)
    #             pac.convert_wav_to_16bit_mono(out_file.name,out_file.name)
                # converting mp3 to wav for easy resampling with pyaudio converter
                if file_name.endswith("mp3"):
                    print("mp3 file recorgnised !!!!!!!")
                    sound = AudioSegment.from_mp3(out_file.name)
                    sound.export(out_file.name, format="wav")
                    print("#############mp3 detected#################")
                pac.convert_wav_to_16bit_mono(out_file.name,out_file.name)
                files = [out_file.name]
                speech_array, sampling_rate = torchaudio.load(out_file.name)
                print("updated sample rate is:",sampling_rate)
                print("file loaded is **************",file.file)
                start = timeit.default_timer()
                for fname, transcription in zip(files, asr_model.transcribe(paths2audio_files=files)):
                    print(f"Audio in {fname} was recognized as: {transcription}")
                    stop = timeit.default_timer()
                    print(transcription[0])
                    return {"message": transcription[0], "filename": file.filename,"TrancriptionTime":stop-start}
            else:
                return {"message": "unsupported audio format please use .wav or mp3 file only", "filename": file.filename}

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
