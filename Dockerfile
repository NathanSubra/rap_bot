FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .
RUN #mkdir -p backend/instance
RUN mkdir -p instance
EXPOSE 8000
CMD ["python","-m","flask","--app","backend/app","run","-h","0.0.0.0","-p","8000"]
#CMD ["python","-m","flask","--app","backend.app","run","--host=0.0.0.0","--port=8000"]

