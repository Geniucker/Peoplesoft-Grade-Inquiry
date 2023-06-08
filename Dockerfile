FROM python:3.9-slim
LABEL Name=score-inquiry

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

EXPOSE 50080

CMD ["python3", "webapi.py"]
