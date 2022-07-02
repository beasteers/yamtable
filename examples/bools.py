'''Change how booleans are displayed.


'''
import yamtable
import random

def dump_bool(name):
    print(yamtable.dump({name: [{str(x): x for x in [True, False]}]*2}, bool_icon=name))


print("You can choose from any of these bool icons")
print()

for name in yamtable.BOOLS:
    dump_bool(name)
    print()


# format: [True, False]
print("Or add your own!")
yamtable.BOOLS['elf'] = ['🧝🏿‍♀️', '🧟‍♀️']
dump_bool('elf')
yamtable.BOOLS['gays'] = ['🏳️‍🌈', '👮‍♂️'] # acab
dump_bool('gays')
