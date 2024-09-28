## commands :

**create .env file from .env.sample**

```bash 
mv .env.sample .env
```

*hints:*

* it is a good idea to change db password

* POSTGRES_DB and DB_NAME should be equal such as DB_USER and POSTGRES_USER

**run docker for first time**

```bash
docker compose up -d --build
```

**run docker**

```bash
docker compose up -d

```

**create super user**

```bash
 docker exec -it wh_main_container python manage.py createsuperuser

```

