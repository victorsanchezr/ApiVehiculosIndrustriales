FROM python:3.4.5-slim
RUN mkdir /app
WORKDIR /app
ADD ./miweb .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "app.py", "runserver"]
