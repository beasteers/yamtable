'''
'''
from __future__ import annotations
import textwrap
import tabulate
from . import util


class Yam:
    table_no_data_text = 'no data'

    def __init__(
        self, *, 
        tab_width: int=2, 
        table_format: str='simple', 
        float_format: str='.3g', 
        bool_icon: str='rose', 
        color: bool=False, 
        maxcolwidths=None, 
        **config
    ):
        '''YamTable format class. This handles all the logistics for formatting different types.
        
        Arguments:
            tab_width: how many spaces should a tab have? 
            table_format (str): the tabulate table format.
            float_format (str):
            bool_icon (str): the name of the bool icon set to use.
            color (bool): whether to format keys and headers with color.
            maxcolwidths (int, list): the max width for each column.
        '''
        self._config = {
            'tab_width': tab_width, 
            'table_format': table_format, 
            'float_format': float_format, 
            'bool_icon': bool_icon,
            'color': color,
            'max_depth': 0,
            'max_table_depth': 1,
            'maxcolwidths': maxcolwidths,
            **config
        }

    def config(self, **update):
        if update:
            self._config.update(update)
        print(self._config['color'])
        return self._config

    def _init_config(self, *, _formatter=None, _c=True, **kw):
        # merge kw with default config
        if _c:
            _c = self._config if _c is True else _c
            kw = {**_c, '_c': None, **kw}
        # initialize formatter
        if not _formatter:
            _formatter = ColorFormatter() if kw['color'] else Formatter()
        kw['_formatter'] = _formatter
        return kw

    def dump(self, d, _ignore_indent=False, **kw):
        '''
        
        '''
        kw = self._init_config(**kw)
        level = kw.get('_level', 0)
        table_level = kw.get('_table_level', 0)
        max_depth = kw.get('max_depth', 0)
        max_table_depth = kw.get('max_table_depth') or max_depth

        if not max_table_depth or max_table_depth - table_level > 0:
            if self.is_table(d):
                d = self.dump_table(d, **kw)

        if not max_depth or max_depth - level > 0:
            if isinstance(d, dict):
                d = self.dump_dict(d, **kw)
            elif isinstance(d, (list, tuple)):
                d = self.dump_list(d, **kw)

        if util.is_ndarray(d):
            d = self.dump_ndarray(d, **kw)
        elif isinstance(d, bool):
            d = self.dump_bool(d, **kw)
        elif isinstance(d, float):
            d = self.dump_float(d, **kw)

        d = self.dump_default(d, **kw)
        d = str(d) if d is not None else ''

        if not _ignore_indent and level and len(d.splitlines()) > 1:
            return '\n' + util.indent(d, width=kw['tab_width'])
        return d

    def dump_default(self, d, **kw):
        return d

    def _dump_deeper(self, x, *, _level=0, **kw):
        return self.dump(x, _level=_level+1, **kw)

    def is_table(self, d):
        return isinstance(d, list) and all(di is None or isinstance(di, dict) for di in d)

    SUBROW_SEP = '\n'
    SUBCOL_SEP = ' | '
    SUBROW_HEADER_SEP = ' / '
    SUBCOL_HEADER_SEP = ' | '

    def dump_table(self, data, columns=None, table_format=None, _table_level=0, **kw):
        if not isinstance(data, (list, tuple)):
            return data
        elif not data:
            return f'-- {self.table_no_data_text} --'

        formatter = kw['_formatter']

        # convert to table
        cols = util.get_column_format(columns, data)
        return self._table([
                [
                    self.SUBROW_SEP.join([
                        self.SUBCOL_SEP.join(
                            self._dump_deeper(
                                util.nested_key(d, c, None), 
                                _ignore_indent=True,
                                _table_level=_table_level+1, 
                                **kw) 
                            for c in csc
                        )
                        for csc in csr
                    ]) 
                    for csr in cols
                ]
                for d in data
            ], 
            headers=[self.SUBROW_HEADER_SEP.join(self.SUBCOL_HEADER_SEP.join(formatter.key(c) for c in cj) for cj in ci) for ci in cols],
            table_format=table_format, **kw)

    def _table(self, data, headers=None, table_format=None, float_format=None, tabulate_kw=None, **kw): #int_format=None, 
        return tabulate.tabulate(
            data, headers=headers,
            tablefmt=table_format,
            # intfmt=int_format or self.int_format,
            floatfmt=float_format,
            missingval='--',
            **(tabulate_kw or {})
        )

    def dump_dict(self, d, *, _formatter, _keys=(), **kw):
        return '\n'.join(
            '{}: {}'.format(
                _formatter.key(k), 
                self._dump_deeper(di, _keys=_keys + (k,), **kw)
            )
            for k, di in d.items())

    def dump_list(self, d, *, _formatter, _keys=(), **kw):
        return '\n'.join(
            '{}{} {}'.format(
                ' '*(kw['tab_width']-2), 
                _formatter.tick('-'),
                self._dump_deeper(di, _keys=_keys + (i,), **kw).strip()
            ) 
            for i, di in enumerate(d))

    def dump_ndarray(self, d, **kw):
        if d.size > 20 or d.ndim > 2:
            d = f'{d.shape} {d.dtype}'
        return d

    def dump_bool(self, d, bool_icon, **kw):
        if not bool_icon:
            return str(d)
        BOOL = bool_icon if isinstance(bool_icon, (list, tuple)) else BOOLS[bool_icon]
        return BOOL[0] if d else BOOL[1]

    def dump_float(self, d, float_format, **kw):
        return '{:{float_format}}'.format(d, float_format=float_format)



# formatters - let us swap out colors

class Formatter:
    key_format = '{}'
    # value_format = '{}'
    def __init__(self, key=None, **data): # , value=None
        self.data = data
        self.key_format = key or self.key_format
        # self.value_format = value or self.value_format

    def key(self, k, **data):
        return self.key_format.format(k, **self.data, **data)
    # def value(self, k, **data):
    #     return self.value_format.format(k, **self.data, **data)
    def tick(self, k, **data):
        return self.key_format.format(k, **self.data, **data)

class ColorFormatter(Formatter):
    key_format = f'{util.C.RED}{{}}{util.C.END}'
    # value_format = f'{C.RED}{{}}{C.END}'


# tabulate tablefmt options

TABLE_FORMATS = [
    "plain", "simple", "github", "grid", "fancy_grid", "pipe", "orgtbl", 
    "jira", "presto", "pretty", "psql", "rst", "mediawiki", "moinmoin", 
    "youtrack", "html", "unsafehtml", "latex", "latex_raw", "latex_booktabs", 
    "latex_longtable", "textile", "tsv"
]

# boolean display

BOOLS = {
    'moon': ['🌖', '🌒'],
    'full-moon': ['🌕', '🌑'],
    'rose': ['🌹', '🥀'],
    'rainbow': ['🌈', '☔️'],
    'octopus': ['🐙', '🐍'],
    'virus': ['🔬', '🦠'],
    'party-horn': ['🎉', '💥'],
    'party-ball': ['🎊', '🧨'],

    'relieved': ['😅', '🥺'],
    'laughing': ['😂', '😰'],
    'elated': ['🥰', '🤬'],
    'fleek': ['💅', '👺'],
    'thumb': ['👍', '👎'],
    'green-heart': ['💚', '💔'],
    'circle': ['🟢', '🔴'],
    'green-check': ['✅', '❗️'],
    'TF': ['T', 'F'],
    'tf': ['t', 'f'],
    'YN': ['Y', 'N'],
    'yn': ['y', 'n'],
    'check': ['✓', ''],
    'checkx': ['✓', 'x'],
}
