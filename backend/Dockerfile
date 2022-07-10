FROM python:3.8.5-slim-buster

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt && pip install gunicorn

EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]