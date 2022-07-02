'''You can select any of tabulate's table formats.

More info here: https://github.com/astanin/python-tabulate
'''
import yamtable

import random
def sensor_data(n=3):
    return [
        {
            'is_up': random.choice([False, True]), 
            'value_A': random.random(), 
            'value_B': random.random() + 100,
            'id': random.randint(1000, 5000)
        } 
        for i in range(n)
    ]


data = sensor_data()
for fmt in yamtable.TABLE_FORMATS:
    print(fmt)
    print(yamtable.dump(data, table_format=fmt))
    print()