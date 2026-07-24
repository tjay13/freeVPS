FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD sh -c "python HTTPINJECTOR.py & python HTTPCUSTOM.py & python DARKTUNNEL.py & python NPVTUNNEL.py & python SSCCUSTOM.py"
