import asyncio
import sys
import time
import os

from NetworkShellClass import SSHConnection,TelnetConnection

IPV4 = "(?:(?:1[0-9][0-9]\.)|(?:2[0-4][0-9]\.)|(?:25[0-5]\.)|(?:[1-9][0-9]\.)|(?:[0-9]\.)){3}(?:(?:1[0-9][0-9])|(?:2[0-4][0-9])|(?:25[0-5])|(?:[1-9][0-9])|(?:[0-9]))"

MAC = "(?:(?:[0-9A-Fa-f]{2}[:\-.]){5}(?:[0-9A-Fa-f]{2}))"

IPV6 = "(?:(?:(?:[0-9A-Fa-f]{1,4}:){7}(?:[0-9A-Fa-f]{1,4}|:))|(?:(?:[0-9A-Fa-f]{1,4}:){6}(?::[0-9A-Fa-f]{1,4}|(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(?:(?:[0-9A-Fa-f]{1,4}:){5}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,2})|:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(?:(?:[0-9A-Fa-f]{1,4}:){4}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,3})|(?:(?::[0-9A-Fa-f]{1,4})?:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){3}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,4})|(?:(?::[0-9A-Fa-f]{1,4}){0,2}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){2}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,5})|(?:(?::[0-9A-Fa-f]{1,4}){0,3}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){1}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,6})|(?:(?::[0-9A-Fa-f]{1,4}){0,4}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?::(?:(?:(?::[0-9A-Fa-f]{1,4}){1,7})|(?:(?::[0-9A-Fa-f]{1,4}){0,5}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))"

SHUTDOWN = "shutdown"

PATTERNS_COLOR = {
    IPV4: "green",
    MAC: "green",
    IPV6: "green",
    SHUTDOWN: "red"
}

LOGS_FOLDER = "./logs"

if(not os.path.isabs(LOGS_FOLDER)):
    os.chdir(os.path.dirname(__file__))

if not os.path.exists(LOGS_FOLDER):
    os.makedirs(LOGS_FOLDER)
    print("logs folder not found")
    print("logs folder created\n")
else:
    print("logs folder found\n")

arguments = sys.argv

now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

device = None

log_file = None

SPECIAL_KEYS = {
    '\x00H': '\x1b[A',  # up
    '\x00P': '\x1b[B',  # down
    '\x00K': '\x1b[D',  # left
    '\x00M': '\x1b[C',  # right

    '\x007': '\x1b[3~',  # delete
    '\x01': '\x1b[H',  # Home
    '\x05': '\x1b[F',  # End
}

try:
    # format ip port
    host = arguments[1]
    port = int(arguments[2])
    print(f"connecting to {host} on port {port}")
except IndexError:
    # format 'telnet://ip:port/' or 'ssh://ip:port/'
    try:
        colon_index = arguments[1].find(":")
        arguments[1] = arguments[1][colon_index+3:]
        colon_index = arguments[1].find(":")
        host = arguments[1][:colon_index]
        port = int(arguments[1][colon_index+1:-1])
        print(f"connecting to {host} on port {port}")
    except Exception:
        print(f"{arguments}\tinput error")
        pass

method = "ssh" if len(arguments)<=3 else "telnet"
if method == "ssh":
    # format prefix username password 
    username = arguments[-2]
    password = arguments[-1]


loop = asyncio.get_event_loop()
if method == "ssh":
    conn = SSHConnection(host, port, username, password)
else:
    conn = TelnetConnection(host, port)
loop.run_until_complete(conn.shell())