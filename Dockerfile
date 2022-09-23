FROM python:3.10

WORKDIR /STT

COPY ./requirements.txt /STT/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /STT/requirements.txt

# !python -m pip install git+https://github.com/NVIDIA/NeMo.git@r1.11.0#egg=nemo_toolkit[all]
CMD [ "python3 -m pip install git+https://github.com/NVIDIA/NeMo.git@r1.11.0" ] 
# 
COPY ./app/main.py /STT/

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5005"]
