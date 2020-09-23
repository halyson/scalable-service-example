FROM python:3.6-alpine

WORKDIR /app

COPY . /app

RUN pip install -r /app/requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]
