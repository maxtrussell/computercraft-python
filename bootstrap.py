import requests

from cc import fs

BASE_URL = 'https://raw.githubusercontent.com/maxtrussell/computercraft-python/master'
BOOTSTRAP_FILE = 'download_code.py'

resp = requests.get(BASE_URL + '/' + BOOTSTRAP_FILE)
with fs.open(BOOTSTRAP_FILE, 'w') as f:
    f.write(resp.text)
