from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable

from pyproj import CRS
from netCDF4 import Dataset, Variable
import numpy as np
from pathlib import Path

from shyft.hydrology import parse_cf_time
from shyft.hydrology.repository.netcdf.concat_utils import ConcatSourceVariables, HeightVariable, WindSpeedSources, \
    SourceMethods

from shyft.time_series import (DtsClient, GeoGridSpec, GeoTimeSeriesConfiguration, GeoPointVector, GeoPoint, TimeAxis,
                               GeoSlice, POINT_AVERAGE_VALUE, create_ts_vector_from_np_array, GeoMatrix, Calendar, time,
                               UtcPeriod, POINT_INSTANT_VALUE, point_interpretation_policy)


@dataclass
class EnsembleDimension:
    """
    Holds the parameters for the ensemble dimension
    """
    dimension_name: str | None
    n_ensembles: int = 1


class EnsembleParser(ABC):
    def __init__(self, file_path: Path):
        """
        Base class for parsing the dimension parameters of ensembles in concat files

        Args:
            file_path: the file to parse
        """
        self.file_path = file_path

    @abstractmethod
    def get(self) -> EnsembleDimension:
        """
        Parse execution method

        Returns:

        """
        raise NotImplementedError(f'Method not implemented')


class DimensionEnsembleParser(EnsembleParser):
    def __init__(self, file_path: Path, dimension_name: str):
        """
        Parse the ensemble dimension as a dataset dimension. If the dimension does not exist, this is reflected in the
        returned object instead of raising an error.

        Args:
            file_path: file to parse
            dimension_name: name of the dataset dimension representing ensembles
        """
        super().__init__(file_path)
        self.dimension_name = dimension_name

    def get(self) -> EnsembleDimension:
        with Dataset(self.file_path) as dataset:
            if self.dimension_name in dataset.dimensions:
                return EnsembleDimension(self.dimension_name, dataset.dimensions[self.dimension_name].size)
        return EnsembleDimension(None, 1)


class EpsgParser(ABC):
    def __init__(self, file_path: Path):
        """
        Base class for parsing EPSG code in concat files

        Args:
            file_path: the file that is parsed
        """
        self.file_path = file_path

    @abstractmethod
    def get(self) -> int:
        """
        Parse execution method

        Returns:

        """
        raise NotImplementedError(f'Method not implemented')


class ConcatVariableError(Exception):
    """
    Error raised if a variable name is not found as a variable in the NetCDF
    """
    pass


class CRSVariableEpsgParser(EpsgParser):
    def __init__(self, file_path: Path, variable_name: str | None, attribute_name: str):
        """
        Parse dataset variable with string attribute using pyproj CRS, and convert to EPSG. The variable name can be set
        to None to go through all variables, but the attribute name must be set

        Args:
            file_path:
            variable_name:
            attribute_name:
        """
        super().__init__(file_path)
        self.variable_name = variable_name
        self.attribute_name = attribute_name
        self.validate()

    def validate(self):
        if not self.attribute_name:
            raise RuntimeError(f'Attribute name not provided')
        with Dataset(self.file_path) as dataset:
            if self.variable_name is not None:
                if self.variable_name not in dataset.variables:
                    raise ConcatVariableError(f'Invalid variable name: {self.variable_name}')
                variable = [dataset.variables[self.variable_name]]
            else:
                variable = dataset.variables.values()
            for variable in variable:
                if self.attribute_name in variable.ncattrs():
                    if self.variable_name is None:
                        self.variable_name = variable.name
                    return
            raise RuntimeError(f'Attribute not found: {self.attribute_name}')

    def get(self) -> int:
        with Dataset(self.file_path) as dataset:
            variable = dataset.variables[self.variable_name]
            attribute_value = variable.getncattr(self.attribute_name)
            epsg = CRS(attribute_value).to_epsg()
            if not isinstance(epsg, int):
                raise RuntimeError(f'Unknown EPSG from projection: {attribute_value}')
            return epsg


class CoordinateEpsgParser(EpsgParser):
    def __init__(self, file_path: Path, latitude_variable: str = 'latitude', longitude_variable: str = 'longitude'):
        """
        Checks if the dataset can be handled with latitude and longitude, and returns the correct epsg for geographic
        coordinates.

        Args:
            file_path:
            latitude_variable:
            longitude_variable:
        """
        super().__init__(file_path)
        self.latitude_variable = latitude_variable
        self.longitude_variable = longitude_variable
        self.validate()

    def validate(self):
        with Dataset(self.file_path) as dataset:
            for variable_name in [self.latitude_variable, self.longitude_variable]:
                if variable_name not in dataset.variables:
                    raise RuntimeError(f'Invalid grid coordinate variable name: {variable_name}')

    def get(self) -> int:
        return 4326


@dataclass
class HeightDimension:
    """
    Holds the parameters for the height dimension
    """
    dimension_name: str | None
    heights: list[float] | None = None


class HeightParser(ABC):
    def __init__(self, file_path: Path):
        """
        Base class for parsing the height data dimension in netcdf files

        Args:
            file_path: the file to parse
        """
        self.file_path = file_path

    @abstractmethod
    def get(self) -> HeightDimension:
        """
        Parse execution method

        Returns:

        """
        raise NotImplementedError(f'Method not implemented')


class DimensionHeightParser(HeightParser):
    def __init__(self, file_path: Path, dimension_name: str):
        """
        Parse the height dimension as a dataset dimension. If the dimension does not exist, this is reflected in the
        returned object instead of raising an error.

        Args:
            file_path: file to parse
            dimension_name: name of the dataset dimension representing heights

        """
        super().__init__(file_path)
        self.dimension_name = dimension_name

    def get(self) -> HeightDimension:
        with Dataset(self.file_path) as dataset:
            if self.dimension_name in dataset.dimensions:
                if self.dimension_name in dataset.variables:
                    heights = [float(h) for h in dataset.variables[self.dimension_name]]
                    return HeightDimension(self.dimension_name, heights)
                return HeightDimension(self.dimension_name)
        return HeightDimension(None)


@dataclass
class GridDimension:
    """
    Holds the parameters for the grid dimension
    """
    grid_dimensions: dict[str, int]
    points: GeoPointVector


class GridParser(ABC):
    def __init__(self, file_path: Path):
        """
        Base class for parsing grid dimension in a file
        Args:
            file_path:
        """
        self.file_path = file_path

    @abstractmethod
    def get(self) -> GridDimension:
        """
        Execution method

        Returns:

        """
        raise NotImplementedError(f'Method not implemented')


class VariablesGridParser(GridParser):
    def __init__(self, file_path: Path, x_variable: str, y_variable: str, z_variable: str | None):
        """
        Parse variables for x and y (grid, coordinates etc) and z (height, altitude etc). Uses the dimension of the
        x and y variables to determine all grid points. Adds z-component if it is a valid dataset variable.

        Args:
            file_path:
            x_variable:
            y_variable:
            z_variable:
        """
        super().__init__(file_path)
        self.x_variable = x_variable
        self.y_variable = y_variable
        self.z_variable = z_variable
        self.validate()

    def validate(self):
        with Dataset(self.file_path) as dataset:
            if self.x_variable not in dataset.variables:
                raise RuntimeError(f'Unknown x grid variable: {self.x_variable}')
            if self.y_variable not in dataset.variables:
                raise RuntimeError(f'Unknown y grid variable: {self.y_variable}')

    def get(self) -> GridDimension:
        with Dataset(self.file_path) as dataset:
            grid_dimension_names = tuple()
            for grid_variable in [self.x_variable, self.y_variable]:
                for var_dimension in dataset.variables[grid_variable].dimensions:
                    if var_dimension not in grid_dimension_names:
                        grid_dimension_names = grid_dimension_names + (var_dimension, )
            grid_dimensions = {grid_dimension: dataset.dimensions[grid_dimension].size
                               for grid_dimension in grid_dimension_names}

            x_data = np.array(dataset.variables[self.x_variable]).astype(float)
            if x_data.shape != tuple(grid_dimensions.values()):
                x_data = np.array([x_data] * grid_dimensions[self.y_variable]).transpose()

            y_data = np.array(dataset.variables[self.y_variable]).astype(float)
            if y_data.shape != tuple(grid_dimensions.values()):
                y_data = np.array([y_data] * grid_dimensions[self.x_variable])

            if self.z_variable is not None and self.z_variable in dataset.variables:
                z_data = np.array(dataset.variables[self.z_variable]).astype(float)
            else:
                z_data = np.zeros(tuple(grid_dimensions.values()))

            n = np.prod(tuple(grid_dimensions.values()))
            grid_points = np.dstack((x_data, y_data, z_data)).reshape(int(n), 3)
            grid_points = GeoPointVector([GeoPoint(x, y, z) for (x, y, z) in grid_points])
        return GridDimension(grid_dimensions, grid_points)


@dataclass
class TimeAxisDimensions:
    time_axis_dimension_name: str
    start_time_variable_name: str | None
    time_axes: list[TimeAxis]


class TimeAxesParser(ABC):
    def __init__(self, file_path: Path):
        """
        Base class for parsing the two time axis dimensions in concat files

        Args:
            file_path:
        """
        self.file_path = file_path

    @abstractmethod
    def get(self) -> TimeAxisDimensions:
        """
        Execution method

        Returns:

        """
        raise NotImplementedError(f'Method not implemented')


class TimeAxesDimensions(TimeAxesParser):
    def __init__(self, file_path: Path, time_str_formatter: Callable[[str], str] | None = None):
        """
        Parsing the time axes dimensions. If concatenated data, all time axes are extracted. If all time-points in a
        time axis have equal spacing, it is converted to a fixed_dt time axis.

        Assumptions:
            The dataset has a dimension named 'time'
            The dataset may have a dimension called 'lead_time', which is then the data time axis. The 'time' dimension
                is then assumed to be the concatenation times. Otherwise, the dataset may have a dimension called
                'forecast_reference_time'. This is then assumed to be the concatenation times, and 'time' is the data
                time axis. If none of these applies, no concatenation time axes are found.
            The unit of the time dimensions represent the resolution of the time axis. The unit is either listed in the
                delta_t_units dictionary, or it can be parsed as a string. The time_str_formatter can be used to get the
                correct string formatting. The parser assumes time strings similar to this format:
                'seconds since 1970-01-01 00:00:00 +00:00'
            The last time step is equal to the next-to-last time step (includes the time period of the last data point)


        Args:
            file_path: file to parse
            time_str_formatter: optional function for formatting an invalid time string

        """
        super().__init__(file_path)
        self.time_str_formatter = time_str_formatter
        self.delta_t_units: dict[str, time] = {'hours': Calendar.HOUR}
        self.validate()

    def validate(self):
        with Dataset(self.file_path) as dataset:
            if 'time' not in dataset.dimensions:
                raise RuntimeError(f'Unknown names for time dimensions')

    def _parse_time_variable(self, time_var: Variable) -> list[time]:
        """
        Parsing one time variable by combining the variable values and unit to obtain the time points

        Args:
            time_var:

        Returns:

        """
        if time_var.units in self.delta_t_units.keys():
            t0 = time(float(time_var[0]))
            time_var_period = UtcPeriod(t0, t0 + self.delta_t_units[time_var.units])
        else:
            cf_time = time_var.units
            if self.time_str_formatter is not None:
                cf_time = self.time_str_formatter(cf_time)

            time_var_period = parse_cf_time(cf_time)
            if not time_var_period.valid():
                raise RuntimeError(f'File has invalid time format: {cf_time}')

        time_vals = [time_var[0]] if len(time_var.dimensions) == 0 else time_var[:]
        return [float(t) * time_var_period.timespan() + time_var_period.start for t in time_vals]

    def get_time_axes(self, time_axis_dimension_name: str, start_time_variable_name: str | None) -> list[TimeAxis]:
        """
        Parsing the time axis dimensions in the file by combining the time axis and the concatenation start times. The
        concatenation start times are used for time offset if there is no time offset in the data time axis.

        Args:
            time_axis_dimension_name:
            start_time_variable_name:

        Returns:

        """
        with Dataset(self.file_path) as dataset:
            time_stamps = self._parse_time_variable(dataset.variables[time_axis_dimension_name])
            if start_time_variable_name is not None:
                start_times = self._parse_time_variable(dataset.variables[start_time_variable_name])
            else:
                start_times = [time(0)]

            time_axes = []
            for start_time in start_times:
                timestamps = [t + start_time for t in time_stamps] if time_stamps[0] == time(0) else time_stamps
                last_dt = timestamps[-1] - timestamps[-2]
                if len(set(timestamps[i+1] - t for i, t in enumerate(timestamps[:-1]))) > 1:
                    time_axes.append(TimeAxis(timestamps + [timestamps[-1] + last_dt]))
                else:  # Fixed dt
                    time_axes.append(TimeAxis(timestamps[0], last_dt, len(timestamps)))
        return time_axes

    def get(self) -> TimeAxisDimensions:
        with Dataset(self.file_path) as dataset:
            if 'time' in dataset.dimensions and 'lead_time' in dataset.dimensions:
                time_axis_dimension_name = 'lead_time'
                start_time_variable_name = 'time'
            elif 'time' in dataset.dimensions and 'forecast_reference_time' in dataset.variables:
                time_axis_dimension_name = 'time'
                start_time_variable_name = 'forecast_reference_time'
            else:
                start_time_variable_name = None
                time_axis_dimension_name = 'time'
        time_axes = self.get_time_axes(time_axis_dimension_name, start_time_variable_name)
        return TimeAxisDimensions(time_axis_dimension_name, start_time_variable_name, time_axes)


@dataclass
class DataDimensions:
    """
    Data class representing the required dimensions of the data
    """
    epsg: int
    ensembles: EnsembleDimension
    height: HeightDimension
    grid: GridDimension
    time_axes: TimeAxisDimensions

    def get_ordered_dimensions(self) -> list[str]:
        """
        Get the variable dimension names in the correct order for parsing each variable as a numpy array. Since the
        dimension names are lost when transforming a Variable to a ndarray, this order is fixed. The first dimension
        refers to concatenation times, if the dimension exists. The second dimension is ensembles, if it exists. The
        next dimensions are the grid point dimensions, usually x and y, but this may also be one common dimension. The
        last dimension is the time axis dimension. The order matter here so that the data is correctly mapped in the
        data matrix.

        Returns:

        """
        parse_dim_order = []
        if self.time_axes.start_time_variable_name is not None:
            parse_dim_order.append(self.time_axes.start_time_variable_name)
        if self.ensembles.dimension_name is not None:
            parse_dim_order.append(self.ensembles.dimension_name)
        for grid_dim_name in self.grid.grid_dimensions.keys():
            parse_dim_order.append(grid_dim_name)
        if self.time_axes.time_axis_dimension_name is not None:
            parse_dim_order.append(self.time_axes.time_axis_dimension_name)
        return parse_dim_order


class DimensionParser(ABC):
    def __init__(self, epsg_parser: EpsgParser,
                 ensemble_parser: EnsembleParser,
                 height_parser: HeightParser,
                 grid_parser: GridParser,
                 time_exes_parser: TimeAxesParser):
        """
        Base class for retrieving the variable dimension setup

        Args:
            epsg_parser:
            ensemble_parser:
            height_parser:
            grid_parser:
            time_exes_parser:
        """
        self.epsg_parser = epsg_parser
        self.ensemble_parser = ensemble_parser
        self.height_parser = height_parser
        self.grid_parser = grid_parser
        self.time_axes_parser = time_exes_parser

    def get(self) -> DataDimensions:
        """
        Executes parsing of the variable dimensions

        Returns:

        """
        epsg = self.epsg_parser.get()
        ensembles = self.ensemble_parser.get()
        heights = self.height_parser.get()
        grid = self.grid_parser.get()
        time_axes = self.time_axes_parser.get()
        return DataDimensions(epsg, ensembles, heights, grid, time_axes)


class VariableParser(ABC):
    def __init__(self, file_path: Path):
        """
        Base class for extracting variable names and time series point interpretation type

        Args:
            file_path:
        """
        self.file_path = file_path

    @abstractmethod
    def get(self) -> dict[str, point_interpretation_policy]:
        raise NotImplementedError(f'Method not implemented')


class ConcatVariableParser(VariableParser):
    def __init__(self, file_path: Path, dimensions: DataDimensions, skip_variables: list[str] | None = None):
        """
        Implementation for variable parser matching the utility methods, aimed at creating source variables

        Args:
            file_path: file to parse
            dimensions:
            skip_variables:
        """
        super().__init__(file_path)
        self.dimensions = dimensions
        self.source_variables = ConcatSourceVariables()
        self.skip_variables = skip_variables or []

    def get(self) -> dict[str, point_interpretation_policy]:
        """
        Extracts variable names and units from the dataset, by verifying that the required dimensions are present. The
        variable names are then checked against the existing concat processing methods to verify that the unit is the
        same as the hardcoded unit, and the ts-type is extracted from a processing method where the variable is used.

        Returns:
            Dictionary of variable names and the point interpretation of the time series

        """
        required_dimensions = [self.dimensions.time_axes.time_axis_dimension_name] \
                              + list(self.dimensions.grid.grid_dimensions.keys())
        with Dataset(self.file_path) as dataset:
            variable_units = {k: v.units for k, v in dataset.variables.items() if
                              np.all([dim in v.dimensions for dim in required_dimensions])}

        source_methods = self.source_variables.get_methods(list(variable_units.keys()))
        ts_types = {}
        for variable, unit in variable_units.items():
            methods_match = [m for m in source_methods if variable in m.variable_names]
            if len(methods_match) > 0:
                source_variable = [v for v in methods_match[0].variables if v.name == variable][0]
                if unit.strip() != source_variable.unit.strip():
                    raise RuntimeError(f'Inconsistent unit of {variable}: {unit}: expected {source_variable.unit}')
                ts_types[variable] = methods_match[0].ts_type
            else:
                if variable not in self.skip_variables:
                    raise RuntimeError(f'Unknown source variable for variable: {variable}')
        return ts_types


class HeightVariableParser:
    def __init__(self, file_path: Path, dimensions: DataDimensions, variable_source_map: dict[str, type[SourceMethods]]):
        """
        Implementation splitting a variable into several according to extra height dimensions

        Args:
            file_path: file to parse
            dimensions:
            variable_source_map
        """
        self.file_path = file_path
        self.dimensions = dimensions
        self.variable_source_map = variable_source_map

    def get(self) -> list[HeightVariable]:
        """
        Finds all variables with height as a variable dimension and creates corresponding height variables for each
        height of the data variable

        Returns:
            Metadata for the height variables

        """
        if self.dimensions.height.heights is None:
            return []
        required_dimensions = [self.dimensions.time_axes.time_axis_dimension_name] \
                              + list(self.dimensions.grid.grid_dimensions.keys())
        height_variables = []
        with Dataset(self.file_path) as dataset:
            for k, v in dataset.variables.items():
                if np.all([dim in v.dimensions for dim in required_dimensions]) and \
                        self.dimensions.height.dimension_name in v.dimensions and k in self.variable_source_map.keys():
                    for ix, height in enumerate(self.dimensions.height.heights):
                        height_variables.append(self.variable_source_map[k].height_variable(k, ix, height))
        return height_variables


class HeightDependentVariableParser(VariableParser):
    def __init__(self, file_path: Path, dimensions: DataDimensions, height_variables: list[HeightVariable]):
        """
        Implementation for variable parser for source variables at different heights, f.ex wind speed at several height
        levels

        Args:
            file_path: file to parse
            dimensions:
            height_variables:
        """
        super().__init__(file_path)
        self.dimensions = dimensions
        self.height_variables = height_variables
        self.source_variables = ConcatSourceVariables()

    def get(self) -> dict[str, point_interpretation_policy]:
        """
        Extracts variable names and units from the dataset, by verifying that the required dimensions are present. The
        variable names are then checked against the existing concat processing methods to verify that the unit is the
        same as the hardcoded unit, and the ts-type is extracted from a processing method where the variable is used.

        Returns:
            Dictionary of variable names and the point interpretation of the time series

        """
        required_dimensions = [self.dimensions.time_axes.time_axis_dimension_name] \
                              + list(self.dimensions.grid.grid_dimensions.keys())
        variable_units = {}
        with Dataset(self.file_path) as dataset:
            for k, v in dataset.variables.items():
                if np.all([dim in v.dimensions for dim in required_dimensions]) and \
                        k != self.dimensions.time_axes.time_axis_dimension_name and \
                        self.dimensions.height.dimension_name not in v.dimensions:
                    variable_units[k] = v.units
        for height_var in self.height_variables:
            variable_units[height_var.height_variable_name] = height_var.unit

        source_methods = self.source_variables.get_methods(list(variable_units.keys()))
        ts_types = {}
        for variable, unit in variable_units.items():
            methods_match = [m for m in source_methods if variable in m.variable_names]
            if len(methods_match) > 0:
                source_variable = [v for v in methods_match[0].variables if v.name == variable][0]
                if unit.strip() != source_variable.unit.strip():
                    raise RuntimeError(f'Inconsistent unit of {variable}: {unit}: expected {source_variable.unit}')
                ts_types[variable] = methods_match[0].ts_type
            else:
                raise RuntimeError(f'Unknown source variable for variable: {variable}')
        return ts_types


class DataParser:
    def __init__(self, file_path: Path,
                 dimensions: DataDimensions,
                 variables: dict[str, point_interpretation_policy],
                 height_variables: list[HeightVariable] | None = None):
        """
        Base class for parsing the data for all variables with the given data dimensions

        Args:
            file_path: file to parse
            dimensions: data dimensions
            variables: dict with variable names and the type of time series point interpretation
            height_variables: variables with metadata for height mapping

        """
        self.file_path = file_path
        self.dimensions = dimensions
        self.variables = variables
        self.height_variable_dict = {hv.height_variable_name: hv for hv in height_variables or []}

    def _extract_variable_data(self, variable: str, **dim_kwargs) -> np.array:
        """
        Helper function for extracting data for one variable, with correct dimensions. Unused dimensions are removed and
        required dimensions are added. If there are extra dimension layers in the data, these can be assigned as keyword
        arguments.

        Args:
            variable: name of variable to be parsed
            **dim_kwargs: For extra dimensions in the data

        Returns:

        """
        dimension_order = self.dimensions.get_ordered_dimensions()
        with Dataset(self.file_path) as dataset:
            np_data = np.array(dataset.variables[variable]).astype(float)
            data_dims = dataset.variables[variable].dimensions
            if data_dims != tuple(dimension_order):
                unused_dims = list(set(data_dims).difference(dimension_order))
                np_data = np_data.transpose([data_dims.index(d) for d in unused_dims + dimension_order])
                for unused_dim in unused_dims:
                    np_data = np_data[dim_kwargs.get(str(unused_dim), 0)]

            if self.dimensions.time_axes.start_time_variable_name not in dimension_order:
                np_data = np.expand_dims(np_data, 0)
            if self.dimensions.ensembles.dimension_name not in dimension_order:
                np_data = np.expand_dims(np_data, 1)
        return np_data

    def get_geo_data(self, config_name: str,
                     description: str | None = None,
                     **kwargs) -> tuple[GeoTimeSeriesConfiguration, GeoMatrix]:
        """
        Creates the geo-objects to store to a dtss. Setting up the geo-configuration according to the metadata,
        dimensions and variables, creating the GeoMatrix from the data space and filling with data for each variable,
        concatenation time, ensemble and grid point. The order is optimized for speed when iterating over many grid
        points, as opposed to many variables, ensembles or concatenation times.

        Args:
            config_name: geo-dtss name
            description: description of the geo time series configuration
            **kwargs: Optional keys and arguments, used for setting unused dimensions in the variables

        Returns:

        """
        description = description or str(self.file_path)
        gdb = GeoTimeSeriesConfiguration(prefix='shyft://',
                                         name=config_name,
                                         description=description,
                                         grid=GeoGridSpec(epsg=self.dimensions.epsg, points=self.dimensions.grid.points),
                                         t0_times=[ta.time(0) for ta in self.dimensions.time_axes.time_axes],
                                         dt=self.dimensions.time_axes.time_axes[0].total_period().timespan(),
                                         n_ensembles=self.dimensions.ensembles.n_ensembles,
                                         variables=list(self.variables.keys()))

        g_slice = GeoSlice(v=[i for i in range(len(gdb.variables))], e=[i for i in range(gdb.n_ensembles)],
                           g=[gix for gix in range(len(gdb.grid.points))], t=gdb.t0_times, ts_dt=gdb.dt)
        fcm = gdb.create_ts_matrix(g_slice)

        for v in range(fcm.shape.n_v):
            variable_name = gdb.variables[v]
            if len(self.height_variable_dict) > 0:
                kwargs.update({self.dimensions.height.dimension_name: self.height_variable_dict[gdb.variables[v]].height_index})
                variable_name = self.height_variable_dict[gdb.variables[v]].data_variable_name
            np_data = self._extract_variable_data(variable_name, **kwargs)
            for t in range(fcm.shape.n_t0):
                time_axis = self.dimensions.time_axes.time_axes[t]
                for e in range(fcm.shape.n_e):
                    grid_data = np_data[t][e]
                    if not grid_data.shape == (len(self.dimensions.grid.points), len(time_axis)):
                        grid_data = grid_data.reshape(len(self.dimensions.grid.points), len(time_axis))  # 2D -> 1D
                    tsv = create_ts_vector_from_np_array(time_axis, grid_data, self.variables[gdb.variables[v]])

                    for g in range(fcm.shape.n_g):
                        fcm.set_ts(t, v, e, g, tsv[g])
        return gdb, fcm


class ConcatFileDimensionParser(DimensionParser):
    def __init__(self, file_path: Path):
        """
        Parsing the dimensions in a concatenated file.

        Assumptions:
            The grid variables are called 'x' and 'y', and 'z' if the third grid dimension exist
            The epsg is either provided by 'proj4' attribute of variable named 'crs', or use geographic coordinates
            The ensemble dimension is called 'ensemble_member' if it exists
            The height dimension is called 'height0' if it exists
            There has to be a time axis dimension named 'time'. If there is a 'lead_time' dimension, this is the data
                time axis and 'time' refers to the concatenation time axis. If there is a 'forecast_reference_time',
                this is the concatenation time axis and 'time' is the data time axis. Else, there is no concatenation
                time axis. See TimeAxesDimensions for more details.

        Args:
            file_path:
        """
        self.file_path = file_path
        grid_parser = VariablesGridParser(self.file_path, x_variable='x', y_variable='y', z_variable='z')
        try:
            epsg_parser = CRSVariableEpsgParser(self.file_path, variable_name='crs', attribute_name='proj4')
        except ConcatVariableError:
            epsg_parser = CoordinateEpsgParser(self.file_path, grid_parser.x_variable, grid_parser.y_variable)
        ensemble_parser = DimensionEnsembleParser(self.file_path, dimension_name='ensemble_member')
        height_parser = DimensionHeightParser(self.file_path, dimension_name='height0')
        time_axes_parser = TimeAxesDimensions(self.file_path, self.time_str_formatter)
        super().__init__(epsg_parser, ensemble_parser, height_parser, grid_parser, time_axes_parser)

    @staticmethod
    def time_str_formatter(cf_time: str) -> str:
        """
        Function for fixing the formatting of the time axis as a string. If the time string misses the minutes
        information in the time zone offset, the string is modified to include :00.

        Args:
            cf_time: timestamp as a string

        Returns:

        """
        if '+' in cf_time and len(cf_time.split('+')[-1]) > 0 and ':' not in cf_time.split('+')[-1]:
            cf_time = cf_time[:-2] + ':00'
        return cf_time


class ConcatDataParser(DataParser):
    def __init__(self, file_path: Path):
        """
        Data parser for netcdf with concatenated netcdf files, where there can be several time axes per point, variable
        and ensemble.

        The parser is aimed at replicating the parsing functionality of ConcatDataRepository, and is tested against some
        of the files provided in the Shyft_Data repository. The variables are required to be matched against the
        methods listed in concat_utils and the corresponding unit. The dimensions of the file is parsed using
        ConcatFileDimensionParser, see documentation for required setup. All variables, except the ones listed in
        skip_variables, are parsed.

        Args:
            file_path:

        """
        dimension_parser = ConcatFileDimensionParser(file_path)
        dimensions = dimension_parser.get()
        skip_variables = ['surface_geopotential']
        variable_parser = ConcatVariableParser(file_path, dimensions, skip_variables)
        variables = variable_parser.get()
        super().__init__(file_path, dimensions, variables)


class NewaFileDimensions(DimensionParser):
    def __init__(self, file_path: Path):
        """
        Parsing the dimensions in the file from NEWA.

        Assumptions:
            There is no ensembles in the file (or the dimension is called 'ensemble_member')
            The height dimension is named 'height'
            The grid is in geographic coordinates, so epsg = 4326
            The grid coordinates are variables named 'XLAT' and 'XLON'
            The time axis is at midnight UTC time
            The time stamps variable is named 'time'
            There is only one time axis per point, height and variable (no extra t0)


        Args:
            file_path:
        """
        self.file_path = file_path
        ensemble_parser = DimensionEnsembleParser(self.file_path, dimension_name='ensemble_member')
        height_parser = DimensionHeightParser(self.file_path, dimension_name='height')
        grid_parser = VariablesGridParser(self.file_path, x_variable='XLAT', y_variable='XLON', z_variable=None)
        epsg_parser = CoordinateEpsgParser(self.file_path, grid_parser.x_variable, grid_parser.y_variable)
        time_axes_parser = TimeAxesDimensions(self.file_path, self.time_str_formatter)
        super().__init__(epsg_parser, ensemble_parser, height_parser, grid_parser, time_axes_parser)

    @staticmethod
    def time_str_formatter(cf_time: str) -> str:
        """
        Function for fixing the formatting of the time axis as a string. If the time string only contain dates, but
        misses more detailed info of the time of the day, the time is assumed to be midnight, UTC, and the timestamp
        string is expanded with this time of day info

        Args:
            cf_time: timestamp as a string

        Returns:

        """
        if ':' not in cf_time:
            cf_time += ' 00:00:00 +00:00'
        return cf_time


class NewaDataParser(DataParser):
    def __init__(self, file_path: Path):
        """
        Data parser for netcdf files from NEWA; New European Wind Atlas (https://map.neweuropeanwindatlas.eu/). The
        parser has been suited for the meso-scale datasets, providing wind data time series at different elevations per
        location across Europe. The different dimensions of the file are assumed to be readable by NewaFileDimensions
        class, and the wind speed variable is assumed to be called 'WS'.

        Each set of wind speed data per elevation is extracted as its own variable defined by WindSpeedSources, so that
        the allowed heights are limited to the methods implemented in WindSpeedSources. Here, 10 m is mapped to variable
        named wind_speed, 50m is mapped to wind_speed_50m, 100m is mapped to wind_speed_100m, etc. If the height does
        not have a corresponding variable name, it will raise an error.


        Args:
            file_path:
        """
        dimension_parser = NewaFileDimensions(file_path)
        dimensions = dimension_parser.get()
        height_variable_parser = HeightVariableParser(file_path, dimensions, {'WS': WindSpeedSources})
        height_variables = height_variable_parser.get()
        variable_parser = HeightDependentVariableParser(file_path, dimensions, height_variables)
        variables = variable_parser.get()
        super().__init__(file_path, dimensions, variables, height_variables)


class ConcatGeoDtss:
    def __init__(self, file_path: Path, url: str, config_name: str, data_parser: DataParser | None = None):
        """
        Setup for connecting to a dtss and dumping the file content using the provided data parser. If not data parser
        is provided, the ConcatDataParser is used.

        Args:
            file_path: path to the file to parse
            url: url to the dtss
            config_name: name of the GeoTimeSeriesConfiguration
            data_parser: data parser for the file

        """
        self.file_path = file_path
        self.url = url
        self.config_name = config_name
        self.data_parser = data_parser

    def validate(self):
        """
        Verify that the file exists, and that the config name does not exist in the dtss
        """
        if not self.file_path.is_file():
            raise RuntimeError(f"Not a file: {self.file_path}")

        c = DtsClient(self.url)
        db_infos = c.get_geo_db_ts_info()
        c.close()
        db_infos = [db for db in db_infos if db.name == self.config_name]
        if db_infos:
            raise RuntimeError(f'Config already existing: {self.config_name}')

    def dump(self, description: str | None = None):
        """
        Validates and extracts the data by the data parser, or ConcatDataParser, and stores as a geo-dtss

        Args:
            description: description used for GeoTimeSeriesConfiguration object
        """
        self.validate()
        if self.data_parser is None:
            self.data_parser = ConcatDataParser(self.file_path)
        gdb, fcm = self.data_parser.get_geo_data(self.config_name, description)
        c = DtsClient(self.url)
        c.add_geo_ts_db(gdb)
        c.geo_store(gdb.name, fcm, False, False)
        c.close()
