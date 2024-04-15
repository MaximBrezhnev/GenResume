FROM python:3.11
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app
COPY . .

COPY fonts/arial.ttf /usr/share/fonts/truetype/
RUN fc-cache -f -v

RUN pip install -r requirements.txt

CMD ["python3", "./pet_django/manage.py", "runserver", "0.0.0.0:7000"]
