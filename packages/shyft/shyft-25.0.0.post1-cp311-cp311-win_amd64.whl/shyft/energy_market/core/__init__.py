from shyft.time_series import time,ModelInfo
from os import path

# The absolute import here is PyCharm specific. Please consider removing this when PyCharm improves!
from shyft.energy_market import *
from shyft.energy_market import __doc__ as __doc__
from shyft.energy_market import __version__ as __version__
# from _core import *
from shyft.energy_market.core.model_repository import ModelRepository
import functools
from typing import Callable, Any, List, Generator, Union

HydroConnectionList = list
TurbineOperatingZoneList = list
IntStringDict = dict
StringTimeSeriesDict = dict
PointList = list
XyPointCurveList = list
RunVector = list

class EnergyMarketCorePropertyError(Exception):
    """Error type for when a C++ object's property fails, but
    it shouldn't attempt __getattr__ afterwards."""
    pass


def no_getattr_if_exception(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    Decorator for energy_market.core properties that might throw AttributeErrors,
    but that we don't want to continue into __getattr__.
    Instead we want it to throw the error received from the first attempt.
    """
    @functools.wraps(func)
    def wrapped_func(self: Any) -> Any:
        try:
            return func(self)
        except AttributeError as err:
            raise EnergyMarketCorePropertyError(f"Error in {self.__class__}.{func.__name__}: {err}")
    return wrapped_func


class requires_data_object:
    """
    Decorator class for functions for lazy evaluations of Energy Market Core object attributes.
    The decorator checks whether "obj"-attribute has been set, and if not, applies a user-defined function
    to construct obj, before making the function call.
    """
    def __init__(self, construct_func):
        """
        :param construct_func: Function that's assumed to take one positional argument and return anything.
            Intended usage is that construct_func takes em.core.<Python wrapped C++ object> and construct
            an instance of some Python object that will help in mimicking the interfaces found in statkraft.ltm classes.
        """
        self.construct_func = construct_func

    def __call__(self, func):
        """
        Decorator function.
        :param func: Function to be decorated.
            Intended usage is that func should be a class method, and so the first argument should be "self".
        :return:  Decorated function that first constructs Python object, if necessary.
        """
        @functools.wraps(func)
        def wrapped_func(cppobj, *args, **kwargs):
            if cppobj.obj is None:
                wrapped_func.counter += 1
                cppobj.obj = self.construct_func(cppobj)
            return func(cppobj, *args, **kwargs)
        wrapped_func.counter = 0
        return wrapped_func

# **********************************************************************************************************************
#                   Backward compatibility
# **********************************************************************************************************************
Aggregate = Unit
AggregateList = UnitList
PowerStation = PowerPlant
PowerStationList = PowerPlantList
WaterRoute = Waterway
WaterRouteList = WaterwayList
TurbineEfficiency = TurbineOperatingZone
TurbineEfficiencyList = TurbineOperatingZoneList

# HydroPowerSystem.create_river = lambda self, uid, name, json="": HydroPowerSystemBuilder(self).create_river(uid, name, json)
# HydroPowerSystem.create_tunnel = lambda self, uid, name, json="": HydroPowerSystemBuilder(self).create_tunnel(uid, name, json)
# HydroPowerSystem.create_unit = lambda self, uid, name, json="": HydroPowerSystemBuilder(self).create_unit(uid, name, json)
# HydroPowerSystem.create_unit = lambda self, uid, name, json="": HydroPowerSystemBuilder(self).create_unit(uid, name, json)
# HydroPowerSystem.create_gate = lambda self, uid, name, json="": HydroPowerSystemBuilder(self).create_gate(uid, name, json)

# HydroPowerSystem.create_power_station = lambda self, uid, name, json="": HydroPowerSystemBuilder(self).create_power_plant(uid, name, json)
# HydroPowerSystem.create_power_plant = lambda self, uid, name, json="": HydroPowerSystemBuilder(self).create_power_plant(uid, name, json)
# HydroPowerSystem.create_reservoir = lambda self, uid, name, json="": HydroPowerSystemBuilder(self).create_reservoir(uid, name, json)
# HydroPowerSystem.create_catchment = lambda self, uid, name, json="": HydroPowerSystemBuilder(self).create_catchment(uid, name, json)
# HydroPowerSystem.to_blob = lambda self: HydroPowerSystem.to_blob_ref(self)

# fixup building Model, ModelArea
# Model.create_model_area = lambda self, uid, name, json="": ModelBuilder(self).create_model_area(uid, name, json)
# Model.create_power_module = lambda self, area, uid, name, json="": ModelBuilder(self).create_power_module( uid, name, json, area)
# Model.create_power_line = lambda self, a, b, uid, name, json="": ModelBuilder(self).create_power_line(uid, name, json, a, b)
# ModelArea.create_power_module = lambda self, uid, name, json="": ModelBuilder(self.model).create_power_module(uid, name, json,self)


def create_model_service(model_directory:str , storage_type: str ='blob'):
    """
    Create and return the client for the Ltm model service

    Parameters
    ----------
    model_directory:
        specifies the network host name, ip, name
    storage_type:
        specifies type of api-service, ('blob')
        default = 'blob'

    """
    if storage_type == 'blob':
        if not path.exists(model_directory):
            raise RuntimeError("Model directory does not exists:'{0}'".format(model_directory))

        if not path.isdir(model_directory):
            raise RuntimeError("Specified model directory is not a directory:'{0}'".format(model_directory))

        return ModelRepository(model_directory)

    raise RuntimeError("unknown service storage type specified, please support 'db' or 'blob'")


def get_dir(self) -> List:
    return sorted(set(super(self.__class__, self).__dir__() + self.obj.__dir__()))

def get_object_attribute(self, attr):
    return getattr(self.obj, attr)

__all__ = [
 'IdBase',
 'Catchment',
 'CatchmentList',
 'Client',
 'ConnectionRole',
 'Gate',
 'GateList',
 'HydroComponent',
 'HydroComponentList',
 'HydroConnection',
 'HydroConnectionList',
 'HydroGraphTraversal',
 'HydroPowerSystem',
 'HydroPowerSystemBuilder',
 'HydroPowerSystemDict',
 'HydroPowerSystemList',
 'IntStringDict',
 'StringTimeSeriesDict',
 'Model',
 'ModelArea',
 'ModelAreaDict',
 'ModelBuilder',
 'ModelInfo',
 'ModelList',
 'Point',
 'PointList',
 'PowerLine',
 'PowerLineList',
 'PowerModule',
 'PowerModuleDict',
 'PowerPlant',
 'PowerPlantList',
 'R_CREATED',
 'R_FAILED',
 'R_FINISHED_RUN',
 'R_FROZEN',
 'R_PREP_INPUT',
 'R_READ_RESULT',
 'R_RUNNING',
 'Reservoir',
 'ReservoirList',
 'Run',
 'RunClient',
 'RunServer',
 'Server',
 'TurbineCapability',
 'TurbineDescription',
 'TurbineOperatingZone',
 'TurbineOperatingZoneList',
 'Unit',
 'UnitList',
 'Waterway',
 'WaterwayList',
 'XyPointCurve',
 'XyPointCurveList',
 'XyPointCurveWithZ',
 'XyPointCurveWithZList',
  'XyzPointCurve',
 'bypass',
 'compressed_size',
 'flood',
 'input',
 'main',
 'points_from_x_y',
 'run_state',
 'downstream_reservoirs',
 'downstream_units',
 'upstream_reservoirs',
 'upstream_units',
 'has_forward_capability',
 'has_backward_capability',
 'has_reversible_capability'
]
