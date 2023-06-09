# Foodgram

## Project Description

FOODGRAM is resource for sharing recipes
Users can share their recipes, subscribe for other users, add recipes in liked, and make shopping list in PDF

## Installing the project locally

* Склонировать репозиторий на локальную машину:
```

git clone https://github.com/Samsooon/foodgram-project-react.git

cd foodgram-project-react

```

* Create and activate a virtual environment:

```
for WIN

python -m venv venv

source venv/bin/activate

```
```
for MAC

python3 -m venv venv

source venv/bin/activate

```


* Create a file `.env` in the `/infra/` directory with the contents:

```

SECRET_KEY=секретный ключ django
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

```

* Install requirements.txt:

```

cd backend/

pip install -r requirements.txt

```

* Make migrations:

```
python3 manage.py migrate
```

* Run server:
```

python3 manage.py runserver

```


## Site
The site is available at: 158.160.105.206

ADMIN USER:
```
{

    "email": "adm1@adm.adm",
    "password": "adm"

}
```

## Author
[Samsonov Dmitrii](https://github.com/Samsooon?tab=repositories) - Python developer.  Developed the backend and deployment for the service Foodgram.  
[Yandex.Practikum](https://github.com/yandex-praktikum) Frontend for Foodgram.
