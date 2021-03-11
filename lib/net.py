from cc import peripheral, rednet

SIDES = ['left', 'right', 'top', 'bottom', 'front', 'back']
modem = None

class InvalidUrlException(Exception):
    pass

class HostNotFoundException(Exception):
    pass

class RednetConnectionException(Exception):
    pass

def connect():
    global modem
    if modem is not None and rednet.isOpen(modem):
        return True

    for side in SIDES:
        if peripheral.getType(side) == 'modem':
            rednet.open(side)
            if rednet.isOpen(side):
                modem = side
                return
    raise RednetConnectionException('Could not establish connection. Is a modem attached?')

def get_id(host, protocol):
    connect()
    id = rednet.lookup(protocol, host)
    if id is None:
        print(f'No such host "{host}" on protocol "{protocol}"')
    return id

def send_to_host(msg, host, protocol):
    connect()
    id = get_id(host, protocol)
    if not id:
        raise HostNotFoundException(f'Host "{host}" not found')
    send(msg, id, protocol)

def send(msg, id, protocol):
    # can only send byte strings
    if isinstance(msg, str):
        msg = msg.encode('utf-8')
    rednet.send(id, msg, protocol)

def get(msg, host, protocol):
    """ Very roughly an HTTP GET """
    connect()
    send_to_host(msg, host, protocol)
    resp = rednet.receive(protocol, 5)
    if resp:
        return resp[1].decode('utf-8')  # returns response message

def broadcast(msg, protocol):
    connect()
    rednet.broadcast(msg, protocol)
    
def listen(protocol, id=None):
    connect()
    while True:
        sender_id, msg, _ = rednet.receive(protocol)
        msg = msg.decode('utf-8')
        if id is None or sender_id == id:
            return sender_id, msg

def parse_url(url):
    # TODO: this is way too lazy atm
    if ':' not in url or '/' not in url:
        raise InvalidUrlException(f'Invalid URL {url}')
    host, tail = url.split(':', 1)
    proto, route = tail.split('/', 1)
    return host, proto, '/' + route

def listen_and_serve(hostname, protocol, router):
    # BYOF -- bring your own functions
    connect()
    rednet.host(protocol, hostname)

    while True:
        client_id, msg = listen(protocol)
        print(f'Request from {client_id}: {msg}')
        func = router(msg)
        if func is not None:
            func(client_id, msg, protocol)
        else:
            send(f'404: {msg} not found', client_id, protocol)
