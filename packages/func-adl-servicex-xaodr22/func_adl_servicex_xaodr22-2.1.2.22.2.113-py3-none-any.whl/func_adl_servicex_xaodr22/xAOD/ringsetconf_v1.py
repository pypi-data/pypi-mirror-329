from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
from enum import Enum
import func_adl_servicex_xaodr22

_method_map = {
    'isEMSection': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'isEMSection',
        'return_type': 'bool',
    },
    'isHADSection': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'isHADSection',
        'return_type': 'bool',
    },
    'isPSLayer': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'isPSLayer',
        'return_type': 'bool',
    },
    'isEM1Layer': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'isEM1Layer',
        'return_type': 'bool',
    },
    'isEM2Layer': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'isEM2Layer',
        'return_type': 'bool',
    },
    'isEM3Layer': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'isEM3Layer',
        'return_type': 'bool',
    },
    'isHAD1Layer': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'isHAD1Layer',
        'return_type': 'bool',
    },
    'isHAD2Layer': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'isHAD2Layer',
        'return_type': 'bool',
    },
    'isHAD3Layer': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'isHAD3Layer',
        'return_type': 'bool',
    },
    'nRings': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'nRings',
        'return_type': 'unsigned int',
    },
    'nLayers': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'nLayers',
        'return_type': 'unsigned int',
    },
    'layers': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'layers',
        'return_type_element': 'CaloSampling::CaloSample',
        'return_type_collection': 'const vector<CaloSampling::CaloSample>',
    },
    'layerAt': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'layerAt',
        'return_type': 'CaloSampling::CaloSample',
    },
    'etaWidth': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'etaWidth',
        'return_type': 'float',
    },
    'phiWidth': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'phiWidth',
        'return_type': 'float',
    },
    'cellMaxDEtaDist': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'cellMaxDEtaDist',
        'return_type': 'float',
    },
    'cellMaxDPhiDist': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'cellMaxDPhiDist',
        'return_type': 'float',
    },
    'doEtaAxesDivision': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'doEtaAxesDivision',
        'return_type': 'bool',
    },
    'doPhiAxesDivision': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'doPhiAxesDivision',
        'return_type': 'bool',
    },
    'layerStartIdx': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'layerStartIdx',
        'return_type': 'unsigned int',
    },
    'sectionStartIdx': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'sectionStartIdx',
        'return_type': 'unsigned int',
    },
    'layerEndIdx': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'layerEndIdx',
        'return_type': 'unsigned int',
    },
    'sectionEndIdx': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'sectionEndIdx',
        'return_type': 'unsigned int',
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'index',
        'return_type': 'int',
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'hasStore',
        'return_type': 'bool',
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
    },
    'trackIndices': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'trackIndices',
        'return_type': 'bool',
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'auxdataConst',
        'return_type': 'U',
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'isAvailable',
        'return_type': 'bool',
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

        s_update = s_update.MetaData({
            'metadata_type': 'inject_code',
            'name': 'xAODCaloRings/versions/RingSetConf_v1.h',
            'body_includes': ["xAODCaloRings/versions/RingSetConf_v1.h"],
        })


        s_update = s_update.MetaData({
            'metadata_type': 'inject_code',
            'name': 'xAODCaloRings',
            'link_libraries': ["xAODCaloRings"],
        })

        for md in _enum_map.get(a.func.attr, []):
            s_update = s_update.MetaData(md)
        return s_update, a
    else:
        return s, a


@func_adl_callback(_add_method_metadata)
class RingSetConf_v1:
    "A class"


    def isEMSection(self, layers: func_adl_servicex_xaodr22.vector_calosampling_calosample_.vector_CaloSampling_CaloSample_) -> bool:
        "A method"
        ...

    def isHADSection(self, layers: func_adl_servicex_xaodr22.vector_calosampling_calosample_.vector_CaloSampling_CaloSample_) -> bool:
        "A method"
        ...

    def isPSLayer(self, layers: func_adl_servicex_xaodr22.vector_calosampling_calosample_.vector_CaloSampling_CaloSample_) -> bool:
        "A method"
        ...

    def isEM1Layer(self, layers: func_adl_servicex_xaodr22.vector_calosampling_calosample_.vector_CaloSampling_CaloSample_) -> bool:
        "A method"
        ...

    def isEM2Layer(self, layers: func_adl_servicex_xaodr22.vector_calosampling_calosample_.vector_CaloSampling_CaloSample_) -> bool:
        "A method"
        ...

    def isEM3Layer(self, layers: func_adl_servicex_xaodr22.vector_calosampling_calosample_.vector_CaloSampling_CaloSample_) -> bool:
        "A method"
        ...

    def isHAD1Layer(self, layers: func_adl_servicex_xaodr22.vector_calosampling_calosample_.vector_CaloSampling_CaloSample_) -> bool:
        "A method"
        ...

    def isHAD2Layer(self, layers: func_adl_servicex_xaodr22.vector_calosampling_calosample_.vector_CaloSampling_CaloSample_) -> bool:
        "A method"
        ...

    def isHAD3Layer(self, layers: func_adl_servicex_xaodr22.vector_calosampling_calosample_.vector_CaloSampling_CaloSample_) -> bool:
        "A method"
        ...

    def nRings(self) -> int:
        "A method"
        ...

    def nLayers(self) -> int:
        "A method"
        ...

    def layers(self) -> func_adl_servicex_xaodr22.vector_calosampling_calosample_.vector_CaloSampling_CaloSample_:
        "A method"
        ...

    def layerAt(self, idx: int) -> func_adl_servicex_xaodr22.calosampling.CaloSampling.CaloSample:
        "A method"
        ...

    def etaWidth(self) -> float:
        "A method"
        ...

    def phiWidth(self) -> float:
        "A method"
        ...

    def cellMaxDEtaDist(self) -> float:
        "A method"
        ...

    def cellMaxDPhiDist(self) -> float:
        "A method"
        ...

    def doEtaAxesDivision(self) -> bool:
        "A method"
        ...

    def doPhiAxesDivision(self) -> bool:
        "A method"
        ...

    def layerStartIdx(self) -> int:
        "A method"
        ...

    def sectionStartIdx(self) -> int:
        "A method"
        ...

    def layerEndIdx(self) -> int:
        "A method"
        ...

    def sectionEndIdx(self) -> int:
        "A method"
        ...

    def index(self) -> int:
        "A method"
        ...

    def usingPrivateStore(self) -> bool:
        "A method"
        ...

    def usingStandaloneStore(self) -> bool:
        "A method"
        ...

    def hasStore(self) -> bool:
        "A method"
        ...

    def hasNonConstStore(self) -> bool:
        "A method"
        ...

    def clearDecorations(self) -> bool:
        "A method"
        ...

    def trackIndices(self) -> bool:
        "A method"
        ...

    @func_adl_parameterized_call(lambda s, a, param_1: func_adl_servicex_xaodr22.type_support.cpp_generic_1arg_callback('auxdataConst', s, a, param_1))
    @property
    def auxdataConst(self) -> func_adl_servicex_xaodr22.type_support.index_type_forwarder[func_adl_servicex_xaodr22.str.str]:
        "A method"
        ...

    @func_adl_parameterized_call(lambda s, a, param_1: func_adl_servicex_xaodr22.type_support.cpp_generic_1arg_callback('isAvailable', s, a, param_1))
    @property
    def isAvailable(self) -> func_adl_servicex_xaodr22.type_support.index_type_forwarder[func_adl_servicex_xaodr22.str.str]:
        "A method"
        ...
