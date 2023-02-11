FROM tiangolo/uvicorn-gunicorn:python3.8

RUN apt-get update
RUN apt-get install -y libsndfile1 espeak-ng git
RUN pip install --upgrade pip

WORKDIR /code/tts-api
COPY ./app/ /code/tts-api
COPY requirements.txt /code/tts-api/
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]