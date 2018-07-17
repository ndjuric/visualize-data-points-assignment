```bash
$ virtualenv -p python3 venv
$ source venv/bin/activate

$ pip install -r requirements.txt

$ docker-compose rm -fv
$ docker volume ls -qf dangling=true | xargs -r docker volume rm
$ docker-compose up
```