#!/usr/bin/env python3
"""check_asterisk

Usage: check_asterisk -p <peer>

  Report issues to: https://github.com/mjmunger/check_asterisk

"""

import sys
import subprocess
from docopt import docopt


class Host:
    column_definitions = None
    name = None
    host = None
    status = None
    lagged = False
    ping_time = 0

    def __init__(self, column_definitions):
        self.column_definitions = column_definitions

    def parse_status(self):
        if "OK" in self.status:
            buffer = self.status.replace("OK (", "")
            self.ping_time = int(buffer.replace(" ms)", "").strip())

            if self.ping_time > 199:
                self.lagged = True
            else:
                self.lagged = False

            self.status = "OK"

    def parse_line(self, line):
        self.name = line[self.column_definitions.column_host:self.column_definitions.column_name].strip()

        if "/" in self.name:
            self.name = self.name.split("/")[0]

        self.host = line[self.column_definitions.column_name: self.column_definitions.column_dyn].strip()
        self.status = line[self.column_definitions.column_status: self.column_definitions.column_description].strip()
        self.parse_status()

    def __str__(self):
        return "Name: {0}\nHost: {1}\nStatus: {2}\nLagged: {3}\n".format(self.name, self.host, self.status, ("Yes" if self.lagged else "No"))

    def return_code(self):
        if self.status == "OK":
            if not self.lagged:
                return 0
            else:
                return 1

        if self.status == "UNREACHABLE":
            return 2

        if self.status == "UNKNOWN":
            return 3


class Columns:
    column_host = 0
    column_status = 0
    column_name = 0
    column_dyn = 0
    column_description = 0

    def __str__(self):
        return "Name: {0}\nHost: {1}\nStatus: {2}".format(self.column_name, self.column_host, self.column_status)


def find_columns(header_line):
    cols = Columns()
    cols.column_host = 0
    cols.column_name = header_line.find("Host")
    cols.column_status = header_line.find("Status")
    cols.column_dyn = header_line.find("Dyn")
    cols.column_description = header_line.find("Description")
    return cols

def show_help():
    print("""
Usage: check_asterisk.py -p [peer name]

Specify the peer name of the peer you want to check as it appears in the `sip show peers` command.
If a given peer also shows a username (name/username), the name to the left of the "/" is what is used.

Report issues to github: https://github.com/mjmunger/check_asterisk

    """)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='check_asterisk 0.1')

target_name = arguments['<peer>']

cmd = ('asterisk', '-rx', 'sip show peers')
ps = subprocess.Popen(cmd, stdout=subprocess.PIPE)
output = ps.communicate()[0].decode('utf-8')

lines = output.split("\n")
header = lines.pop(0)
columns = find_columns(header)
hosts = []
target_host = None

for line in lines:
    host = Host(columns)
    host.parse_line(line)
    if host.name == target_name:
        target_host = host

if target_host is None:
    sys.exit(3)

sys.exit(host.return_code())