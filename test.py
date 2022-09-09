from fastapi  import FastAPI, UploadFile, File, status
from fastapi.responses import JSONResponse

import aiofiles
app = FastAPI( debug = True ) 

@app.post("/upload_file/", response_description="", response_model = "")
async def result(file:UploadFile = File(...)):
     try:
        async with aiofiles.open(file.filename, 'wb') as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write
            print(out_file.name)

     except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
     else:
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {"result":'success'}
            )