FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

COPY product_helper/ /app

RUN python -m pip install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "product_helper.wsgi:application", "--bind", "0:8000"]