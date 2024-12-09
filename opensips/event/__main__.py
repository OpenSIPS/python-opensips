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

""" OpenSIPS Event script """

import sys
import json
import time
import signal
import argparse
from opensips.mi import OpenSIPSMI
from opensips.event import OpenSIPSEventHandler, OpenSIPSEventException

parser = argparse.ArgumentParser()

communication = parser.add_argument_group('communication')

communication.add_argument('-t', '--type',
                           type=str,
                           default='fifo',
                           choices=['fifo', 'http', 'datagram'],
                           help='OpenSIPS MI Communication Type')
communication.add_argument('-i', '--ip',
                           type=str,
                           help='OpenSIPS MI IP Address',
                           default='127.0.0.1')
communication.add_argument('-p', '--port',
                           type=int,
                           help='OpenSIPS MI Port',
                           default=8888)
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

parser.add_argument('-bc', '--bash-complete',
                    type=str,
                    nargs='?',
                    const='',
                    help='Provide options for bash completion')

event = parser.add_argument_group('event')

event.add_argument('event',
                   type=str,
                   nargs='?',
                   help='OpenSIPS Event Name')

event.add_argument('-T', '--transport',
                   type=str,
                   choices=['datagram', 'stream'],
                   help='OpenSIPS Event Transport',
                   default='datagram')
event.add_argument('-li', '--listen-ip',
                   type=str,
                   help='OpenSIPS Event Listen IP Address',
                   default='0.0.0.0')
event.add_argument('-lp', '--listen-port',
                   type=int,
                   help='OpenSIPS Event Listen Port',
                   default=0)
event.add_argument('-e', '--expire',
                   type=int,
                   help='OpenSIPS Event Expire Time',
                   default=None)


def main():
    """ Main function of the opensips-event script """

    args = parser.parse_args()

    if args.type == 'fifo':
        fifo_args = {}
        if args.fifo_file:
            fifo_args['fifo_file'] = args.fifo_file
        if args.fifo_fallback:
            fifo_args['fifo_file_fallback'] = args.fifo_fallback
        if args.fifo_reply_dir:
            fifo_args['fifo_reply_dir'] = args.fifo_reply_dir
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
            print(f'ERROR: unknown type: {args.type}')
        sys.exit(1)

    if args.bash_complete is not None:
        if args.bash_complete != '':
            if len(args.bash_complete) > 1:
                last_arg = '--' + args.bash_complete
            else:
                last_arg = '-' + args.bash_complete
            
            for action in parser._actions:
                if last_arg in action.option_strings:
                    if action.choices:
                        print(' '.join(action.choices))
                    break
            sys.exit(0)
        else:
            options = []
            for action in parser._actions:
                for opt in action.option_strings:
                    options.append(opt)
            print(' '.join(options))
        try:
            response = mi.execute('events_list', [])
            events = response.get("Events", [])
            event_names = [event["name"] for event in events]
            print(' '.join(event_names))
            sys.exit(0)
        except Exception as e:
            sys.exit(1)

    if args.event is None:
        print(f'ERROR: unknown type: {args.type}')
        sys.exit(1)

    hdl = OpenSIPSEventHandler(mi, args.transport,
                               ip=args.listen_ip,
                               port=args.listen_port)

    def event_handler(message):
        """ Event handler callback """
        if message is None:
            ev.unsubscribe()
            sys.exit(1)

        try:
            print(json.dumps(message, indent=4))
        except json.JSONDecodeError as e:
            print(f"ERROR: failed to decode JSON: {e}")

    ev = None

    def timer(*_):
        """ Timer to notify when the event expires """
        ev.unsubscribe()
        sys.exit(0)  # successful

    if args.expire:
        signal.signal(signal.SIGALRM, timer)
        signal.alarm(args.expire)

    signal.signal(signal.SIGINT, timer)
    signal.signal(signal.SIGTERM, timer)

    try:
        ev = hdl.subscribe(args.event, event_handler, args.expire)
    except OpenSIPSEventException as e:
        print("ERROR:", e)
        sys.exit(1)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
