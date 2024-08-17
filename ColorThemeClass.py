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
        return f"\033[30m\033[1m{s}\033[0m"

    @staticmethod
    def red(s: str):
        """
        红色的输出;
        :param s:
        :return:
        """
        return f"\033[31m\033[1m{s}\033[0m"

    @staticmethod
    def green(s: str):
        """绿色字体的输出;
        """
        return f"\033[32m\033[1m{s}\033[0m"

    @staticmethod
    def yellow(s: str):
        """黄色字体打印;
        """
        return f"\033[33m\033[1m{s}\033[0m"

    @staticmethod
    def blue(s: str):
        """蓝色字体的打印;
        """
        return f"\033[34m\033[1m{s}\033[0m"

    @staticmethod
    def purplish(s: str):
        """紫红色字体打印;
        """
        return f"\033[35m\033[1m{s}\033[0m"

    @staticmethod
    def cyan(s: str):
        """青色字体的打印;
        """
        return f"\033[36m\033[1m{s}\033[0m"

    @staticmethod
    def black(s: str):
        """黑色字体打印;
        """
        return f"\033[37m\033[1m{s}\033[0m"

    @staticmethod
    def strProcess(s: str, pattern_color: dict[str, str]):
        func = {
            "purplish": ColorTheme.purplish,
            "red": ColorTheme.red,
            "green": ColorTheme.green,
            "yellow": ColorTheme.yellow,
            "blue": ColorTheme.blue,
            "cyan": ColorTheme.cyan,
            "white": ColorTheme.white,
            "black": ColorTheme.black
        }
        for pat, col in pattern_color.items():
            matches = re.findall(pat, s)
            for match in matches:
                if not isinstance(match, str):
                    match = match[0]
                s = s.replace(match, func.get(col.lower(),ColorTheme.cyan)(match))
        return s



if __name__ == '__main__':
    
    # Regular Colors
    Black="\[\033[0;30m\]"        # Black
    Red="\[\033[0;31m\]"          # Red
    Green="\[\033[0;32m\]"        # Green
    Yellow="\[\033[0;33m\]"       # Yellow
    Blue="\[\033[0;34m\]"         # Blue
    Purple="\[\033[0;35m\]"       # Purple
    Cyan="\[\033[0;36m\]"         # Cyan
    White="\[\033[0;37m\]"        # White

    # Bold
    BBlack="\[\033[1;30m\]"       # Black
    BRed="\[\033[1;31m\]"         # Red
    BGreen="\[\033[1;32m\]"       # Green
    BYellow="\[\033[1;33m\]"      # Yellow
    BBlue="\[\033[1;34m\]"        # Blue
    BPurple="\[\033[1;35m\]"      # Purple
    BCyan="\[\033[1;36m\]"        # Cyan
    BWhite="\[\033[1;37m\]"       # White

    # Underline
    UBlack="\[\033[4;30m\]"       # Black
    URed="\[\033[4;31m\]"         # Red
    UGreen="\[\033[4;32m\]"       # Green
    UYellow="\[\033[4;33m\]"      # Yellow
    UBlue="\[\033[4;34m\]"        # Blue
    UPurple="\[\033[4;35m\]"      # Purple
    UCyan="\[\033[4;36m\]"        # Cyan
    UWhite="\[\033[4;37m\]"       # White

    # Background
    On_Black="\[\033[40m\]"       # Black
    On_Red="\[\033[41m\]"         # Red
    On_Green="\[\033[42m\]"       # Green
    On_Yellow="\[\033[43m\]"      # Yellow
    On_Blue="\[\033[44m\]"        # Blue
    On_Purple="\[\033[45m\]"      # Purple
    On_Cyan="\[\033[46m\]"        # Cyan
    On_White="\[\033[47m\]"       # White

    # High Intensty
    IBlack="\[\033[0;90m\]"       # Black
    IRed="\[\033[0;91m\]"         # Red
    IGreen="\[\033[0;92m\]"       # Green
    IYellow="\[\033[0;93m\]"      # Yellow
    IBlue="\[\033[0;94m\]"        # Blue
    IPurple="\[\033[0;95m\]"      # Purple
    ICyan="\[\033[0;96m\]"        # Cyan
    IWhite="\[\033[0;97m\]"       # White

    # Bold High Intensty
    BIBlack="\[\033[1;90m\]"      # Black
    BIRed="\[\033[1;91m\]"        # Red
    BIGreen="\[\033[1;92m\]"      # Green
    BIYellow="\[\033[1;93m\]"     # Yellow
    BIBlue="\[\033[1;94m\]"       # Blue
    BIPurple="\[\033[1;95m\]"     # Purple
    BICyan="\[\033[1;96m\]"       # Cyan
    BIWhite="\[\033[1;97m\]"      # White

    # High Intensty backgrounds
    On_IBlack="\[\033[0;100m\]"   # Black
    On_IRed="\[\033[0;101m\]"     # Red
    On_IGreen="\[\033[0;102m\]"   # Green
    On_IYellow="\[\033[0;103m\]"  # Yellow
    On_IBlue="\[\033[0;104m\]"    # Blue
    On_IPurple="\[\033[10;95m\]"  # Purple
    On_ICyan="\[\033[0;106m\]"    # Cyan
    On_IWhite="\[\033[0;107m\]"   # White
    
    input = "在网络配置中，服务器的IPv4地址是192.168.1.10，而另一台设备的IPv4地址则为10.0.0.254。对于IPv6地址，主服务器使用的是2001:0db8:85a3:0000:0000:8a2e:0370:7334，而备份服务器的IPv6地址是fe80::1ff:fe23:4567:890a。同时，网络交换机的MAC地址为00:1A:2B:3C:4D:5E，而路由器的MAC地址则是AA-BB-CC-DD-EE-FF。"
    
    IPV4 = "(?:(?:1[0-9][0-9]\.)|(?:2[0-4][0-9]\.)|(?:25[0-5]\.)|(?:[1-9][0-9]\.)|(?:[0-9]\.)){3}(?:(?:1[0-9][0-9])|(?:2[0-4][0-9])|(?:25[0-5])|(?:[1-9][0-9])|(?:[0-9]))"

    MAC = "(?:(?:[0-9A-Fa-f]{2}[:\-.]){5}(?:[0-9A-Fa-f]{2}))"

    IPV6 = "(?:(?:(?:[0-9A-Fa-f]{1,4}:){7}(?:[0-9A-Fa-f]{1,4}|:))|(?:(?:[0-9A-Fa-f]{1,4}:){6}(?::[0-9A-Fa-f]{1,4}|(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(?:(?:[0-9A-Fa-f]{1,4}:){5}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,2})|:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(?:(?:[0-9A-Fa-f]{1,4}:){4}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,3})|(?:(?::[0-9A-Fa-f]{1,4})?:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){3}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,4})|(?:(?::[0-9A-Fa-f]{1,4}){0,2}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){2}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,5})|(?:(?::[0-9A-Fa-f]{1,4}){0,3}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){1}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,6})|(?:(?::[0-9A-Fa-f]{1,4}){0,4}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?::(?:(?:(?::[0-9A-Fa-f]{1,4}){1,7})|(?:(?::[0-9A-Fa-f]{1,4}){0,5}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))"
    
    result = ColorTheme.strProcess(input, {IPV4: "red", IPV6: "blue", MAC: "black"})
    print(result)
    
    text_green = "\033[92mHello World    \033[1mHello World\033[0m\n"\
        "\033[102mHello World    \033[1mHello World\033[0m\n"\
        "\033[42mHello World    \033[1mHello World\033[0m\n"\
        "\033[32mHello World    \033[1mHello World\033[0m\n"
    text_red="\033[91mHello World    \033[1mHello World\033[0m\n"\
        "\033[101mHello World    \033[1mHello World\033[0m\n"\
        "\033[41mHello World    \033[1mHello World\033[0m\n"\
        "\033[31mHello World    \033[1mHello World\033[0m\n"
    text_blue="\033[94mHello World    \033[1mHello World\033[0m\n"\
        "\033[104mHello World    \033[1mHello World\033[0m\n"\
        "\033[44mHello World    \033[1mHello World\033[0m\n"\
        "\033[34mHello World    \033[1mHello World\033[0m\n"
    text_yellow="\033[93mHello World    \033[1mHello World\033[0m\n"\
        "\033[103mHello World    \033[1mHello World\033[0m\n"\
        "\033[43mHello World    \033[1mHello World\033[0m\n"\
        "\033[33mHello World    \033[1mHello World\033[0m\n"
    text_purple="\033[95mHello World    \033[1mHello World\033[0m\n"\
        "\033[105mHello World    \033[1mHello World\033[0m\n"\
        "\033[45mHello World    \033[1mHello World\033[0m\n"\
        "\033[35mHello World    \033[1mHello World\033[0m\n"
    text_cyan="\033[96mHello World    \033[1mHello World\033[0m\n"\
        "\033[106mHello World    \033[1mHello World\033[0m\n"\
        "\033[46mHello World    \033[1mHello World\033[0m\n"\
        "\033[36mHello World    \033[1mHello World\033[0m\n"
    text_black="\033[97mHello World    \033[1mHello World\033[0m\n"\
        "\033[107mHello World    \033[1mHello World\033[0m\n"\
        "\033[47mHello World    \033[1mHello World\033[0m\n"\
        "\033[37mHello World    \033[1mHello World\033[0m\n"
    text_white="\033[90mHello World    \033[1mHello World\033[0m\n"\
        "\033[100mHello World    \033[1mHello World\033[0m\n"\
        "\033[40mHello World    \033[1mHello World\033[0m\n"\
        "\033[30mHello World    \033[1mHello World\033[0m\n"
        
    text = text_green + text_red + text_blue + text_yellow + text_purple + text_cyan + text_black + text_white
        
    # print(text)


