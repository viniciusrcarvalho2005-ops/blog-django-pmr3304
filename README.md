# Caderno de Engenharia

Blog em Django feito para a segunda entrega de laboratório de PMR3304.

## Rodar localmente

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_blog
python manage.py createsuperuser
python manage.py runserver
```

## Deploy no Render

- Build command: `./build.sh`
- Start command: `gunicorn config.wsgi`
- Variáveis de ambiente: `SECRET_KEY`, `DEBUG=False`, `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD`
