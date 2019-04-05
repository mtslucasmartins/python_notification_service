FROM python:3.7.0
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

RUN python -m pytest tests/

CMD ["python", "app.py"]
