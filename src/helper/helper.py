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

def progress_bar(percent=0, width=30):
    """Emulate a progress bar

        Args:
            percent: Int for the progress percentage
            width: Int width of the progress bar (default 30)
    """

    # The number of hashes to show is based on the percent passed in. The
    # number of blanks is whatever space is left after.
    hashes = width * percent // 100
    blanks = width - hashes
    print('\r[\x1b[1;34;47m', hashes*'#', blanks*' ', ']', f' {percent:.0f}%', sep='',
        end='', flush=True)

