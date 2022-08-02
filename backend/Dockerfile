FROM python:3.10.5

RUN apt update

WORKDIR /usr/src/backend
COPY . .
RUN pip install -r requirements.txt


ENV FLASK_APP=/usr/src/backend/server/server.py
ENV FLASK_ENV=development
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV ACCESS_TOKEN=""
ENV PYTHONPATH=/usr/src/backend

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]