from fastapi import FastAPI, File, UploadFile
import nemo
import nemo.collections.asr as nemo_asr
app = FastAPI()


@app.get("/")
async def read_root():

    return ("Welcome to kinyarwanda Speech To Text Model API")


@app.post("/files/")
async def create_file(file: bytes = File()):
    asr_model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained(
        model_name="stt_rw_conformer_transducer_large")
    files = [file.file]
    for fname, transcription in zip(files, asr_model.transcribe(paths2audio_files=files)):
        print(f"Audio in {fname} was recognized as: {transcription}")
        print(transcription[0])
    return {"text": transcription[0], "file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    asr_model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained(
        model_name="stt_rw_conformer_transducer_large")
    files = [file.file]
    for fname, transcription in zip(files, asr_model.transcribe(paths2audio_files=files)):
        print(f"Audio in {fname} was recognized as: {transcription}")
        print(transcription[0])
    return {"text": transcription[0], "file_size": len(file), "filename": file.filename}
