import os
os.system('pybabel extract -F babel.cfg -o mercure.pot .')
os.system('pybabel update -i mercure.pot -d locales')
os.unlink('mercure.pot')