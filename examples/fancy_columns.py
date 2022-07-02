'''Fancy column configuration!

It takes a fully text-based spec so that it can be specified from the command line.

e.g. ``columns="is_up, id|name/desc, ..., value_*"``

 - "," separates different table columns
 - "/" separates rows within a row meaning you can stack data on top of eachother
 - "|" separates sub-columns when using sub-rows (e.g. id|name|is_up/desc, useful where desc is long)
 - "*" can be used as a wildcard to match columns
 - "..." can be used to fill with the remaining columns

'''
import yamtable

import random
def sensor_data(n=8):
    return [
        {
            'is_up': random.choice([False, True]), 
            'value_A': random.random(), 
            'value_B': random.random() + 100,
            'value_C': random.random() - 100,
            'id': random.randint(1000, 5000),
            'name': f"Sensor {i}",
            'desc': f"this is sensor {i}",
            'something': 'asdfjasdf',
        } 
        for i in range(n)
    ]

print("Without fancy columns:")
print(yamtable.dump(sensor_data()))

columns = 'is_up, id|name/desc, ..., value_*'

print()
print(f"With fancy columns: {columns!r}")
print(yamtable.dump(sensor_data(), columns=columns))
# this is also equivalent:
# print(yamtable.dump(sensor_data(), columns=['is_up', 'id|name/desc', '...', 'value_*']))
