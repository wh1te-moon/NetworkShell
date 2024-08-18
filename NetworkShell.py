import asyncio
import asyncssh
import telnetlib3
import re
import os
import sys
import time
import readchar
import paramiko

from queue import Queue

from ColorThemeClass import ColorTheme

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
    # '\r': '\r\n'
}


class BaseConnection:
    async def connect(self):
        self.reader = None
        self.writer = None

    async def read(self, n=-1):
        return await self.reader.read(n)

    async def write(self, data):
        self.writer.write(data)

    async def close(self):
        raise NotImplementedError


class TelnetConnection(BaseConnection):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

    async def connect(self):
        self.reader, self.writer = await telnetlib3.open_connection(self.host, self.port)

    async def close(self):
        self.writer.close()
        await self.writer.protocol.waiter_closed


# class SSHConnection(BaseConnection):
#     def __init__(self, host, port, username, password):
#         self.host = host
#         self.port = port
#         self.username = username
#         self.password = password
#         self.reader = None
#         self.writer = None

#     async def connect(self):
#         self.client = await asyncssh.connect(self.host, port=self.port, username=self.username, password=self.password)
#         # self.writer,self.reader = await self.client.create_session(asyncssh.SSHClient,encoding='utf-8')
#         self.process = await self.client.create_process()
#         # print(self.process.env())
#         self.process._encoding = 'utf-8'
#         self.reader = self.process.stdout
#         self.writer = self.process.stdin
        
#     async def read(self, n=-1):
#         return await self.reader.readexactly(n)

#     async def close(self):
#         self.client.close()
#         await self.client.wait_closed()

class SSHConnection(BaseConnection):
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None
        self.channel = None
        self.char = ''

    async def connect(self):
        # Run the blocking SSH connection in a separate thread
        await asyncio.to_thread(self._connect)

    def _connect(self):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.connect(self.host, port=self.port, username=self.username, password=self.password)
        self.channel = self.client.invoke_shell()
        # self.timeout = 0.01
        # self.stdin = self.channel.recv
        # self.stdout = self.channel.send

    async def read(self, n=-1):
        # Read data from stdout in a separate thread
        async def _read(n):
            while True:
                if self.channel.recv_ready():
                    self.char = self.channel.recv(n).decode('utf-8')
                    break
                else:
                    await asyncio.sleep(0.1)
                    continue
        await _read(n)
        return self.char


    async def write(self, data:str):
        # Write data to stdin in a separate thread
        # print(data,end='')
        data = data.encode('utf-8')
        await asyncio.to_thread(self.channel.send, data)

    async def close(self):
        if self.client:
            await asyncio.to_thread(self.client.close)


async def readkey_async():
    loop = asyncio.get_event_loop()
    char = await loop.run_in_executor(None, readchar.readkey)
    return char


async def handle_input(writer:BaseConnection):
    while True:
        char = await readkey_async()
        if char is not None:
            if char in SPECIAL_KEYS:
                char = SPECIAL_KEYS[char]
            await writer.write(char)


async def handle_output(reader:BaseConnection):
    global device
    buffer = ''
    while True:
        while len(buffer) < 1024:
            try:
                # outp = await reader.read(1)
                # await asyncio.sleep(0.01)
                outp = await asyncio.wait_for(reader.read(1),timeout=0.01)
            except asyncio.TimeoutError:
                break
            except Exception as e:
                # print(e)
                break

            if not outp:
                break
            buffer += outp
            
            if outp == '\n':
                break

        if buffer:
            if not device:
                try:
                    device = re.search(r'(\S+)(?=[#>])', buffer).group(0)
                except AttributeError:
                    device = None

            if device:
                with open(f"./logs/{device}_{now}.txt", "a+") as f:
                    f.write(buffer)

            if len(buffer) > 1:
                buffer = ColorTheme.strProcess(buffer, PATTERNS_COLOR)
            print(buffer, end='', flush=True)
            buffer = ''



async def shell(conn: BaseConnection):
    await conn.connect()
    await asyncio.gather(
        handle_input(conn),
        handle_output(conn)
    )
    await conn.close()

loop = asyncio.get_event_loop()

# For Telnet connection
# telnet_conn = TelnetConnection("192.168.109.128", 32776)
# loop.run_until_complete(shell(telnet_conn))

# For SSH connection
ssh_conn = SSHConnection("192.168.255.1", 22, "root", "password")
loop.run_until_complete(shell(ssh_conn))
