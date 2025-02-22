"""
Shyft python api for the RPMGSK model
"""
from __future__ import annotations
import shyft.hydrology
import shyft.hydrology.r_pt_gs_k
import shyft.time_series
import typing
__all__ = ['RPMGSKAllCollector', 'RPMGSKCellActualEvapotranspirationResponseStatistics', 'RPMGSKCellAll', 'RPMGSKCellAllStateHandler', 'RPMGSKCellAllStatistics', 'RPMGSKCellAllVector', 'RPMGSKCellGammaSnowResponseStatistics', 'RPMGSKCellGammaSnowStateStatistics', 'RPMGSKCellKirchnerStateStatistics', 'RPMGSKCellOpt', 'RPMGSKCellOptStateHandler', 'RPMGSKCellOptStatistics', 'RPMGSKCellOptVector', 'RPMGSKCellPenmanMonteithResponseStatistics', 'RPMGSKDischargeCollector', 'RPMGSKModel', 'RPMGSKNullCollector', 'RPMGSKOptModel', 'RPMGSKOptimizer', 'RPMGSKParameter', 'RPMGSKParameterMap', 'RPMGSKResponse', 'RPMGSKState', 'RPMGSKStateVector', 'RPMGSKStateWithId', 'RPMGSKStateWithIdVector', 'StateCollector', 'create_full_model_clone', 'create_opt_model_clone', 'deserialize', 'deserialize_from_bytes', 'extract_state_vector', 'serialize', 'version']
class RPMGSKAllCollector:
    """
    collect all cell response from a run
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def ae_output(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: actual evap mm/h
        """
    @property
    def avg_charge(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: average charge in [m^3/s]
        """
    @property
    def avg_discharge(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: Kirchner Discharge given in [m^3/s] for the timestep
        """
    @property
    def destination_area(self) -> float:
        """
        float: a copy of cell area [m2]
        """
    @property
    def end_response(self) -> RPMGSKResponse:
        """
        RPMGSKResponse: end_response, at the end of collected
        """
    @property
    def glacier_melt(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: glacier melt (outflow) [m3/s] for the timestep
        """
    @property
    def pe_output(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: pot evap mm/h
        """
    @property
    def snow_outflow(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: gamma snow output [m^3/s] for the timestep
        """
    @property
    def snow_sca(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: gamma snow covered area fraction, sca.. 0..1 - at the end of timestep (state)
        """
    @property
    def snow_swe(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: gamma snow swe, [mm] over the cell sca.. area, - at the end of timestep
        """
class RPMGSKCellActualEvapotranspirationResponseStatistics:
    """
    ActualEvapotranspiration response statistics
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, cells: RPMGSKCellAllVector) -> None:
        ...
    @typing.overload
    def output(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def output(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def output_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns for cells matching catchments_ids at the i'th timestep
        """
    @typing.overload
    def pot_ratio(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns the avg ratio (1-exp(-water_level*3/scale_factor)) for catcment_ids
        """
    @typing.overload
    def pot_ratio(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns the ratio the ratio (1-exp(-water_level*3/scale_factor)) for cells matching catchments_ids at the i'th timestep
        """
    def pot_ratio_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns the ratio avg (1-exp(-water_level*3/scale_factor)) value for cells matching catchments_ids at the i'th timestep
        """
class RPMGSKCellAll:
    """
    tbd: RPMGSKCellAll doc
    """
    vector_t = RPMGSKCellAllVector
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
    def mid_point(self) -> shyft.time_series.GeoPoint:
        """
        returns geo.mid_point()
        """
    def run(self, time_axis: shyft.time_series.TimeAxisFixedDeltaT, start_step: int, n_steps: int) -> None:
        """
        run the cell (given it's initialized)
        before run, the caller must ensure the cell is ready to run, is initialized
        after the run, the cell state, as well as resource collector/state-collector is updated
        
        Args:
            time_axis (TimeAxisFixedDeltaT): time-axis to run, should match the run-time-axis used for env_ts
        
            start_step (int): first interval, ref. time-axis to start run
        
            n_steps (int): number of time-steps to run
        """
    def set_parameter(self, parameter: RPMGSKParameter) -> None:
        """
        set the cell method stack parameters, typical operations at region_level, executed after the interpolation, before the run
        """
    def set_snow_sca_swe_collection(self, arg0: bool) -> None:
        """
        collecting the snow sca and swe on for calibration scenario
        """
    def set_state_collection(self, on_or_off: bool) -> None:
        """
        collecting the state during run could be very useful to understand models
        """
    @property
    def env_ts(self) -> shyft.hydrology.CellEnvironment:
        """
        CellEnvironment: environment time-series as projected to the cell after the interpolation/preparation step
        """
    @env_ts.setter
    def env_ts(self, arg0: shyft.hydrology.CellEnvironment) -> None:
        ...
    @property
    def geo(self) -> shyft.hydrology.GeoCellData:
        """
        GeoCellData: geo_cell_data information for the cell, such as mid-point, forest-fraction and other cell-specific personalities.
        """
    @geo.setter
    def geo(self, arg0: shyft.hydrology.GeoCellData) -> None:
        ...
    @property
    def parameter(self) -> RPMGSKParameter:
        """
        RPMGSKParameter: reference to parameter for this cell, typically shared for a catchment
        """
    @parameter.setter
    def parameter(self, arg1: RPMGSKParameter) -> None:
        ...
    @property
    def rc(self) -> RPMGSKAllCollector:
        """
        RPMGSKCellAllResponseCollector
        """
    @property
    def sc(self) -> StateCollector:
        """
        RPMGSKCellAllStateCollector
        """
    @property
    def state(self) -> RPMGSKState:
        """
        RPMGSKState: the current state of the cell
        """
    @state.setter
    def state(self, arg0: RPMGSKState) -> None:
        ...
class RPMGSKCellAllStateHandler:
    """
    Provides functionality to extract and restore state from cells
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, cells: RPMGSKCellAllVector) -> None:
        ...
    def apply_state(self, cell_id_state_vector: RPMGSKStateWithIdVector, cids: list[int]) -> list[int]:
        """
        apply the supplied cell-identified state to the cells,
        limited to the optionally supplied catchment id's
        If no catchment-id's specified, it applies to all cells
        
        Args:
            cell_id_state_vector (): 
        
            cids (IntVector): list of catchment-id's, if empty, apply all
        
        Returns:
            IntVector: not_applied_list. a list of indices into cell_id_state_vector that did not match any cells
        	 taken into account the optionally catchment-id specification
        """
    def extract_state(self, cids: list[int]) -> RPMGSKStateWithIdVector:
        """
        Extract cell state for the optionaly specified catchment ids, cids
        
        Args:
            cids (IntVector): list of catchment-id's, if empty, extract all
        
        Returns:
            CellStateIdVector: cell_states. the state with identifier for the cells
        """
class RPMGSKCellAllStatistics:
    """
    This class provides statistics for group of cells, as specified
    by the list of catchment identifiers, or list of cell-indexes passed to the methods.
    It is provided both as a separate class, but is also provided
    automagically through the region_model.statistics property.
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, cells: RPMGSKCellAllVector) -> None:
        ...
    @typing.overload
    def charge(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum charge[m^3/s] for catcment_ids
        """
    @typing.overload
    def charge(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns charge[m^3/s]  for cells matching catchments_ids at the i'th timestep
        """
    def charge_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns charge[m^3/s] for cells matching catchments_ids at the i'th timestep
        """
    @typing.overload
    def discharge(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def discharge(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def discharge_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def elevation(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns area-average elevation[m.a.s.l] for cells matching catchments_ids
        """
    def forest_area(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns forest area[m2] for cells matching catchments_ids
        """
    def glacier_area(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns glacier area[m2] for cells matching catchments_ids
        """
    def lake_area(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns lake area[m2] for cells matching catchments_ids
        """
    @typing.overload
    def precipitation(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def precipitation(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def precipitation_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    @typing.overload
    def radiation(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def radiation(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def radiation_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    @typing.overload
    def rel_hum(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def rel_hum(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def rel_hum_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def reservoir_area(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns reservoir area[m2] for cells matching catchments_ids
        """
    @typing.overload
    def snow_sca(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns snow_sca [] for catcment_ids
        """
    @typing.overload
    def snow_sca(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns snow_sca []  for cells matching catchments_ids at the i'th timestep
        """
    def snow_sca_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns snow_sca [] for cells matching catchments_ids at the i'th timestep
        """
    def snow_storage_area(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns snow_storage area where snow can build up[m2], eg total_area - lake and reservoir
        """
    @typing.overload
    def snow_swe(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns snow_swe [mm] for catcment_ids
        """
    @typing.overload
    def snow_swe(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns snow_swe [mm]  for cells matching catchments_ids at the i'th timestep
        """
    def snow_swe_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns snow_swe [mm] for cells matching catchments_ids at the i'th timestep
        """
    @typing.overload
    def temperature(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def temperature(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def temperature_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def total_area(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns total area[m2] for cells matching catchments_ids
        """
    def unspecified_area(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns unspecified area[m2] for cells matching catchments_ids
        """
    @typing.overload
    def wind_speed(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def wind_speed(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def wind_speed_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
class RPMGSKCellAllVector:
    """
    vector of cells
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @staticmethod
    def create_from_geo_cell_data_vector(arg0: list[float]) -> RPMGSKCellAllVector:
        """
        create a cell-vector filling in the geo_cell_data records as given by the DoubleVector.
        This function works together with the geo_cell_data_vector static method
        that provides a correctly formatted persistable vector
        Notice that the context and usage of these two functions is related
        to python orchestration and repository data-caching
        """
    @staticmethod
    def create_from_geo_cell_data_vector_to_tin(arg0: list[float]) -> RPMGSKCellAllVector:
        """
        create a cell-vector filling in the geo_cell_data records as given by the DoubleVector.
        This function works together with the geo_cell_data_vector static method
        that provides a correctly formatted persistable vector
        Notice that the context and usage of these two functions is related
        to python orchestration and repository data-caching
        """
    @staticmethod
    def geo_cell_data_vector(arg0: RPMGSKCellAllVector) -> list[float]:
        """
        returns a persistable DoubleVector representation of of geo_cell_data for all cells.
        that object can in turn be used to construct a <Cell>Vector of any cell type
        using the <Cell>Vector.create_from_geo_cell_data_vector
        """
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
    def __eq__(self, arg0: RPMGSKCellAllVector) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> RPMGSKCellAllVector:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> RPMGSKCellAll:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: RPMGSKCellAllVector) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[RPMGSKCellAll]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: RPMGSKCellAllVector) -> bool:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: RPMGSKCellAll) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: RPMGSKCellAllVector) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: RPMGSKCellAll) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    @typing.overload
    def extend(self, L: RPMGSKCellAllVector) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: RPMGSKCellAll) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> RPMGSKCellAll:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> RPMGSKCellAll:
        """
        Remove and return the item at index ``i``
        """
    def size(self) -> int:
        ...
class RPMGSKCellGammaSnowResponseStatistics:
    """
    GammaSnow response statistics
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, cells: RPMGSKCellAllVector) -> None:
        ...
    @typing.overload
    def glacier_melt(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids[m3/s]
        """
    @typing.overload
    def glacier_melt(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep [m3/s]
        """
    def glacier_melt_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep[m3/s]
        """
    @typing.overload
    def outflow(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def outflow(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def outflow_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    @typing.overload
    def sca(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def sca(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def sca_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    @typing.overload
    def swe(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def swe(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def swe_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
class RPMGSKCellGammaSnowStateStatistics:
    """
    GammaSnow state statistics
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, cells: RPMGSKCellAllVector) -> None:
        ...
    @typing.overload
    def acc_melt(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def acc_melt(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def acc_melt_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    @typing.overload
    def albedo(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def albedo(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def albedo_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    @typing.overload
    def alpha(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def alpha(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def alpha_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    @typing.overload
    def iso_pot_energy(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def iso_pot_energy(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def iso_pot_energy_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    @typing.overload
    def lwc(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def lwc(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def lwc_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    @typing.overload
    def sdc_melt_mean(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def sdc_melt_mean(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def sdc_melt_mean_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    @typing.overload
    def surface_heat(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def surface_heat(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def surface_heat_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    @typing.overload
    def temp_swe(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def temp_swe(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def temp_swe_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
class RPMGSKCellKirchnerStateStatistics:
    """
    Kirchner response statistics
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, cells: RPMGSKCellAllVector) -> None:
        ...
    @typing.overload
    def discharge(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def discharge(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def discharge_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns sum discharge[m3/s]  for cells matching catchments_ids at the i'th timestep
        """
class RPMGSKCellOpt:
    """
    tbd: RPMGSKCellOpt doc
    """
    vector_t = RPMGSKCellOptVector
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
    def mid_point(self) -> shyft.time_series.GeoPoint:
        """
        returns geo.mid_point()
        """
    def run(self, time_axis: shyft.time_series.TimeAxisFixedDeltaT, start_step: int, n_steps: int) -> None:
        """
        run the cell (given it's initialized)
        before run, the caller must ensure the cell is ready to run, is initialized
        after the run, the cell state, as well as resource collector/state-collector is updated
        
        Args:
            time_axis (TimeAxisFixedDeltaT): time-axis to run, should match the run-time-axis used for env_ts
        
            start_step (int): first interval, ref. time-axis to start run
        
            n_steps (int): number of time-steps to run
        """
    def set_parameter(self, parameter: RPMGSKParameter) -> None:
        """
        set the cell method stack parameters, typical operations at region_level, executed after the interpolation, before the run
        """
    def set_snow_sca_swe_collection(self, arg0: bool) -> None:
        """
        collecting the snow sca and swe on for calibration scenario
        """
    def set_state_collection(self, on_or_off: bool) -> None:
        """
        collecting the state during run could be very useful to understand models
        """
    @property
    def env_ts(self) -> shyft.hydrology.CellEnvironment:
        """
        CellEnvironment: environment time-series as projected to the cell after the interpolation/preparation step
        """
    @env_ts.setter
    def env_ts(self, arg0: shyft.hydrology.CellEnvironment) -> None:
        ...
    @property
    def geo(self) -> shyft.hydrology.GeoCellData:
        """
        GeoCellData: geo_cell_data information for the cell, such as mid-point, forest-fraction and other cell-specific personalities.
        """
    @geo.setter
    def geo(self, arg0: shyft.hydrology.GeoCellData) -> None:
        ...
    @property
    def parameter(self) -> RPMGSKParameter:
        """
        RPMGSKParameter: reference to parameter for this cell, typically shared for a catchment
        """
    @parameter.setter
    def parameter(self, arg1: RPMGSKParameter) -> None:
        ...
    @property
    def rc(self) -> RPMGSKDischargeCollector:
        """
        RPMGSKCellOptResponseCollector
        """
    @property
    def sc(self) -> RPMGSKNullCollector:
        """
        RPMGSKCellOptStateCollector
        """
    @property
    def state(self) -> RPMGSKState:
        """
        RPMGSKState: the current state of the cell
        """
    @state.setter
    def state(self, arg0: RPMGSKState) -> None:
        ...
class RPMGSKCellOptStateHandler:
    """
    Provides functionality to extract and restore state from cells
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, cells: RPMGSKCellOptVector) -> None:
        ...
    def apply_state(self, cell_id_state_vector: RPMGSKStateWithIdVector, cids: list[int]) -> list[int]:
        """
        apply the supplied cell-identified state to the cells,
        limited to the optionally supplied catchment id's
        If no catchment-id's specified, it applies to all cells
        
        Args:
            cell_id_state_vector (): 
        
            cids (IntVector): list of catchment-id's, if empty, apply all
        
        Returns:
            IntVector: not_applied_list. a list of indices into cell_id_state_vector that did not match any cells
        	 taken into account the optionally catchment-id specification
        """
    def extract_state(self, cids: list[int]) -> RPMGSKStateWithIdVector:
        """
        Extract cell state for the optionaly specified catchment ids, cids
        
        Args:
            cids (IntVector): list of catchment-id's, if empty, extract all
        
        Returns:
            CellStateIdVector: cell_states. the state with identifier for the cells
        """
class RPMGSKCellOptStatistics:
    """
    This class provides statistics for group of cells, as specified
    by the list of catchment identifiers, or list of cell-indexes passed to the methods.
    It is provided both as a separate class, but is also provided
    automagically through the region_model.statistics property.
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, cells: RPMGSKCellOptVector) -> None:
        ...
    @typing.overload
    def charge(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum charge[m^3/s] for catcment_ids
        """
    @typing.overload
    def charge(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns charge[m^3/s]  for cells matching catchments_ids at the i'th timestep
        """
    def charge_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns charge[m^3/s] for cells matching catchments_ids at the i'th timestep
        """
    @typing.overload
    def discharge(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def discharge(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def discharge_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def elevation(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns area-average elevation[m.a.s.l] for cells matching catchments_ids
        """
    def forest_area(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns forest area[m2] for cells matching catchments_ids
        """
    def glacier_area(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns glacier area[m2] for cells matching catchments_ids
        """
    def lake_area(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns lake area[m2] for cells matching catchments_ids
        """
    @typing.overload
    def precipitation(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def precipitation(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def precipitation_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    @typing.overload
    def radiation(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def radiation(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def radiation_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    @typing.overload
    def rel_hum(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def rel_hum(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def rel_hum_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def reservoir_area(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns reservoir area[m2] for cells matching catchments_ids
        """
    @typing.overload
    def snow_sca(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns snow_sca [] for catcment_ids
        """
    @typing.overload
    def snow_sca(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns snow_sca []  for cells matching catchments_ids at the i'th timestep
        """
    def snow_sca_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns snow_sca [] for cells matching catchments_ids at the i'th timestep
        """
    def snow_storage_area(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns snow_storage area where snow can build up[m2], eg total_area - lake and reservoir
        """
    @typing.overload
    def snow_swe(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns snow_swe [mm] for catcment_ids
        """
    @typing.overload
    def snow_swe(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns snow_swe [mm]  for cells matching catchments_ids at the i'th timestep
        """
    def snow_swe_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns snow_swe [mm] for cells matching catchments_ids at the i'th timestep
        """
    @typing.overload
    def temperature(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def temperature(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def temperature_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def total_area(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns total area[m2] for cells matching catchments_ids
        """
    def unspecified_area(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns unspecified area[m2] for cells matching catchments_ids
        """
    @typing.overload
    def wind_speed(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def wind_speed(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def wind_speed_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
class RPMGSKCellOptVector:
    """
    vector of cells
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @staticmethod
    def create_from_geo_cell_data_vector(arg0: list[float]) -> RPMGSKCellOptVector:
        """
        create a cell-vector filling in the geo_cell_data records as given by the DoubleVector.
        This function works together with the geo_cell_data_vector static method
        that provides a correctly formatted persistable vector
        Notice that the context and usage of these two functions is related
        to python orchestration and repository data-caching
        """
    @staticmethod
    def create_from_geo_cell_data_vector_to_tin(arg0: list[float]) -> RPMGSKCellOptVector:
        """
        create a cell-vector filling in the geo_cell_data records as given by the DoubleVector.
        This function works together with the geo_cell_data_vector static method
        that provides a correctly formatted persistable vector
        Notice that the context and usage of these two functions is related
        to python orchestration and repository data-caching
        """
    @staticmethod
    def geo_cell_data_vector(arg0: RPMGSKCellOptVector) -> list[float]:
        """
        returns a persistable DoubleVector representation of of geo_cell_data for all cells.
        that object can in turn be used to construct a <Cell>Vector of any cell type
        using the <Cell>Vector.create_from_geo_cell_data_vector
        """
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
    def __eq__(self, arg0: RPMGSKCellOptVector) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> RPMGSKCellOptVector:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> RPMGSKCellOpt:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: RPMGSKCellOptVector) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[RPMGSKCellOpt]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: RPMGSKCellOptVector) -> bool:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: RPMGSKCellOpt) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: RPMGSKCellOptVector) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: RPMGSKCellOpt) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    @typing.overload
    def extend(self, L: RPMGSKCellOptVector) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: RPMGSKCellOpt) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> RPMGSKCellOpt:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> RPMGSKCellOpt:
        """
        Remove and return the item at index ``i``
        """
    def size(self) -> int:
        ...
class RPMGSKCellPenmanMonteithResponseStatistics:
    """
    PenmanMonteith response statistics
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, cells: RPMGSKCellAllVector) -> None:
        ...
    @typing.overload
    def output(self, indexes: list[int], ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> shyft.time_series.TimeSeries:
        """
        returns sum  for catcment_ids
        """
    @typing.overload
    def output(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> list[float]:
        """
        returns  for cells matching catchments_ids at the i'th timestep
        """
    def output_value(self, indexes: list[int], i: int, ix_type: shyft.hydrology.stat_scope = shyft.hydrology.stat_scope.catchment) -> float:
        """
        returns for cells matching catchments_ids at the i'th timestep
        """
class RPMGSKDischargeCollector:
    """
    collect all cell response from a run
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def avg_charge(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: average charge in [m^3/s]
        """
    @property
    def avg_discharge(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: Kirchner Discharge given in [m^3/s] for the timestep
        """
    @property
    def cell_area(self) -> float:
        """
        float: a copy of cell area [m2]
        """
    @property
    def collect_snow(self) -> bool:
        """
        bool: controls collection of snow routine
        """
    @collect_snow.setter
    def collect_snow(self, arg0: bool) -> None:
        ...
    @property
    def destination_area(self) -> float:
        """
        float: a copy of cell area [m2]
        """
    @property
    def end_response(self) -> RPMGSKResponse:
        """
        RPMGSKResponse: end_response, at the end of collected
        """
    @property
    def snow_sca(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: gamma snow covered area fraction, sca.. 0..1 - at the end of timestep (state)
        """
    @property
    def snow_swe(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: gamma snow swe, [mm] over the cell sca.. area, - at the end of timestep
        """
class RPMGSKModel:
    """
    RPMGSKModel , a region_model is the calculation model for a region, where we can have
    one or more catchments.
    The role of the region_model is to describe region, so that we can run the
    region computational model efficiently for a number of type of cells, interpolation and
    catchment level algorihtms.
    
    The region model keeps a list of cells, of specified type 
    as well as parameters for the cells.
    The model also keeps state, such as region_env(forcing variables), time-axis and intial state
    - they are non-empty after initializing, and running the model
    """
    cell_t = RPMGSKCellAll
    opt_model_t = RPMGSKOptModel
    parameter_t = RPMGSKParameter
    state_t = RPMGSKState
    state_with_id_t = RPMGSKStateWithId
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, other_model: RPMGSKModel) -> None:
        """
        Create a copy of the other_model
        
        Args:
            other_model (RegionModel): region-model to copy
        """
    @typing.overload
    def __init__(self, geo_data_vector: shyft.hydrology.GeoCellDataVector, region_param: RPMGSKParameter) -> None:
        """
        Creates a model from GeoCellDataVector and region model parameters
        
        Args:
            geo_data_vector (GeoCellDataVector): contains the geo-related characteristics for the cells
        
            region_param (Parameter): contains the parameters for all cells of this region model
        """
    @typing.overload
    def __init__(self, cells: RPMGSKCellAllVector, region_param: RPMGSKParameter, catchment_parameters: RPMGSKParameterMap) -> None:
        """
        Creates a model from cells and region model parameters, and specified catchment parameters
        The cell-vector and catchment-id's should match those specified in the catchment_parameters mapping
        
        Args:
            cells (CellVector): contains the cells, each with geo-properties and type matching the region-model type
        
            region_param (Parameter): contains the parameters for cells that does not have catchment specific parameters
        
            catchment_parameters (ParameterMap): contains mapping (a kind of dict, where the key is catchment-id and value is parameters for cells matching catchment-id
        """
    def adjust_q(self, q_scale: float, cids: list[int]) -> None:
        """
        adjust the current state content q of ground storage by scale-factor
        
        Adjust the content of the ground storage, e.g. state.kirchner.q, or
        hbv state.(tank|soil).(uz,lz|sm), by the specified scale factor.
        The this function plays key role for adjusting the state to
        achieve a specified/wanted average discharge flow output for the
        model at the first time-step.
        
        Args:
            q_scale (float): the scale factor to apply to current storage state
        
            cids (IntVector): if empty, all cells are in scope, otherwise only cells that have specified catchment ids.
        """
    def adjust_state_to_target_flow(self, wanted_flow_m3s: float, cids: list[int], start_step: int = 0, scale_range: float = 10.0, scale_eps: float = 0.001, max_iter: int = 300, n_steps: int = 1) -> shyft.hydrology.FlowAdjustResult:
        """
        state adjustment to achieve wanted/observed flow
        
        This function provides an easy and consistent way to adjust the
        state of the cells(kirchner, or hbv-tank-levels) so that the average output
        from next n_steps time-steps matches the wanted flow for the same period.
        
        This is quite complex, since the amount of adjustment needed is dependent of the
        cell-state, temperature/precipitation in time-step, glacier-melt, length of the time-step,
        and calibration factors sensitivity.
        
        The approach here is to use dlib::find_min_single_variable to solve
        the problem, instead of trying to reverse compute the needed state.
        
        This has several benefits, it deals with the full stack and state, and it can be made
        method stack independent.
        
        Notice that the model should be prepared for run prior to calling this function
        and that there should be a current model state that gives the starting point
        for the adjustment.
        Also note that when returning, the active state reflects the
        achieved flow returned, and that the current state  for the cells
        belonging to the catchment-ids is modified as needed to provide this average-flow.
        The state when returning is set to the start of the i'th period specified
        to reach the desired flow.
        
        
        Args:
            wanted_flow_m3s (float): the average flow first time-step we want to achieve
        
            cids (IntVector):  catchments, represented by catchment-ids that should be adjusted
        
            start_step (int): what time-step number in the time-axis to use, py::default 0
        
            scale_range (float): optimizer boundaries is s_0/scale_range .. s_0*scale_range, s_0=wanted_flow_m3s/q_0 , py::default =10.0
        
            scale_eps (float): optimizer eps, stop criteria (ref. dlib), eps=s_0*scale_eps , py::default =1-e3
        
            max_iter (int): optimizer max evaluations before giving up to find optimal solution
        
            n_steps (int): number of time-steps in the time-axis to average the to the wanted_flow_m3s, py::default=1
        
        Returns:
            FlowAdjustResult: obtained flow in m3/s units.. note: this can deviate from wanted flow due to model and state constraints
        """
    def connect_catchment_to_river(self, cid: int, rid: int) -> None:
        """
        Connect routing of all the cells in the specified catchment id to the specified river id
        
        
        Args:
            cid (int): catchment identifier
        
            rid (int): river identifier, can be set to 0 to indicate disconnect from routing
        """
    def create_opt_model_clone(self, with_catchment_params: bool = False) -> RPMGSKOptModel:
        """
        Clone a model to a another similar type model, full to opt-model or vice-versa
        The entire state except catchment-specific parameters, filter and result-series are cloned
        The returned model is ready to run_cells(), state and interpolated enviroment is identical to the clone source
        
        Args:
            src_model (XXXX?Model): The model to be cloned, with state interpolation done, etc
        
            with_catchment_params (bool): default false, if true also copy catchment specific parameters
        
        Returns:
            XXXX?Model: new_model. new_model ready to run_cells, or to put into the calibrator/optimizer
        """
    def extract_geo_cell_data(self) -> shyft.hydrology.GeoCellDataVector:
        """
        extracts the geo_cell_data and return it as GeoCellDataVector that can
        be passed into a the constructor of a new region-model (clone-operation)
        """
    def get_catchment_parameter(self, catchment_id: int) -> RPMGSKParameter:
        """
        return the parameter valid for specified catchment_id, or global parameter if not found.
        note Be aware that if you change the returned parameter, it will affect the related cells.
        param catchment_id 0 based catchment id as placed on each cell
        returns reference to the real parameter structure for the catchment_id if exists,
        otherwise the global parameters
        """
    def get_cells(self) -> RPMGSKCellAllVector:
        ...
    def get_region_parameter(self) -> RPMGSKParameter:
        """
        provide access to current region parameter-set
        """
    def get_states(self, end_states: RPMGSKStateVector) -> None:
        """
        collects current state from all the cells
        note that catchment filter can influence which states are calculated/updated.
        param end_states a reference to the vector<state_t> that are filled with cell state, in order of appearance.
        """
    def has_catchment_parameter(self, catchment_id: int) -> bool:
        """
        returns true if there exist a specific parameter override for the specified 0-based catchment_id
        """
    def has_routing(self) -> bool:
        """
        true if some cells routes to river-network
        """
    @typing.overload
    def initialize_cell_environment(self, time_axis: shyft.time_series.TimeAxisFixedDeltaT) -> None:
        """
        Initializes the cell enviroment (cell.env.ts* )
        
        The method initializes the cell environment, that keeps temperature, precipitation etc
        that is local to the cell.The initial values of these time - series is set to zero.
        The region-model time-axis is set to the supplied time-axis, so that
        the any calculation steps will use the supplied time-axis.
        This call is needed once prior to call to the .interpolate() or .run_cells() methods
        
        The call ensures that all cells.env ts are reset to zero, with a time-axis and
         value-vectors according to the supplied time-axis.
         Also note that the region-model.time_axis is set to the supplied time-axis.
        
        
        Args:
            time_axis (TimeAxisFixedDeltaT): specifies the time-axis for the region-model, and thus the cells
        
        Returns:
            : nothing. 
        """
    @typing.overload
    def initialize_cell_environment(self, time_axis: shyft.time_series.TimeAxis) -> None:
        """
        Initializes the cell enviroment (cell.env.ts* )
        
        The method initializes the cell environment, that keeps temperature, precipitation etc
        that is local to the cell.The initial values of these time - series is set to zero.
        The region-model time-axis is set to the supplied time-axis, so that
        the any calculation steps will use the supplied time-axis.
        This call is needed once prior to call to the .interpolate() or .run_cells() methods
        
        The call ensures that all cells.env ts are reset to zero, with a time-axis and
         value-vectors according to the supplied time-axis.
         Also note that the region-model.time_axis is set to the supplied time-axis.
        
        
        Args:
            time_axis (TimeAxis): specifies the time-axis (fixed type) for the region-model, and thus the cells
        
        Returns:
            : nothing. 
        """
    def interpolate(self, interpolation_parameter: shyft.hydrology.InterpolationParameter, env: shyft.hydrology.ARegionEnvironment, best_effort: bool = True) -> bool:
        """
        do interpolation interpolates region_environment temp,precip,rad.. point sources
        to a value representative for the cell.mid_point().
        
        note: initialize_cell_environment should be called once prior to this function
        
        Only supplied vectors of temp, precip etc. are interpolated, thus
        the user of the class can choose to put in place distributed series in stead.
        
        
        Args:
            interpolation_parameter (InterpolationParameter): contains wanted parameters for the interpolation
        
            env (RegionEnvironment): contains the region environment with geo-localized time-series for P,T,R,W,Rh
        
            best_effort (bool): default=True, don't throw, just return True/False if problem, with best_effort, unfilled values is nan
        
        Returns:
            bool: success. True if interpolation runs with no exceptions(btk,raises if to few neighbours)
        """
    def is_calculated(self, catchment_id: int) -> bool:
        """
        true if catchment id is calculated during runs, ref set_catchment_calculation_filter
        """
    def is_cell_env_ts_ok(self) -> bool:
        """
        Use this function after the interpolation step, before .run_cells(), to verify
        that all cells selected for computation (calculation_filter), do have 
        valid values.
        
        Returns:
            bool: all_ok. return false if any nan is found, otherwise true
        """
    def number_of_catchments(self) -> int:
        """
        compute and return number of catchments using info in cells.geo.catchment_id()
        """
    def remove_catchment_parameter(self, catchment_id: int) -> None:
        """
        remove a catchment specific parameter override, if it exists.
        """
    def revert_to_initial_state(self) -> None:
        """
        Given that the cell initial_states are established, these are 
        copied back into the cells
        Note that the cell initial_states vector is established at the first call to 
        .set_states() or run_cells()
        """
    def river_local_inflow_m3s(self, rid: int) -> shyft.time_series.TsFixed:
        """
        returns the routed local inflow from connected cells to the specified river id (rid))
        """
    def river_output_flow_m3s(self, rid: int) -> shyft.time_series.TsFixed:
        """
        returns the routed output flow of the specified river id (rid))
        """
    def river_upstream_inflow_m3s(self, rid: int) -> shyft.time_series.TsFixed:
        """
        returns the routed upstream inflow to the specified river id (rid))
        """
    def run_cells(self, use_ncore: int = 0, start_step: int = 0, n_steps: int = 0) -> None:
        """
        run_cells calculations over specified time_axis,optionally with thread_cell_count, start_step and n_steps
        require that initialize(time_axis) or run_interpolation is done first
        If start_step and n_steps are specified, only the specified part of the time-axis is covered.
        The result and state time-series are updated for the specified run-period, other parts are left unchanged.
        notice that in any case, the current model state is used as a starting point
        
        Args:
            use_ncore (int): number of worker threads, or cores to use, if 0 is passed, the the core-count is used to determine the count
        
            start_step (int): start_step in the time-axis to start at, py::default=0, meaning start at the beginning
        
            n_steps (int): number of steps to run in a partial run, py::default=0 indicating the complete time-axis is covered
        """
    @typing.overload
    def run_interpolation(self, interpolation_parameter: shyft.hydrology.InterpolationParameter, time_axis: shyft.time_series.TimeAxisFixedDeltaT, env: shyft.hydrology.ARegionEnvironment, best_effort: bool = True) -> bool:
        """
        run_interpolation interpolates region_environment temp,precip,rad.. point sources
        to a value representative for the cell.mid_point().
        
        note: This function is equivalent to
            self.initialize_cell_environment(time_axis)
            self.interpolate(interpolation_parameter,env)
        
        Args:
            interpolation_parameter (InterpolationParameter): contains wanted parameters for the interpolation
        
            time_axis (TimeAxisFixedDeltaT): should be equal to the time-axis the region_model is prepared running for
        
            env (RegionEnvironment): contains the ref: region_environment type
        
            best_effort (bool): default=True, don't throw, just return True/False if problem, with best_effort, unfilled values is nan
        
        Returns:
            bool: success. True if interpolation runs with no exceptions(btk,raises if to few neighbours)
        """
    @typing.overload
    def run_interpolation(self, interpolation_parameter: shyft.hydrology.InterpolationParameter, time_axis: shyft.time_series.TimeAxis, env: shyft.hydrology.ARegionEnvironment, best_effort: bool = True) -> bool:
        """
        run_interpolation interpolates region_environment temp,precip,rad.. point sources
        to a value representative for the cell.mid_point().
        
        note: This function is equivalent to
            self.initialize_cell_environment(time_axis)
            self.interpolate(interpolation_parameter,env)
        
        Args:
            interpolation_parameter (InterpolationParameter): contains wanted parameters for the interpolation
        
            time_axis (TimeAxis): should be equal to the time-axis the region_model is prepared running for
        
            env (RegionEnvironment): contains the ref: region_environment type
        
            best_effort (bool): default=True, don't throw, just return True/False if problem, with best_effort, unfilled values is nan
        
        Returns:
            bool: success. True if interpolation runs with no exceptions(btk,raises if to few neighbours)
        """
    def set_calculation_filter(self, catchment_id_list: list[int], river_id_list: list[int]) -> None:
        """
        set/reset the catchment *and* river based calculation filter. This affects what get simulate/calculated during
        the run command. Pass an empty list to reset/clear the filter (i.e. no filter).
        
        param catchment_id_list is a catchment id vector
        param river_id_list is a river id vector
        """
    def set_catchment_calculation_filter(self, catchment_id_list: list[int]) -> None:
        """
        set/reset the catchment based calculation filter. This affects what get simulate/calculated during
        the run command. Pass an empty list to reset/clear the filter (i.e. no filter).
        
        param catchment_id_list is a catchment id vector
        """
    def set_catchment_parameter(self, catchment_id: int, p: RPMGSKParameter) -> None:
        """
        creates/modifies a pr catchment override parameter
        param catchment_id the 0 based catchment_id that correlates to the cells catchment_id
        param a reference to the parameter that will be kept for those cells
        """
    def set_cell_environment(self, time_axis: shyft.time_series.TimeAxis, region_env: shyft.hydrology.ARegionEnvironment) -> bool:
        """
        Set the forcing data cell enviroment (cell.env_ts.* )
        
        The method initializes the cell environment, that keeps temperature, precipitation etc
        for all the cells.
        The region-model time-axis is set to the supplied time-axis, so that
        the the region model is ready to run cells, using this time-axis.
        
        There are strict requirements to the content of the `region_env` parameter:
        
         - rm.cells[i].mid_point()== region_env.temperature[i].mid_point() for all i
         - similar for precipitation,rel_hum,radiation,wind_speed
        
        So same number of forcing data, in the same order and geo position as the cells.
        Tip: If time_axis is equal to the forcing time-axis, it is twice as fast.
        
        
        Args:
            time_axis (TimeAxis): specifies the time-axisfor the region-model, and thus the cells
        
            region_env (ARegionEnvironment): A region environment with ready to use forcing data for all the cells.
        
        Returns:
            bool: success. true if successfull, raises exception otherwise
        """
    def set_region_parameter(self, p: RPMGSKParameter) -> None:
        """
        set the region parameter, apply it to all cells 
        that do *not* have catchment specific parameters.
        """
    def set_snow_sca_swe_collection(self, catchment_id: int, on_or_off: bool) -> None:
        """
        enable/disable collection of snow sca|sca for calibration purposes
        param cachment_id to enable snow calibration for, -1 means turn on/off for all
        param on_or_off true|or false.
        note if the underlying cell do not support snow sca|swe collection, this 
        """
    def set_state_collection(self, catchment_id: int, on_or_off: bool) -> None:
        """
        enable state collection for specified or all cells
        note that this only works if the underlying cell is configured to
        do state collection. This is typically not the  case for
        cell-types that are used during calibration/optimization
        """
    def set_states(self, states: RPMGSKStateVector) -> None:
        """
        set current state for all the cells in the model.
        states is a vector<state_t> of all states, must match size/order of cells.
        note throws runtime-error if states.size is different from cells.size
        """
    def size(self) -> int:
        """
        return number of cells
        """
    @property
    def actual_evaptranspiration_response(self) -> RPMGSKCellActualEvapotranspirationResponseStatistics:
        ...
    @property
    def auto_routing_time_axis(self) -> bool:
        """
        TimeAxis: use fine time-resolution for the routing step allowing better handling of sub-timestep routing effects.
        For 24h time-step, a 1h routing timestep is used, for less than 24h time-step a 6 minute routing timestep is used.
        If set to false, the simulation-time-axis is used for the routing-step.
        """
    @auto_routing_time_axis.setter
    def auto_routing_time_axis(self, arg0: bool) -> None:
        ...
    @property
    def catchment_ids(self) -> list[int]:
        """
        IntVector: provides the list of catchment identifiers,'cids' within this model
        """
    @property
    def cells(self) -> RPMGSKCellAllVector:
        ...
    @property
    def current_state(self) -> RPMGSKStateVector:
        """
        RPMGSKStateVector: a copy of the current model state
        """
    @property
    def gamma_snow_response(self) -> RPMGSKCellGammaSnowResponseStatistics:
        ...
    @property
    def gamma_snow_state(self) -> RPMGSKCellGammaSnowStateStatistics:
        ...
    @property
    def initial_state(self) -> RPMGSKStateVector:
        """
        RPMGSKState: empty or the the initial state as established on the first invokation of .set_states() or .run_cells()
        """
    @initial_state.setter
    def initial_state(self, arg0: RPMGSKStateVector) -> None:
        ...
    @property
    def interpolation_parameter(self) -> shyft.hydrology.InterpolationParameter:
        """
        InterpolationParameter: most recently used interpolation parameter as passed to run_interpolation or interpolate routine
        """
    @interpolation_parameter.setter
    def interpolation_parameter(self, arg0: shyft.hydrology.InterpolationParameter) -> None:
        ...
    @property
    def kirchner_state(self) -> RPMGSKCellKirchnerStateStatistics:
        ...
    @property
    def ncore(self) -> int:
        """
        int: determines how many core to utilize during run_cell processing,
        0(=default) means detect by hardware probe
        """
    @ncore.setter
    def ncore(self, arg0: int) -> None:
        ...
    @property
    def penman_monteith_response(self) -> RPMGSKCellPenmanMonteithResponseStatistics:
        ...
    @property
    def region_env(self) -> shyft.hydrology.ARegionEnvironment:
        """
        ARegionEnvironment: empty or the region_env as passed to run_interpolation() or interpolate()
        """
    @region_env.setter
    def region_env(self, arg0: shyft.hydrology.ARegionEnvironment) -> None:
        ...
    @property
    def river_network(self) -> shyft.hydrology.RiverNetwork:
        """
        RiverNetwork: river network that when enabled do the routing part of the region-model
        See also RiverNetwork class for how to build a working river network
        Then use the connect_catchment_to_river(cid,rid) method
        to route cell discharge into the river-network
        """
    @river_network.setter
    def river_network(self, arg0: shyft.hydrology.RiverNetwork) -> None:
        ...
    @property
    def state(self) -> RPMGSKCellAllStateHandler:
        ...
    @property
    def statistics(self) -> RPMGSKCellAllStatistics:
        ...
    @property
    def time_axis(self) -> shyft.time_series.TimeAxisFixedDeltaT:
        """
        TimeAxisFixedDeltaT:  time_axis (type TimeAxisFixedDeltaT) as set from run_interpolation, determines the time-axis for run
        """
class RPMGSKNullCollector:
    """
    A null collector, useful during calibration to minimize memory&maximize speed
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class RPMGSKOptModel:
    """
    RPMGSKOptModel , a region_model is the calculation model for a region, where we can have
    one or more catchments.
    The role of the region_model is to describe region, so that we can run the
    region computational model efficiently for a number of type of cells, interpolation and
    catchment level algorihtms.
    
    The region model keeps a list of cells, of specified type 
    as well as parameters for the cells.
    The model also keeps state, such as region_env(forcing variables), time-axis and intial state
    - they are non-empty after initializing, and running the model
    """
    cell_t = RPMGSKCellOpt
    full_model_t = RPMGSKModel
    optimizer_t = RPMGSKOptimizer
    parameter_t = RPMGSKParameter
    state_t = RPMGSKState
    state_with_id_t = RPMGSKStateWithId
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, other_model: RPMGSKOptModel) -> None:
        """
        Create a copy of the other_model
        
        Args:
            other_model (RegionModel): region-model to copy
        """
    @typing.overload
    def __init__(self, geo_data_vector: shyft.hydrology.GeoCellDataVector, region_param: RPMGSKParameter) -> None:
        """
        Creates a model from GeoCellDataVector and region model parameters
        
        Args:
            geo_data_vector (GeoCellDataVector): contains the geo-related characteristics for the cells
        
            region_param (Parameter): contains the parameters for all cells of this region model
        """
    @typing.overload
    def __init__(self, cells: RPMGSKCellOptVector, region_param: RPMGSKParameter, catchment_parameters: RPMGSKParameterMap) -> None:
        """
        Creates a model from cells and region model parameters, and specified catchment parameters
        The cell-vector and catchment-id's should match those specified in the catchment_parameters mapping
        
        Args:
            cells (CellVector): contains the cells, each with geo-properties and type matching the region-model type
        
            region_param (Parameter): contains the parameters for cells that does not have catchment specific parameters
        
            catchment_parameters (ParameterMap): contains mapping (a kind of dict, where the key is catchment-id and value is parameters for cells matching catchment-id
        """
    def adjust_q(self, q_scale: float, cids: list[int]) -> None:
        """
        adjust the current state content q of ground storage by scale-factor
        
        Adjust the content of the ground storage, e.g. state.kirchner.q, or
        hbv state.(tank|soil).(uz,lz|sm), by the specified scale factor.
        The this function plays key role for adjusting the state to
        achieve a specified/wanted average discharge flow output for the
        model at the first time-step.
        
        Args:
            q_scale (float): the scale factor to apply to current storage state
        
            cids (IntVector): if empty, all cells are in scope, otherwise only cells that have specified catchment ids.
        """
    def adjust_state_to_target_flow(self, wanted_flow_m3s: float, cids: list[int], start_step: int = 0, scale_range: float = 10.0, scale_eps: float = 0.001, max_iter: int = 300, n_steps: int = 1) -> shyft.hydrology.FlowAdjustResult:
        """
        state adjustment to achieve wanted/observed flow
        
        This function provides an easy and consistent way to adjust the
        state of the cells(kirchner, or hbv-tank-levels) so that the average output
        from next n_steps time-steps matches the wanted flow for the same period.
        
        This is quite complex, since the amount of adjustment needed is dependent of the
        cell-state, temperature/precipitation in time-step, glacier-melt, length of the time-step,
        and calibration factors sensitivity.
        
        The approach here is to use dlib::find_min_single_variable to solve
        the problem, instead of trying to reverse compute the needed state.
        
        This has several benefits, it deals with the full stack and state, and it can be made
        method stack independent.
        
        Notice that the model should be prepared for run prior to calling this function
        and that there should be a current model state that gives the starting point
        for the adjustment.
        Also note that when returning, the active state reflects the
        achieved flow returned, and that the current state  for the cells
        belonging to the catchment-ids is modified as needed to provide this average-flow.
        The state when returning is set to the start of the i'th period specified
        to reach the desired flow.
        
        
        Args:
            wanted_flow_m3s (float): the average flow first time-step we want to achieve
        
            cids (IntVector):  catchments, represented by catchment-ids that should be adjusted
        
            start_step (int): what time-step number in the time-axis to use, py::default 0
        
            scale_range (float): optimizer boundaries is s_0/scale_range .. s_0*scale_range, s_0=wanted_flow_m3s/q_0 , py::default =10.0
        
            scale_eps (float): optimizer eps, stop criteria (ref. dlib), eps=s_0*scale_eps , py::default =1-e3
        
            max_iter (int): optimizer max evaluations before giving up to find optimal solution
        
            n_steps (int): number of time-steps in the time-axis to average the to the wanted_flow_m3s, py::default=1
        
        Returns:
            FlowAdjustResult: obtained flow in m3/s units.. note: this can deviate from wanted flow due to model and state constraints
        """
    def connect_catchment_to_river(self, cid: int, rid: int) -> None:
        """
        Connect routing of all the cells in the specified catchment id to the specified river id
        
        
        Args:
            cid (int): catchment identifier
        
            rid (int): river identifier, can be set to 0 to indicate disconnect from routing
        """
    def create_full_model_clone(self, with_catchment_params: bool = False) -> RPMGSKModel:
        """
        Clone a model to a another similar type model, full to opt-model or vice-versa
        The entire state except catchment-specific parameters, filter and result-series are cloned
        The returned model is ready to run_cells(), state and interpolated enviroment is identical to the clone source
        
        Args:
            src_model (XXXX?Model): The model to be cloned, with state interpolation done, etc
        
            with_catchment_params (bool): default false, if true also copy catchment specific parameters
        
        Returns:
            XXXX?Model: new_model. new_model ready to run_cells, or to put into the calibrator/optimizer
        """
    def extract_geo_cell_data(self) -> shyft.hydrology.GeoCellDataVector:
        """
        extracts the geo_cell_data and return it as GeoCellDataVector that can
        be passed into a the constructor of a new region-model (clone-operation)
        """
    def get_catchment_parameter(self, catchment_id: int) -> RPMGSKParameter:
        """
        return the parameter valid for specified catchment_id, or global parameter if not found.
        note Be aware that if you change the returned parameter, it will affect the related cells.
        param catchment_id 0 based catchment id as placed on each cell
        returns reference to the real parameter structure for the catchment_id if exists,
        otherwise the global parameters
        """
    def get_cells(self) -> RPMGSKCellOptVector:
        ...
    def get_region_parameter(self) -> RPMGSKParameter:
        """
        provide access to current region parameter-set
        """
    def get_states(self, end_states: RPMGSKStateVector) -> None:
        """
        collects current state from all the cells
        note that catchment filter can influence which states are calculated/updated.
        param end_states a reference to the vector<state_t> that are filled with cell state, in order of appearance.
        """
    def has_catchment_parameter(self, catchment_id: int) -> bool:
        """
        returns true if there exist a specific parameter override for the specified 0-based catchment_id
        """
    def has_routing(self) -> bool:
        """
        true if some cells routes to river-network
        """
    @typing.overload
    def initialize_cell_environment(self, time_axis: shyft.time_series.TimeAxisFixedDeltaT) -> None:
        """
        Initializes the cell enviroment (cell.env.ts* )
        
        The method initializes the cell environment, that keeps temperature, precipitation etc
        that is local to the cell.The initial values of these time - series is set to zero.
        The region-model time-axis is set to the supplied time-axis, so that
        the any calculation steps will use the supplied time-axis.
        This call is needed once prior to call to the .interpolate() or .run_cells() methods
        
        The call ensures that all cells.env ts are reset to zero, with a time-axis and
         value-vectors according to the supplied time-axis.
         Also note that the region-model.time_axis is set to the supplied time-axis.
        
        
        Args:
            time_axis (TimeAxisFixedDeltaT): specifies the time-axis for the region-model, and thus the cells
        
        Returns:
            : nothing. 
        """
    @typing.overload
    def initialize_cell_environment(self, time_axis: shyft.time_series.TimeAxis) -> None:
        """
        Initializes the cell enviroment (cell.env.ts* )
        
        The method initializes the cell environment, that keeps temperature, precipitation etc
        that is local to the cell.The initial values of these time - series is set to zero.
        The region-model time-axis is set to the supplied time-axis, so that
        the any calculation steps will use the supplied time-axis.
        This call is needed once prior to call to the .interpolate() or .run_cells() methods
        
        The call ensures that all cells.env ts are reset to zero, with a time-axis and
         value-vectors according to the supplied time-axis.
         Also note that the region-model.time_axis is set to the supplied time-axis.
        
        
        Args:
            time_axis (TimeAxis): specifies the time-axis (fixed type) for the region-model, and thus the cells
        
        Returns:
            : nothing. 
        """
    def interpolate(self, interpolation_parameter: shyft.hydrology.InterpolationParameter, env: shyft.hydrology.ARegionEnvironment, best_effort: bool = True) -> bool:
        """
        do interpolation interpolates region_environment temp,precip,rad.. point sources
        to a value representative for the cell.mid_point().
        
        note: initialize_cell_environment should be called once prior to this function
        
        Only supplied vectors of temp, precip etc. are interpolated, thus
        the user of the class can choose to put in place distributed series in stead.
        
        
        Args:
            interpolation_parameter (InterpolationParameter): contains wanted parameters for the interpolation
        
            env (RegionEnvironment): contains the region environment with geo-localized time-series for P,T,R,W,Rh
        
            best_effort (bool): default=True, don't throw, just return True/False if problem, with best_effort, unfilled values is nan
        
        Returns:
            bool: success. True if interpolation runs with no exceptions(btk,raises if to few neighbours)
        """
    def is_calculated(self, catchment_id: int) -> bool:
        """
        true if catchment id is calculated during runs, ref set_catchment_calculation_filter
        """
    def is_cell_env_ts_ok(self) -> bool:
        """
        Use this function after the interpolation step, before .run_cells(), to verify
        that all cells selected for computation (calculation_filter), do have 
        valid values.
        
        Returns:
            bool: all_ok. return false if any nan is found, otherwise true
        """
    def number_of_catchments(self) -> int:
        """
        compute and return number of catchments using info in cells.geo.catchment_id()
        """
    def remove_catchment_parameter(self, catchment_id: int) -> None:
        """
        remove a catchment specific parameter override, if it exists.
        """
    def revert_to_initial_state(self) -> None:
        """
        Given that the cell initial_states are established, these are 
        copied back into the cells
        Note that the cell initial_states vector is established at the first call to 
        .set_states() or run_cells()
        """
    def river_local_inflow_m3s(self, rid: int) -> shyft.time_series.TsFixed:
        """
        returns the routed local inflow from connected cells to the specified river id (rid))
        """
    def river_output_flow_m3s(self, rid: int) -> shyft.time_series.TsFixed:
        """
        returns the routed output flow of the specified river id (rid))
        """
    def river_upstream_inflow_m3s(self, rid: int) -> shyft.time_series.TsFixed:
        """
        returns the routed upstream inflow to the specified river id (rid))
        """
    def run_cells(self, use_ncore: int = 0, start_step: int = 0, n_steps: int = 0) -> None:
        """
        run_cells calculations over specified time_axis,optionally with thread_cell_count, start_step and n_steps
        require that initialize(time_axis) or run_interpolation is done first
        If start_step and n_steps are specified, only the specified part of the time-axis is covered.
        The result and state time-series are updated for the specified run-period, other parts are left unchanged.
        notice that in any case, the current model state is used as a starting point
        
        Args:
            use_ncore (int): number of worker threads, or cores to use, if 0 is passed, the the core-count is used to determine the count
        
            start_step (int): start_step in the time-axis to start at, py::default=0, meaning start at the beginning
        
            n_steps (int): number of steps to run in a partial run, py::default=0 indicating the complete time-axis is covered
        """
    @typing.overload
    def run_interpolation(self, interpolation_parameter: shyft.hydrology.InterpolationParameter, time_axis: shyft.time_series.TimeAxisFixedDeltaT, env: shyft.hydrology.ARegionEnvironment, best_effort: bool = True) -> bool:
        """
        run_interpolation interpolates region_environment temp,precip,rad.. point sources
        to a value representative for the cell.mid_point().
        
        note: This function is equivalent to
            self.initialize_cell_environment(time_axis)
            self.interpolate(interpolation_parameter,env)
        
        Args:
            interpolation_parameter (InterpolationParameter): contains wanted parameters for the interpolation
        
            time_axis (TimeAxisFixedDeltaT): should be equal to the time-axis the region_model is prepared running for
        
            env (RegionEnvironment): contains the ref: region_environment type
        
            best_effort (bool): default=True, don't throw, just return True/False if problem, with best_effort, unfilled values is nan
        
        Returns:
            bool: success. True if interpolation runs with no exceptions(btk,raises if to few neighbours)
        """
    @typing.overload
    def run_interpolation(self, interpolation_parameter: shyft.hydrology.InterpolationParameter, time_axis: shyft.time_series.TimeAxis, env: shyft.hydrology.ARegionEnvironment, best_effort: bool = True) -> bool:
        """
        run_interpolation interpolates region_environment temp,precip,rad.. point sources
        to a value representative for the cell.mid_point().
        
        note: This function is equivalent to
            self.initialize_cell_environment(time_axis)
            self.interpolate(interpolation_parameter,env)
        
        Args:
            interpolation_parameter (InterpolationParameter): contains wanted parameters for the interpolation
        
            time_axis (TimeAxis): should be equal to the time-axis the region_model is prepared running for
        
            env (RegionEnvironment): contains the ref: region_environment type
        
            best_effort (bool): default=True, don't throw, just return True/False if problem, with best_effort, unfilled values is nan
        
        Returns:
            bool: success. True if interpolation runs with no exceptions(btk,raises if to few neighbours)
        """
    def set_calculation_filter(self, catchment_id_list: list[int], river_id_list: list[int]) -> None:
        """
        set/reset the catchment *and* river based calculation filter. This affects what get simulate/calculated during
        the run command. Pass an empty list to reset/clear the filter (i.e. no filter).
        
        param catchment_id_list is a catchment id vector
        param river_id_list is a river id vector
        """
    def set_catchment_calculation_filter(self, catchment_id_list: list[int]) -> None:
        """
        set/reset the catchment based calculation filter. This affects what get simulate/calculated during
        the run command. Pass an empty list to reset/clear the filter (i.e. no filter).
        
        param catchment_id_list is a catchment id vector
        """
    def set_catchment_parameter(self, catchment_id: int, p: RPMGSKParameter) -> None:
        """
        creates/modifies a pr catchment override parameter
        param catchment_id the 0 based catchment_id that correlates to the cells catchment_id
        param a reference to the parameter that will be kept for those cells
        """
    def set_cell_environment(self, time_axis: shyft.time_series.TimeAxis, region_env: shyft.hydrology.ARegionEnvironment) -> bool:
        """
        Set the forcing data cell enviroment (cell.env_ts.* )
        
        The method initializes the cell environment, that keeps temperature, precipitation etc
        for all the cells.
        The region-model time-axis is set to the supplied time-axis, so that
        the the region model is ready to run cells, using this time-axis.
        
        There are strict requirements to the content of the `region_env` parameter:
        
         - rm.cells[i].mid_point()== region_env.temperature[i].mid_point() for all i
         - similar for precipitation,rel_hum,radiation,wind_speed
        
        So same number of forcing data, in the same order and geo position as the cells.
        Tip: If time_axis is equal to the forcing time-axis, it is twice as fast.
        
        
        Args:
            time_axis (TimeAxis): specifies the time-axisfor the region-model, and thus the cells
        
            region_env (ARegionEnvironment): A region environment with ready to use forcing data for all the cells.
        
        Returns:
            bool: success. true if successfull, raises exception otherwise
        """
    def set_region_parameter(self, p: RPMGSKParameter) -> None:
        """
        set the region parameter, apply it to all cells 
        that do *not* have catchment specific parameters.
        """
    def set_snow_sca_swe_collection(self, catchment_id: int, on_or_off: bool) -> None:
        """
        enable/disable collection of snow sca|sca for calibration purposes
        param cachment_id to enable snow calibration for, -1 means turn on/off for all
        param on_or_off true|or false.
        note if the underlying cell do not support snow sca|swe collection, this 
        """
    def set_state_collection(self, catchment_id: int, on_or_off: bool) -> None:
        """
        enable state collection for specified or all cells
        note that this only works if the underlying cell is configured to
        do state collection. This is typically not the  case for
        cell-types that are used during calibration/optimization
        """
    def set_states(self, states: RPMGSKStateVector) -> None:
        """
        set current state for all the cells in the model.
        states is a vector<state_t> of all states, must match size/order of cells.
        note throws runtime-error if states.size is different from cells.size
        """
    def size(self) -> int:
        """
        return number of cells
        """
    @property
    def auto_routing_time_axis(self) -> bool:
        """
        TimeAxis: use fine time-resolution for the routing step allowing better handling of sub-timestep routing effects.
        For 24h time-step, a 1h routing timestep is used, for less than 24h time-step a 6 minute routing timestep is used.
        If set to false, the simulation-time-axis is used for the routing-step.
        """
    @auto_routing_time_axis.setter
    def auto_routing_time_axis(self, arg0: bool) -> None:
        ...
    @property
    def catchment_ids(self) -> list[int]:
        """
        IntVector: provides the list of catchment identifiers,'cids' within this model
        """
    @property
    def cells(self) -> RPMGSKCellOptVector:
        ...
    @property
    def current_state(self) -> RPMGSKStateVector:
        """
        RPMGSKStateVector: a copy of the current model state
        """
    @property
    def initial_state(self) -> RPMGSKStateVector:
        """
        RPMGSKState: empty or the the initial state as established on the first invokation of .set_states() or .run_cells()
        """
    @initial_state.setter
    def initial_state(self, arg0: RPMGSKStateVector) -> None:
        ...
    @property
    def interpolation_parameter(self) -> shyft.hydrology.InterpolationParameter:
        """
        InterpolationParameter: most recently used interpolation parameter as passed to run_interpolation or interpolate routine
        """
    @interpolation_parameter.setter
    def interpolation_parameter(self, arg0: shyft.hydrology.InterpolationParameter) -> None:
        ...
    @property
    def ncore(self) -> int:
        """
        int: determines how many core to utilize during run_cell processing,
        0(=default) means detect by hardware probe
        """
    @ncore.setter
    def ncore(self, arg0: int) -> None:
        ...
    @property
    def region_env(self) -> shyft.hydrology.ARegionEnvironment:
        """
        ARegionEnvironment: empty or the region_env as passed to run_interpolation() or interpolate()
        """
    @region_env.setter
    def region_env(self, arg0: shyft.hydrology.ARegionEnvironment) -> None:
        ...
    @property
    def river_network(self) -> shyft.hydrology.RiverNetwork:
        """
        RiverNetwork: river network that when enabled do the routing part of the region-model
        See also RiverNetwork class for how to build a working river network
        Then use the connect_catchment_to_river(cid,rid) method
        to route cell discharge into the river-network
        """
    @river_network.setter
    def river_network(self, arg0: shyft.hydrology.RiverNetwork) -> None:
        ...
    @property
    def state(self) -> RPMGSKCellOptStateHandler:
        ...
    @property
    def statistics(self) -> RPMGSKCellOptStatistics:
        ...
    @property
    def time_axis(self) -> shyft.time_series.TimeAxisFixedDeltaT:
        """
        TimeAxisFixedDeltaT:  time_axis (type TimeAxisFixedDeltaT) as set from run_interpolation, determines the time-axis for run
        """
class RPMGSKOptimizer:
    """
    The optimizer for parameters for a region model
    It provides needed functionality to orchestrate a search for the optimal parameters so that the goal function
    specified by the target_specifications are minimized.
    The user can specify which parameters (model specific) to optimize, giving range min..max for each of the
    parameters. Only parameters with min != max are used, thus minimizing the parameter space.
    
    Target specification ref: TargetSpecificationVector allows a lot of flexibility when it comes to what
    goes into the goal-function.
    
    This class provides several goal-function search algorithms:
        .optimize               min-bobyqa  a fast local optimizer, http://dlib.net/optimization.html#find_min_bobyqa
        .optimize_global   a global optimizer, http://dlib.net/optimization.html#global_function_search
        .optimize_sceua   a global optimizer,  https://www.sciencedirect.com/science/article/pii/0022169494900574
        .optimize_dream  a global optimizer,
                                                                Theory is found in: Vrugt, J. et al: Accelerating Markov Chain Monte Carlo
                                                                simulations by Differential Evolution with Self-Adaptive Randomized Subspace
                                                                Sampling. Int. J. of Nonlinear Sciences and Numerical Simulation 10(3) 2009.
    
    
    Each method searches for the optimum parameter-set, given the input-constraints and time-limit, max_iterations and accuracy(method dependent).
    Also note that after the optimization, you have a complete trace of the parameter-search with the corresponding goal-function value
    This enable you to analyze the search-function, and allows you to select other parameter-sets that based on 
    hydrological criterias that is not captured in the goal-function specification
    
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, model: RPMGSKOptModel, targets: shyft.hydrology.TargetSpecificationVector, p_min: list[float], p_max: list[float]) -> None:
        """
        Construct an optimizer for the specified region model.
        Set  p_min.param.x = p_max.param.x  to disable optimization for a parameter param.x
        
        
        Args:
            model (OptModel): the model to be optimized, the model should be initialized, interpolation/preparation  step done
        
            targets (TargetSpecificationVector): specifies how to calculate the goal-function
        
            p_min (Parameter): minimum values for the parameters to be optimized
        
            p_max (Parameter): maximum values for the parameters to be optimized
        """
    @typing.overload
    def __init__(self, model: RPMGSKOptModel) -> None:
        """
        Construct a parameter Optimizer for the supplied model
        Use method .set_target_specification(...) to provide the target specification,
        then invoke opt_param= o.optimize(p_starting_point..)
        to get back the optimized parameters for the supplied model and target-specification
        
        
        Args:
            model (OptModel): the model to be optimized, the model should be initialized, interpolation/preparation  step done
        """
    @typing.overload
    def calculate_goal_function(self, full_vector_of_parameters: list[float]) -> float:
        """
        (Deprecated)calculate the goal_function as used by minbobyqa,etc.,
        using the full set of  parameters vectors (as passed to optimize())
        and also ensures that the shyft state/cell/catchment result is consistent
        with the passed parameters passed
        param full_vector_of_parameters contains all parameters that will be applied to the run.
        returns the goal-function, weigthed nash_sutcliffe|Kling-Gupta sum 
        """
    @typing.overload
    def calculate_goal_function(self, parameters: RPMGSKParameter) -> float:
        """
        Calculate the goal_function as used by minbobyqa,etc.,
        using the supplied set of parameters
        and also ensures that the shyft state/cell/catchment result is consistent
        with the passed parameters passed
        param parameters contains all parameters that will be applied to the run.
        You can also use this function to build your own external supplied optimizer in python
        
        Args:
            parameters (Parameter): the region model parameter to use when evaluating the goal-function
        
        Returns:
            float: goal_function_value. the goal-function, weigthed nash_sutcliffe|Kling-Gupta sum etc. value 
        """
    def establish_initial_state_from_model(self) -> None:
        """
        Copies the Optimizer referenced region-model current state
        to a private store in the Optimizer object.
        This state is used to for restore prior to each run of the model during calibration
        notice that if you forget to call this method, it will be called automatically once you
        call one of the optimize methods.
        """
    def get_initial_state(self, i: int) -> RPMGSKState:
        """
        returns a copy of the i'th cells initial state
        """
    @typing.overload
    def optimize(self, p: list[float], max_n_evaluations: int, tr_start: float, tr_stop: float) -> list[float]:
        """
        (deprecated)Call to optimize model, starting with p parameter set, using p_min..p_max as boundaries.
        where p is the full parameter vector.
        the p_min,p_max specified in constructor is used to reduce the parameterspace for the optimizer
        down to a minimum number to facilitate fast run.
        param p contains the starting point for the parameters
        param max_n_evaluations stop after n calls of the objective functions, i.e. simulations.
        param tr_start is the trust region start , py::default 0.1, ref bobyqa
        param tr_stop is the trust region stop, py::default 1e-5, ref bobyqa
        return the optimized parameter vector
        """
    @typing.overload
    def optimize(self, p: RPMGSKParameter, max_n_evaluations: int, tr_start: float, tr_stop: float) -> RPMGSKParameter:
        """
        Call to optimize model, using find_min_bobyqa,  starting with p parameters
        as the start point
        The current target specification, parameter lower and upper bound
        is taken into account
        
        
        Args:
            p (Parameter): contains the starting point for the parameters
        
            max_n_evaluations (int): stop after n calls of the objective functions, i.e. simulations.
        
            tr_start (float): minbobyqa is the trust region start , py::default 0.1, ref bobyqa
        
            tr_stop (float):  is the trust region stop, py::default 1e-5, ref bobyqa
        
        Returns:
            Parameter: p_opt. the the optimized parameters
        """
    @typing.overload
    def optimize_dream(self, p: list[float], max_n_evaluations: int) -> list[float]:
        """
        (Deprecated)Call to optimize model, using DREAM alg., find p, using p_min..p_max as boundaries.
        where p is the full parameter vector.
        the p_min,p_max specified in constructor is used to reduce the parameterspace for the optimizer
        down to a minimum number to facilitate fast run.
        param p is used as start point (not really, DREAM use random, but we should be able to pass u and q....
        param max_n_evaluations stop after n calls of the objective functions, i.e. simulations.
        return the optimized parameter vector
        """
    @typing.overload
    def optimize_dream(self, p: RPMGSKParameter, max_n_evaluations: int) -> RPMGSKParameter:
        """
        Call to optimize model with the DREAM algorithm.
        The supplied p is ignored (DREAM selects starting point randomly)
        The current target specification, parameter lower and upper bound
        is taken into account
        
        
        Args:
            p (Parameter): the potential starting point for the global search(currently not used by dlib impl)
        
            max_n_evaluations (int): stop after n calls of the objective functions, i.e. simulations.
        
        Returns:
            Parameter: p_opt. the optimal found minima given the inputs
        """
    def optimize_global(self, p: RPMGSKParameter, max_n_evaluations: int, max_seconds: float, solver_eps: float) -> RPMGSKParameter:
        """
        Finds the global optimum parameters for the model.
        The current target specification, parameter lower and upper bound
        is taken into account
        .. refer to _dlib_global_search:
         http://dlib.net/optimization.html#global_function_search
        
        
        Args:
            p (Parameter): the potential starting point for the global search(currently not used by dlib impl)
        
            max_n_evaluations (int): stop after n calls of the objective functions, i.e. simulations.
        
            max_seconds (float): stop search for for solution after specified time-limit
        
            solver_eps (float): search for minimum goal-function value at this accuracy, continue search for possibly other global minima when this accuracy is reached.
        
        Returns:
            Parameter: p_opt. the optimal found minima given the inputs
        """
    @typing.overload
    def optimize_sceua(self, p: list[float], max_n_evaluations: int, x_eps: float, y_eps: float) -> list[float]:
        """
        (Deprecated)Call to optimize model, using SCE UA, using p as startpoint, find p, using p_min..p_max as boundaries.
        where p is the full parameter vector.
        the p_min,p_max specified in constructor is used to reduce the parameter-space for the optimizer
        down to a minimum number to facilitate fast run.
        param p is used as start point and is updated with the found optimal points
        param max_n_evaluations stop after n calls of the objective functions, i.e. simulations.
        param x_eps is stop condition when all changes in x's are within this range
        param y_eps is stop condition, and search is stopped when goal function does not improve anymore within this range
        return the optimized parameter vector
        """
    @typing.overload
    def optimize_sceua(self, p: RPMGSKParameter, max_n_evaluations: int, x_eps: float, y_eps: float) -> RPMGSKParameter:
        """
        Call to optimize model using SCE UA algorithm, starting with p parameters
        as the start point
        The current target specification, parameter lower and upper bound
        is taken into account
        
        
        Args:
            p (Parameter): the potential starting point for the global search
        
            max_n_evaluations (int): stop after n calls of the objective functions, i.e. simulations.
        
            x_eps (float): is stop condition when all changes in x's are within this range
        
            y_eps (float): is stop condition, and search is stopped when goal function does not improve anymore within this range
        
        Returns:
            Parameter: p_opt. the optimal found minima given the inputs
        """
    def parameter_active(self, i: int) -> bool:
        """
        returns true if the i'th parameter is active, i.e. lower != upper bound
        
        
        Args:
            i (int): the index of the parameter
        
        Returns:
            bool: active. True if the parameter abs(p[i].min -p[i].max)> zero_limit
        """
    def reset_states(self) -> None:
        """
        reset the state of the model to the initial state before starting the run/optimize
        """
    def set_parameter_ranges(self, p_min: list[float], p_max: list[float]) -> None:
        """
        Set the parameter ranges for the optimization search.
         Set min=max=wanted parameter value for those not subject to change during optimization
         - changes/sets the parameter_lower_bound.. paramter_upper_bound as specified in constructor
        
        
        Args:
            p_min (Parameter): the lower bounds of the parameters
        
            p_max (Parameter): the upper bounds of the parameters
        """
    def set_target_specification(self, target_specification: shyft.hydrology.TargetSpecificationVector, parameter_lower_bound: RPMGSKParameter, parameter_upper_bound: RPMGSKParameter) -> None:
        """
        Set the target specification, parameter lower and upper bound to be used during 
        subsequent call to the .optimize() methods.
        Only parameters with lower_bound != upper_bound will be subject to optimization
        The object properties target_specification,lower and upper bound are updated and
        will reflect the current setting.
        
        
        Args:
            target_specification (TargetSpecificationVector): the complete target specification composition of one or more criteria
        
            parameter_lower_bound (Parameter): the lower bounds of the parameters
        
            parameter_upper_bound (Parameter): the upper bounds of the parameters
        """
    def set_verbose_level(self, level: int) -> None:
        """
        set verbose level on stdout during calibration,0 is silent,1 is more etc.
        """
    def trace_goal_function_value(self, i: int) -> float:
        """
        returns the i'th goal function value
        """
    def trace_parameter(self, i: int) -> RPMGSKParameter:
        """
        returns the i'th parameter tried, corresponding to the 
        i'th trace_goal_function value
        
        See also:
            trace_goal_function,trace_size
        """
    def warning(self, i: int) -> str:
        """
        returns the i'th nan warning issued, use warn_size to get valid i range
        """
    @property
    def notify_cb(self) -> typing.Callable[[], bool]:
        """
        Callable[[],bool]: notify callback that you can assign from python.
        It is called after each iteration in the optimization.
        The function should return True to continue optimization,
        or False to stop as soon as possible.
        You can check/use the latest goal function value
        and the corresponding parameters etc.
        note: do NOT change anything in the model or parameters during callback,
        as this will at least give unspecified optimization behaviour
        """
    @notify_cb.setter
    def notify_cb(self, arg0: typing.Callable[[], bool]) -> None:
        ...
    @property
    def parameter_lower_bound(self) -> RPMGSKParameter:
        """
        the lower bound parameters
        """
    @parameter_lower_bound.setter
    def parameter_lower_bound(self, arg0: RPMGSKParameter) -> None:
        ...
    @property
    def parameter_upper_bound(self) -> RPMGSKParameter:
        """
        the upper bound parameters
        """
    @parameter_upper_bound.setter
    def parameter_upper_bound(self, arg0: RPMGSKParameter) -> None:
        ...
    @property
    def target_specification(self) -> shyft.hydrology.TargetSpecificationVector:
        """
        TargetSpecificationVector:  current target-specifications used during optimization
        """
    @target_specification.setter
    def target_specification(self, arg0: shyft.hydrology.TargetSpecificationVector) -> None:
        ...
    @property
    def trace_goal_function_values(self) -> list[float]:
        """
        DoubleVector: the goal-function values in the order of searching for the minimum value
        The trace_parameter(i) gives the corresponding i'th parameter
        
        See also:
            trace_parameter,trace_value,trace_size
        """
    @property
    def trace_size(self) -> int:
        """
        int: returns the size of the parameter-trace
        
        See also:
            trace_goal_function_value,trace_parameter
        """
    @property
    def warn_size(self) -> int:
        """
        int: returns the size of the warning messages
        
        See also:
            trace_goal_function_value,trace_parameter
        """
class RPMGSKParameter:
    """
    Contains the parameters to the methods used in the RPMGSK assembly
    radiation, penman_monteith, gamma_snow,actual_evapotranspiration,precipitation_correction,kirchner
    """
    __hash__: typing.ClassVar[None] = None
    map_t = RPMGSKParameterMap
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @staticmethod
    def deserialize(blob: shyft.time_series.ByteVector) -> RPMGSKParameter:
        ...
    def __eq__(self, arg0: RPMGSKParameter) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, p: RPMGSKParameter) -> None:
        """
        clone a parameter
        """
    @typing.overload
    def __init__(self, rad: shyft.hydrology.RadiationParameter, pm: shyft.hydrology.PenmanMonteithParameter, gs: shyft.hydrology.GammaSnowParameter, ae: shyft.hydrology.ActualEvapotranspirationParameter, k: shyft.hydrology.KirchnerParameter, p_corr: shyft.hydrology.PrecipitationCorrectionParameter, gm: shyft.hydrology.GlacierMeltParameter = ..., routing: shyft.hydrology.UHGParameter = ..., msp: shyft.hydrology.MethodStackParameter = ...) -> None:
        ...
    def __ne__(self, arg0: RPMGSKParameter) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get(self, i: int) -> float:
        """
        return the value of the i'th parameter, name given by .get_name(i)
        """
    def get_name(self, i: int) -> str:
        """
        returns the i'th parameter name, see also .get()/.set() and .size()
        """
    def serialize(self) -> shyft.time_series.ByteVector:
        """
        serializes the parameters to a blob, that later can be passed in to .deserialize()
        """
    def set(self, p: list[float]) -> None:
        """
        set parameters from vector/list of float, ordered as by get_name(i)
        """
    def size(self) -> int:
        """
        returns total number of calibration parameters
        """
    @property
    def ae(self) -> shyft.hydrology.ActualEvapotranspirationParameter:
        """
        ActualEvapotranspirationParameter: actual evapotranspiration parameter
        """
    @ae.setter
    def ae(self, arg0: shyft.hydrology.ActualEvapotranspirationParameter) -> None:
        ...
    @property
    def gm(self) -> shyft.hydrology.GlacierMeltParameter:
        """
        GlacierMeltParameter: glacier melt parameter
        """
    @gm.setter
    def gm(self, arg0: shyft.hydrology.GlacierMeltParameter) -> None:
        ...
    @property
    def gs(self) -> shyft.hydrology.GammaSnowParameter:
        """
        GammaSnowParameter: gamma-snow parameter
        """
    @gs.setter
    def gs(self, arg0: shyft.hydrology.GammaSnowParameter) -> None:
        ...
    @property
    def kirchner(self) -> shyft.hydrology.KirchnerParameter:
        """
        KirchnerParameter: kirchner parameter
        """
    @kirchner.setter
    def kirchner(self, arg0: shyft.hydrology.KirchnerParameter) -> None:
        ...
    @property
    def msp(self) -> shyft.hydrology.MethodStackParameter:
        """
        MethodStackParameter: contains the method stack parameters
        """
    @msp.setter
    def msp(self, arg0: shyft.hydrology.MethodStackParameter) -> None:
        ...
    @property
    def p_corr(self) -> shyft.hydrology.PrecipitationCorrectionParameter:
        """
        PrecipitationCorrectionParameter: precipitation correction parameter
        """
    @p_corr.setter
    def p_corr(self, arg0: shyft.hydrology.PrecipitationCorrectionParameter) -> None:
        ...
    @property
    def pm(self) -> shyft.hydrology.PenmanMonteithParameter:
        """
        PenmanMonteithParameter: penman_monteith parameter
        """
    @pm.setter
    def pm(self, arg0: shyft.hydrology.PenmanMonteithParameter) -> None:
        ...
    @property
    def rad(self) -> shyft.hydrology.RadiationParameter:
        """
        RadiationParameter: radiation parameter
        """
    @rad.setter
    def rad(self, arg0: shyft.hydrology.RadiationParameter) -> None:
        ...
    @property
    def routing(self) -> shyft.hydrology.UHGParameter:
        """
        UHGParameter: routing cell-to-river catchment specific parameters
        """
    @routing.setter
    def routing(self, arg0: shyft.hydrology.UHGParameter) -> None:
        ...
class RPMGSKParameterMap:
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
    def __eq__(self, arg0: RPMGSKParameterMap) -> bool:
        ...
    def __getitem__(self, arg0: int) -> RPMGSKParameter:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: RPMGSKParameterMap) -> None:
        """
        CopyConstructor
        """
    def __iter__(self) -> typing.Iterator[int]:
        ...
    def __len__(self) -> int:
        ...
    def __neq__(self, arg0: RPMGSKParameterMap) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setitem__(self, arg0: int, arg1: RPMGSKParameter) -> None:
        ...
    def __str__(self) -> str:
        ...
    def get(self, key: int, default: RPMGSKParameter | None = None) -> RPMGSKParameter | None:
        """
        Return the value for key if key is in the dictionary, else default.
        """
    def items(self) -> shyft.hydrology.r_pt_gs_k.ItemsView:
        ...
    def keys(self) -> shyft.hydrology.r_pt_gs_k.KeysView:
        ...
    def values(self) -> shyft.hydrology.r_pt_gs_k.ValuesView:
        ...
class RPMGSKResponse:
    """
    This struct contains the responses of the methods used in the RPMGSK assembly
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def ae(self) -> shyft.hydrology.ActualEvapotranspirationResponse:
        """
        ActualEvapotranspirationResponse: actual evapotranspiration response
        """
    @ae.setter
    def ae(self, arg0: shyft.hydrology.ActualEvapotranspirationResponse) -> None:
        ...
    @property
    def gm_melt_m3s(self) -> float:
        """
        float: glacier melt response[m3s]
        """
    @gm_melt_m3s.setter
    def gm_melt_m3s(self, arg0: float) -> None:
        ...
    @property
    def gs(self) -> shyft.hydrology.GammaSnowResponse:
        """
        GammaSnowResponse: gamma-snnow response
        """
    @gs.setter
    def gs(self, arg0: shyft.hydrology.GammaSnowResponse) -> None:
        ...
    @property
    def kirchner(self) -> shyft.hydrology.KirchnerResponse:
        """
        KirchnerResponse: kirchner response
        """
    @kirchner.setter
    def kirchner(self, arg0: shyft.hydrology.KirchnerResponse) -> None:
        ...
    @property
    def pm(self) -> shyft.hydrology.PenmanMonteithResponse:
        """
        PenmanMonteithResponse: penman_monteith response
        """
    @pm.setter
    def pm(self, arg0: shyft.hydrology.PenmanMonteithResponse) -> None:
        ...
    @property
    def rad(self) -> shyft.hydrology.RadiationResponse:
        """
        RadiationResponse: radiation response
        """
    @rad.setter
    def rad(self, arg0: shyft.hydrology.RadiationResponse) -> None:
        ...
    @property
    def total_discharge(self) -> float:
        """
        float: total stack response
        """
    @total_discharge.setter
    def total_discharge(self, arg0: float) -> None:
        ...
class RPMGSKState:
    vector_t = RPMGSKStateVector
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, gs: shyft.hydrology.GammaSnowState, k: shyft.hydrology.KirchnerState) -> None:
        ...
    @property
    def gs(self) -> shyft.hydrology.GammaSnowState:
        """
        GammSnowState: gamma-snow state
        """
    @gs.setter
    def gs(self, arg0: shyft.hydrology.GammaSnowState) -> None:
        ...
    @property
    def kirchner(self) -> shyft.hydrology.KirchnerState:
        """
        KirchnerState: kirchner state
        """
    @kirchner.setter
    def kirchner(self, arg0: shyft.hydrology.KirchnerState) -> None:
        ...
class RPMGSKStateVector:
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
    def __eq__(self, arg0: RPMGSKStateVector) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> RPMGSKStateVector:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> RPMGSKState:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: RPMGSKStateVector) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[RPMGSKState]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: RPMGSKStateVector) -> bool:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: RPMGSKState) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: RPMGSKStateVector) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: RPMGSKState) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    @typing.overload
    def extend(self, L: RPMGSKStateVector) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: RPMGSKState) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> RPMGSKState:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> RPMGSKState:
        """
        Remove and return the item at index ``i``
        """
    def size(self) -> int:
        ...
class RPMGSKStateWithId:
    """
    Keep the cell id and cell state
    """
    vector_t = RPMGSKStateWithIdVector
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @staticmethod
    def cell_state(geo_cell_data: shyft.hydrology.GeoCellData) -> shyft.hydrology.CellStateId:
        """
        create a cell state with id for the supplied cell.geo
        """
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, id: shyft.hydrology.CellStateId, state: RPMGSKState) -> None:
        """
        Creates a cell state with its characteristics cell-id
        
        Args:
            id (CellStateId): The cell characteristics id
        
            state (): The cell state (type safe)
        """
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    @property
    def id(self) -> shyft.hydrology.CellStateId:
        """
        int: the cell identifier for the state
        """
    @id.setter
    def id(self, arg0: shyft.hydrology.CellStateId) -> None:
        ...
    @property
    def state(self) -> RPMGSKState:
        """
        RPMGSKState: Cell-state
        """
    @state.setter
    def state(self, arg0: RPMGSKState) -> None:
        ...
class RPMGSKStateWithIdVector:
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
    def __eq__(self, arg0: RPMGSKStateWithIdVector) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> RPMGSKStateWithIdVector:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> RPMGSKStateWithId:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: RPMGSKStateWithIdVector) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[RPMGSKStateWithId]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: RPMGSKStateWithIdVector) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: RPMGSKStateWithId) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: RPMGSKStateWithIdVector) -> None:
        """
        Assign list elements using a slice object
        """
    def __str__(self) -> str:
        ...
    def append(self, x: RPMGSKStateWithId) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def deserialize_from_str(self: str) -> RPMGSKStateWithIdVector:
        ...
    @typing.overload
    def extend(self, L: RPMGSKStateWithIdVector) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: RPMGSKStateWithId) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> RPMGSKStateWithId:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> RPMGSKStateWithId:
        """
        Remove and return the item at index ``i``
        """
    def serialize_to_bytes(self) -> shyft.time_series.ByteVector:
        ...
    def serialize_to_str(self) -> str:
        ...
    def size(self) -> int:
        ...
    @property
    def state_vector(self) -> RPMGSKStateVector:
        ...
class StateCollector:
    """
    collects state, if collect_state flag is set to true
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def collect_state(self) -> bool:
        """
        if true, collect state, otherwise ignore (and the state of time-series are undefined/zero)
        """
    @collect_state.setter
    def collect_state(self, arg0: bool) -> None:
        ...
    @property
    def gs_acc_melt(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: acc melt
        """
    @property
    def gs_albedo(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: albedo
        """
    @property
    def gs_alpha(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: alpha
        """
    @property
    def gs_iso_pot_energy(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: iso pot energy
        """
    @property
    def gs_lwc(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: lwc
        """
    @property
    def gs_sdc_melt_mean(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: sdc melt mean
        """
    @property
    def gs_surface_heat(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: surface heat
        """
    @property
    def gs_temp_swe(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: temp swe
        """
    @property
    def kirchner_discharge(self) -> shyft.time_series.TsFixed:
        """
        TsFixed: Kirchner state instant Discharge given in m^3/s
        """
def create_full_model_clone(src_model: RPMGSKOptModel, with_catchment_params: bool = False) -> RPMGSKModel:
    """
    Clone a model to a another similar type model, full to opt-model or vice-versa
    The entire state except catchment-specific parameters, filter and result-series are cloned
    The returned model is ready to run_cells(), state and interpolated enviroment is identical to the clone source
    
    Args:
        src_model (XXXX?Model): The model to be cloned, with state interpolation done, etc
    
        with_catchment_params (bool): default false, if true also copy catchment specific parameters
    
    Returns:
        XXXX?Model: new_model. new_model ready to run_cells, or to put into the calibrator/optimizer
    """
def create_opt_model_clone(src_model: RPMGSKModel, with_catchment_params: bool = False) -> RPMGSKOptModel:
    """
    Clone a model to a another similar type model, full to opt-model or vice-versa
    The entire state except catchment-specific parameters, filter and result-series are cloned
    The returned model is ready to run_cells(), state and interpolated enviroment is identical to the clone source
    
    Args:
        src_model (XXXX?Model): The model to be cloned, with state interpolation done, etc
    
        with_catchment_params (bool): default false, if true also copy catchment specific parameters
    
    Returns:
        XXXX?Model: new_model. new_model ready to run_cells, or to put into the calibrator/optimizer
    """
def deserialize(bytes: shyft.time_series.ByteVector, states: RPMGSKStateWithIdVector) -> None:
    """
    from a blob, fill in states
    """
def deserialize_from_bytes(bytes: shyft.time_series.ByteVector) -> RPMGSKStateWithIdVector:
    ...
def extract_state_vector(cell_state_id_vector: RPMGSKStateWithIdVector) -> RPMGSKStateVector:
    """
    Given a cell-state-with-id-vector, returns a pure state vector that can be inserted directly into region-model
    
    Args:
        cell_state_id_vector (xStateWithIdVector): a complete consistent with region-model vector, all states, as in cell-order
    
    Returns:
        XStateVector: cell_state_vector. a vector with cell-id removed, order preserved
    """
def serialize(states: RPMGSKStateWithIdVector) -> shyft.time_series.ByteVector:
    """
    make a blob out of the states
    """
def version() -> str:
    ...
