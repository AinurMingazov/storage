FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /web

COPY requirements.txt /web/requirements.txt
RUN pip install -r requirements.txt

COPY . /web

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
