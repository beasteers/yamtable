import sys
import types
import inspect
import fire

import yamtable

_OG_PrintResult = fire.core._PrintResult
def patch():
  fire.core._PrintResult = _PrintResult

dump = yamtable.dump
def set_serializer(new_dump):
  global dump
  dump = new_dump


from fire.core import FireError, value_types, _OneLineResult, _DictAsString, helptext, Display
def _PrintResult(component_trace, verbose=False):
  """Prints the result of the Fire call to stdout in a human readable way."""
  # TODO(dbieber): Design human readable deserializable serialization method
  # and move serialization to its own module.
  result = component_trace.GetResult()

  if dump and isinstance(result, (list, tuple, dict)):
    result = dump(result)

  if value_types.HasCustomStr(result):
    # If the object has a custom __str__ method, rather than one inherited from
    # object, then we use that to serialize the object.
    print(str(result))
    return

  if isinstance(result, (list, set, frozenset, types.GeneratorType)):
    for i in result:
      print(_OneLineResult(i))
  elif inspect.isgeneratorfunction(result):
    raise NotImplementedError
  elif isinstance(result, dict) and value_types.IsSimpleGroup(result):
    print(_DictAsString(result, verbose))
  elif isinstance(result, tuple):
    print(_OneLineResult(result))
  elif isinstance(result, value_types.VALUE_TYPES):
    if result is not None:
      print(result)
  else:
    help_text = helptext.HelpText(
        result, trace=component_trace, verbose=verbose)
    output = [help_text]
    Display(output, out=sys.stdout)
