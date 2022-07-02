'''

'''
import fnmatch
from typing import List


import sys
def is_ndarray(d):
    np = sys.modules.get('numpy')
    return np and isinstance(d, np.ndarray)

# def is_dataframe(d):
#     pd = sys.modules.get('pandas')
#     return pd and isinstance(d, pd.DataFrame)



class C:
    BLACK = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# class S:
#     DEFAULT = '0'
#     BOLD = '1'


# def style(style):
#     return '\x1b[{}m{{}}\x1b[0m'


def get_column_format(cols, data, drop=None):
    # get all columns across the data
    all_cols = get_data_columns(data) - set(drop or ())

    # break out columns into a uniform list
    cols = split_nested(cols or list(all_cols), ',/|')
    # replace any wildcards
    cols = [
        [
            [c for csc in csr for c in maybe_glob(csc, all_cols)]
            for csr in c
        ] for c in cols
    ]
    
    # handle leftover columns
    given_cols = {c for ci in cols for cj in ci for c in cj}
    remaining_cols = list(all_cols - given_cols)
    # replace ... with the leftover columns
    # !! this might have weird stuff with nested '...'
    cols = [
        ci for ci_ in cols for ci in (
            [[[c]] for c in sorted(remaining_cols)]
            if ci_ == [['...']] else 
            [ci_]
        )
    ]
    return cols







def get_data_columns(data: List[dict]):
    '''Get columns from a list of dictionaries.'''
    return {c for d in data for c in (d if isinstance(d, dict) else ())}

def maybe_glob(x, options):
    '''Glob from a list of items, if the '''
    if options and isinstance(x, str) and '*' in x:
        return sorted(c for c in options if fnmatch.fnmatch(c, x))
    return [x]


def indent(d, indent=1, width=2):
    '''Indent a multi-line string.'''
    return '\n'.join('{}{}'.format(' '*indent*width, l) for l in d.splitlines())
indent_ = indent

def nested_key(d, k, default=...):
    '''Get a nested key (a.b.c) from a nested dictionary.'''
    for ki in k.split('.'):
        try:
            d = d[ki]
        except (TypeError, KeyError):
            if default is ...:
                raise
            return default
    return d

def split_nested(cols, seps=',/|'):
    '''Splits a shorthand column layout into a nested column list.
    e.g.
        'time,max_laeq|avg_laeq/l90|min_laeq,emb_*,...'
        [
            [['time]],
            [
                ['max_laeq', 'avg_laeq'],
                ['l90', 'min_laeq']
            ],
            [['emb_min']], [['emb_max'], ...],
            [['time']], ...  # leftover columns
        ]
    '''
    return list(_isplitnested(cols, seps))

def _isplitnested(cols, seps=',/|'):
    if not seps:
        yield cols
        return

    sep, nextseps = seps[0], seps[1:]
    for xi in _maybesplit(cols, sep):
        yield list(_isplitnested(xi, nextseps)) if nextseps else xi

def _maybesplit(x, ch, strip=True, filter=True):
    '''Coerce a string to a list by splitting by a certain character,
    or skip if already a list.'''
    return [
        x.strip() if strip and isinstance(x, str) else x
        for x in (x.split(ch) if isinstance(x, str) else x)
        if not filter or x]
