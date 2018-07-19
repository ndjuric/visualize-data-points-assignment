```bash
$ virtualenv -p python3 venv
$ source venv/bin/activate

$ pip install -r requirements.txt

$ docker-compose rm -fv
$ docker volume ls -qf dangling=true | xargs -r docker volume rm
$ docker-compose up

$ python manage.py db upgrade
$ python manage.py db migrate
$ python manage.py parse

$ python manage.py geojson
```