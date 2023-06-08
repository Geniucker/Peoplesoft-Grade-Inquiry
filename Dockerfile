FROM python:3.9.5-slim
LABEL Name=score-inquiry

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

CMD ["python3", "api.py"]
