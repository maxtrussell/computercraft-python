import requests

from cc import fs

BASE_URL = 'https://raw.githubusercontent.com/maxtrussell/computercraft-python/{}'
FILES = [
    "/bin/quarry.py",
    "/lib/inv.py",
    "/lib/refuel.py"
]

branch = 'master'
if len(args) == 1:
    branch = args[0]

def get_file(filename):
    resp = requests.get(BASE_URL.format(branch) + filename)
    resp.raise_for_status()

    print(f'Getting {filename}...')
    with fs.open(filename, 'w') as f:
        f.write(resp.text)

for d in ['/lib', '/bin', '/scripts']:
    if not fs.exists(d):
        fs.makeDir(d)

for f in FILES:
    get_file(f)
