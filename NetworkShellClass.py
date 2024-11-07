import asyncio
# import asyncssh
import telnetlib3
import re
import os
import sys
import time
import readchar
import paramiko

from queue import Queue

from ColorThemeClass import ColorTheme

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
    
    def __init__(self, pattern_color={}, log_folder="./logs/"):
        self.reader = None
        self.writer = None
        self.pattern_color = pattern_color
        self.now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        self.log_folder = log_folder
        self.device = None

    async def read(self, n=-1):
        return await self.reader.read(n)

    async def write(self, data):
        self.writer.write(data)

    async def close(self):
        raise NotImplementedError
    
    async def connect(self):
        raise NotImplementedError

    @staticmethod
    async def readkey_async():
        loop = asyncio.get_event_loop()
        char = await loop.run_in_executor(None, readchar.readkey)
        return char

    async def handle_input(self):
        while True:
            char = await BaseConnection.readkey_async()
            if char is not None:
                if char in SPECIAL_KEYS:
                    char = SPECIAL_KEYS[char]
                await self.write(char)

    async def handle_output(self):
        buffer = ''
        while True:
            while len(buffer) < 1024:
                try:
                    outp = await asyncio.wait_for(self.read(1), timeout=0.04)
                except asyncio.TimeoutError:
                    break
                except Exception as e:
                    break

                if not outp:
                    break
                buffer += outp

                if outp == '\n':
                    break

            if buffer:
                if not self.device:
                    try:
                        self.device = re.search(
                            r'(\S+)(?=[#>])', buffer).group(0)
                        self.device = re.sub(r'[^\w]', '', self.device)
                    except AttributeError:
                        self.device = None

                if self.device:
                    with open(f"{self.log_folder}/{self.device}_{self.now}.txt", "a+") as f:
                        f.write(buffer)

                if len(buffer) > 1:
                    buffer = ColorTheme.STRToColoredSTR(buffer, self.pattern_color)
                print(buffer, end='', flush=True)
                buffer = ''

    async def shell(self, *args):
        await self.connect(*args)
        await asyncio.gather(
            self.handle_input(),
            self.handle_output()
        )
        await self.close()


class TelnetConnection(BaseConnection):
    def __init__(self,*args) -> None:
        super().__init__(*args)
    
    async def connect(self, host, port):
        self.host = host
        self.port = port
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
    def __init__(self,*args) -> None:
        super().__init__(*args)
    
    async def connect(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        # Run the blocking SSH connection in a separate thread
        await asyncio.to_thread(self._connect)

    def _connect(self):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.connect(self.host, port=self.port,
                            username=self.username, password=self.password)
        self.channel = self.client.invoke_shell()

    async def read(self, n=-1):
        while True:
            if self.channel.recv_ready():
                self.char = self.channel.recv(n).decode('utf-8')
                break
            else:
                await asyncio.sleep(0.01)
                continue
        return self.char

    async def write(self, data: str):
        # Write data to stdin in a separate thread
        # print(data,end='')
        data = data.encode('utf-8')
        await asyncio.to_thread(self.channel.send, data)

    async def close(self):
        if self.client:
            await asyncio.to_thread(self.client.close)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    # For Telnet connection
    # telnet_conn = TelnetConnection("192.168.109.128", 32776)
    # loop.run_until_complete(shell(telnet_conn))

    # For SSH connection
    ssh_conn = SSHConnection()
    loop.run_until_complete(ssh_conn.shell(
        "192.168.1.1", 22, "root", "password"))
