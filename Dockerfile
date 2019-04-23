FROM python:3.7-alpine
MAINTAINER vbichov
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
