```bash
~ $ tar -xvzf motionlogic.tar.gz
~ $ cd motionlogic
~/motionlogic $
~/motionlogic $ git clone https://github.com/mapbox/tippecanoe.git
~/motionlogic $ cd tippecanoe
~/motionlogic/tippecanoe $ docker build -t tippecanoe:latest .
~/motionlogic/tippecanoe $ cd ..
~/motionlogic $ docker-compose up

~/motionlogic $ virtualenv -p python3 venv
~/motionlogic $ source venv/bin/activate
~/motionlogic $ pip install -r requirements.txt

~/motionlogic $ python manage.py db upgrade
~/motionlogic $ python manage.py db migrate
~/motionlogic $ python manage.py parse

~/motionlogic $ python manage.py geojson
~/motionlogic $ docker-compose run tippecanoe sh -c 'tippecanoe -o /data/out.mbtiles -zg --drop-densest-as-needed /data/602.json'
```


```bash
$ docker-compose rm -fv
$ docker volume ls -qf dangling=true | xargs -r docker volume rm
$ docker-compose up
```