FROM python:3.9-slim

WORKDIR /app


RUN sudo apt-get update
RUN sudo apt-get install graphviz -y

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]