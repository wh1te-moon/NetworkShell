import asyncio
import sys
import time
import os

from NetworkShellClass import SSHConnection, TelnetConnection

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

if (not os.path.isabs(LOGS_FOLDER)):
    os.chdir(os.path.dirname(__file__))
    LOGS_FOLDER = os.path.abspath(LOGS_FOLDER)

if not os.path.exists(LOGS_FOLDER):
    os.makedirs(LOGS_FOLDER)
    print("logs folder not found")
    print(f"logs folder created {LOGS_FOLDER}\n")
else:
    print(f"logs folder found {LOGS_FOLDER}\n")

arguments = sys.argv
# arguments = ["", "192.168.1.1", "22", "root", "password"]

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

method = "telnet" if len(arguments) <= 3 else "ssh"
if method == "ssh":
    # format prefix username password
    username = arguments[-2]
    password = arguments[-1]


loop = asyncio.get_event_loop()
if method == "ssh":
    conn = SSHConnection(PATTERNS_COLOR, LOGS_FOLDER)
    loop.run_until_complete(conn.shell(host, port, username, password))
else:
    conn = TelnetConnection(PATTERNS_COLOR, LOGS_FOLDER)
    loop.run_until_complete(conn.shell(host, port))
