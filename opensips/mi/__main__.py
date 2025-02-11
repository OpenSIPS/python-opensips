#!/usr/bin/env python
#
# This file is part of the OpenSIPS Python Package
# (see https://github.com/OpenSIPS/python-opensips).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

""" Script to run OpenSIPS MI commands """

import sys
import json
import os
import argparse
from opensips.mi import OpenSIPSMI, OpenSIPSMIException


def load_env_file(env_file_path):
    if not os.path.isfile(env_file_path):
        return
    with open(env_file_path) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

parser = argparse.ArgumentParser()

parser.add_argument('--env-file',
                    type=str,
                    default='.env',
                    help='Load environment variables from file')

communication = parser.add_argument_group('communication')

communication.add_argument('-t', '--type',
                           type=str,
                           choices=['fifo', 'http', 'datagram'],
                           help='OpenSIPS MI Communication Type')
communication.add_argument('-i', '--ip',
                           type=str,
                           help='OpenSIPS MI IP Address')
communication.add_argument('-p', '--port',
                           type=int,
                           help='OpenSIPS MI Port')
communication.add_argument('-f', '--fifo-file',
                           metavar='FIFO_FILE',
                           type=str,
                           help='OpenSIPS MI FIFO File')
communication.add_argument('-fb', '--fifo-fallback',
                           metavar='FIFO_FALLBACK_FILE',
                           type=str,
                           help='OpenSIPS MI Fallback FIFO File')
communication.add_argument('-fd', '--fifo-reply-dir',
                           metavar='FIFO_DIR',
                           type=str,
                           help='OpenSIPS MI FIFO Reply Directory')

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('-s', '--stats',
                   nargs='+',
                   default=[],
                   help='statistics')

group.add_argument('command',
                   nargs='?',
                   type=str,
                   help='command')

group.add_argument('-bc', '--bash-complete',
                    type=str,
                    nargs='?',
                    const='commands',
                    help='Provide options for bash completion')

group = parser.add_mutually_exclusive_group(required=False)

group.add_argument('-j', '--json',
                   type=str,
                   help='json',
                   required=False)

group.add_argument('parameters',
                   nargs='*',
                   default=[],
                   help='cmd args')


def main():
    """ Main function of the opensips-mi script """
    args = parser.parse_args()

    load_env_file(args.env_file)

    if not args.type:
        args.type = os.getenv('OPENSIPS_MI_TYPE', 'fifo')
    if not args.ip:
        args.ip = os.getenv('OPENSIPS_MI_IP', '127.0.0.1')
    if not args.port:
        args.port = os.getenv('OPENSIPS_MI_PORT', 8080)
    if not args.fifo_file:
        args.fifo_file = os.getenv('OPENSIPS_MI_FIFO_FILE', '/var/run/opensips/opensips_fifo')
    if not args.fifo_fallback:
        args.fifo_fallback = os.getenv('OPENSIPS_MI_FIFO_FALLBACK', '/tmp/opensips_fifo')
    if not args.fifo_reply_dir:
        args.fifo_reply_dir = os.getenv('OPENSIPS_MI_FIFO_REPLY_DIR', '/tmp/')

    if args.type == 'fifo':
        fifo_args = {
            'fifo_file': args.fifo_file,
            'fifo_file_fallback': args.fifo_fallback,
            'fifo_reply_dir': args.fifo_reply_dir,
        }
        mi = OpenSIPSMI('fifo', **fifo_args)
    elif args.type == 'http':
        mi = OpenSIPSMI('http', url=f'http://{args.ip}:{args.port}/mi')
    elif args.type == 'datagram':
        mi = OpenSIPSMI('datagram',
                        datagram_ip=args.ip,
                        datagram_port=args.port,
                        timeout=0.1)
    else:
        if not args.bash_complete:
            print(f'Unknown type: {args.type}')
        sys.exit(1)


    if args.bash_complete is not None:
        if args.bash_complete not in ['params', 'commands']:
            last_arg = '--' + args.bash_complete if len(args.bash_complete) > 1 else '-' + args.bash_complete
            
            for action in parser._actions:
                if last_arg in action.option_strings:
                    if action.choices:
                        print(' '.join(action.choices))
                    break
            sys.exit(0)

        if args.bash_complete == 'params':
            options = []
            for action in parser._actions:
                for opt in action.option_strings:
                    options.append(opt)
            print(' '.join(options))
            sys.exit(0)

        # if args.bash_complete == 'commands':
        try:
            response = mi.execute('which', [])
            print(" ".join(response))
            sys.exit(0)
        except Exception as e:
            options = []
            for action in parser._actions:
                for opt in action.option_strings:
                    options.append(opt)
            print(' '.join(options))
            sys.exit(0)

    if args.stats:
        args.command = 'get_statistics'

        if args.json:
            print('ERROR: cannot use -s/--stats with -j/--json!')
            sys.exit(1)

        args.parameters = {'statistics': args.stats}
    else:
        if args.json:
            try:
                args.parameters = json.loads(args.json)
            except json.JSONDecodeError as e:
                print('ERROR: invalid JSON: ', e)
                sys.exit(1)

    try:
        response = mi.execute(args.command, args.parameters)
        print(json.dumps(response, indent=4))
    except OpenSIPSMIException as e:
        print('ERROR: ', e)
        sys.exit(1)


if __name__ == "__main__":
    main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
