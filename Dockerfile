FROM python:3.8.18
RUN mkdir /app
WORKDIR /app
ADD ./web /app/web
RUN pip install -r web/requirements.txt
ENV PYTHONPATH=/app
EXPOSE 8080
CMD ["python", "web/app.py", "runserver"]
