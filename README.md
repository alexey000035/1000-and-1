# 1000-and-1
Веб-сервер ИМИТ.

## Запуск сервера для разработки

1. Выполнить clone репозитория:
```
git clone https://github.com/alexey000035/1000-and-1
```

2. Перейти в директорию проекта:
```
cd web
```

3. Установить пакеты(Для linux):
```
apt-get install python3-venv
```

4. Создать виртуальную среду:
```
python3 -m venv env
```

5. Активировать среду:


linux:
```
source env/bin/activate
```
windows:


```
.\env\Scripts\activate
```
6. Установить зависимости из requirements.txt
```
pip3 install -r requirements.txt
```

7. Перейти на уровень выше и зайти в папку imit:
```
cd ..
cd  imit
```

8. Создать конфигурационный файл

linux:
```
touch imit_config.py
```

windows:
```
"">  imit_config.py
```

9. Заполнить конфигурационный файл. Пример содержимого файла настроек:
```
DEBUG = False
TESTING = False
LOG_FILE = "../imit/logs/imit.log"
SQLITE_DATABASE_PATH = "//path/to/sqlitedb/imit.db"
MYSQL_USER = "user"
MYSQL_PASSWORD = "pass"
MYSQL_HOST = "localhost"
MYSQL_DATABASE = "imit"
QLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASE)
```

10. Задать путь до конфигурационного файла в переменной IMIT_CONFIG:


linux:
```
export IMIT_CONFIG=/path/to/config/imit_config.py
```

windows:
```
set IMIT_CONFIG=/path/to/config/imit_config.py
$env:IMIT_CONFIG = "/path/to/config/imit_config.py"
```
11. Выполнить миграции базы данных. Для этого экспортируем переменную FLASK_APP


linux:
```
export FLASK_APP=imit/__init__.py
```

windows:
```
set FLASK_APP=imit/__init__.py
$env:FLASK_APP = "imit/__init__.py"
```
12. Выполняем миграции
```
flask db upgrade
```

13. Перейти в директорию с репозиторием проекта и запустить сервер
linux:
```
python3 runserver.py
```
windows:
```
python runserver.py
```

## Настройка сервер (linux)

1. Установить необходимые пакеты
```
apt-get install uwsgi nginx uwsgi-plugin-python3
```

2. Выполняем миграции для базы данных (см. пункт для запуска сервера для разработки).

3. Настроить uwsgi в файле /etc/uwsgi/apps-available/imit.ini Пример настройки:
```
[uwsgi]
appname = imit
base = /srv/www/imit
plugin = python3
socket = /var/run/%(appname).sock
chmod-socket = 600
chown-socket = www-data:www-data
threads = 40
master = 1
autoload = 1
env = IMIT_CONFIG=%(base)/imit/imit_config.py
module = %(appname):app
chdir = %(base)/app
logto = /srv/www/imit/log/imit-uwsgi.log
#logto = /var/log/uwsgi/%n.log
virtualenv = env
uid=imit
gid=www
```

4. Настроить nginx в файле /etc/nginx/sites-available/imit.conf Пример настройки:
```
server {
        listen 80;
        server_name XX.XX.XX.XX;
        #rewrite ^ https://imit.petrsu.ru/$request_uri;
        access_log  /srv/www/imit/log/imit.access.log;

	location = /favicon.ico { access_log off; log_not_found off; }
        root /srv/www/imit/app/imit/static;

        client_max_body_size 32m;

        location / {
                try_files $uri @imit;
        }

        location @imit {
            include uwsgi_params;
            uwsgi_modifier1 30;
            uwsgi_pass unix:/var/run/imit.sock;
        }
}
```
