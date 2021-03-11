from cc import import_file

net = import_file('/lib/net.py')

def main():
    host, proto, route = net.parse_url(args[0])
    print(net.get(route, host, proto))

if len(args) != 1:
    print('Usage: curl host:protocol/route')
else:
    main()
