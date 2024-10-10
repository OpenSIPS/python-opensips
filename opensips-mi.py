import argparse
from opensips.mi import OpenSIPSMI, OpenSIPSMIException
import json
  
parser = argparse.ArgumentParser()

communication = parser.add_argument_group('communication')

communication.add_argument('-t', '--type',
                    type=str,
                    help='OpenSIPS MI Communication Type',
                    default='http')
communication.add_argument('-i', '--ip',
                    type=str,
                    help='OpenSIPS MI IP Address',
                    default='127.0.0.1')
communication.add_argument('-p', '--port',
                    type=int,
                    help='OpenSIPS MI Port',
                    default=8888)

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('-s', '--stats',
                    nargs='+',                                                                                                                                                     
                    default=[],
                    help='statistics')

group.add_argument('command',
                    nargs='?',
                    type=str,
                    help='command')

group = parser.add_mutually_exclusive_group(required=False)

group.add_argument('-j', '--json',
                    type=str,
                    help='json',
                    required=False)

group.add_argument('parameters',
                    nargs='*',
                    default=[],
                    help='cmd args')

args = parser.parse_args()
print(args)

if args.stats:
    print('Using get_statistics! Be careful not to use command after -s/--stats.')
    print(args.stats)
    args.command = 'get_statistics'

    if args.json:
        print('Cannot use -s/--stats with -j/--json!')
        exit(1)

    args.parameters = {'statistics': args.stats}
else:
    if args.json:
        try:
            args.parameters = json.loads(args.json)
            print(args.parameters)
        except json.JSONDecodeError as e:
            print('Invalid JSON: ', e)
            exit(1)
    
if args.type == 'http':
    mi = OpenSIPSMI('http', url='http://{}:{}/mi'.format(args.ip, args.port))

if args.type == 'datagram':
    mi = OpenSIPSMI('datagram', datagram_ip=args.ip, datagram_port=args.port)

try:
    response = mi.execute(args.command, args.parameters)
    print(json.dumps(response, indent=4))
except OpenSIPSMIException as e:
    print('Error: ', e)
    exit(1)
