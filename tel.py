import telnetlib
import readchar
import sys
import time

# 获取命令行参数列表
arguments = sys.argv

# get ip address and port from arguments
# host = arguments[1]
# port = int(arguments[2])
host="10.255.255.1"
port=5021

special_keys = {
    # '\x03': 'Ctrl+C',
    # '\x04': 'Ctrl+D',
    # '\x1a': 'Ctrl+Z',
    # '\r': '',
    # '\n': '',
    '\x00H':'\x1b[A',#up
    '\x00P':'\x1b[B',#down
    '\x00K':'\x1b[C',#left
    '\x00M':'\x1b[D',#right
    # '\x1b[A': 'Up',    # ANSI转义序列表示向上箭头键
    # '\x1b[B': 'Down',  # ANSI转义序列表示向下箭头键
    # '\x1b[C': 'Right', # ANSI转义序列表示向右箭头键
    # '\x1b[D': 'Left',  # ANSI转义序列表示向左箭头键
}

# 创建一个Telnet对象
tn = telnetlib.Telnet(host, port)

# 不断循环，接收用户输入的命令
result = tn.read_very_eager().decode('ascii')
print(result, end="")
while True:
    result = tn.read_very_eager().decode('ascii')
    print(result, end="")
    
    # 获取用户输入的命令
    # command = ""
    # while True:
    #     char = readchar.readkey()
    #     if char == '\r' or char == '\n':
    #         break
    #     if char in special_keys:
    #         command += special_keys[char]
    #         break
    #     else:
    #         command += char
    char = readchar.readkey()
    if char in special_keys:
        char= special_keys[char]
    # 发送命令到远程主机
    tn.write(char.encode('ascii'))
