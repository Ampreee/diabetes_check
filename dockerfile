FROM python:3.13.3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        tesseract-ocr \
        libtesseract-dev \
        poppler-utils \
        python3-dev \
        gcc \
        libgl1 \
        libglib2.0-0 \
        && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY src ./src

COPY .env .env

EXPOSE 8000 8501

CMD ["streamlit", "run", "src/app.py"]