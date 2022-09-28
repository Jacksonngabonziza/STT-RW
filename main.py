from fastapi import FastAPI,status
from fastapi.responses import JSONResponse
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch
# from ui import title, description, examples
from langs import LANGS
app = FastAPI()
TASK = "translation"
CKPT = "facebook/nllb-200-distilled-600M"
model = AutoModelForSeq2SeqLM.from_pretrained(CKPT).cpu()
# to('cpu')
tokenizer = AutoTokenizer.from_pretrained(CKPT)
device ="cpu"

@app.get("/")
async def read_root():

    return ("Welcome to machine translation  we can help you translate 5 languages ")

@app.post("/translate/", response_description="", response_model = "")
async def result(text, src_lang, tgt_lang, max_length=400):
    translation_pipeline = pipeline(TASK,
                                    model=model,
                                    tokenizer=tokenizer,
                                    src_lang=src_lang,
                                    tgt_lang=tgt_lang,
                                    max_length=max_length,
                                    device=device)
    result = translation_pipeline(text)
    return result[0]['translation_text']
