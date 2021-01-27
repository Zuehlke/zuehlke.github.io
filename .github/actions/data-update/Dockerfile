FROM python:3.8

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/ .
COPY ./input ./input

ENTRYPOINT ["python"]
CMD [ "main.py" ]
