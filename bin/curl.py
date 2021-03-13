from cc import import_file

net = import_file('/lib/net.py')

if len(args) != 1:
    print('Usage: curl host:protocol/route')
else:
    print(net.request(args[0]))
