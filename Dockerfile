# FROM python:3.10-slim

FROM python:alpine

RUN pip install --upgrade pip


WORKDIR /user/src/books_api/app

COPY ./requirements.txt /user/src/books_api/app/
RUN python3 -m pip install -r requirements.txt
COPY . /user/src/books_api



# CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]


