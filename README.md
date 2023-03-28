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
""> newfile
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

