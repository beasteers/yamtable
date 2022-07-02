'''This isn't yamtable related, just prints out those handy color tables.'''

def print_format_table():
    """prints table of formatted text format options"""
    for style in range(8):
        print('\n'.join(
            ''.join(
                '\x1b[{0}m {0} \x1b[0m'.format(';'.join(map(str, (style, fg, bg))))
                for bg in range(40,48)
            ) for fg in range(30,38)
        ), '\n')

print_format_table()