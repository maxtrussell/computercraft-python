import requests

from cc import fs, parallel

BASE_URL = 'https://raw.githubusercontent.com/maxtrussell/computercraft-python/{}{}'
FILES = [
    "/bin/curl.py",
    "/bin/file_server.py",
    "/bin/quarry.py",
    "/bin/schematic.py",
    "/lib/dig.py",
    "/lib/fuel.py",
    "/lib/inv.py",
    "/lib/nav.py",
    "/lib/net.py",
    "/schematics/house.txt",
]

def wrapper(func, f, branch):
    def wrap():
        return func(f, branch)
    return wrap

def get_file(filename, branch):
    resp = requests.get(BASE_URL.format(branch, filename))
    resp.raise_for_status()
    with fs.open(filename, 'w') as f:
        f.write(resp.text)

for d in ['/lib', '/bin', '/docs', '/schematics', '/scripts']:
    if not fs.exists(d):
        fs.makeDir(d)

branch = args[0] if len(args) >= 1 else 'master'
print(f'Getting files asynchronously:')
for f in sorted(FILES):
    print(f)
parallel.waitForAll(*[wrapper(get_file, f, branch) for f in FILES])
