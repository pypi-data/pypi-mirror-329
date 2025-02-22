"""
Shyft Open Source Energy Market model core
"""
from __future__ import annotations
import pybind11_stubgen.typing_ext
import shyft.time_series
import typing
__all__ = ['AFRR_DOWN', 'AFRR_UP', 'AnyAttrDict', 'AreaDict', 'COMMIT', 'Catchment', 'CatchmentList', 'Client', 'ConnectionRole', 'FCR_D_DOWN', 'FCR_D_UP', 'FCR_N_DOWN', 'FCR_N_UP', 'FFR', 'Gate', 'GateList', 'HydroComponent', 'HydroComponentList', 'HydroConnection', 'HydroGraphTraversal', 'HydroPowerSystem', 'HydroPowerSystemBuilder', 'HydroPowerSystemList', 'MFRR_DOWN', 'MFRR_UP', 'Model', 'ModelArea', 'ModelBuilder', 'PRODUCTION', 'Point', 'PowerLine', 'PowerLineList', 'PowerModule', 'PowerModuleDict', 'PowerPlant', 'PowerPlantList', 'RR_DOWN', 'RR_UP', 'R_CREATED', 'R_FAILED', 'R_FINISHED_RUN', 'R_FROZEN', 'R_PREP_INPUT', 'R_READ_RESULT', 'R_RUNNING', 'Reservoir', 'ReservoirList', 'Run', 'RunClient', 'RunServer', 'Server', 'TsAttrDict', 'TurbineCapability', 'TurbineDescription', 'TurbineOperatingZone', 'TurbineOperatingZoneList', 'UNSPECIFIED', 'Unit', 'UnitGroupType', 'UnitList', 'Waterway', 'WaterwayList', 'XyPointCurve', 'XyPointCurveWithZ', 'XyPointCurveWithZList', 'XyPointList', 'XyzPointCurve', 'XyzPointCurveDict', 'bool_attr', 'bypass', 'compressed_size', 'double_attr', 'downstream_reservoirs', 'downstream_units', 'flood', 'geo_point_attr', 'has_backward_capability', 'has_forward_capability', 'has_reversible_capability', 'i16_attr', 'i32_attr', 'i64_attr', 'i8_attr', 'input', 'main', 'message_list_attr', 'points_from_x_y', 'run_state', 'string_attr', 't_turbine_description', 't_xy', 't_xy_attr', 't_xy_z_list_attr', 't_xyz', 't_xyz_attr', 't_xyz_list', 'time_axis_attr', 'ts_attr', 'turbine_backward', 'turbine_description_attr', 'turbine_forward', 'turbine_none', 'turbine_reversible', 'u16_attr', 'unit_group_type_attr', 'upstream_reservoirs', 'upstream_units']
class AnyAttrDict:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the map is nonempty
        """
    @typing.overload
    def __contains__(self, arg0: str) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: typing.Any) -> bool:
        ...
    def __delitem__(self, arg0: str) -> None:
        ...
    def __getitem__(self, arg0: str) -> bool | float | int | int | shyft.time_series.TimeSeries | t_xy | t_xyz | t_xyz_list | t_turbine_description | str | shyft.time_series.TsVector | UnitGroupType | shyft.time_series.TimeAxis | shyft.time_series.GeoPoint:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: AnyAttrDict) -> None:
        """
        CopyConstructor
        """
    def __iter__(self) -> typing.Iterator[str]:
        ...
    def __len__(self) -> int:
        ...
    def __repr__(self) -> str:
        ...
    def __setitem__(self, arg0: str, arg1: bool | float | int | int | shyft.time_series.TimeSeries | t_xy | t_xyz | t_xyz_list | t_turbine_description | str | shyft.time_series.TsVector | UnitGroupType | shyft.time_series.TimeAxis | shyft.time_series.GeoPoint) -> None:
        ...
    def __str__(self) -> str:
        ...
    def get(self, key: str, default: bool | float | int | int | shyft.time_series.TimeSeries | t_xy | t_xyz | t_xyz_list | t_turbine_description | str | shyft.time_series.TsVector | UnitGroupType | shyft.time_series.TimeAxis | shyft.time_series.GeoPoint | None = None) -> bool | float | int | int | shyft.time_series.TimeSeries | t_xy | t_xyz | t_xyz_list | t_turbine_description | str | shyft.time_series.TsVector | UnitGroupType | shyft.time_series.TimeAxis | shyft.time_series.GeoPoint | None:
        """
        Return the value for key if key is in the dictionary, else default.
        """
    def items(self) -> typing.ItemsView:
        ...
    def keys(self) -> typing.KeysView:
        ...
    def values(self) -> typing.ValuesView:
        ...
class AreaDict:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the map is nonempty
        """
    @typing.overload
    def __contains__(self, arg0: int) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: typing.Any) -> bool:
        ...
    def __delitem__(self, arg0: int) -> None:
        ...
    def __eq__(self, arg0: AreaDict) -> bool:
        ...
    def __getitem__(self, arg0: int) -> ModelArea:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: AreaDict) -> None:
        """
        CopyConstructor
        """
    def __iter__(self) -> typing.Iterator[int]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: AreaDict) -> bool:
        ...
    def __setitem__(self, arg0: int, arg1: ModelArea) -> None:
        ...
    def get(self, key: int, default: ModelArea | None = None) -> ModelArea | None:
        """
        Return the value for key if key is in the dictionary, else default.
        """
    def items(self) -> typing.ItemsView:
        ...
    def keys(self) -> typing.KeysView:
        ...
    def values(self) -> typing.ValuesView:
        ...
class Catchment:
    """
    Catchment descriptive component, suitable for energy market long-term and/or short term managment.
    This component usually would contain usable view of the much more details shyft.hydrology region model
    
    """
    custom: AnyAttrDict
    id: int
    json: str
    name: str
    ts: TsAttrDict
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, arg0: Catchment) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __init__(self, id: int, name: str, json: str, hps: HydroPowerSystem) -> None:
        ...
    def __ne__(self, arg0: Catchment) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_tsm_object(self, key: str) -> ts_attr:
        """
        Get a specific extra time series for this object.
        
        The returned time series is wrapped in an object which exposes method for retrieving url etc.
        
        Args:
            key (str): The key in the tsm of the time series to get.
        
        Raises:
            runtime_error: If specified key does not exist.
        """
    @property
    def hps(self) -> HydroPowerSystem:
        """
        HydroPowerSystem: returns the hydro power system this component is a part of
        """
    @property
    def obj(self) -> typing.Any:
        """
        object: a python object
        """
    @obj.setter
    def obj(self, arg1: typing.Any) -> None:
        ...
class CatchmentList:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: CatchmentList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> CatchmentList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> Catchment:
        ...
    @typing.overload
    def __getitem__(self, arg0: str) -> Catchment:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: CatchmentList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[Catchment]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: CatchmentList) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: Catchment) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: CatchmentList) -> None:
        """
        Assign list elements using a slice object
        """
    def __str__(self) -> str:
        ...
    def append(self, x: Catchment) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    @typing.overload
    def extend(self, L: CatchmentList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: Catchment) -> None:
        """
        Insert an item at a given position.
        """
    def items(self) -> list[tuple[str, Catchment]]:
        ...
    def keys(self) -> list[str]:
        ...
    @typing.overload
    def pop(self) -> Catchment:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> Catchment:
        """
        Remove and return the item at index ``i``
        """
    def size(self) -> int:
        ...
    def values(self) -> CatchmentList:
        ...
class Client:
    """
    The client-api for the energy_market
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @staticmethod
    def get_model_infos(*args, **kwargs) -> list[shyft.time_series.ModelInfo]:
        """
        returns all or selected model-info objects based on model-identifiers(mids)
        
        Args:
            mids (IntVector): empty = all, or a list of known exisiting model-identifiers
        
            created_in (UtcPeriod): For which period you are interested in model-infos.
        
        Returns:
            ModelInfoVector: model_infos. Strongly typed list of ModelInfo
        """
    def __init__(self, host_port: str, timeout_ms: int, operation_timeout_ms: int = 0) -> None:
        """
        Creates a python client that can communicate with the corresponding server
        """
    def close(self) -> None:
        """
        Close the connection. It will automatically reopen if needed.
        """
    def read_model(self, mid: int) -> Model:
        """
        Read and return the model for specified model-identifier (mid)
        
        Args:
            mid (int): the model-identifer for the wanted model
        
        Returns:
            Model: m. The resulting model from the server
        """
    def read_models(self, mids: list[int]) -> list[Model]:
        """
        Read and return the model for specified model-identifier (mid)
        
        Args:
            mids (list[int]): A strongly typed list of ints, the model-identifers for the wanted models
        
        Returns:
            Model: m. The resulting model from the server
        """
    def remove_model(self, mid: int) -> int:
        """
        Remove the specified model bymodel-identifier (mid)
        
        Args:
            mid (int): the model-identifer for the wanted model
        
        Returns:
            int: ec. 0 or error-code?
        """
    def store_model(self, m: Model, mi: shyft.time_series.ModelInfo) -> int:
        """
        Store the model to backend, if m.id==0 then a new unique model-info is created and used
        
        Args:
            m (Model): The model to store
        
            mi (ModelInfo): The model-info to store for the model
        
        Returns:
            int: mid. model-identifier for the stored model and model-info
        """
    def update_model_info(self, mid: int, mi: shyft.time_series.ModelInfo) -> bool:
        """
        Update the model-info for specified model-identifier(mid)
        
        Args:
            mid (int): model-identifer
        
            mi (ModelInfo): The new updated model-info
        
        Returns:
            bool: ok. true if success
        """
    @property
    def host_port(self) -> str:
        """
        str: Endpoint network address of the remote server.
        """
    @property
    def is_open(self) -> bool:
        """
        bool: If the connection to the remote server is (still) open.
        """
    @property
    def operation_timeout_ms(self) -> int:
        """
        int: Operation timeout for remote server operations, in number milliseconds.
        """
    @operation_timeout_ms.setter
    def operation_timeout_ms(self, arg1: int) -> None:
        ...
    @property
    def reconnect_count(self) -> int:
        """
        int: Number of reconnects to the remote server that have been performed.
        """
    @property
    def timeout_ms(self) -> int:
        """
        int: Timout for remote server operations, in number milliseconds.
        """
class ConnectionRole:
    """
    Members:
    
      main
    
      bypass
    
      flood
    
      input
    """
    __members__: typing.ClassVar[dict[str, ConnectionRole]]  # value = {'main': <ConnectionRole.main: 0>, 'bypass': <ConnectionRole.bypass: 1>, 'flood': <ConnectionRole.flood: 2>, 'input': <ConnectionRole.input: 3>}
    bypass: typing.ClassVar[ConnectionRole]  # value = <ConnectionRole.bypass: 1>
    flood: typing.ClassVar[ConnectionRole]  # value = <ConnectionRole.flood: 2>
    input: typing.ClassVar[ConnectionRole]  # value = <ConnectionRole.input: 3>
    main: typing.ClassVar[ConnectionRole]  # value = <ConnectionRole.main: 0>
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Gate:
    """
    A gate controls the amount of flow into the waterway by the gate-opening.
    In the case of tunnels, it's usually either closed or open.
    For reservoir flood-routes, the gate should be used to model the volume-flood characteristics.
    The resulting flow through a waterway is a function of many factors, most imporant:
        
        * gate opening and gate-characteristics
        * upstream water-level
        * downstrem water-level(in some-cases)
        * waterway properties(might be state dependent)
    
    
    """
    custom: AnyAttrDict
    id: int
    json: str
    name: str
    ts: TsAttrDict
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, arg0: Gate) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __init__(self, id: int, name: str, json: str = '') -> None:
        ...
    def __ne__(self, arg0: Gate) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_tsm_object(self, key: str) -> ts_attr:
        """
        Get a specific extra time series for this object.
        
        The returned time series is wrapped in an object which exposes method for retrieving url etc.
        
        Args:
            key (str): The key in the tsm of the time series to get.
        
        Raises:
            runtime_error: If specified key does not exist.
        """
    @property
    def hps(self) -> HydroPowerSystem:
        """
        HydroPowerSystem: returns the hydro power system this component is a part of
        """
    @property
    def obj(self) -> typing.Any:
        """
        object: a python object
        """
    @obj.setter
    def obj(self, arg1: typing.Any) -> None:
        ...
    @property
    def water_route(self) -> Waterway:
        """
        Waterway: ref. to the waterway where this gate controls the flow
        """
    @property
    def waterway(self) -> Waterway:
        """
        Waterway: ref. to the waterway where this gate controls the flow
        """
class GateList:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: GateList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> GateList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> Gate:
        ...
    @typing.overload
    def __getitem__(self, arg0: str) -> Gate:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: GateList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[Gate]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: GateList) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: Gate) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: GateList) -> None:
        """
        Assign list elements using a slice object
        """
    def __str__(self) -> str:
        ...
    def append(self, x: Gate) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    @typing.overload
    def extend(self, L: GateList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: Gate) -> None:
        """
        Insert an item at a given position.
        """
    def items(self) -> list[tuple[str, Gate]]:
        ...
    def keys(self) -> list[str]:
        ...
    @typing.overload
    def pop(self) -> Gate:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> Gate:
        """
        Remove and return the item at index ``i``
        """
    def size(self) -> int:
        ...
    def values(self) -> GateList:
        ...
class HydroComponent:
    """
    A hydro component keeps the common attributes and relational properties common for all components that can contain water
    """
    custom: AnyAttrDict
    id: int
    json: str
    name: str
    ts: TsAttrDict
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, arg0: HydroComponent) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __ne__(self, arg0: HydroComponent) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def disconnect_from(self, other: HydroComponent) -> None:
        """
        disconnect from another component
        """
    def equal_structure(self, other: HydroComponent) -> bool:
        """
        Returns true if the `other` object have the same interconnections to the close neighbors as self.
        The neighbors are identified by their `.id` attribute, and they must appear in the same role to be considered equal.
        E.g. if for a reservoir, a waterway is in role flood for self, and in role bypass for other, they are different connections.
        
        Args:
            other (): the other object, of same type, hydro component, to compare.
        
        Returns:
            : bool. True if the other have same interconnections as self
        """
    def get_tsm_object(self, key: str) -> ts_attr:
        """
        Get a specific extra time series for this object.
        
        The returned time series is wrapped in an object which exposes method for retrieving url etc.
        
        Args:
            key (str): The key in the tsm of the time series to get.
        
        Raises:
            runtime_error: If specified key does not exist.
        """
    @property
    def downstreams(self) -> list[HydroConnection]:
        """
        HydroComponentList: list of hydro-components that are conceptually downstreams
        """
    @property
    def hps(self) -> HydroPowerSystem:
        """
        HydroPowerSystem: returns the hydro power system this component is a part of
        """
    @property
    def obj(self) -> typing.Any:
        """
        object: a python object
        """
    @obj.setter
    def obj(self, arg1: typing.Any) -> None:
        ...
    @property
    def upstreams(self) -> list[HydroConnection]:
        """
        HydroComponentList: list of hydro-components that are conceptually upstreams
        """
class HydroComponentList:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: HydroComponentList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> HydroComponentList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> HydroComponent:
        ...
    @typing.overload
    def __getitem__(self, arg0: str) -> HydroComponent:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: HydroComponentList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[HydroComponent]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: HydroComponentList) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: HydroComponent) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: HydroComponentList) -> None:
        """
        Assign list elements using a slice object
        """
    def __str__(self) -> str:
        ...
    def append(self, x: HydroComponent) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    @typing.overload
    def extend(self, L: HydroComponentList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: HydroComponent) -> None:
        """
        Insert an item at a given position.
        """
    def items(self) -> list[tuple[str, HydroComponent]]:
        ...
    def keys(self) -> list[str]:
        ...
    @typing.overload
    def pop(self) -> HydroComponent:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> HydroComponent:
        """
        Remove and return the item at index ``i``
        """
    def size(self) -> int:
        ...
    def values(self) -> HydroComponentList:
        ...
class HydroConnection:
    """
    A hydro connection is the connection object that relate one hydro component to another.
    A hydro component have zero or more hydro connections, contained in upstream and downstream lists.
    If you are using the hydro system builder, there will always be a mutual/two way connection.
    That is, if a reservoir connects downstream to a tunell (in role main), then the tunell will have
    a upstream connection pointing to the reservoir (as in role input)
    
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    @property
    def has_target(self) -> bool:
        """
        bool: true if valid/available target
        """
    @property
    def role(self) -> ConnectionRole:
        """
        ConnectionRole: role like main,bypass,flood,input
        """
    @role.setter
    def role(self, arg0: ConnectionRole) -> None:
        ...
    @property
    def target(self) -> HydroComponent:
        """
        HydroComponent: target of the hydro-connection, Reservoir|Unit|Waterway
        """
class HydroGraphTraversal:
    """
    A collection of hydro operations
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @staticmethod
    def extract_water_courses(hps: HydroPowerSystem) -> HydroPowerSystemList:
        """
        extracts the sub-hydro system from a given hydro system
        """
    @staticmethod
    @typing.overload
    def get_path_between(arg0: HydroComponent, arg1: HydroComponent, arg2: ConnectionRole) -> HydroComponentList:
        """
        finds path between two hydro components
        """
    @staticmethod
    @typing.overload
    def get_path_between(arg0: HydroComponent, arg1: HydroComponent) -> HydroComponentList:
        """
        finds path between two hydro components
        """
    @staticmethod
    @typing.overload
    def get_path_to_ocean(arg0: HydroComponent, arg1: ConnectionRole) -> HydroComponentList:
        """
        finds path to ocean for a given hydro component
        """
    @staticmethod
    @typing.overload
    def get_path_to_ocean(arg0: HydroComponent) -> HydroComponentList:
        """
        finds path to ocean for a given hydro component
        """
    @staticmethod
    @typing.overload
    def is_connected(arg0: HydroComponent, arg1: HydroComponent, arg2: ConnectionRole) -> bool:
        """
        finds whether two hydro components are connected
        """
    @staticmethod
    @typing.overload
    def is_connected(arg0: HydroComponent, arg1: HydroComponent) -> bool:
        """
        finds whether two hydro components are connected
        """
    @staticmethod
    @typing.overload
    def path_to_ocean(arg0: HydroComponentList, arg1: ConnectionRole) -> None:
        """
        finds path to ocean for a given hydro component
        """
    @staticmethod
    @typing.overload
    def path_to_ocean(arg0: HydroComponentList) -> None:
        """
        finds path to ocean for a given hydro component
        """
class HydroPowerSystem:
    """
    
    """
    aggregates: UnitList
    catchments: CatchmentList
    custom: AnyAttrDict
    id: int
    json: str
    name: str
    power_plants: PowerPlantList
    power_stations: PowerPlantList
    reservoirs: ReservoirList
    ts: TsAttrDict
    units: UnitList
    water_routes: WaterwayList
    waterways: WaterwayList
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @staticmethod
    def from_blob(blob_string: shyft.time_series.ByteVector) -> HydroPowerSystem:
        """
        constructs a model from a blob_string previously created by the to_blob method
        
        Args:
            blob_string (string): blob-formatted representation of the model, as create by the to_blob method
        """
    @staticmethod
    def to_blob_ref(arg0: HydroPowerSystem) -> shyft.time_series.ByteVector:
        """
        serialize the model into an blob
        
        Returns:
            string: blob. blob-serialized version of the model
        
        See also:
            from_blob
        """
    def __eq__(self, arg0: HydroPowerSystem) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    @typing.overload
    def __init__(self, name: str) -> None:
        """
        creates an empty hydro power system with the specified name
        """
    @typing.overload
    def __init__(self, id: int, name: str, json: str = '') -> None:
        """
        creates a an empty new hydro power system with specified id and name and json str info
        """
    def __ne__(self, arg0: HydroPowerSystem) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def create_aggregate(self, id: int, name: str, json: str = '') -> Unit:
        ...
    def create_catchment(self, id: int, name: str, json: str = '') -> Catchment:
        """
        create and add catchment to the system
        """
    def create_gate(self, id: int, name: str, json: str = '') -> Gate:
        ...
    def create_power_plant(self, id: int, name: str, json: str = '') -> PowerPlant:
        ...
    def create_power_station(self, id: int, name: str, json: str = '') -> PowerPlant:
        ...
    def create_reservoir(self, id: int, name: str, json: str = '') -> Reservoir:
        ...
    def create_river(self, id: int, name: str, json: str = '') -> Waterway:
        ...
    def create_tunnel(self, id: int, name: str, json: str = '') -> Waterway:
        ...
    def create_unit(self, id: int, name: str, json: str = '') -> Unit:
        ...
    def equal_content(self, other_hps: HydroPowerSystem) -> bool:
        """
        returns true if alle the content of the hps are equal, same as the equal == operator, except that .id, .name .created at the top level is not compared
        """
    def equal_structure(self, other_hps: HydroPowerSystem) -> bool:
        """
        returns true if equal structure of identified objects, using the .id, but not comparing .name, .attributes etc., to the other
        """
    def find_gate_by_id(self, id: int) -> Gate:
        """
        returns object with specified id
        """
    def find_gate_by_name(self, name: str) -> Gate:
        """
        returns object that exactly  matches name
        """
    def find_power_plant_by_id(self, id: int) -> PowerPlant:
        """
        returns object with specified id
        """
    def find_power_plant_by_name(self, name: str) -> PowerPlant:
        """
        returns object that exactly  matches name
        """
    def find_reservoir_by_id(self, id: int) -> Reservoir:
        """
        returns object with specified id
        """
    def find_reservoir_by_name(self, name: str) -> Reservoir:
        """
        returns object that exactly  matches name
        """
    def find_unit_by_id(self, id: int) -> Unit:
        """
        returns object with specified id
        """
    def find_unit_by_name(self, name: str) -> Unit:
        """
        returns object that exactly  matches name
        """
    def find_waterway_by_id(self, id: int) -> Waterway:
        """
        returns object with specified id
        """
    def find_waterway_by_name(self, name: str) -> Waterway:
        """
        returns object that exactly  matches name
        """
    def get_tsm_object(self, key: str) -> ts_attr:
        """
        Get a specific extra time series for this object.
        
        The returned time series is wrapped in an object which exposes method for retrieving url etc.
        
        Args:
            key (str): The key in the tsm of the time series to get.
        
        Raises:
            runtime_error: If specified key does not exist.
        """
    def to_blob(self) -> shyft.time_series.ByteVector:
        """
        serialize the model into an blob
        
        Returns:
            string: blob. blob-serialized version of the model
        
        See also:
            from_blob
        """
    @property
    def created(self) -> shyft.time_series.time:
        """
        time: The time when this system was created(you should specify it when you create it)
        """
    @created.setter
    def created(self, arg0: shyft.time_series.time) -> None:
        ...
    @property
    def gates(self) -> GateList:
        """
        GateList: all the gates of the system
        """
    @property
    def model_area(self) -> ModelArea:
        """
        ModelArea: returns the model area this hydro-power-system is a part of
        
        See also:
            ModelArea
        """
    @model_area.setter
    def model_area(self, arg1: ModelArea) -> None:
        ...
    @property
    def obj(self) -> typing.Any:
        """
        object: a python object
        """
    @obj.setter
    def obj(self, arg1: typing.Any) -> None:
        ...
class HydroPowerSystemBuilder:
    """
    class to support building hydro-power-systems save and easy
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, hydro_power_system: HydroPowerSystem) -> None:
        ...
    def create_aggregate(self, id: int, name: str, json: str = '') -> Unit:
        """
        creates a new unit with the specified parameters
        """
    def create_catchment(self, id: int, name: str, json: str = '') -> Catchment:
        """
        create and add catchmment to the system
        """
    def create_gate(self, id: int, name: str, json: str = '') -> Gate:
        """
        create and add a gate to the system
        """
    def create_power_plant(self, id: int, name: str, json: str = '') -> PowerPlant:
        """
        creates and adds a power plant to the system
        """
    def create_power_station(self, id: int, name: str, json: str = '') -> PowerPlant:
        """
        creates and adds a power plant to the system
        """
    def create_reservoir(self, id: int, name: str, json: str = '') -> Reservoir:
        """
        creates and adds a reservoir to the system
        """
    def create_river(self, id: int, name: str, json: str = '') -> Waterway:
        """
        create and add river to the system
        """
    def create_tunnel(self, id: int, name: str, json: str = '') -> Waterway:
        """
        create and add river to the system
        """
    def create_unit(self, id: int, name: str, json: str = '') -> Unit:
        """
        creates a new unit with the specified parameters
        """
    def create_water_route(self, id: int, name: str, json: str = '') -> Waterway:
        """
        create and add river to the system
        """
    def create_waterway(self, id: int, name: str, json: str = '') -> Waterway:
        """
        create and add river to the system
        """
class HydroPowerSystemList:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: HydroPowerSystemList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> HydroPowerSystemList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> HydroPowerSystem:
        ...
    @typing.overload
    def __getitem__(self, arg0: str) -> HydroPowerSystem:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: HydroPowerSystemList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[HydroPowerSystem]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: HydroPowerSystemList) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: HydroPowerSystem) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: HydroPowerSystemList) -> None:
        """
        Assign list elements using a slice object
        """
    def __str__(self) -> str:
        ...
    def append(self, x: HydroPowerSystem) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    @typing.overload
    def extend(self, L: HydroPowerSystemList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: HydroPowerSystem) -> None:
        """
        Insert an item at a given position.
        """
    def items(self) -> list[tuple[str, HydroPowerSystem]]:
        ...
    def keys(self) -> list[str]:
        ...
    @typing.overload
    def pop(self) -> HydroPowerSystem:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> HydroPowerSystem:
        """
        Remove and return the item at index ``i``
        """
    def size(self) -> int:
        ...
    def values(self) -> HydroPowerSystemList:
        ...
class Model:
    """
    The Model class describes the  LTM (persisted) model
    A model consists of model_areas and power-lines interconnecting them.
    To buid a model use the .add_area() and .add_power_line() methods
    
    See also:
        ModelArea,PowerLine,PowerModule
    """
    custom: AnyAttrDict
    id: int
    json: str
    name: str
    ts: TsAttrDict
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @staticmethod
    def from_blob(blob: shyft.time_series.ByteVector) -> Model:
        """
        constructs a model from a blob previously created by the to_blob method
        
        Args:
            blob (ByteVector): blob representation of the model, as create by the to_blob method
        """
    def __eq__(self, arg0: Model) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __init__(self, id: int, name: str, json: str = '') -> None:
        """
        constructs a Model object with the specified parameters
        
        Args:
            id (int): a global unique identifier of the mode
        
            name (string): the name of the model
        
            json (string): extra info as json for the model
        """
    def __ne__(self, arg0: Model) -> bool:
        ...
    def create_model_area(self, uid: int, name: str, json: str = '') -> ModelArea:
        """
        create and add an area to the model.
        ensures that area_name, and that area_id is unique.
        
        Args:
            uid (int): unique identifier for the area, must be unique within model
        
            name (string): any valid area-name, must be unique within model
        
            json (string): json for the area
        
        Returns:
            ModelArea: area. a reference to the newly added area
        
        See also:
            add_area
        """
    def create_power_line(self, a: ModelArea, b: ModelArea, id: int, name: str, json: str = '') -> PowerLine:
        """
        create and add a power line with capacity_MW between area a and b to the model
        
        Args:
            a (ModelArea): from existing model-area, that is part of the current model
        
            b (ModelArea): to existing model-area, that is part of the current model
        
            uid (int): unique ID of the power-line
        
            name (string): unique name of the power-line
        
            json (string): json for the power-line
        
        Returns:
            PowerLine: pl. the newly created power-line, that is now a part of the model
        """
    def create_power_module(self, model_area: ModelArea, id: int, name: str, json: str = '') -> PowerModule:
        """
        create and add power-module to the area, doing validity checks
        
        Args:
            model_area (ModelArea): the model-area for which we create a power-module
        
            uid (string): encoded power_type/load/wind module id
        
            module_name (string): unique module-name for each area
        
            json (string): json for the pm
        
        Returns:
            PowerModule: pm. a reference to the created and added power-module
        """
    def equal_content(self, other: Model) -> bool:
        """
        Compare this model with other_model for equality, except for the `.id`, `.name`,`.created`, attributes of the model it self.
        This is the same as the equal,==, operation, except that the self model local attributes are not compared.
        This method can be used to determine that two models have the same content, even if they model.id etc. are different.
        
        Args:
            other (Model): The model to compare with
        
        Returns:
            bool: equal. true if other have exactly the same content as self(disregarding the model .id,.name,.created,.json attributes)
        """
    def equal_structure(self, other: Model) -> bool:
        """
        Compare this model with other_model for equality in topology and interconnections.
        The comparison is using each object`.id` member to identify the same objects.
        Notice that the attributes of the objects are not considered, only the topology.
        
        Args:
            other (Model): The model to compare with
        
        Returns:
            bool: equal. true if other_model has structure and objects as self
        """
    def get_tsm_object(self, key: str) -> ts_attr:
        """
        Get a specific extra time series for this object.
        
        The returned time series is wrapped in an object which exposes method for retrieving url etc.
        
        Args:
            key (str): The key in the tsm of the time series to get.
        
        Raises:
            runtime_error: If specified key does not exist.
        """
    def to_blob(self) -> shyft.time_series.ByteVector:
        """
        serialize the model into a blob
        
        Returns:
            ByteVector: blob. serialized version of the model
        
        See also:
            from_blob
        """
    @property
    def area(self) -> AreaDict:
        """
        ModelAreaDict: a dict(area-name,area) for the model-areas
        """
    @property
    def created(self) -> shyft.time_series.time:
        """
        time: The timestamp when the model was created, utc seconds 1970
        """
    @created.setter
    def created(self, arg0: shyft.time_series.time) -> None:
        ...
    @property
    def obj(self) -> typing.Any:
        """
        object: a python object
        """
    @obj.setter
    def obj(self, arg1: typing.Any) -> None:
        ...
    @property
    def power_lines(self) -> PowerLineList:
        """
        PowerLineList: list of power-lines,each with connection to the areas they interconnect
        """
class ModelArea:
    """
    The ModelArea class describes the EMPS LTM (persisted) model-area
    A model-area consists of power modules and hydro-power-system.
    To buid a model-are use the .add_power_module() and the hydro-power-system builder
    
    See also:
        Model,PowerLine,PowerModule,HydroPowerSystem
    """
    custom: AnyAttrDict
    id: int
    json: str
    name: str
    ts: TsAttrDict
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, arg0: ModelArea) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __init__(self, model: Model, id: int, name: str, json: str = '') -> None:
        """
        constructs a ModelArea object with the specified parameters
        
        Args:
            model (Model): the model owning the created model-area
        
            id (int): a global unique identifier of the model-area
        
            name (string): the name of the model-area
        
            json (string): extra info as json
        """
    def __ne__(self, arg0: ModelArea) -> bool:
        ...
    def create_power_module(self, uid: int, name: str, json: str = '') -> PowerModule:
        """
        create and add power-module to the area, doing validity checks
        
        Args:
            id (string): encoded power_type/load/wind module id
        
            module_name (string): unique module-name for each area
        
            json (string): json for the pm
        
        Returns:
            PowerModule: pm. a reference to the created and added power-module
        """
    def equal_structure(self, other: ModelArea) -> bool:
        """
        Compare this model-area with other_model-area for equality in topology and interconnections.
        The comparison is using each object`.id` member to identify the same objects.
        Notice that the attributes of the objects are not considered, only the topology.
        
        Args:
            other (ModelArea): The model-area to compare with
        
        Returns:
            bool: equal. true if other_model has structure and objects as self
        """
    def get_tsm_object(self, key: str) -> ts_attr:
        """
        Get a specific extra time series for this object.
        
        The returned time series is wrapped in an object which exposes method for retrieving url etc.
        
        Args:
            key (str): The key in the tsm of the time series to get.
        
        Raises:
            runtime_error: If specified key does not exist.
        """
    @property
    def detailed_hydro(self) -> HydroPowerSystem:
        """
        HydroPowerSystem:  detailed hydro description.
        
        See also:
            HydroPowerSystem
        """
    @detailed_hydro.setter
    def detailed_hydro(self, arg1: HydroPowerSystem) -> None:
        ...
    @property
    def model(self) -> Model:
        """
        Model: the model for the area
        """
    @property
    def obj(self) -> typing.Any:
        """
        object: a python object
        """
    @obj.setter
    def obj(self, arg1: typing.Any) -> None:
        ...
    @property
    def power_modules(self) -> PowerModuleDict:
        """
        PowerModuleDict: power-modules in this area, a dictionary using power-module unique id
        """
class ModelBuilder:
    """
    This class helps building an EMPS model, step by step
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, model: Model) -> None:
        """
        Make a model-builder for the model
        The model can be modified/built using the methods
        available in this class
        
        Args:
            model (Model): the model to be built/modified
        """
    def create_model_area(self, id: int, name: str, json: str = '') -> ModelArea:
        """
        create and add an area to the model.
        ensures that area_name, and that area_id is unique.
        
        Args:
            id (int): unique identifier for the area, must be unique within model
        
            name (string): any valid area-name, must be unique within model
        
            json (string): json for the area
        
        Returns:
            ModelArea: area. a reference to the newly added area
        
        See also:
            add_area
        """
    def create_power_line(self, id: int, name: str, json: str, a: ModelArea, b: ModelArea) -> PowerLine:
        """
        create and add a power line with capacity_MW between area a and b to the model
        
        Args:
            id (int): unique ID of the power-line
        
            name (string): unique name of the power-line
        
            json (string): json for the power-line
        
            a (ModelArea): from existing model-area, that is part of the current model
        
            b (ModelArea): to existing model-area, that is part of the current model
        
        Returns:
            PowerLine: pl. the newly created power-line, that is now a part of the model
        """
    def create_power_module(self, id: int, name: str, json: str, model_area: ModelArea) -> PowerModule:
        """
        create and add power-module to the area, doing validity checks
        
        Args:
            id (int): encoded power_type/load/wind module id
        
            name (string): unique module-name for each area
        
            json (string): json for the pm
        
            model_area (ModelArea): the model-area for which we create a power-module
        
        Returns:
            PowerModule: pm. a reference to the created and added power-module
        """
class Point:
    """
    Simply a point (x,y)
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, arg0: Point) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, x: float, y: float) -> None:
        """
        construct a point with x and y
        """
    @typing.overload
    def __init__(self, clone: Point) -> None:
        """
        Create a clone.
        """
    def __ne__(self, arg0: Point) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    @property
    def x(self) -> float:
        """
        float: 
        """
    @x.setter
    def x(self, arg0: float) -> None:
        ...
    @property
    def y(self) -> float:
        """
        float: 
        """
    @y.setter
    def y(self, arg0: float) -> None:
        ...
class PowerLine:
    """
    The PowerLine class describes the LTM (persisted) power-line
    A power-line represents the transmission capacity between two model-areas.
    Use the ModelArea.create_power_line(a1,a2,id) to build a power line
    
    See also:
        Model,ModelArea,PowerModule,HydroPowerSystem
    """
    custom: AnyAttrDict
    id: int
    json: str
    name: str
    ts: TsAttrDict
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, arg0: PowerLine) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __init__(self, model: Model, area_1: ModelArea, area_2: ModelArea, id: int, name: str, json: str = '') -> None:
        """
        constructs a PowerLine object between area 1 and 2 with the specified id
        
        Args:
            model (Model): the model for the power-line
        
            area_1 (ModelArea): a reference to an existing area in the model
        
            area_2 (ModelArea): a reference to an existing area in the model
        
            id (int): a global unique identifier for the power-line
        
            name (string): a global unique name for the power-line
        
            json (string): extra json for the power-line
        """
    def __ne__(self, arg0: PowerLine) -> bool:
        ...
    def equal_structure(self, other: PowerLine) -> bool:
        """
        Compare this power-line with the other for equality in topology and interconnections.
        The comparison is using each object`.id` member to identify the same objects.
        Notice that the attributes of the objects are not considered, only the topology.
        
        Args:
            other (): The model-area to compare with
        
        Returns:
            bool: equal. true if other has structure equal to self
        """
    def get_tsm_object(self, key: str) -> ts_attr:
        """
        Get a specific extra time series for this object.
        
        The returned time series is wrapped in an object which exposes method for retrieving url etc.
        
        Args:
            key (str): The key in the tsm of the time series to get.
        
        Raises:
            runtime_error: If specified key does not exist.
        """
    @property
    def area_1(self) -> ModelArea:
        """
        ModelArea: reference to area-from
        """
    @area_1.setter
    def area_1(self, arg1: ModelArea) -> None:
        ...
    @property
    def area_2(self) -> ModelArea:
        """
        ModelArea: reference to area-to
        """
    @area_2.setter
    def area_2(self, arg1: ModelArea) -> None:
        ...
    @property
    def model(self) -> Model:
        """
        Model: the model for this power-line
        """
    @property
    def obj(self) -> typing.Any:
        """
        object: a python object
        """
    @obj.setter
    def obj(self, arg1: typing.Any) -> None:
        ...
class PowerLineList:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: PowerLineList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> PowerLineList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> PowerLine:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: PowerLineList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[PowerLine]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: PowerLineList) -> bool:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: PowerLine) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: PowerLineList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: PowerLine) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    @typing.overload
    def extend(self, L: PowerLineList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: PowerLine) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> PowerLine:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> PowerLine:
        """
        Remove and return the item at index ``i``
        """
    def size(self) -> int:
        ...
class PowerModule:
    """
    The PowerModule class describes the LTM (persisted) power-module
    A power-module represents an actor that consume/produces power for given price/volume
    characteristics. The user can influence this characteristics giving
    specific semantic load_type/power_type and extra data and/or relations to
    other power-modules within the same area.
    
    See also:
        Model,ModelArea,PowerLine,HydroPowerSystem
    """
    custom: AnyAttrDict
    id: int
    json: str
    name: str
    ts: TsAttrDict
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, arg0: PowerModule) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __init__(self, area: ModelArea, id: int, name: str, json: str = '') -> None:
        """
        constructs a PowerModule with specified mandatory name and module-id
        
        Args:
            area (ModelArea): the area for this power-module
        
            id (int): unique pm-id for area
        
            name (string): the name of the power-module
        
            json (string): optional json 
        """
    def __ne__(self, arg0: PowerModule) -> bool:
        ...
    def get_tsm_object(self, key: str) -> ts_attr:
        """
        Get a specific extra time series for this object.
        
        The returned time series is wrapped in an object which exposes method for retrieving url etc.
        
        Args:
            key (str): The key in the tsm of the time series to get.
        
        Raises:
            runtime_error: If specified key does not exist.
        """
    @property
    def area(self) -> ModelArea:
        """
        ModelArea: the model-area for this power-module
        """
    @property
    def obj(self) -> typing.Any:
        """
        object: a python object
        """
    @obj.setter
    def obj(self, arg1: typing.Any) -> None:
        ...
class PowerModuleDict:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the map is nonempty
        """
    @typing.overload
    def __contains__(self, arg0: int) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: typing.Any) -> bool:
        ...
    def __delitem__(self, arg0: int) -> None:
        ...
    def __eq__(self, arg0: PowerModuleDict) -> bool:
        ...
    def __getitem__(self, arg0: int) -> PowerModule:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: PowerModuleDict) -> None:
        """
        CopyConstructor
        """
    def __iter__(self) -> typing.Iterator[int]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: PowerModuleDict) -> bool:
        ...
    def __setitem__(self, arg0: int, arg1: PowerModule) -> None:
        ...
    def get(self, key: int, default: PowerModule | None = None) -> PowerModule | None:
        """
        Return the value for key if key is in the dictionary, else default.
        """
    def items(self) -> typing.ItemsView:
        ...
    def keys(self) -> typing.KeysView:
        ...
    def values(self) -> typing.ValuesView:
        ...
class PowerPlant:
    """
    A hydro power plant is the site/building that contains a number of units.
    The attributes of the power plant, are typically sum-requirement and/or operations that applies
    all of the units.
    
    """
    custom: AnyAttrDict
    id: int
    json: str
    name: str
    ts: TsAttrDict
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, arg0: PowerPlant) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __init__(self, id: int, name: str, json: str, hps: HydroPowerSystem) -> None:
        ...
    def __ne__(self, arg0: PowerPlant) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def add_aggregate(self, unit: Unit) -> None:
        """
        add unit to plant
        """
    def add_unit(self, unit: Unit) -> None:
        """
        add unit to plant
        """
    def get_tsm_object(self, key: str) -> ts_attr:
        """
        Get a specific extra time series for this object.
        
        The returned time series is wrapped in an object which exposes method for retrieving url etc.
        
        Args:
            key (str): The key in the tsm of the time series to get.
        
        Raises:
            runtime_error: If specified key does not exist.
        """
    def remove_aggregate(self, unit: Unit) -> None:
        """
        remove unit from plant
        """
    def remove_unit(self, unit: Unit) -> None:
        """
        remove unit from plant
        """
    @property
    def aggregates(self) -> UnitList:
        """
        UnitList: associated units
        """
    @aggregates.setter
    def aggregates(self, arg0: UnitList) -> None:
        ...
    @property
    def hps(self) -> HydroPowerSystem:
        """
        HydroPowerSystem: returns the hydro power system this component is a part of
        """
    @property
    def obj(self) -> typing.Any:
        """
        object: a python object
        """
    @obj.setter
    def obj(self, arg1: typing.Any) -> None:
        ...
    @property
    def units(self) -> UnitList:
        """
        UnitList: associated units
        """
    @units.setter
    def units(self, arg0: UnitList) -> None:
        ...
class PowerPlantList:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: PowerPlantList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> PowerPlantList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> PowerPlant:
        ...
    @typing.overload
    def __getitem__(self, arg0: str) -> PowerPlant:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: PowerPlantList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[PowerPlant]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: PowerPlantList) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: PowerPlant) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: PowerPlantList) -> None:
        """
        Assign list elements using a slice object
        """
    def __str__(self) -> str:
        ...
    def append(self, x: PowerPlant) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    @typing.overload
    def extend(self, L: PowerPlantList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: PowerPlant) -> None:
        """
        Insert an item at a given position.
        """
    def items(self) -> list[tuple[str, PowerPlant]]:
        ...
    def keys(self) -> list[str]:
        ...
    @typing.overload
    def pop(self) -> PowerPlant:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> PowerPlant:
        """
        Remove and return the item at index ``i``
        """
    def size(self) -> int:
        ...
    def values(self) -> PowerPlantList:
        ...
class Reservoir(HydroComponent):
    """
    
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, arg0: Reservoir) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __init__(self, id: int, name: str, json: str, hps: HydroPowerSystem) -> None:
        ...
    def __ne__(self, arg0: Reservoir) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def input_from(self, other: Waterway) -> Reservoir:
        """
        Connect the input of the reservoir to the output of the waterway.
        """
    def output_to(self, other: Waterway, role: ConnectionRole = ConnectionRole.main) -> Reservoir:
        """
        Connect the output of this reservoir to the input of the waterway, and assign the connection role
        """
class ReservoirList:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: ReservoirList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> ReservoirList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> Reservoir:
        ...
    @typing.overload
    def __getitem__(self, arg0: str) -> Reservoir:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: ReservoirList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[Reservoir]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: ReservoirList) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: Reservoir) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: ReservoirList) -> None:
        """
        Assign list elements using a slice object
        """
    def __str__(self) -> str:
        ...
    def append(self, x: Reservoir) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    @typing.overload
    def extend(self, L: ReservoirList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: Reservoir) -> None:
        """
        Insert an item at a given position.
        """
    def items(self) -> list[tuple[str, Reservoir]]:
        ...
    def keys(self) -> list[str]:
        ...
    @typing.overload
    def pop(self) -> Reservoir:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> Reservoir:
        """
        Remove and return the item at index ``i``
        """
    def size(self) -> int:
        ...
    def values(self) -> ReservoirList:
        ...
class Run:
    """
    Provides a Run concept, goes through states, created->prepinput->running->collect_result->frozen
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, arg0: Run) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, id: int, name: str, created: shyft.time_series.time, json: str = '', mid: int = 0) -> None:
        """
        create a run
        """
    def __ne__(self, arg0: Run) -> bool:
        ...
    @property
    def created(self) -> shyft.time_series.time:
        """
        the time of creation, or last modification of the model
        """
    @created.setter
    def created(self, arg0: shyft.time_series.time) -> None:
        ...
    @property
    def id(self) -> int:
        """
        the unique model id, can be used to retrieve the real model
        """
    @id.setter
    def id(self, arg0: int) -> None:
        ...
    @property
    def json(self) -> str:
        """
        a json formatted string to enable scripting and python to store more information
        """
    @json.setter
    def json(self, arg0: str) -> None:
        ...
    @property
    def mid(self) -> int:
        """
        model id (attached) for this run
        """
    @mid.setter
    def mid(self, arg0: int) -> None:
        ...
    @property
    def name(self) -> str:
        """
        any useful name or description
        """
    @name.setter
    def name(self, arg0: str) -> None:
        ...
    @property
    def state(self) -> run_state:
        """
        the current observed state for the run, like created, running,finished_run etc
        """
    @state.setter
    def state(self, arg0: run_state) -> None:
        ...
class RunClient:
    """
    The client-api for the generic run-repository
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @staticmethod
    def get_model_infos(*args, **kwargs) -> list[shyft.time_series.ModelInfo]:
        """
        returns all or selected model-info objects based on model-identifiers(mids)
        
        Args:
            mids (IntVector): empty = all, or a list of known exisiting model-identifiers
        
            created_in (UtcPeriod): For which period you are interested in model-infos.
        
        Returns:
            ModelInfoVector: model_infos. Strongly typed list of ModelInfo
        """
    def __init__(self, host_port: str, timeout_ms: int, operation_timeout_ms: int = 0) -> None:
        """
        Creates a python client that can communicate with the corresponding server
        """
    def close(self) -> None:
        """
        Close the connection. It will automatically reopen if needed.
        """
    def read_model(self, mid: int) -> Run:
        """
        Read and return the model for specified model-identifier (mid)
        
        Args:
            mid (int): the model-identifer for the wanted model
        
        Returns:
            Model: m. The resulting model from the server
        """
    def read_models(self, mids: list[int]) -> list[Run]:
        """
        Read and return the model for specified model-identifier (mid)
        
        Args:
            mids (list[int]): A strongly typed list of ints, the model-identifers for the wanted models
        
        Returns:
            Model: m. The resulting model from the server
        """
    def remove_model(self, mid: int) -> int:
        """
        Remove the specified model bymodel-identifier (mid)
        
        Args:
            mid (int): the model-identifer for the wanted model
        
        Returns:
            int: ec. 0 or error-code?
        """
    def store_model(self, m: Run, mi: shyft.time_series.ModelInfo) -> int:
        """
        Store the model to backend, if m.id==0 then a new unique model-info is created and used
        
        Args:
            m (Model): The model to store
        
            mi (ModelInfo): The model-info to store for the model
        
        Returns:
            int: mid. model-identifier for the stored model and model-info
        """
    def update_model_info(self, mid: int, mi: shyft.time_series.ModelInfo) -> bool:
        """
        Update the model-info for specified model-identifier(mid)
        
        Args:
            mid (int): model-identifer
        
            mi (ModelInfo): The new updated model-info
        
        Returns:
            bool: ok. true if success
        """
    @property
    def host_port(self) -> str:
        """
        str: Endpoint network address of the remote server.
        """
    @property
    def is_open(self) -> bool:
        """
        bool: If the connection to the remote server is (still) open.
        """
    @property
    def operation_timeout_ms(self) -> int:
        """
        int: Operation timeout for remote server operations, in number milliseconds.
        """
    @operation_timeout_ms.setter
    def operation_timeout_ms(self, arg1: int) -> None:
        ...
    @property
    def reconnect_count(self) -> int:
        """
        int: Number of reconnects to the remote server that have been performed.
        """
    @property
    def timeout_ms(self) -> int:
        """
        int: Timout for remote server operations, in number milliseconds.
        """
class RunServer:
    """
    The server-side component for the skeleton generic run repository
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @staticmethod
    def get_model_infos(*args, **kwargs) -> list[shyft.time_series.ModelInfo]:
        """
        returns all or selected model-info objects based on model-identifiers(mids)
        
        Args:
            mids (IntVector): empty = all, or a list of known exisiting model-identifiers
        
            created_in (UtcPeriod): For which period you are interested in model-infos.
        
        Returns:
            ModelInfoVector: model_infos. Strongly typed list of ModelInfo
        """
    def __init__(self, root_dir: str, config: shyft.time_series.ServerConfig = ...) -> None:
        """
        Creates a server object that serves models from root_dir.
        The root_dir will be create if it does not exists.
        
        Args:
            root_dir (str): Path to the root-directory that keeps/will keep the model-files
        
            config (ServerConfig): Configuration of the server
        """
    def get_listening_port(self) -> int:
        """
        returns the port number it's listening at for serving incoming request
        """
    def get_max_connections(self) -> int:
        """
        returns the maximum number of connections to be served concurrently
        """
    def is_running(self) -> bool:
        """
        true if server is listening and running
        
        See also:
            start_server()
        """
    def read_model(self, mid: int) -> Run:
        """
        Read and return the model for specified model-identifier (mid)
        
        Args:
            mid (int): the model-identifer for the wanted model
        
        Returns:
            Model: m. The resulting model from the server
        """
    def read_model_blob(self, mid: int) -> list[str]:
        """
        Read and return the model blob for specified model-identifier (mid)
        
        Args:
            mid (int): the model-identifer for the wanted model
        
        Returns:
            ByteVector: m. The resulting blob model from the server
        """
    def read_models(self, mids: list[int]) -> list[Run]:
        """
        Read and return the model for specified model-identifier (mid)
        
        Args:
            mids (list[int]): A strongly typed list of ints, the model-identifers for the wanted models
        
        Returns:
            Model: m. The resulting model from the server
        """
    def remove_model(self, mid: int) -> int:
        """
        Remove the specified model bymodel-identifier (mid)
        
        Args:
            mid (int): the model-identifer for the wanted model
        
        Returns:
            int: ec. 0 or error-code?
        """
    def set_listening_ip(self, ip: str) -> None:
        """
        set the listening port for the service
        
        Args:
            ip (str): ip or host-name to start listening on
        
        Returns:
            None: nothing. 
        """
    def set_listening_port(self, port_no: int) -> None:
        """
        set the listening port for the service
        
        Args:
            port_no (int): a valid and available tcp-ip port number to listen on.
            typically it could be 20000 (avoid using official reserved numbers)
        
        Returns:
            None: nothing. 
        """
    def set_max_connections(self, max_connect: int) -> None:
        """
        limits simultaneous connections to the server (it's multithreaded, and uses on thread pr. connect)
        
        Args:
            max_connect (int): maximum number of connections before denying more connections
        
        See also:
            get_max_connections()
        """
    def start_server(self) -> int:
        """
        start server listening in background, and processing messages
        
        See also:
            set_listening_port(port_no),is_running
        
        Returns:
            in: port_no. the port used for listening operations, either the value as by set_listening_port, or if it was unspecified, a new available port
        """
    def stop_server(self, timeout: int = 1000) -> None:
        """
        stop serving connections, gracefully.
        
        See also:
            start_server()
        """
    def store_model(self, m: Run, mi: shyft.time_series.ModelInfo) -> int:
        """
        Store the model to backend, if m.id==0 then a new unique model-info is created and used
        
        Args:
            m (Model): The model to store
        
            mi (ModelInfo): The model-info to store for the model
        
        Returns:
            int: mid. model-identifier for the stored model and model-info
        """
    def update_model_info(self, mid: int, mi: shyft.time_series.ModelInfo) -> bool:
        """
        Update the model-info for specified model-identifier(mid)
        
        Args:
            mid (int): model-identifer
        
            mi (ModelInfo): The new updated model-info
        
        Returns:
            bool: ok. true if success
        """
    @property
    def stale_connection_close_count(self) -> int:
        """
        int: returns count of connection closed due to stale/no communication activity
        """
class Server:
    """
    The server-side component for the skeleton energy_market model repository
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @staticmethod
    def get_model_infos(*args, **kwargs) -> list[shyft.time_series.ModelInfo]:
        """
        returns all or selected model-info objects based on model-identifiers(mids)
        
        Args:
            mids (IntVector): empty = all, or a list of known exisiting model-identifiers
        
            created_in (UtcPeriod): For which period you are interested in model-infos.
        
        Returns:
            ModelInfoVector: model_infos. Strongly typed list of ModelInfo
        """
    def __init__(self, root_dir: str, config: shyft.time_series.ServerConfig = ...) -> None:
        """
        Creates a server object that serves models from root_dir.
        The root_dir will be create if it does not exists.
        
        Args:
            root_dir (str): Path to the root-directory that keeps/will keep the model-files
        
            config (ServerConfig): Configuration of the server
        """
    def get_listening_port(self) -> int:
        """
        returns the port number it's listening at for serving incoming request
        """
    def get_max_connections(self) -> int:
        """
        returns the maximum number of connections to be served concurrently
        """
    def is_running(self) -> bool:
        """
        true if server is listening and running
        
        See also:
            start_server()
        """
    def read_model(self, mid: int) -> Model:
        """
        Read and return the model for specified model-identifier (mid)
        
        Args:
            mid (int): the model-identifer for the wanted model
        
        Returns:
            Model: m. The resulting model from the server
        """
    def read_model_blob(self, mid: int) -> list[str]:
        """
        Read and return the model blob for specified model-identifier (mid)
        
        Args:
            mid (int): the model-identifer for the wanted model
        
        Returns:
            ByteVector: m. The resulting blob model from the server
        """
    def read_models(self, mids: list[int]) -> list[Model]:
        """
        Read and return the model for specified model-identifier (mid)
        
        Args:
            mids (list[int]): A strongly typed list of ints, the model-identifers for the wanted models
        
        Returns:
            Model: m. The resulting model from the server
        """
    def remove_model(self, mid: int) -> int:
        """
        Remove the specified model bymodel-identifier (mid)
        
        Args:
            mid (int): the model-identifer for the wanted model
        
        Returns:
            int: ec. 0 or error-code?
        """
    def set_listening_ip(self, ip: str) -> None:
        """
        set the listening port for the service
        
        Args:
            ip (str): ip or host-name to start listening on
        
        Returns:
            None: nothing. 
        """
    def set_listening_port(self, port_no: int) -> None:
        """
        set the listening port for the service
        
        Args:
            port_no (int): a valid and available tcp-ip port number to listen on.
            typically it could be 20000 (avoid using official reserved numbers)
        
        Returns:
            None: nothing. 
        """
    def set_max_connections(self, max_connect: int) -> None:
        """
        limits simultaneous connections to the server (it's multithreaded, and uses on thread pr. connect)
        
        Args:
            max_connect (int): maximum number of connections before denying more connections
        
        See also:
            get_max_connections()
        """
    def start_server(self) -> int:
        """
        start server listening in background, and processing messages
        
        See also:
            set_listening_port(port_no),is_running
        
        Returns:
            in: port_no. the port used for listening operations, either the value as by set_listening_port, or if it was unspecified, a new available port
        """
    def stop_server(self, timeout: int = 1000) -> None:
        """
        stop serving connections, gracefully.
        
        See also:
            start_server()
        """
    def store_model(self, m: Model, mi: shyft.time_series.ModelInfo) -> int:
        """
        Store the model to backend, if m.id==0 then a new unique model-info is created and used
        
        Args:
            m (Model): The model to store
        
            mi (ModelInfo): The model-info to store for the model
        
        Returns:
            int: mid. model-identifier for the stored model and model-info
        """
    def update_model_info(self, mid: int, mi: shyft.time_series.ModelInfo) -> bool:
        """
        Update the model-info for specified model-identifier(mid)
        
        Args:
            mid (int): model-identifer
        
            mi (ModelInfo): The new updated model-info
        
        Returns:
            bool: ok. true if success
        """
    @property
    def stale_connection_close_count(self) -> int:
        """
        int: returns count of connection closed due to stale/no communication activity
        """
class TsAttrDict:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the map is nonempty
        """
    @typing.overload
    def __contains__(self, arg0: str) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: typing.Any) -> bool:
        ...
    def __delitem__(self, arg0: str) -> None:
        ...
    def __getitem__(self, arg0: str) -> shyft.time_series.TimeSeries:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: TsAttrDict) -> None:
        """
        CopyConstructor
        """
    def __iter__(self) -> typing.Iterator[str]:
        ...
    def __len__(self) -> int:
        ...
    def __repr__(self) -> str:
        ...
    def __setitem__(self, arg0: str, arg1: shyft.time_series.TimeSeries) -> None:
        ...
    def __str__(self) -> str:
        ...
    def get(self, key: str, default: shyft.time_series.TimeSeries | None = None) -> shyft.time_series.TimeSeries | None:
        """
        Return the value for key if key is in the dictionary, else default.
        """
    def items(self) -> typing.ItemsView:
        ...
    def keys(self) -> typing.KeysView:
        ...
    def values(self) -> typing.ValuesView:
        ...
class TurbineCapability:
    """
    Describes the capabilities of a turbine.
    
    
    Members:
    
      turbine_none
    
      turbine_forward
    
      turbine_backward
    
      turbine_reversible
    """
    __members__: typing.ClassVar[dict[str, TurbineCapability]]  # value = {'turbine_none': <TurbineCapability.turbine_none: 0>, 'turbine_forward': <TurbineCapability.turbine_forward: 1>, 'turbine_backward': <TurbineCapability.turbine_backward: 2>, 'turbine_reversible': <TurbineCapability.turbine_reversible: 3>}
    turbine_backward: typing.ClassVar[TurbineCapability]  # value = <TurbineCapability.turbine_backward: 2>
    turbine_forward: typing.ClassVar[TurbineCapability]  # value = <TurbineCapability.turbine_forward: 1>
    turbine_none: typing.ClassVar[TurbineCapability]  # value = <TurbineCapability.turbine_none: 0>
    turbine_reversible: typing.ClassVar[TurbineCapability]  # value = <TurbineCapability.turbine_reversible: 3>
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class TurbineDescription:
    """
    Complete description of efficiencies a turbine for all operating zones.
    
    Pelton turbines typically have multiple operating zones; one for each needle combination.
    Other turbines normally have only a single operating zone describing the entire turbine,
    but may have more than one to model different isolated operating zones.
    Each operating zone is described with a turbine efficiency object, which in turn may
    contain multiple efficiency curves; one for each net head.
    """
    __hash__: typing.ClassVar[None] = None
    operating_zones: TurbineOperatingZoneList
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, arg0: TurbineDescription) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, operating_zones: TurbineOperatingZoneList) -> None:
        ...
    @typing.overload
    def __init__(self, clone: TurbineDescription) -> None:
        """
        Create a clone.
        """
    def __ne__(self, arg0: TurbineDescription) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def capability(self) -> TurbineCapability:
        """
        Return the capability of the turbine
        """
    def get_operating_zone(self, p: float) -> TurbineOperatingZone:
        """
        Find operating zone for given production value p
        
        Notes:
            If operating zones are overlapping then the zone with lowest value of production_min will be selected.
        """
class TurbineOperatingZone:
    """
    A turbine efficiency.
    
    Defined by a set of efficiency curves, one for each net head, with optional production limits.
    Part of the turbine description, to describe the efficiency of an entire turbine, or an isolated
    operating zone or a Pelton needle combination. Production limits are only relevant when representing
    an isolated operating zone or a Pelton needle combination.
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, arg0: TurbineOperatingZone) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, efficiency_curves: XyPointCurveWithZList) -> None:
        ...
    @typing.overload
    def __init__(self, efficiency_curves: XyPointCurveWithZList, production_min: float, production_max: float) -> None:
        ...
    @typing.overload
    def __init__(self, efficiency_curves: XyPointCurveWithZList, production_min: float, production_max: float, production_nominal: float, fcr_min: float, fcr_max: float) -> None:
        ...
    @typing.overload
    def __init__(self, clone: TurbineOperatingZone) -> None:
        """
        Create a clone.
        """
    def __ne__(self, arg0: TurbineOperatingZone) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def evaluate(self, x: float, z: float) -> float:
        """
        Evaluate the efficiency curves at a point (x, z)
        """
    @property
    def efficiency_curves(self) -> XyPointCurveWithZList:
        """
        XyPointCurveWithZList: A list of XyPointCurveWithZ efficiency curves for the net head range of the entire turbine, or an isolated operating zone or a Pelton needle combination.
        """
    @efficiency_curves.setter
    def efficiency_curves(self, arg0: XyPointCurveWithZList) -> None:
        ...
    @property
    def fcr_max(self) -> float:
        """
        float: The temporary maximum production allowed for this set of efficiency curves when delivering FCR.
        
        Notes:
            Only relevant when representing an isolated operating zone or a Pelton needle combination.
        """
    @fcr_max.setter
    def fcr_max(self, arg0: float) -> None:
        ...
    @property
    def fcr_min(self) -> float:
        """
        float: The temporary minimum production allowed for this set of efficiency curves when delivering FCR.
        
        Notes:
            Only relevant when representing an isolated operating zone or a Pelton needle combination.
        """
    @fcr_min.setter
    def fcr_min(self, arg0: float) -> None:
        ...
    @property
    def production_max(self) -> float:
        """
        float: The maximum production for which the efficiency curves are valid.
        
        Notes:
            Only relevant when representing an isolated operating zone or a Pelton needle combination.
        """
    @production_max.setter
    def production_max(self, arg0: float) -> None:
        ...
    @property
    def production_min(self) -> float:
        """
        float: The minimum production for which the efficiency curves are valid.
        
        Notes:
            Only relevant when representing an isolated operating zone or a Pelton needle combination.
        """
    @production_min.setter
    def production_min(self, arg0: float) -> None:
        ...
    @property
    def production_nominal(self) -> float:
        """
        float: The nominal production, or installed/rated/nameplate capacity, for which the efficiency curves are valid.
        
        Notes:
            Only relevant when representing an isolated operating zone or a Pelton needle combination.
        """
    @production_nominal.setter
    def production_nominal(self, arg0: float) -> None:
        ...
class TurbineOperatingZoneList:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: TurbineOperatingZoneList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> TurbineOperatingZoneList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> TurbineOperatingZone:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: TurbineOperatingZoneList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[TurbineOperatingZone]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: TurbineOperatingZoneList) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: TurbineOperatingZone) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: TurbineOperatingZoneList) -> None:
        """
        Assign list elements using a slice object
        """
    def __str__(self) -> str:
        ...
    def append(self, x: TurbineOperatingZone) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    @typing.overload
    def extend(self, L: TurbineOperatingZoneList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: TurbineOperatingZone) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> TurbineOperatingZone:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> TurbineOperatingZone:
        """
        Remove and return the item at index ``i``
        """
    def size(self) -> int:
        ...
class Unit(HydroComponent):
    """
    An Unit consist of a turbine and a connected generator.
    The turbine is hydrologically connected to upstream tunnel and downstream tunell/river.
    The generator part is connected to the electrical grid through a busbar.
    In the long term models, the entire power plant is represented by a virtual unit that represents
    the total capability of the power-plant.
    
    The short-term detailed models, usually describes every aggratate up to a granularity that is
    relevant for the short-term optimization/simulation horizont.
    
    A power plant is a collection of one or more units that are natural to group into one power plant.
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, arg0: Unit) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __init__(self, id: int, name: str, json: str, hps: HydroPowerSystem) -> None:
        ...
    def __ne__(self, arg0: Unit) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def input_from(self, other: Waterway) -> Unit:
        """
        Connect the input of this unit to the output of the waterway.
        """
    def output_to(self, other: Waterway) -> Unit:
        """
        Connect the output of this unit to the input of the waterway.
        """
    @property
    def downstream(self) -> Waterway:
        """
        Waterway: returns downstream waterway(river/tunnel) object(if any)
        """
    @property
    def is_pump(self) -> bool:
        """
        bool: Returns true if the unit is a pump, otherwise, returns false
        """
    @property
    def power_plant(self) -> PowerPlant:
        """
        PowerPlant: return the hydro power plant associated with this unit
        """
    @property
    def power_station(self) -> PowerPlant:
        """
        PowerPlant: return the hydro power plant associated with this unit
        """
    @property
    def upstream(self) -> Waterway:
        """
        Waterway: returns upstream tunnel(water-route) object(if any)
        """
class UnitGroupType:
    """
    The unit-group type specifies the purpose of the group, and thus also how
    it is mapped to the optimization as constraint. E.g. operational reserve fcr_n.up.
    Current mapping to optimizer/shop:
    
        *        FCR* :  primary reserve, instant response, note, sensitivity set by droop settings on the unit 
        *       AFRR* : automatic frequency restoration reserve, ~ minute response
        *       MFRR* : it is the manual frequency restoration reserve, ~ 15 minute response
        *         FFR : NOT MAPPED, fast frequency restoration reserve, 49.5..49.7 Hz, ~ 1..2 sec response
        *        RR*  : NOT MAPPED, replacement reserve, 40..60 min response
        *      COMMIT : currently not mapped
        *  PRODUCTION : used for energy market area unit groups
    
    
    
    
    Members:
    
      UNSPECIFIED
    
      FCR_N_UP
    
      FCR_N_DOWN
    
      FCR_D_UP
    
      FCR_D_DOWN
    
      AFRR_UP
    
      AFRR_DOWN
    
      MFRR_UP
    
      MFRR_DOWN
    
      FFR
    
      RR_UP
    
      RR_DOWN
    
      COMMIT
    
      PRODUCTION
    """
    AFRR_DOWN: typing.ClassVar[UnitGroupType]  # value = <UnitGroupType.AFRR_DOWN: 6>
    AFRR_UP: typing.ClassVar[UnitGroupType]  # value = <UnitGroupType.AFRR_UP: 5>
    COMMIT: typing.ClassVar[UnitGroupType]  # value = <UnitGroupType.COMMIT: 12>
    FCR_D_DOWN: typing.ClassVar[UnitGroupType]  # value = <UnitGroupType.FCR_D_DOWN: 4>
    FCR_D_UP: typing.ClassVar[UnitGroupType]  # value = <UnitGroupType.FCR_D_UP: 3>
    FCR_N_DOWN: typing.ClassVar[UnitGroupType]  # value = <UnitGroupType.FCR_N_DOWN: 2>
    FCR_N_UP: typing.ClassVar[UnitGroupType]  # value = <UnitGroupType.FCR_N_UP: 1>
    FFR: typing.ClassVar[UnitGroupType]  # value = <UnitGroupType.FFR: 9>
    MFRR_DOWN: typing.ClassVar[UnitGroupType]  # value = <UnitGroupType.MFRR_DOWN: 8>
    MFRR_UP: typing.ClassVar[UnitGroupType]  # value = <UnitGroupType.MFRR_UP: 7>
    PRODUCTION: typing.ClassVar[UnitGroupType]  # value = <UnitGroupType.PRODUCTION: 13>
    RR_DOWN: typing.ClassVar[UnitGroupType]  # value = <UnitGroupType.RR_DOWN: 11>
    RR_UP: typing.ClassVar[UnitGroupType]  # value = <UnitGroupType.RR_UP: 10>
    UNSPECIFIED: typing.ClassVar[UnitGroupType]  # value = <UnitGroupType.UNSPECIFIED: 0>
    __members__: typing.ClassVar[dict[str, UnitGroupType]]  # value = {'UNSPECIFIED': <UnitGroupType.UNSPECIFIED: 0>, 'FCR_N_UP': <UnitGroupType.FCR_N_UP: 1>, 'FCR_N_DOWN': <UnitGroupType.FCR_N_DOWN: 2>, 'FCR_D_UP': <UnitGroupType.FCR_D_UP: 3>, 'FCR_D_DOWN': <UnitGroupType.FCR_D_DOWN: 4>, 'AFRR_UP': <UnitGroupType.AFRR_UP: 5>, 'AFRR_DOWN': <UnitGroupType.AFRR_DOWN: 6>, 'MFRR_UP': <UnitGroupType.MFRR_UP: 7>, 'MFRR_DOWN': <UnitGroupType.MFRR_DOWN: 8>, 'FFR': <UnitGroupType.FFR: 9>, 'RR_UP': <UnitGroupType.RR_UP: 10>, 'RR_DOWN': <UnitGroupType.RR_DOWN: 11>, 'COMMIT': <UnitGroupType.COMMIT: 12>, 'PRODUCTION': <UnitGroupType.PRODUCTION: 13>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class UnitList:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: UnitList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> UnitList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> Unit:
        ...
    @typing.overload
    def __getitem__(self, arg0: str) -> Unit:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: UnitList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[Unit]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: UnitList) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: Unit) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: UnitList) -> None:
        """
        Assign list elements using a slice object
        """
    def __str__(self) -> str:
        ...
    def append(self, x: Unit) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    @typing.overload
    def extend(self, L: UnitList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: Unit) -> None:
        """
        Insert an item at a given position.
        """
    def items(self) -> list[tuple[str, Unit]]:
        ...
    def keys(self) -> list[str]:
        ...
    @typing.overload
    def pop(self) -> Unit:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> Unit:
        """
        Remove and return the item at index ``i``
        """
    def size(self) -> int:
        ...
    def values(self) -> UnitList:
        ...
class Waterway(HydroComponent):
    """
    The waterway can be a river or a tunnel, and connects the reservoirs, units(turbine).
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, arg0: Waterway) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __init__(self, id: int, name: str, json: str, hps: HydroPowerSystem) -> None:
        ...
    def __ne__(self, arg0: Waterway) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def add_gate(self, gate: Gate) -> None:
        """
        add a gate to the waterway
        """
    @typing.overload
    def input_from(self, other: Waterway) -> Waterway:
        """
        Connect the input of this waterway to the output of the other waterway.
        """
    @typing.overload
    def input_from(self, other: Unit) -> Waterway:
        """
        Connect the input of this waterway to the output of the unit.
        """
    @typing.overload
    def input_from(self, reservoir: Reservoir, role: ConnectionRole = ConnectionRole.main) -> Waterway:
        """
        Connect the input of this waterway to the output of the reservoir, and assign the connection role.
        """
    @typing.overload
    def output_to(self, other: Waterway) -> Waterway:
        """
        Connect the output of this waterway to the input of the other waterway.
        """
    @typing.overload
    def output_to(self, other: Reservoir) -> Waterway:
        """
        Connect the output of this waterway to the input of the reservoir.
        """
    @typing.overload
    def output_to(self, other: Unit) -> Waterway:
        """
        Connect the output of this waterway to the input of the unit.
        """
    def remove_gate(self, gate: Gate) -> None:
        """
        remove a gate from the waterway
        """
    @property
    def downstream(self) -> HydroComponent:
        """
        HydroComponent: returns downstream object(if any)
        """
    @property
    def gates(self) -> GateList:
        """
        GateList: the gates attached to the inlet of the waterway
        """
    @property
    def upstream(self) -> HydroComponent:
        """
        HydroComponent: returns upstream object(if any)
        """
    @property
    def upstream_role(self) -> ConnectionRole:
        """
        the role the water way has relative to the component above
        """
class WaterwayList:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: WaterwayList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> WaterwayList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> Waterway:
        ...
    @typing.overload
    def __getitem__(self, arg0: str) -> Waterway:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: WaterwayList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[Waterway]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: WaterwayList) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: Waterway) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: WaterwayList) -> None:
        """
        Assign list elements using a slice object
        """
    def __str__(self) -> str:
        ...
    def append(self, x: Waterway) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    @typing.overload
    def extend(self, L: WaterwayList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: Waterway) -> None:
        """
        Insert an item at a given position.
        """
    def items(self) -> list[tuple[str, Waterway]]:
        ...
    def keys(self) -> list[str]:
        ...
    @typing.overload
    def pop(self) -> Waterway:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> Waterway:
        """
        Remove and return the item at index ``i``
        """
    def size(self) -> int:
        ...
    def values(self) -> WaterwayList:
        ...
class XyPointCurve:
    """
    A curve described using points, piecewise linear.
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, arg0: XyPointCurve) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, points: XyPointList) -> None:
        ...
    @typing.overload
    def __init__(self, x_vector: list[float], y_vector: list[float]) -> None:
        ...
    @typing.overload
    def __init__(self, clone: XyPointCurve) -> None:
        """
        Create a clone.
        """
    def __ne__(self, arg0: XyPointCurve) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    @typing.overload
    def calculate_x(self, x: float) -> float:
        """
        interpolating and extending
        """
    @typing.overload
    def calculate_x(self, x: shyft.time_series.TimeSeries, method: shyft.time_series.interpolation_scheme = 'linear') -> shyft.time_series.TimeSeries:
        """
        interpolating and extending
        """
    @typing.overload
    def calculate_y(self, x: float) -> float:
        """
        interpolating and extending
        """
    @typing.overload
    def calculate_y(self, x: shyft.time_series.TimeSeries, method: shyft.time_series.interpolation_scheme = 'linear') -> shyft.time_series.TimeSeries:
        """
        interpolating and extending
        """
    def is_convex(self) -> bool:
        """
        true if y=f(x) is convex
        """
    def is_mono_increasing(self) -> bool:
        """
        true if y=f(x) is monotone and increasing
        """
    def x_max(self) -> float:
        """
        returns largest value of x
        """
    def x_min(self) -> float:
        """
        returns smallest value of x
        """
    def y_max(self) -> float:
        """
        returns largest value of y
        """
    def y_min(self) -> float:
        """
        returns smallest value of y
        """
    @property
    def points(self) -> XyPointList:
        """
        PointList: describing the curve
        """
    @points.setter
    def points(self, arg0: XyPointList) -> None:
        ...
class XyPointCurveWithZ:
    """
    A XyPointCurve with a reference value z.
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, arg0: XyPointCurveWithZ) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, other: XyPointCurveWithZ) -> None:
        ...
    @typing.overload
    def __init__(self, xy_point_curve: XyPointCurve, z: float) -> None:
        ...
    def __ne__(self, arg0: XyPointCurveWithZ) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    @property
    def xy_point_curve(self) -> XyPointCurve:
        """
        XyPointCurve: describes the function at z
        """
    @xy_point_curve.setter
    def xy_point_curve(self, arg0: XyPointCurve) -> None:
        ...
    @property
    def z(self) -> float:
        """
        float: z value
        """
    @z.setter
    def z(self, arg0: float) -> None:
        ...
class XyPointCurveWithZList:
    """
    A strongly typed list of XyPointCurveWithZ.
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: XyPointCurveWithZList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> XyPointCurveWithZList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> XyPointCurveWithZ:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: XyPointCurveWithZList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[XyPointCurveWithZ]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: XyPointCurveWithZList) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: XyPointCurveWithZ) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: XyPointCurveWithZList) -> None:
        """
        Assign list elements using a slice object
        """
    def __str__(self) -> str:
        ...
    def append(self, x: XyPointCurveWithZ) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def evaluate(self, x: float, z: float) -> float:
        """
        Evaluate the curve at the point (x, z)
        """
    @typing.overload
    def extend(self, L: XyPointCurveWithZList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: XyPointCurveWithZ) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> XyPointCurveWithZ:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> XyPointCurveWithZ:
        """
        Remove and return the item at index ``i``
        """
    def size(self) -> int:
        ...
    def x_max(self) -> float:
        """
        returns largest value of x
        """
    def x_min(self) -> float:
        """
        returns smallest value of x
        """
    def y_max(self) -> float:
        """
        returns largest value of y
        """
    def y_min(self) -> float:
        """
        returns smallest value of y
        """
    def z_max(self) -> float:
        """
        returns largest value of z
        """
    def z_min(self) -> float:
        """
        returns smallest value of z
        """
class XyPointList:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: XyPointList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> XyPointList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> Point:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: XyPointList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[Point]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: XyPointList) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: Point) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: XyPointList) -> None:
        """
        Assign list elements using a slice object
        """
    def __str__(self) -> str:
        ...
    def append(self, x: Point) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    @typing.overload
    def extend(self, L: XyPointList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: Point) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> Point:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> Point:
        """
        Remove and return the item at index ``i``
        """
    def size(self) -> int:
        ...
class XyzPointCurve:
    """
    A 3D curve consisting of one or more 2D curves parametrised over a third variable.
    """
    __hash__: typing.ClassVar[None] = None
    curves: XyzPointCurveDict
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, arg0: XyzPointCurve) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, curves: XyPointCurveWithZList) -> None:
        """
        Create from a list.
        """
    @typing.overload
    def __init__(self, curves: XyzPointCurveDict) -> None:
        ...
    def __ne__(self, arg0: XyzPointCurve) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def evaluate(self, x: float, z: float) -> float:
        """
        Evaluate the curve at the point (x, z)
        """
    def get_curve(self, z: float) -> XyPointCurve:
        """
        get the curve assigned to the value
        """
    def gradient(self, arg0: float, arg1: float) -> typing.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(2)]:
        ...
    def set_curve(self, z: float, xy: XyPointCurve) -> None:
        """
        Assign an XyzPointCurve to a z-value
        """
class XyzPointCurveDict:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the map is nonempty
        """
    @typing.overload
    def __contains__(self, arg0: float) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: typing.Any) -> bool:
        ...
    def __delitem__(self, arg0: float) -> None:
        ...
    def __eq__(self, arg0: XyzPointCurveDict) -> bool:
        ...
    def __getitem__(self, arg0: float) -> XyPointCurve:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: XyzPointCurveDict) -> None:
        """
        CopyConstructor
        """
    def __iter__(self) -> typing.Iterator[float]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: XyzPointCurveDict) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setitem__(self, arg0: float, arg1: XyPointCurve) -> None:
        ...
    def __str__(self) -> str:
        ...
    def get(self, key: float, default: XyPointCurve | None = None) -> XyPointCurve | None:
        """
        Return the value for key if key is in the dictionary, else default.
        """
    def items(self) -> typing.ItemsView:
        ...
    def keys(self) -> typing.KeysView:
        ...
    def values(self) -> typing.ValuesView:
        ...
class bool_attr:
    """
    A wrapped attribute class encapsulates a basic type, like TimeSeries,
    and make it an optional property of the class.
    
     - `self.exists` property indicates the existence of the value
     - `self.value` property can be used to get/set the underlying value
     - `self.url()` generates url suitable for ui/expressions work
     - `self.remove()` clear/removes the attribute
    
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __eq__(self, arg0: bool_attr) -> bool:
        ...
    @typing.overload
    def __eq__(self, arg0: bool) -> bool:
        ...
    def __ne__(self, arg0: bool_attr) -> bool:
        ...
    def __neq__(self, arg0: bool) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def remove(self) -> None:
        """
        Remove the attribute.
        
        After calling this the .exists returns False.
        
        Returns:
            bool: removed_item. True if removed.
        False if it was already away when invoking the method.
        """
    def url(self, prefix: str = '', levels: int = -1, template_levels: int = -1, fmt: bool = False) -> str:
        """
        Generate an almost unique, url-like string for a proxy attribute.
        The string will be based on the attribute's ID, the owning object's type and ID,
        and the owning object's parent, if present.
        
        Args:
            prefix (str): What the resulting string starts with
        
            levels (int): How many levels of the url to include. levels == 0 includes only this level. Use level < 0 to include all levels
        
            template_levels (int): From what level, and onwards, to use templates instead of identifying string. Use template_levels < 0 to ensure no use of templates.
        
            fmt (bool): make string position format friendly, replacing {o_id} with {} etc. 
        
        Returns:
            str: attr_url. url-type string for the attribute
        """
    @property
    def exists(self) -> bool:
        """
        bool: Check if attribute is available/filled in.
        
        Returns:
            bool: . True if the attribute exists, otherwise False
        """
    @property
    def value(self) -> bool:
        """
        Access to the wrapped value to get or set it.
        """
    @value.setter
    def value(self, arg1: bool) -> None:
        ...
class double_attr:
    """
    A wrapped attribute class encapsulates a basic type, like TimeSeries,
    and make it an optional property of the class.
    
     - `self.exists` property indicates the existence of the value
     - `self.value` property can be used to get/set the underlying value
     - `self.url()` generates url suitable for ui/expressions work
     - `self.remove()` clear/removes the attribute
    
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __eq__(self, arg0: double_attr) -> bool:
        ...
    @typing.overload
    def __eq__(self, arg0: float) -> bool:
        ...
    def __ne__(self, arg0: double_attr) -> bool:
        ...
    def __neq__(self, arg0: float) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def remove(self) -> None:
        """
        Remove the attribute.
        
        After calling this the .exists returns False.
        
        Returns:
            bool: removed_item. True if removed.
        False if it was already away when invoking the method.
        """
    def url(self, prefix: str = '', levels: int = -1, template_levels: int = -1, fmt: bool = False) -> str:
        """
        Generate an almost unique, url-like string for a proxy attribute.
        The string will be based on the attribute's ID, the owning object's type and ID,
        and the owning object's parent, if present.
        
        Args:
            prefix (str): What the resulting string starts with
        
            levels (int): How many levels of the url to include. levels == 0 includes only this level. Use level < 0 to include all levels
        
            template_levels (int): From what level, and onwards, to use templates instead of identifying string. Use template_levels < 0 to ensure no use of templates.
        
            fmt (bool): make string position format friendly, replacing {o_id} with {} etc. 
        
        Returns:
            str: attr_url. url-type string for the attribute
        """
    @property
    def exists(self) -> bool:
        """
        bool: Check if attribute is available/filled in.
        
        Returns:
            bool: . True if the attribute exists, otherwise False
        """
    @property
    def value(self) -> float:
        """
        Access to the wrapped value to get or set it.
        """
    @value.setter
    def value(self, arg1: float) -> None:
        ...
class geo_point_attr:
    """
    A wrapped attribute class encapsulates a basic type, like TimeSeries,
    and make it an optional property of the class.
    
     - `self.exists` property indicates the existence of the value
     - `self.value` property can be used to get/set the underlying value
     - `self.url()` generates url suitable for ui/expressions work
     - `self.remove()` clear/removes the attribute
    
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __eq__(self, arg0: geo_point_attr) -> bool:
        ...
    @typing.overload
    def __eq__(self, arg0: shyft.time_series.GeoPoint) -> bool:
        ...
    def __ne__(self, arg0: geo_point_attr) -> bool:
        ...
    def __neq__(self, arg0: shyft.time_series.GeoPoint) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def remove(self) -> None:
        """
        Remove the attribute.
        
        After calling this the .exists returns False.
        
        Returns:
            bool: removed_item. True if removed.
        False if it was already away when invoking the method.
        """
    def url(self, prefix: str = '', levels: int = -1, template_levels: int = -1, fmt: bool = False) -> str:
        """
        Generate an almost unique, url-like string for a proxy attribute.
        The string will be based on the attribute's ID, the owning object's type and ID,
        and the owning object's parent, if present.
        
        Args:
            prefix (str): What the resulting string starts with
        
            levels (int): How many levels of the url to include. levels == 0 includes only this level. Use level < 0 to include all levels
        
            template_levels (int): From what level, and onwards, to use templates instead of identifying string. Use template_levels < 0 to ensure no use of templates.
        
            fmt (bool): make string position format friendly, replacing {o_id} with {} etc. 
        
        Returns:
            str: attr_url. url-type string for the attribute
        """
    @property
    def exists(self) -> bool:
        """
        bool: Check if attribute is available/filled in.
        
        Returns:
            bool: . True if the attribute exists, otherwise False
        """
    @property
    def value(self) -> shyft.time_series.GeoPoint:
        """
        Access to the wrapped value to get or set it.
        """
    @value.setter
    def value(self, arg1: shyft.time_series.GeoPoint) -> None:
        ...
class i16_attr:
    """
    A wrapped attribute class encapsulates a basic type, like TimeSeries,
    and make it an optional property of the class.
    
     - `self.exists` property indicates the existence of the value
     - `self.value` property can be used to get/set the underlying value
     - `self.url()` generates url suitable for ui/expressions work
     - `self.remove()` clear/removes the attribute
    
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __eq__(self, arg0: i16_attr) -> bool:
        ...
    @typing.overload
    def __eq__(self, arg0: int) -> bool:
        ...
    def __ne__(self, arg0: i16_attr) -> bool:
        ...
    def __neq__(self, arg0: int) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def remove(self) -> None:
        """
        Remove the attribute.
        
        After calling this the .exists returns False.
        
        Returns:
            bool: removed_item. True if removed.
        False if it was already away when invoking the method.
        """
    def url(self, prefix: str = '', levels: int = -1, template_levels: int = -1, fmt: bool = False) -> str:
        """
        Generate an almost unique, url-like string for a proxy attribute.
        The string will be based on the attribute's ID, the owning object's type and ID,
        and the owning object's parent, if present.
        
        Args:
            prefix (str): What the resulting string starts with
        
            levels (int): How many levels of the url to include. levels == 0 includes only this level. Use level < 0 to include all levels
        
            template_levels (int): From what level, and onwards, to use templates instead of identifying string. Use template_levels < 0 to ensure no use of templates.
        
            fmt (bool): make string position format friendly, replacing {o_id} with {} etc. 
        
        Returns:
            str: attr_url. url-type string for the attribute
        """
    @property
    def exists(self) -> bool:
        """
        bool: Check if attribute is available/filled in.
        
        Returns:
            bool: . True if the attribute exists, otherwise False
        """
    @property
    def value(self) -> int:
        """
        Access to the wrapped value to get or set it.
        """
    @value.setter
    def value(self, arg1: int) -> None:
        ...
class i32_attr:
    """
    A wrapped attribute class encapsulates a basic type, like TimeSeries,
    and make it an optional property of the class.
    
     - `self.exists` property indicates the existence of the value
     - `self.value` property can be used to get/set the underlying value
     - `self.url()` generates url suitable for ui/expressions work
     - `self.remove()` clear/removes the attribute
    
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __eq__(self, arg0: i32_attr) -> bool:
        ...
    @typing.overload
    def __eq__(self, arg0: int) -> bool:
        ...
    def __ne__(self, arg0: i32_attr) -> bool:
        ...
    def __neq__(self, arg0: int) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def remove(self) -> None:
        """
        Remove the attribute.
        
        After calling this the .exists returns False.
        
        Returns:
            bool: removed_item. True if removed.
        False if it was already away when invoking the method.
        """
    def url(self, prefix: str = '', levels: int = -1, template_levels: int = -1, fmt: bool = False) -> str:
        """
        Generate an almost unique, url-like string for a proxy attribute.
        The string will be based on the attribute's ID, the owning object's type and ID,
        and the owning object's parent, if present.
        
        Args:
            prefix (str): What the resulting string starts with
        
            levels (int): How many levels of the url to include. levels == 0 includes only this level. Use level < 0 to include all levels
        
            template_levels (int): From what level, and onwards, to use templates instead of identifying string. Use template_levels < 0 to ensure no use of templates.
        
            fmt (bool): make string position format friendly, replacing {o_id} with {} etc. 
        
        Returns:
            str: attr_url. url-type string for the attribute
        """
    @property
    def exists(self) -> bool:
        """
        bool: Check if attribute is available/filled in.
        
        Returns:
            bool: . True if the attribute exists, otherwise False
        """
    @property
    def value(self) -> int:
        """
        Access to the wrapped value to get or set it.
        """
    @value.setter
    def value(self, arg1: int) -> None:
        ...
class i64_attr:
    """
    A wrapped attribute class encapsulates a basic type, like TimeSeries,
    and make it an optional property of the class.
    
     - `self.exists` property indicates the existence of the value
     - `self.value` property can be used to get/set the underlying value
     - `self.url()` generates url suitable for ui/expressions work
     - `self.remove()` clear/removes the attribute
    
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __eq__(self, arg0: i64_attr) -> bool:
        ...
    @typing.overload
    def __eq__(self, arg0: int) -> bool:
        ...
    def __ne__(self, arg0: i64_attr) -> bool:
        ...
    def __neq__(self, arg0: int) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def remove(self) -> None:
        """
        Remove the attribute.
        
        After calling this the .exists returns False.
        
        Returns:
            bool: removed_item. True if removed.
        False if it was already away when invoking the method.
        """
    def url(self, prefix: str = '', levels: int = -1, template_levels: int = -1, fmt: bool = False) -> str:
        """
        Generate an almost unique, url-like string for a proxy attribute.
        The string will be based on the attribute's ID, the owning object's type and ID,
        and the owning object's parent, if present.
        
        Args:
            prefix (str): What the resulting string starts with
        
            levels (int): How many levels of the url to include. levels == 0 includes only this level. Use level < 0 to include all levels
        
            template_levels (int): From what level, and onwards, to use templates instead of identifying string. Use template_levels < 0 to ensure no use of templates.
        
            fmt (bool): make string position format friendly, replacing {o_id} with {} etc. 
        
        Returns:
            str: attr_url. url-type string for the attribute
        """
    @property
    def exists(self) -> bool:
        """
        bool: Check if attribute is available/filled in.
        
        Returns:
            bool: . True if the attribute exists, otherwise False
        """
    @property
    def value(self) -> int:
        """
        Access to the wrapped value to get or set it.
        """
    @value.setter
    def value(self, arg1: int) -> None:
        ...
class i8_attr:
    """
    A wrapped attribute class encapsulates a basic type, like TimeSeries,
    and make it an optional property of the class.
    
     - `self.exists` property indicates the existence of the value
     - `self.value` property can be used to get/set the underlying value
     - `self.url()` generates url suitable for ui/expressions work
     - `self.remove()` clear/removes the attribute
    
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __eq__(self, arg0: i8_attr) -> bool:
        ...
    @typing.overload
    def __eq__(self, arg0: int) -> bool:
        ...
    def __ne__(self, arg0: i8_attr) -> bool:
        ...
    def __neq__(self, arg0: int) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def remove(self) -> None:
        """
        Remove the attribute.
        
        After calling this the .exists returns False.
        
        Returns:
            bool: removed_item. True if removed.
        False if it was already away when invoking the method.
        """
    def url(self, prefix: str = '', levels: int = -1, template_levels: int = -1, fmt: bool = False) -> str:
        """
        Generate an almost unique, url-like string for a proxy attribute.
        The string will be based on the attribute's ID, the owning object's type and ID,
        and the owning object's parent, if present.
        
        Args:
            prefix (str): What the resulting string starts with
        
            levels (int): How many levels of the url to include. levels == 0 includes only this level. Use level < 0 to include all levels
        
            template_levels (int): From what level, and onwards, to use templates instead of identifying string. Use template_levels < 0 to ensure no use of templates.
        
            fmt (bool): make string position format friendly, replacing {o_id} with {} etc. 
        
        Returns:
            str: attr_url. url-type string for the attribute
        """
    @property
    def exists(self) -> bool:
        """
        bool: Check if attribute is available/filled in.
        
        Returns:
            bool: . True if the attribute exists, otherwise False
        """
    @property
    def value(self) -> int:
        """
        Access to the wrapped value to get or set it.
        """
    @value.setter
    def value(self, arg1: int) -> None:
        ...
class message_list_attr:
    """
    A wrapped attribute class encapsulates a basic type, like TimeSeries,
    and make it an optional property of the class.
    
     - `self.exists` property indicates the existence of the value
     - `self.value` property can be used to get/set the underlying value
     - `self.url()` generates url suitable for ui/expressions work
     - `self.remove()` clear/removes the attribute
    
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __eq__(self, arg0: message_list_attr) -> bool:
        ...
    @typing.overload
    def __eq__(self, arg0: list[tuple[shyft.time_series.time, str]]) -> bool:
        ...
    def __ne__(self, arg0: message_list_attr) -> bool:
        ...
    def __neq__(self, arg0: list[tuple[shyft.time_series.time, str]]) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def remove(self) -> None:
        """
        Remove the attribute.
        
        After calling this the .exists returns False.
        
        Returns:
            bool: removed_item. True if removed.
        False if it was already away when invoking the method.
        """
    def url(self, prefix: str = '', levels: int = -1, template_levels: int = -1, fmt: bool = False) -> str:
        """
        Generate an almost unique, url-like string for a proxy attribute.
        The string will be based on the attribute's ID, the owning object's type and ID,
        and the owning object's parent, if present.
        
        Args:
            prefix (str): What the resulting string starts with
        
            levels (int): How many levels of the url to include. levels == 0 includes only this level. Use level < 0 to include all levels
        
            template_levels (int): From what level, and onwards, to use templates instead of identifying string. Use template_levels < 0 to ensure no use of templates.
        
            fmt (bool): make string position format friendly, replacing {o_id} with {} etc. 
        
        Returns:
            str: attr_url. url-type string for the attribute
        """
    @property
    def exists(self) -> bool:
        """
        bool: Check if attribute is available/filled in.
        
        Returns:
            bool: . True if the attribute exists, otherwise False
        """
    @property
    def value(self) -> list[tuple[shyft.time_series.time, str]]:
        """
        Access to the wrapped value to get or set it.
        """
    @value.setter
    def value(self, arg1: list[tuple[shyft.time_series.time, str]]) -> None:
        ...
class run_state:
    """
    Describes the possible state of the run
    
    
    Members:
    
      R_CREATED
    
      R_PREP_INPUT
    
      R_RUNNING
    
      R_FINISHED_RUN
    
      R_READ_RESULT
    
      R_FROZEN
    
      R_FAILED
    """
    R_CREATED: typing.ClassVar[run_state]  # value = <run_state.R_CREATED: 0>
    R_FAILED: typing.ClassVar[run_state]  # value = <run_state.R_FAILED: 6>
    R_FINISHED_RUN: typing.ClassVar[run_state]  # value = <run_state.R_FINISHED_RUN: 3>
    R_FROZEN: typing.ClassVar[run_state]  # value = <run_state.R_FROZEN: 5>
    R_PREP_INPUT: typing.ClassVar[run_state]  # value = <run_state.R_PREP_INPUT: 1>
    R_READ_RESULT: typing.ClassVar[run_state]  # value = <run_state.R_READ_RESULT: 4>
    R_RUNNING: typing.ClassVar[run_state]  # value = <run_state.R_RUNNING: 2>
    __members__: typing.ClassVar[dict[str, run_state]]  # value = {'R_CREATED': <run_state.R_CREATED: 0>, 'R_PREP_INPUT': <run_state.R_PREP_INPUT: 1>, 'R_RUNNING': <run_state.R_RUNNING: 2>, 'R_FINISHED_RUN': <run_state.R_FINISHED_RUN: 3>, 'R_READ_RESULT': <run_state.R_READ_RESULT: 4>, 'R_FROZEN': <run_state.R_FROZEN: 5>, 'R_FAILED': <run_state.R_FAILED: 6>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class string_attr:
    """
    A wrapped attribute class encapsulates a basic type, like TimeSeries,
    and make it an optional property of the class.
    
     - `self.exists` property indicates the existence of the value
     - `self.value` property can be used to get/set the underlying value
     - `self.url()` generates url suitable for ui/expressions work
     - `self.remove()` clear/removes the attribute
    
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __eq__(self, arg0: string_attr) -> bool:
        ...
    @typing.overload
    def __eq__(self, arg0: str) -> bool:
        ...
    def __ne__(self, arg0: string_attr) -> bool:
        ...
    def __neq__(self, arg0: str) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def remove(self) -> None:
        """
        Remove the attribute.
        
        After calling this the .exists returns False.
        
        Returns:
            bool: removed_item. True if removed.
        False if it was already away when invoking the method.
        """
    def url(self, prefix: str = '', levels: int = -1, template_levels: int = -1, fmt: bool = False) -> str:
        """
        Generate an almost unique, url-like string for a proxy attribute.
        The string will be based on the attribute's ID, the owning object's type and ID,
        and the owning object's parent, if present.
        
        Args:
            prefix (str): What the resulting string starts with
        
            levels (int): How many levels of the url to include. levels == 0 includes only this level. Use level < 0 to include all levels
        
            template_levels (int): From what level, and onwards, to use templates instead of identifying string. Use template_levels < 0 to ensure no use of templates.
        
            fmt (bool): make string position format friendly, replacing {o_id} with {} etc. 
        
        Returns:
            str: attr_url. url-type string for the attribute
        """
    @property
    def exists(self) -> bool:
        """
        bool: Check if attribute is available/filled in.
        
        Returns:
            bool: . True if the attribute exists, otherwise False
        """
    @property
    def value(self) -> str:
        """
        Access to the wrapped value to get or set it.
        """
    @value.setter
    def value(self, arg1: str) -> None:
        ...
class t_turbine_description:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the map is nonempty
        """
    def __call__(self, time: shyft.time_series.time) -> TurbineDescription:
        """
        Find value for a given time.
        """
    @typing.overload
    def __contains__(self, arg0: shyft.time_series.time) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: typing.Any) -> bool:
        ...
    def __delitem__(self, arg0: shyft.time_series.time) -> None:
        ...
    def __eq__(self, arg0: t_turbine_description) -> bool:
        ...
    def __getitem__(self, arg0: shyft.time_series.time) -> TurbineDescription:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: t_turbine_description) -> None:
        """
        CopyConstructor
        """
    def __iter__(self) -> typing.Iterator[shyft.time_series.time]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: t_turbine_description) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setitem__(self, arg0: shyft.time_series.time, arg1: TurbineDescription) -> None:
        ...
    def __str__(self) -> str:
        ...
    def get(self, key: shyft.time_series.time, default: TurbineDescription | None = None) -> TurbineDescription | None:
        """
        Return the value for key if key is in the dictionary, else default.
        """
    def items(self) -> typing.ItemsView:
        ...
    def keys(self) -> typing.KeysView:
        ...
    def values(self) -> typing.ValuesView:
        ...
class t_xy:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the map is nonempty
        """
    def __call__(self, time: shyft.time_series.time) -> XyPointCurve:
        """
        Find value for a given time.
        """
    @typing.overload
    def __contains__(self, arg0: shyft.time_series.time) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: typing.Any) -> bool:
        ...
    def __delitem__(self, arg0: shyft.time_series.time) -> None:
        ...
    def __eq__(self, arg0: t_xy) -> bool:
        ...
    def __getitem__(self, arg0: shyft.time_series.time) -> XyPointCurve:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: t_xy) -> None:
        """
        CopyConstructor
        """
    def __iter__(self) -> typing.Iterator[shyft.time_series.time]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: t_xy) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setitem__(self, arg0: shyft.time_series.time, arg1: XyPointCurve) -> None:
        ...
    def __str__(self) -> str:
        ...
    def get(self, key: shyft.time_series.time, default: XyPointCurve | None = None) -> XyPointCurve | None:
        """
        Return the value for key if key is in the dictionary, else default.
        """
    def items(self) -> typing.ItemsView:
        ...
    def keys(self) -> typing.KeysView:
        ...
    def values(self) -> typing.ValuesView:
        ...
class t_xy_attr:
    """
    A wrapped attribute class encapsulates a basic type, like TimeSeries,
    and make it an optional property of the class.
    
     - `self.exists` property indicates the existence of the value
     - `self.value` property can be used to get/set the underlying value
     - `self.url()` generates url suitable for ui/expressions work
     - `self.remove()` clear/removes the attribute
    
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __eq__(self, arg0: t_xy_attr) -> bool:
        ...
    @typing.overload
    def __eq__(self, arg0: t_xy) -> bool:
        ...
    def __ne__(self, arg0: t_xy_attr) -> bool:
        ...
    def __neq__(self, arg0: t_xy) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def remove(self) -> None:
        """
        Remove the attribute.
        
        After calling this the .exists returns False.
        
        Returns:
            bool: removed_item. True if removed.
        False if it was already away when invoking the method.
        """
    def url(self, prefix: str = '', levels: int = -1, template_levels: int = -1, fmt: bool = False) -> str:
        """
        Generate an almost unique, url-like string for a proxy attribute.
        The string will be based on the attribute's ID, the owning object's type and ID,
        and the owning object's parent, if present.
        
        Args:
            prefix (str): What the resulting string starts with
        
            levels (int): How many levels of the url to include. levels == 0 includes only this level. Use level < 0 to include all levels
        
            template_levels (int): From what level, and onwards, to use templates instead of identifying string. Use template_levels < 0 to ensure no use of templates.
        
            fmt (bool): make string position format friendly, replacing {o_id} with {} etc. 
        
        Returns:
            str: attr_url. url-type string for the attribute
        """
    @property
    def exists(self) -> bool:
        """
        bool: Check if attribute is available/filled in.
        
        Returns:
            bool: . True if the attribute exists, otherwise False
        """
    @property
    def value(self) -> t_xy:
        """
        Access to the wrapped value to get or set it.
        """
    @value.setter
    def value(self, arg1: t_xy) -> None:
        ...
class t_xy_z_list_attr:
    """
    A wrapped attribute class encapsulates a basic type, like TimeSeries,
    and make it an optional property of the class.
    
     - `self.exists` property indicates the existence of the value
     - `self.value` property can be used to get/set the underlying value
     - `self.url()` generates url suitable for ui/expressions work
     - `self.remove()` clear/removes the attribute
    
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __eq__(self, arg0: t_xy_z_list_attr) -> bool:
        ...
    @typing.overload
    def __eq__(self, arg0: t_xyz_list) -> bool:
        ...
    def __ne__(self, arg0: t_xy_z_list_attr) -> bool:
        ...
    def __neq__(self, arg0: t_xyz_list) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def remove(self) -> None:
        """
        Remove the attribute.
        
        After calling this the .exists returns False.
        
        Returns:
            bool: removed_item. True if removed.
        False if it was already away when invoking the method.
        """
    def url(self, prefix: str = '', levels: int = -1, template_levels: int = -1, fmt: bool = False) -> str:
        """
        Generate an almost unique, url-like string for a proxy attribute.
        The string will be based on the attribute's ID, the owning object's type and ID,
        and the owning object's parent, if present.
        
        Args:
            prefix (str): What the resulting string starts with
        
            levels (int): How many levels of the url to include. levels == 0 includes only this level. Use level < 0 to include all levels
        
            template_levels (int): From what level, and onwards, to use templates instead of identifying string. Use template_levels < 0 to ensure no use of templates.
        
            fmt (bool): make string position format friendly, replacing {o_id} with {} etc. 
        
        Returns:
            str: attr_url. url-type string for the attribute
        """
    @property
    def exists(self) -> bool:
        """
        bool: Check if attribute is available/filled in.
        
        Returns:
            bool: . True if the attribute exists, otherwise False
        """
    @property
    def value(self) -> t_xyz_list:
        """
        Access to the wrapped value to get or set it.
        """
    @value.setter
    def value(self, arg1: t_xyz_list) -> None:
        ...
class t_xyz:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the map is nonempty
        """
    def __call__(self, time: shyft.time_series.time) -> XyPointCurveWithZ:
        """
        Find value for a given time.
        """
    @typing.overload
    def __contains__(self, arg0: shyft.time_series.time) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: typing.Any) -> bool:
        ...
    def __delitem__(self, arg0: shyft.time_series.time) -> None:
        ...
    def __eq__(self, arg0: t_xyz) -> bool:
        ...
    def __getitem__(self, arg0: shyft.time_series.time) -> XyPointCurveWithZ:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: t_xyz) -> None:
        """
        CopyConstructor
        """
    def __iter__(self) -> typing.Iterator[shyft.time_series.time]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: t_xyz) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setitem__(self, arg0: shyft.time_series.time, arg1: XyPointCurveWithZ) -> None:
        ...
    def __str__(self) -> str:
        ...
    def get(self, key: shyft.time_series.time, default: XyPointCurveWithZ | None = None) -> XyPointCurveWithZ | None:
        """
        Return the value for key if key is in the dictionary, else default.
        """
    def items(self) -> typing.ItemsView:
        ...
    def keys(self) -> typing.KeysView:
        ...
    def values(self) -> typing.ValuesView:
        ...
class t_xyz_attr:
    """
    A wrapped attribute class encapsulates a basic type, like TimeSeries,
    and make it an optional property of the class.
    
     - `self.exists` property indicates the existence of the value
     - `self.value` property can be used to get/set the underlying value
     - `self.url()` generates url suitable for ui/expressions work
     - `self.remove()` clear/removes the attribute
    
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __eq__(self, arg0: t_xyz_attr) -> bool:
        ...
    @typing.overload
    def __eq__(self, arg0: t_xyz) -> bool:
        ...
    def __ne__(self, arg0: t_xyz_attr) -> bool:
        ...
    def __neq__(self, arg0: t_xyz) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def remove(self) -> None:
        """
        Remove the attribute.
        
        After calling this the .exists returns False.
        
        Returns:
            bool: removed_item. True if removed.
        False if it was already away when invoking the method.
        """
    def url(self, prefix: str = '', levels: int = -1, template_levels: int = -1, fmt: bool = False) -> str:
        """
        Generate an almost unique, url-like string for a proxy attribute.
        The string will be based on the attribute's ID, the owning object's type and ID,
        and the owning object's parent, if present.
        
        Args:
            prefix (str): What the resulting string starts with
        
            levels (int): How many levels of the url to include. levels == 0 includes only this level. Use level < 0 to include all levels
        
            template_levels (int): From what level, and onwards, to use templates instead of identifying string. Use template_levels < 0 to ensure no use of templates.
        
            fmt (bool): make string position format friendly, replacing {o_id} with {} etc. 
        
        Returns:
            str: attr_url. url-type string for the attribute
        """
    @property
    def exists(self) -> bool:
        """
        bool: Check if attribute is available/filled in.
        
        Returns:
            bool: . True if the attribute exists, otherwise False
        """
    @property
    def value(self) -> t_xyz:
        """
        Access to the wrapped value to get or set it.
        """
    @value.setter
    def value(self, arg1: t_xyz) -> None:
        ...
class t_xyz_list:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the map is nonempty
        """
    def __call__(self, time: shyft.time_series.time) -> XyPointCurveWithZList:
        """
        Find value for a given time.
        """
    @typing.overload
    def __contains__(self, arg0: shyft.time_series.time) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: typing.Any) -> bool:
        ...
    def __delitem__(self, arg0: shyft.time_series.time) -> None:
        ...
    def __eq__(self, arg0: t_xyz_list) -> bool:
        ...
    def __getitem__(self, arg0: shyft.time_series.time) -> XyPointCurveWithZList:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: t_xyz_list) -> None:
        """
        CopyConstructor
        """
    def __iter__(self) -> typing.Iterator[shyft.time_series.time]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: t_xyz_list) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setitem__(self, arg0: shyft.time_series.time, arg1: XyPointCurveWithZList) -> None:
        ...
    def __str__(self) -> str:
        ...
    def get(self, key: shyft.time_series.time, default: XyPointCurveWithZList | None = None) -> XyPointCurveWithZList | None:
        """
        Return the value for key if key is in the dictionary, else default.
        """
    def items(self) -> typing.ItemsView:
        ...
    def keys(self) -> typing.KeysView:
        ...
    def values(self) -> typing.ValuesView:
        ...
class time_axis_attr:
    """
    A wrapped attribute class encapsulates a basic type, like TimeSeries,
    and make it an optional property of the class.
    
     - `self.exists` property indicates the existence of the value
     - `self.value` property can be used to get/set the underlying value
     - `self.url()` generates url suitable for ui/expressions work
     - `self.remove()` clear/removes the attribute
    
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __eq__(self, arg0: time_axis_attr) -> bool:
        ...
    @typing.overload
    def __eq__(self, arg0: shyft.time_series.TimeAxis) -> bool:
        ...
    def __ne__(self, arg0: time_axis_attr) -> bool:
        ...
    def __neq__(self, arg0: shyft.time_series.TimeAxis) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def remove(self) -> None:
        """
        Remove the attribute.
        
        After calling this the .exists returns False.
        
        Returns:
            bool: removed_item. True if removed.
        False if it was already away when invoking the method.
        """
    def url(self, prefix: str = '', levels: int = -1, template_levels: int = -1, fmt: bool = False) -> str:
        """
        Generate an almost unique, url-like string for a proxy attribute.
        The string will be based on the attribute's ID, the owning object's type and ID,
        and the owning object's parent, if present.
        
        Args:
            prefix (str): What the resulting string starts with
        
            levels (int): How many levels of the url to include. levels == 0 includes only this level. Use level < 0 to include all levels
        
            template_levels (int): From what level, and onwards, to use templates instead of identifying string. Use template_levels < 0 to ensure no use of templates.
        
            fmt (bool): make string position format friendly, replacing {o_id} with {} etc. 
        
        Returns:
            str: attr_url. url-type string for the attribute
        """
    @property
    def exists(self) -> bool:
        """
        bool: Check if attribute is available/filled in.
        
        Returns:
            bool: . True if the attribute exists, otherwise False
        """
    @property
    def value(self) -> shyft.time_series.TimeAxis:
        """
        Access to the wrapped value to get or set it.
        """
    @value.setter
    def value(self, arg1: shyft.time_series.TimeAxis) -> None:
        ...
class ts_attr:
    """
    A wrapped attribute class encapsulates a basic type, like TimeSeries,
    and make it an optional property of the class.
    
     - `self.exists` property indicates the existence of the value
     - `self.value` property can be used to get/set the underlying value
     - `self.url()` generates url suitable for ui/expressions work
     - `self.remove()` clear/removes the attribute
    
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __eq__(self, arg0: ts_attr) -> bool:
        ...
    @typing.overload
    def __eq__(self, arg0: shyft.time_series.TimeSeries) -> bool:
        ...
    def __ne__(self, arg0: ts_attr) -> bool:
        ...
    def __neq__(self, arg0: shyft.time_series.TimeSeries) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def remove(self) -> None:
        """
        Remove the attribute.
        
        After calling this the .exists returns False.
        
        Returns:
            bool: removed_item. True if removed.
        False if it was already away when invoking the method.
        """
    def url(self, prefix: str = '', levels: int = -1, template_levels: int = -1, fmt: bool = False) -> str:
        """
        Generate an almost unique, url-like string for a proxy attribute.
        The string will be based on the attribute's ID, the owning object's type and ID,
        and the owning object's parent, if present.
        
        Args:
            prefix (str): What the resulting string starts with
        
            levels (int): How many levels of the url to include. levels == 0 includes only this level. Use level < 0 to include all levels
        
            template_levels (int): From what level, and onwards, to use templates instead of identifying string. Use template_levels < 0 to ensure no use of templates.
        
            fmt (bool): make string position format friendly, replacing {o_id} with {} etc. 
        
        Returns:
            str: attr_url. url-type string for the attribute
        """
    @property
    def exists(self) -> bool:
        """
        bool: Check if attribute is available/filled in.
        
        Returns:
            bool: . True if the attribute exists, otherwise False
        """
    @property
    def value(self) -> shyft.time_series.TimeSeries:
        """
        Access to the wrapped value to get or set it.
        """
    @value.setter
    def value(self, arg1: shyft.time_series.TimeSeries) -> None:
        ...
class turbine_description_attr:
    """
    A wrapped attribute class encapsulates a basic type, like TimeSeries,
    and make it an optional property of the class.
    
     - `self.exists` property indicates the existence of the value
     - `self.value` property can be used to get/set the underlying value
     - `self.url()` generates url suitable for ui/expressions work
     - `self.remove()` clear/removes the attribute
    
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __eq__(self, arg0: turbine_description_attr) -> bool:
        ...
    @typing.overload
    def __eq__(self, arg0: t_turbine_description) -> bool:
        ...
    def __ne__(self, arg0: turbine_description_attr) -> bool:
        ...
    def __neq__(self, arg0: t_turbine_description) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def remove(self) -> None:
        """
        Remove the attribute.
        
        After calling this the .exists returns False.
        
        Returns:
            bool: removed_item. True if removed.
        False if it was already away when invoking the method.
        """
    def url(self, prefix: str = '', levels: int = -1, template_levels: int = -1, fmt: bool = False) -> str:
        """
        Generate an almost unique, url-like string for a proxy attribute.
        The string will be based on the attribute's ID, the owning object's type and ID,
        and the owning object's parent, if present.
        
        Args:
            prefix (str): What the resulting string starts with
        
            levels (int): How many levels of the url to include. levels == 0 includes only this level. Use level < 0 to include all levels
        
            template_levels (int): From what level, and onwards, to use templates instead of identifying string. Use template_levels < 0 to ensure no use of templates.
        
            fmt (bool): make string position format friendly, replacing {o_id} with {} etc. 
        
        Returns:
            str: attr_url. url-type string for the attribute
        """
    @property
    def exists(self) -> bool:
        """
        bool: Check if attribute is available/filled in.
        
        Returns:
            bool: . True if the attribute exists, otherwise False
        """
    @property
    def value(self) -> t_turbine_description:
        """
        Access to the wrapped value to get or set it.
        """
    @value.setter
    def value(self, arg1: t_turbine_description) -> None:
        ...
class u16_attr:
    """
    A wrapped attribute class encapsulates a basic type, like TimeSeries,
    and make it an optional property of the class.
    
     - `self.exists` property indicates the existence of the value
     - `self.value` property can be used to get/set the underlying value
     - `self.url()` generates url suitable for ui/expressions work
     - `self.remove()` clear/removes the attribute
    
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __eq__(self, arg0: u16_attr) -> bool:
        ...
    @typing.overload
    def __eq__(self, arg0: int) -> bool:
        ...
    def __ne__(self, arg0: u16_attr) -> bool:
        ...
    def __neq__(self, arg0: int) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def remove(self) -> None:
        """
        Remove the attribute.
        
        After calling this the .exists returns False.
        
        Returns:
            bool: removed_item. True if removed.
        False if it was already away when invoking the method.
        """
    def url(self, prefix: str = '', levels: int = -1, template_levels: int = -1, fmt: bool = False) -> str:
        """
        Generate an almost unique, url-like string for a proxy attribute.
        The string will be based on the attribute's ID, the owning object's type and ID,
        and the owning object's parent, if present.
        
        Args:
            prefix (str): What the resulting string starts with
        
            levels (int): How many levels of the url to include. levels == 0 includes only this level. Use level < 0 to include all levels
        
            template_levels (int): From what level, and onwards, to use templates instead of identifying string. Use template_levels < 0 to ensure no use of templates.
        
            fmt (bool): make string position format friendly, replacing {o_id} with {} etc. 
        
        Returns:
            str: attr_url. url-type string for the attribute
        """
    @property
    def exists(self) -> bool:
        """
        bool: Check if attribute is available/filled in.
        
        Returns:
            bool: . True if the attribute exists, otherwise False
        """
    @property
    def value(self) -> int:
        """
        Access to the wrapped value to get or set it.
        """
    @value.setter
    def value(self, arg1: int) -> None:
        ...
class unit_group_type_attr:
    """
    A wrapped attribute class encapsulates a basic type, like TimeSeries,
    and make it an optional property of the class.
    
     - `self.exists` property indicates the existence of the value
     - `self.value` property can be used to get/set the underlying value
     - `self.url()` generates url suitable for ui/expressions work
     - `self.remove()` clear/removes the attribute
    
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __eq__(self, arg0: unit_group_type_attr) -> bool:
        ...
    @typing.overload
    def __eq__(self, arg0: UnitGroupType) -> bool:
        ...
    def __ne__(self, arg0: unit_group_type_attr) -> bool:
        ...
    def __neq__(self, arg0: UnitGroupType) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def remove(self) -> None:
        """
        Remove the attribute.
        
        After calling this the .exists returns False.
        
        Returns:
            bool: removed_item. True if removed.
        False if it was already away when invoking the method.
        """
    def url(self, prefix: str = '', levels: int = -1, template_levels: int = -1, fmt: bool = False) -> str:
        """
        Generate an almost unique, url-like string for a proxy attribute.
        The string will be based on the attribute's ID, the owning object's type and ID,
        and the owning object's parent, if present.
        
        Args:
            prefix (str): What the resulting string starts with
        
            levels (int): How many levels of the url to include. levels == 0 includes only this level. Use level < 0 to include all levels
        
            template_levels (int): From what level, and onwards, to use templates instead of identifying string. Use template_levels < 0 to ensure no use of templates.
        
            fmt (bool): make string position format friendly, replacing {o_id} with {} etc. 
        
        Returns:
            str: attr_url. url-type string for the attribute
        """
    @property
    def exists(self) -> bool:
        """
        bool: Check if attribute is available/filled in.
        
        Returns:
            bool: . True if the attribute exists, otherwise False
        """
    @property
    def value(self) -> UnitGroupType:
        """
        Access to the wrapped value to get or set it.
        """
    @value.setter
    def value(self, arg1: UnitGroupType) -> None:
        ...
@typing.overload
def compressed_size(double_vector: list[float], accuracy: float) -> int:
    ...
@typing.overload
def compressed_size(float_vector: list[float], accuracy: float) -> int:
    ...
def downstream_reservoirs(component: HydroComponent, max_dist: int = 0) -> ReservoirList:
    """
    Find all reservoirs upstream from component, stopping at `max_dist` traversals
    
    Args:
        max_dist (int): max traversals
    
    Returns:
        ReservoirList: reservoirs. The reservoirs within the specified distance
    """
def downstream_units(component: HydroComponent, max_dist: int = 0) -> UnitList:
    """
    Find all units downstream from component, stopping at `max_dist` traversals
    
    Args:
        max_dist (int): max traversals
    
    Returns:
        UnitList: units. The units within the specified distance
    """
def has_backward_capability(arg0: TurbineCapability) -> bool:
    """
    Checks if a turbine can support pumping
    """
def has_forward_capability(arg0: TurbineCapability) -> bool:
    """
    Checks if a turbine can support generating
    """
def has_reversible_capability(arg0: TurbineCapability) -> bool:
    """
    Checks if a turbine can support both generating and pumping
    """
def points_from_x_y(x: list[float], y: list[float]) -> XyPointList:
    ...
def upstream_reservoirs(component: HydroComponent, max_dist: int = 0) -> ReservoirList:
    """
    Find all reservoirs upstream from component, stopping at `max_dist` traversals.
    
    Args:
        max_dist (int): max traversals
    
    Returns:
        ReservoirList: reservoirs. The reservoirs within the specified distance
    """
def upstream_units(component: HydroComponent, max_dist: int = 0) -> UnitList:
    """
    Find units upstream from component, stopping at `max_dist` traversals
    
    Args:
        max_dist (int): max traversals
    
    Returns:
        UnitList: units. The units within the specified distance
    """
AFRR_DOWN: UnitGroupType  # value = <UnitGroupType.AFRR_DOWN: 6>
AFRR_UP: UnitGroupType  # value = <UnitGroupType.AFRR_UP: 5>
COMMIT: UnitGroupType  # value = <UnitGroupType.COMMIT: 12>
FCR_D_DOWN: UnitGroupType  # value = <UnitGroupType.FCR_D_DOWN: 4>
FCR_D_UP: UnitGroupType  # value = <UnitGroupType.FCR_D_UP: 3>
FCR_N_DOWN: UnitGroupType  # value = <UnitGroupType.FCR_N_DOWN: 2>
FCR_N_UP: UnitGroupType  # value = <UnitGroupType.FCR_N_UP: 1>
FFR: UnitGroupType  # value = <UnitGroupType.FFR: 9>
MFRR_DOWN: UnitGroupType  # value = <UnitGroupType.MFRR_DOWN: 8>
MFRR_UP: UnitGroupType  # value = <UnitGroupType.MFRR_UP: 7>
PRODUCTION: UnitGroupType  # value = <UnitGroupType.PRODUCTION: 13>
RR_DOWN: UnitGroupType  # value = <UnitGroupType.RR_DOWN: 11>
RR_UP: UnitGroupType  # value = <UnitGroupType.RR_UP: 10>
R_CREATED: run_state  # value = <run_state.R_CREATED: 0>
R_FAILED: run_state  # value = <run_state.R_FAILED: 6>
R_FINISHED_RUN: run_state  # value = <run_state.R_FINISHED_RUN: 3>
R_FROZEN: run_state  # value = <run_state.R_FROZEN: 5>
R_PREP_INPUT: run_state  # value = <run_state.R_PREP_INPUT: 1>
R_READ_RESULT: run_state  # value = <run_state.R_READ_RESULT: 4>
R_RUNNING: run_state  # value = <run_state.R_RUNNING: 2>
UNSPECIFIED: UnitGroupType  # value = <UnitGroupType.UNSPECIFIED: 0>
__version__: str = '25.0.0'
bypass: ConnectionRole  # value = <ConnectionRole.bypass: 1>
flood: ConnectionRole  # value = <ConnectionRole.flood: 2>
input: ConnectionRole  # value = <ConnectionRole.input: 3>
main: ConnectionRole  # value = <ConnectionRole.main: 0>
turbine_backward: TurbineCapability  # value = <TurbineCapability.turbine_backward: 2>
turbine_forward: TurbineCapability  # value = <TurbineCapability.turbine_forward: 1>
turbine_none: TurbineCapability  # value = <TurbineCapability.turbine_none: 0>
turbine_reversible: TurbineCapability  # value = <TurbineCapability.turbine_reversible: 3>
