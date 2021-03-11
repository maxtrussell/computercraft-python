""" An example file server """

from cc import fs, import_file

net = import_file('/lib/net.py')

HOSTNAME = 'file-server'
PROTOCOL = 'FILE'

def router(route):
    if fs.exists(route):
        if not fs.isDir(route):
            return serve_file
        else:
            return list_dir
    return None

def serve_file(client_id, route, protocol):
    with fs.open(route, 'r') as f:
        net.send('\n'.join(list(f)), client_id, protocol)

def list_dir(client_id, route, protocol):
    net.send('\n'.join(fs.list(route)), client_id, protocol)

net.listen_and_serve(HOSTNAME, PROTOCOL, router)
