## Setup
Before doing anything, place a file cell_towers.csv into the ./data/
folder.  This is the file downloaded from opencellid.org that contains
all the cell tower locations.

### Steps
Unarchive
```bash
~ $ tar -xvzf motionlogic.tar.gz
~ $ cd motionlogic
~/motionlogic $
```
---

Download tippecanoe and build its docker image. We'll need this later.
```
~/motionlogic $ git clone https://github.com/mapbox/tippecanoe.git
~/motionlogic $ cd tippecanoe
~/motionlogic/tippecanoe $ docker build -t tippecanoe:latest .
~/motionlogic/tippecanoe $ cd ..
~/motionlogic $
```
---

Bring up all the necessary servers (postgresql/postgis, tileserver-gl)
```bash
~/motionlogic $ docker-compose up
```
---

Create a python virtual environment (tested with 3.5.2 and 3.6.5)
```bash
~/motionlogic $ virtualenv -p python3 venv
~/motionlogic $ source venv/bin/activate
~/motionlogic $ pip install -r requirements.txt
```
---

Create db structure
```bash
~/motionlogic $ python manage.py db upgrade
```

---
---

## Commands
Extract all data from cell_towers.csv with mcc 602 (egypt)
```bash
~/motionlogic $ python manage.py parse
```

Run server
```bash
~/motionlogic $ python manage.py runserver
```
---
Select all files with mcc 602 and export them as geojson to ./data/602.json
```bash
~/motionlogic $ python manage.py geojson
```

Take a file ./data/602.json and convert it to ./data/602.mbtiles
```
~/motionlogic $ python manage.py mbtiles
```

Commands also accept --mccs param
python manage.py *command* --mccs 602,381
