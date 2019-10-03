import os, sys
if len(sys.argv) != 2:
    print("usage: i18n_init <language-code>")
    sys.exit(1)
os.system('pybabel -v extract -F babel.cfg -o mercure.pot .')
os.system('pybabel init -i mercure.pot -d locales -l ' + sys.argv[1])
os.unlink('mercure.pot')