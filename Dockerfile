From python:latest
COPY . /app
WORKDIR /app
EXPOSE 8080
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["python3", "app.py"]
