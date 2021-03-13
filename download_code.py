import argparse
import requests

from cc import fs, parallel

BASE_URL = 'https://raw.githubusercontent.com/maxtrussell/computercraft-python/{}{}'
FILES = [
    "/bootstrap.lua",
    "/bin/curl.py",
    "/bin/farm.py",
    "/bin/main_server.py",
    "/bin/quarry.py",
    "/bin/schematic.py",
    "/lib/dig.py",
    "/lib/fuel.py",
    "/lib/inv.py",
    "/lib/nav.py",
    "/lib/net.py",
]
EXTRAS = [
    "/docs/cords.txt",
    "/schematics/house.txt",
    "/schematics/greenhouse.txt",
    "/tests/navigate.py",
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

parser = argparse.ArgumentParser(prog=__file__)
parser.add_argument('branch', nargs='?', default='master', help='target branch, defaults to master')
parser.add_argument('--all', '-a', action='store_true', help='download all files')
parser.add_argument('--extra', '-e', action='store_true', help='download extra files only')
args = parser.parse_args(args=args)

target_files = FILES
if args.all:
    target_files += EXTRAS
elif args.extra:
    target_files = EXTRAS

print(f'Getting files asynchronously:')
for f in sorted(target_files):
    print(f)
parallel.waitForAll(*[wrapper(get_file, f, args.branch) for f in target_files])
