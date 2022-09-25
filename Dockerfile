FROM ubuntu:20.04

WORKDIR /STT

COPY ./requirements.txt /STT/requirements.txt
RUN apt update
RUN apt install python3
RUN apt update
RUN pip install --no-cache-dir --upgrade -r /STT/requirements.txt
RUN pip install wget
RUN apt-get install sox libsndfile1 ffmpeg
RUN pip install unidecode
RUN pip install matplotlib>=3.3.2
RUN pip install git+https://github.com/NVIDIA/NeMo.git@r1.11.0
RUN mkdir configs
RUN wget -P configs/ https://raw.githubusercontent.com/NVIDIA/NeMo/r1.11.0/examples/asr/conf/config.yaml
# 
COPY ./app/main.py /STT/

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5005"]
