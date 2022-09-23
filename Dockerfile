FROM python:3.10

WORKDIR /STT

COPY ./requirements.txt /STT/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /STT/requirements.txt

# !python -m pip install git+https://github.com/NVIDIA/NeMo.git@r1.11.0#egg=nemo_toolkit[all]
RUN python3 -m pip install git+https://github.com/NVIDIA/NeMo.git@r1.11.0#egg=nemo_toolkit[all]
# 
COPY ./app/main.py /STT/

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5005"]
