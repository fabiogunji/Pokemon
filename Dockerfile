FROM python:3.11-slim

WORKDIR /req.txt /api

RUN pip install req.txt

COPY . /api/

EXPOSE 8000

CMD ["sh","c",python main.py migrate && python main.py runserver 0.0.0.0:8000] 