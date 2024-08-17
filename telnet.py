import asyncio
import sys
import telnetlib3
import readchar

from ColorThemeClass import ColorTheme

IPV4 = "(?:(?:1[0-9][0-9]\.)|(?:2[0-4][0-9]\.)|(?:25[0-5]\.)|(?:[1-9][0-9]\.)|(?:[0-9]\.)){3}(?:(?:1[0-9][0-9])|(?:2[0-4][0-9])|(?:25[0-5])|(?:[1-9][0-9])|(?:[0-9]))"

MAC = "(?:(?:[0-9A-Fa-f]{2}[:-.]){5}(?:[0-9A-Fa-f]{2}))"

IPV6 = "(?:(?:(?:[0-9A-Fa-f]{1,4}:){7}(?:[0-9A-Fa-f]{1,4}|:))|(?:(?:[0-9A-Fa-f]{1,4}:){6}(?::[0-9A-Fa-f]{1,4}|(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(?:(?:[0-9A-Fa-f]{1,4}:){5}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,2})|:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(?:(?:[0-9A-Fa-f]{1,4}:){4}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,3})|(?:(?::[0-9A-Fa-f]{1,4})?:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){3}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,4})|(?:(?::[0-9A-Fa-f]{1,4}){0,2}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){2}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,5})|(?:(?::[0-9A-Fa-f]{1,4}){0,3}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){1}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,6})|(?:(?::[0-9A-Fa-f]{1,4}){0,4}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?::(?:(?:(?::[0-9A-Fa-f]{1,4}){1,7})|(?:(?::[0-9A-Fa-f]{1,4}){0,5}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))"

SHUTDOWN = "shutdown"

PATTERNS_COLOR = {
    IPV4: "green",
    MAC: "green",
    IPV6: "green",
    SHUTDOWN: "red"
}

arguments = sys.argv

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
    HOST = arguments[1]
    PORT = int(arguments[2])
    print(f"connecting to {HOST} on port {PORT}")
except IndexError:
    # format 'telnet://ip:port/'
    try:
        colon_index = arguments[1].find(":")
        arguments[1] = arguments[1][colon_index+3:]
        colon_index = arguments[1].find(":")
        HOST = arguments[1][:colon_index]
        PORT = int(arguments[1][colon_index+1:-1])
        print(f"connecting to {HOST} on port {PORT}")
    except Exception:
        print(f"{arguments}\ninput error")
        pass


async def readkey_async():
    loop = asyncio.get_event_loop()
    char = await loop.run_in_executor(None, readchar.readkey)
    return char


async def handle_input(writer):
    while True:
        char = await readkey_async()
        if char is not None:
            if char in SPECIAL_KEYS:
                char = SPECIAL_KEYS[char]
            writer.write(char)


async def handle_output(reader: telnetlib3.TelnetReader):
    buffer = ''
    while True:
        while len(buffer) < 1024:
            try:
                outp = await asyncio.wait_for(reader.read(1), timeout=0.01)
            except asyncio.TimeoutError:
                break

            if not outp:
                break
            buffer += outp
            if outp == '\n':
                break

        if buffer:
            if (len(buffer) > 1):
                buffer = ColorTheme.strProcess(buffer, PATTERNS_COLOR)
            print(buffer, end='', flush=True)

            # with open("./output.txt", "a") as f:
            #     f.write("\nBUFFER\n")
            #     f.write(buffer)
            #     f.write("\nBUFFER\n")

            buffer = ''


async def shell(reader: telnetlib3.TelnetReader, writer: telnetlib3.TelnetWriter):
    writer.write('\n')
    await asyncio.gather(
        handle_input(writer),
        handle_output(reader)
    )

loop = asyncio.get_event_loop()
coro = telnetlib3.open_connection(HOST, PORT, shell=shell)
# coro=telnetlib3.open_connection("192.168.109.128", 32776, shell=shell)
reader, writer = loop.run_until_complete(coro)
loop.run_until_complete(writer.protocol.waiter_closed)
