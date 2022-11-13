FROM python:3.9

RUN apt-get update -y
RUN apt-get upgrade -y

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /server

COPY ./reequirements.txt .

RUN pip install -r reequirements.txt 

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
