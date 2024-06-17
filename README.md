# How to connect to database

From bash:

```bash
mysql -uroot -pP8ssw0rd_
```

From software:

```bash
DATABASE_NAME = 'antdvue'
DATABASE_HOST = "127.0.0.1"
DATABASE_PORT = 3306
DATABASE_USER = "root"
DATABASE_PASSWORD = "P8ssw0rd_"
```

# How to run server

```bash
sudo su && conda activate maochang && python manage.py runserver 0.0.0.0:8012
```

# How to run ui

```bash
cd {customer-ui, registry-ui} && yarn serve
```

'''
Pictures of different types of faces are stored in "face_shape".
Pictures of glasses are stored in "glasses".
'''

# To obtain face measurement results:

python face_lankmark.py

# To try on glasses:

python try_on.py
