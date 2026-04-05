FROM python:3.12-slim
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY docker_req.txt .
RUN pip install --no-cache-dir -r docker_req.txt

COPY code_analyzer/ ./code_analyzer/
RUN cd code_analyzer && npm install

COPY agents/ ./agents/
COPY utils/ ./utils/
COPY app.py .
COPY examples.py .

ENV PYTHONUNBUFFERED=1
ENV GRADIO_SERVER_NAME="0.0.0.0"
CMD ["python", "app.py"]