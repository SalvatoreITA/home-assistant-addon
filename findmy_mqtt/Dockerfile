FROM python:3.11-alpine

# Installazione dipendenze base e fusi orari
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev tzdata

WORKDIR /app

# Installazione librerie Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia script principale
COPY main.py .

CMD ["python", "-u", "main.py"]