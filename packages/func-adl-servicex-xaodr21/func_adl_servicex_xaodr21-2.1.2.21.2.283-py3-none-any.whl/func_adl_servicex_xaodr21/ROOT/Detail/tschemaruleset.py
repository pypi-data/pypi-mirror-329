from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
from enum import Enum
import func_adl_servicex_xaodr21

_method_map = {
    'GetClassVersion': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Detail::TSchemaRuleSet',
        'method_name': 'GetClassVersion',
        'return_type': 'int',
    },
    'ImplFileLine': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Detail::TSchemaRuleSet',
        'method_name': 'ImplFileLine',
        'return_type': 'int',
    },
    'DeclFileLine': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Detail::TSchemaRuleSet',
        'method_name': 'DeclFileLine',
        'return_type': 'int',
    },
    'DistancetoPrimitive': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Detail::TSchemaRuleSet',
        'method_name': 'DistancetoPrimitive',
        'return_type': 'int',
    },
}

_enum_map = {      
}

T = TypeVar('T')


def _add_method_metadata(s: ObjectStream[T], a: ast.Call) -> Tuple[ObjectStream[T], ast.Call]:
    '''Add metadata for a collection to the func_adl stream if we know about it
    '''
    assert isinstance(a.func, ast.Attribute)
    if a.func.attr in _method_map:
        s_update = s.MetaData(_method_map[a.func.attr])


        for md in _enum_map.get(a.func.attr, []):
            s_update = s_update.MetaData(md)
        return s_update, a
    else:
        return s, a


@func_adl_callback(_add_method_metadata)
class TSchemaRuleSet:
    "A class"

    class EConsistencyCheck(Enum):
        kNoCheck = 0
        kCheckAll = 1
        kCheckConflict = 2


    def GetClassVersion(self) -> int:
        "A method"
        ...

    def ImplFileLine(self) -> int:
        "A method"
        ...

    def DeclFileLine(self) -> int:
        "A method"
        ...

    def DistancetoPrimitive(self, px: int, py: int) -> int:
        "A method"
        ...
