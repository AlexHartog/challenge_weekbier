FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=run_weather_app.py
CMD ["flask", "run", "--host", "0.0.0.0"]