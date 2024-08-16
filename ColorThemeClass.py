# -*- coding: utf-8 -*-
"""带颜色打印输出;
"""
import re


class ColorTheme:
    def __init__(self):
        pass

    @staticmethod
    def white(s: str):
        """白色字体打印;
        """
        return f"\033[30m{s}\033[0m"

    @staticmethod
    def red(s: str):
        """
        红色的输出;
        :param s:
        :return:
        """
        return f"\033[31m{s}\033[0m"

    @staticmethod
    def green(s: str):
        """绿色字体的输出;
        """
        return f"\033[32m{s}\033[0m"

    @staticmethod
    def yellow(s: str):
        """黄色字体打印;
        """
        return f"\033[33m{s}\033[0m"

    @staticmethod
    def blue(s: str):
        """蓝色字体的打印;
        """
        return f"\033[34m{s}\033[0m"

    @staticmethod
    def purplish(s: str):
        """紫红色字体打印;
        """
        return f"\033[35m{s}\033[0m"

    @staticmethod
    def cyan(s: str):
        """青色字体的打印;
        """
        return f"\033[36m{s}\033[0m"

    @staticmethod
    def black(s: str):
        """黑色字体打印;
        """
        return f"\033[37m{s}\033[0m"

    @staticmethod
    def strProcess(s: str, pattern: list[str], color: list[str] = ["purplish", "red", "green", "yellow", "blue", "cyan"]):
        func = {
            "purplish": ColorTheme.purplish,
            "red": ColorTheme.red,
            "green": ColorTheme.green,
            "yellow": ColorTheme.yellow,
            "blue": ColorTheme.blue,
            "cyan": ColorTheme.cyan
        }
        for pat, col in zip(pattern, color):
            matches = re.findall(pat, s)
            for match in matches:
                if not isinstance(match,str):
                    match=match[0]
                s = s.replace(match, func[col](match))
                pass
            pass
        return s


if __name__ == '__main__':
    # IP_REGEX="([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"
    # ipv4=f"{IP_REGEX}\.{IP_REGEX}\.{IP_REGEX}\.{IP_REGEX}"
    ipv4 = "(?:(?:1[0-9][0-9]\.)|(?:2[0-4][0-9]\.)|(?:25[0-5]\.)|(?:[1-9][0-9]\.)|(?:[0-9]\.)){3}(?:(?:1[0-9][0-9])|(?:2[0-4][0-9])|(?:25[0-5])|(?:[1-9][0-9])|(?:[0-9]))"
    
    mac = "(?:(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2}))"
    
    ipv6="(?:(?:(?:[0-9A-Fa-f]{1,4}:){7}(?:[0-9A-Fa-f]{1,4}|:))|(?:(?:[0-9A-Fa-f]{1,4}:){6}(?::[0-9A-Fa-f]{1,4}|(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(?:(?:[0-9A-Fa-f]{1,4}:){5}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,2})|:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(?:(?:[0-9A-Fa-f]{1,4}:){4}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,3})|(?:(?::[0-9A-Fa-f]{1,4})?:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){3}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,4})|(?:(?::[0-9A-Fa-f]{1,4}){0,2}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){2}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,5})|(?:(?::[0-9A-Fa-f]{1,4}){0,3}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){1}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,6})|(?:(?::[0-9A-Fa-f]{1,4}){0,4}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?::(?:(?:(?::[0-9A-Fa-f]{1,4}){1,7})|(?:(?::[0-9A-Fa-f]{1,4}){0,5}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))"
    PATTERNS = [
        # ipv4,
        # mac,
        ipv6
    ]
    input = "在网络配置中，服务器的IPv4地址是192.168.1.10，而另一台设备的IPv4地址则为10.0.0.254。对于IPv6地址，主服务器使用的是2001:0db8:85a3:0000:0000:8a2e:0370:7334，而备份服务器的IPv6地址是fe80::1ff:fe23:4567:890a。同时，网络交换机的MAC地址为00:1A:2B:3C:4D:5E，而路由器的MAC地址则是AA-BB-CC-DD-EE-FF。"
    print(ColorTheme.strProcess(input, PATTERNS))
