from fastapi import FastAPI, UploadFile, File, status
from fastapi.responses import JSONResponse
import timeit
import ast
import logging
import requests
import json
import ast
from languages import language,url
from fastapi.middleware.cors import CORSMiddleware
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

    return ("Welcome to Digital Umuganda  machine translation  API")
        
@app.post("/translate/", response_description="", response_model = "")
async def result(source:str,target:str,text:str):
    logging.info("translating from "+source+"to "+target)
    logging.info("content to translate "+text)
    payload = json.dumps({
  "q":text,
 'source': language.get(source),
  'target': language.get(target),
  'format': 'text'
})
    headers = {
  'trans_key': 'AIzaSyB7dDD3UGDO2hSJgBrGYPohWjQJE4xQYYU',
  'Content-Type': 'application/json'
}

    # print(language.get("Kinyarwanda"))
    if language.get(source) and language.get(target):
        response = requests.request("POST", url, headers=headers, data=payload)
        rep= ast.literal_eval(response.text)
        # print(rep.get("data").get("translations")[0].get("translatedText"))
        print(response.text)

        if rep.get("data").get("translations")[0].get("translatedText"):
            return rep.get("data").get("translations")[0].get("translatedText")



        else:
            logging.info("some thing went wrong find the response below")
            print(response.text)
            return "unfortunately something went wrong"
    else:
        return JSONResponse(
                   status_code=status.HTTP_400_BAD_REQUEST, 
                   content={"message": "one of the entered language is wrongly typed ,here are the supported languages: kinyarwanda,swahili,luganda,lingala,english,french"}
                ) 