FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY port-flap.py .

CMD ["python3", "./port-flap.py", "-s Core"]