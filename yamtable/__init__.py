from .core import *

yam = Yam()
dump = yam.dump

def fire_serializer(dump=dump):
    from . import fire_serialize_patch
    fire_serialize_patch.patch()
    fire_serialize_patch.set_serializer(dump)
