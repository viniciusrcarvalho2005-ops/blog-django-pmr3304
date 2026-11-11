# Blog de Engenharia – PMR3304

Segunda entrega de laboratório de PMR3304 (Sistemas de Informação): aplicação CRUD em Django com posts, comentários e categorias.

## Rodar localmente

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_blog        # dados de exemplo
python manage.py createsuperuser
python manage.py runserver
```

## Deploy no Render

- Build command: `./build.sh`
- Start command: `gunicorn config.wsgi`
- Variáveis de ambiente: `SECRET_KEY`, `DEBUG=False`, `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD`
