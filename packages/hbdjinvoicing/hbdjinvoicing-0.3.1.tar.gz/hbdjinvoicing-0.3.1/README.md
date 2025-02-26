# HbDjInvoicing

## Quickstart

```bash
NAME_DB=hbdhinvoicing

# install requirements
pip install -r requirements.txt

# initialize database
createdb $NAME_DB
./manage.py migrate

# create superuser
./manage.py createsuperuser

# launch server
./manage.py runserver
```

## Dev

```bash
# install requirements
pip install -r requirements-dev.txt

# to use celery
sudo apt install redis-server # install redis for ubuntu
celery -A invoicer worker --loglevel=info # launch redis server
# also uncomment lines in __init__ file at project root

# watch changes in sass files
sass --watch invoicer/static/sass/app.sass:invoicer/static/css/app.css

# lint
ruff format
ruff check --fix
```

Linter options in pyproject.toml.


### How to update dependencies

- Update dependencies in pyproject.toml (restrict max version if needed)
- Update requirements files:

    ```bash
    pip-compile --extra=dev -o requirements-dev.txt
    pip-compile -o requirements.txt
    ```

- Actually update dependencies in env:

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt -r requirements-dev.txt
    ```
