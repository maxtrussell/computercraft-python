from cc import fs, import_file, rednet, redstone

net = import_file('/lib/net.py')

HOSTNAME = 'main-server'
PROTOCOLS = ['FILE', 'FUEL']

def router(route, proto):
    if proto == 'FILE':
        if fs.exists(route):
            return list_dir if fs.isDir(route) else serve_file
    elif proto == 'FUEL':
        return handle_fuel
    return None

def serve_file(client_id, route, protocol):
    with fs.open(route, 'r') as f:
        net.send('\n'.join(list(f)), client_id, protocol)

def list_dir(client_id, route, protocol):
    net.send('\n'.join(fs.list(route)), client_id, protocol)

def handle_fuel(client_id, route, protocol):
    low_turtles = []
    if fs.exists('/docs/fuel.txt') and not fs.isDir('/docs/fuel.txt'):
        with fs.open('/docs/fuel.txt', 'r') as f:
            low_turtles = list(f)

    if route == '/ok':
        low_turtles = [t for t in low_turtles if t != str(client_id)]
    elif route == '/low':
        low_turtles = list(set(low_turtles + [str(client_id)]))

    with fs.open('/docs/fuel.txt', 'w') as f:
        for t in low_turtles:
            f.writeLine(t)

    # emit redstone if there are turtles low on fuel
    redstone.setOutput('bottom', bool(low_turtles))

    net.send('200: ACK', client_id, protocol)

def setup_hostname(protocols):
    for proto in protocols:
        rednet.host(proto, HOSTNAME)

setup_hostname(PROTOCOLS)
handle_fuel(0, '/ok', 'FUEL')
net.listen_and_serve(HOSTNAME, None, router)
