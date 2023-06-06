FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

COPY product_helper/ /app

CMD ["gunicorn", "product_helper.wsgi:application", "--bind", "0:8000"]