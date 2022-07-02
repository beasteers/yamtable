# yamtable |🍠✨|

A pretty ✨ formatting library meant for CLIs that need to display complex or ambiguously structured data, e.g. data from a REST API.

The idea is that, sometimes you have data that would look best as YAML, as it is quite good at displaying dictionaries.
And sometimes you might have a list of dictionaries (e.g. a list of entities with attributes) and displaying that would 
look muchhh better in a table because YAML would make it almost impossible to scan through the very tall representation 
of your data.

And sometimes you have a mix of the two. Like you could have some top level keys that would look best as YAML, but then 
you have some tabular data inside of it.

Point being, wouldn't it be nice to be able to print out this mixed data in a nice way without having to rewrite and customize a 
data formatter for each data configuration? Often times you want to look at the data first to even know what's going on and how you want 
to format it!

```python
import yamtable
# some messy object
yamtable.dump({
    'blah0': {
        'something': [{'is_up': False, 'value_A': 0.5367493221202239, 'value_B': 100.0825738163817, 'id': 2588}, {'is_up': True, 'value_A': 0.4559654642937784, 'value_B': 100.76840781583714, 'id': 2259}], 
        'other thing': [{'is_up': False, 'value_A': 0.5881412394062349, 'value_B': 100.18253046678744, 'id': 4778}], 
        'third thing': [1, 2, 3]}, 
    'blah1': {
        'something': [{'is_up': False, 'value_A': 0.6647093697365306, 'value_B': 100.15798391354355, 'id': 2477}, {'is_up': True, 'value_A': 0.8701196743925997, 'value_B': 100.45672829258778, 'id': 4183}], 
        'other thing': [{'is_up': False, 'value_A': 0.9113837527694413, 'value_B': 100.05392635622654, 'id': 2553}], 
        'third thing': [1, 2, 3]}
})
```


Ahhhh!
```yaml
blah0: 
  something: 
      value_A  is_up      value_B    id
    ---------  -------  ---------  ----
        0.894  🥀         100.515  3566
        0.379  🌹         100.345  4560
  other thing: 
      value_A  is_up      value_B    id
    ---------  -------  ---------  ----
        0.218  🥀         100.781  1311
  third thing: 
    - 1
    - 2
    - 3
blah1: 
  something: 
      value_A  is_up      value_B    id
    ---------  -------  ---------  ----
        0.203  🌹         100.998  4346
        0.995  🌹         100.094  3308
  other thing: 
      value_A  is_up      value_B    id
    ---------  -------  ---------  ----
        0.455  🥀         100.621  1686
  third thing: 
    - 1
    - 2
    - 3
```


## Install

```bash
pip install yamtable
```

## Usage

```python
import yamtable

# some test data
import random
def sensor_data(n=8):
    return [
        {
            'is_up': random.choice([False, True]), 
            'value_A': random.random(), 
            'value_B': random.random() + 100,
            'id': random.randint(1000, 5000)
        } 
        for i in range(n)
    ]

yamtable.dump(sensor_data())
```

## Author Notes
This is a fun pet project built so I could stop copying mutating code between CLI projects.
It isn't meant to be mature or fool-proof for all kinds of data. 

Since it deals with deeply nested data, it is difficult to find ways to intuitively customize 
the behavior from a top-level perspective. Defining multi-depth configuration from a dict level
is probably not the best idea, but if you want to customize behavior, you can just override the 
class methods. See `examples/custom.py` for an example.


TODO:
 - add ability to limit data displayed, sometimes a table can just be way too big
 - how to make colors legible and pretty on different systems with different themes
 - 


## More Examples:


```bash
$ python examples/nested.py

wow: 
  blah0: 
    something: 
      +---------+-----------+-----------+------+
      | is_up   |   value_B |   value_A |   id |
      +=========+===========+===========+======+
      | 🥀      |       101 |     0.597 | 4211 |
      +---------+-----------+-----------+------+
      | 🥀      |       101 |     0.11  | 2245 |
      +---------+-----------+-----------+------+
    other thing: 
      +---------+-----------+-----------+------+
      | is_up   |   value_B |   value_A |   id |
      +=========+===========+===========+======+
      | 🌹      |       100 |    0.0576 | 1272 |
      +---------+-----------+-----------+------+
    third thing: 
      - 1
      - 2
      - 3
    oooh: 
      +-----------------------+-------+-------+
      | aaa                   | bbb   |   ccc |
      +=======================+=======+=======+
      | okay: hm              | - 1   |     5 |
      | hmm: interesting      | - 2   |       |
      | more?: wow: srsly?    |       |       |
      +-----------------------+-------+-------+
      | okay: wow             | - 1   |     5 |
      | hmm: interesting      | - 2   |       |
      | more?: wow: srsly?    |       |       |
      +-----------------------+-------+-------+
      | okay: wowwow          | - 1   |     5 |
      | hmm: interesting      | - 2   |       |
      | more?:                |       |       |
      |   is it too much: umm |       |       |
      |   maybe: ...          |       |       |
      +-----------------------+-------+-------+
  blah1: 
    something: 
      +---------+-----------+-----------+------+
      | is_up   |   value_B |   value_A |   id |
      +=========+===========+===========+======+
      | 🥀      |       101 |     0.223 | 1315 |
      +---------+-----------+-----------+------+
      | 🥀      |       101 |     0.409 | 2428 |
      +---------+-----------+-----------+------+
    other thing: 
      +---------+-----------+-----------+------+
      | is_up   |   value_B |   value_A |   id |
      +=========+===========+===========+======+
      | 🌹      |       101 |      0.68 | 4227 |
      +---------+-----------+-----------+------+
    third thing: 
      - 1
      - 2
      - 3
    oooh: 
      +-----------------------+-------+-------+
      | aaa                   | bbb   |   ccc |
      +=======================+=======+=======+
      | okay: hm              | - 1   |     5 |
      | hmm: interesting      | - 2   |       |
      | more?: wow: srsly?    |       |       |
      +-----------------------+-------+-------+
      | okay: wow             | - 1   |     5 |
      | hmm: interesting      | - 2   |       |
      | more?: wow: srsly?    |       |       |
      +-----------------------+-------+-------+
      | okay: wowwow          | - 1   |     5 |
      | hmm: interesting      | - 2   |       |
      | more?:                |       |       |
      |   is it too much: umm |       |       |
      |   maybe: ...          |       |       |
      +-----------------------+-------+-------+
```

```bash
$ python examples/fancy_columns.py

Without fancy columns:
  value_C    id  desc                value_B    value_A  name      something    is_up
---------  ----  ----------------  ---------  ---------  --------  -----------  -------
    -99.1  4395  this is sensor 0        101      0.72   Sensor 0  asdfjasdf    🌹
    -99.1  3523  this is sensor 1        100      0.899  Sensor 1  asdfjasdf    🥀
    -99.1  4136  this is sensor 2        100      0.905  Sensor 2  asdfjasdf    🌹
    -99.6  2474  this is sensor 3        101      0.236  Sensor 3  asdfjasdf    🌹
    -99    3817  this is sensor 4        101      0.6    Sensor 4  asdfjasdf    🌹
    -99.2  1471  this is sensor 5        101      0.192  Sensor 5  asdfjasdf    🥀
    -99.2  3353  this is sensor 6        101      0.24   Sensor 6  asdfjasdf    🥀
    -99    2630  this is sensor 7        101      0.665  Sensor 7  asdfjasdf    🌹

With fancy columns: 'is_up, id|name/desc, ..., value_*'
is_up    id | name / desc    something    value_A | value_B | value_C
-------  ------------------  -----------  -----------------------------
🌹       1157 | Sensor 0     asdfjasdf    0.343 | 101 | -99.7
         this is sensor 0
🥀       4963 | Sensor 1     asdfjasdf    0.214 | 101 | -99.1
         this is sensor 1
🌹       3172 | Sensor 2     asdfjasdf    0.297 | 101 | -99
         this is sensor 2
🥀       1533 | Sensor 3     asdfjasdf    0.948 | 100 | -99.4
         this is sensor 3
🌹       4236 | Sensor 4     asdfjasdf    0.251 | 100 | -99
         this is sensor 4
🥀       4697 | Sensor 5     asdfjasdf    0.799 | 100 | -100
         this is sensor 5
🥀       4500 | Sensor 6     asdfjasdf    0.406 | 100 | -99.5
         this is sensor 6
🥀       3251 | Sensor 7     asdfjasdf    0.49 | 100 | -99.8
         this is sensor 7

```

More examples:
 - `examples/bools.py`: see all the boolean variations and how to customize
 - `examples/custom.py`: see how to alter how things are formatted
 - `examples/table_formats.py`: see all the table format variations
 - ...