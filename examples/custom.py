'''You can override how things are formatted by subclassing.

 - 

'''
import yamtable

class MyYam(yamtable.Yam):
    def __init__(self, my_custom_value=10):
        super().__init__(my_custom_value=my_custom_value)

    def dump_list(self, data, _level=0, **kw):
        if _level > 2:  # if we're more than two levels deep, print something different
            return f'still going! {data}'
        return super().dump_list(data, _level=_level, **kw)

    def dump_default(self, data, my_custom_value=10, **kw):
        # do whatever you want
        if isinstance(data, int):
            if data > 1000:
                return 'big number'
            return data * my_custom_value
        return data


yam = MyYam()

print(yam.dump({
    "hi": [
        ["hello", 5],
        ["hello", 5000],
        ["hello", [6., 70000]],
    ]
}))

'''

hi: 
  - - hello
    - 50
  - - hello
    - big number
  - - hello
    - still going! [6.0, 70000]

'''