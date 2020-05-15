"""This module contains some helper functions"""

# console color
color_dic = {
    'white': '\33[0m',
    'red': '\33[31m',
    'green': '\33[32m',
    'yellow': '\33[33m',
    'blue': '\33[34m',
    'violet': '\33[35m',
    'cyan': '\33[36m',
    'orange': '\x1b[1;33;40m',
}

def cprint(message, color):
    """Print a message in the color wanted"""
    color = color_dic.get(color, 'white')
    print(color + message + color_dic.get('white'))

