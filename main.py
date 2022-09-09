from fastapi import FastAPI, UploadFile, File, status
import aiofiles
import nemo
import nemo.collections.asr as nemo_asr
from fastapi.responses import JSONResponse
app = FastAPI()


@app.get("/")
async def read_root():

    return ("Welcome to kinyarwanda Speech To Text Model API")


@app.post("/files/")
async def create_file(file: bytes = File()):
    asr_model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained(
        model_name="stt_rw_conformer_transducer_large")
    files = [file.file()]
    for fname, transcription in zip(files, asr_model.transcribe(paths2audio_files=files)):
        print(f"Audio in {fname} was recognized as: {transcription}")
        print(transcription[0])
    return {"text": transcription[0], "file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    asr_model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained(
        model_name="stt_rw_conformer_transducer_large")
    files = [file.file]
    print("file loaded is **************",file.file)
    for fname, transcription in zip(files, asr_model.transcribe(paths2audio_files=files)):
        print(f"Audio in {fname} was recognized as: {transcription}")
        print(transcription[0])
    return {"text": transcription[0], "file_size": len(file), "filename": file.filename}


@app.post("/transcribe/", response_description="", response_model = "")
async def result(file:UploadFile = File(...)):
     try:
        async with aiofiles.open(file.filename, 'wb') as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write
            print(out_file.name)
            asr_model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained(
            model_name="stt_rw_conformer_transducer_large")
            files = [out_file.name]
            # print("file loaded is **************",file.file)
            for fname, transcription in zip(files, asr_model.transcribe(paths2audio_files=files)):
                print(f"Audio in {fname} was recognized as: {transcription}")
                print(transcription[0])
                return {"text": transcription[0], "file_size": len(file), "filename": file.filename}

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