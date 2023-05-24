FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

COPY foodgram/ .

COPY data/ingredients.json .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]