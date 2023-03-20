import os
import sys

if len(sys.argv) < 1:
    print("usage: python tr.py <command> <arguments>")
    sys.exit(1)

if sys.argv[1] == 'extract':
    os.system("pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot . ")
elif sys.argv[1] == 'init':
    if len(sys.argv) < 2:
        print("usage: python tr.py init <locale>")
        sys.exit(1)
    os.system("pybabel init -i messages.pot -d translations -l {}".format(sys.argv[2]))
elif sys.argv[1] == 'compile':
    os.system("pybabel compile -d translations")
elif sys.argv[1] == 'update':
    os.system("pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot . ")
    os.system("pybabel update -i messages.pot -d translations")
else:
    print("unknown command, available: extract, init, compile, update")
    sys.exit(1)
