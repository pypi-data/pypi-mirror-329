from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import numpy as np

from shyft.hydrology import (TemperatureSource, TemperatureSourceVector, PrecipitationSource, PrecipitationSourceVector,
                             RadiationSource, RadiationSourceVector, WindSpeedSource, WindSpeedSourceVector,
                             RelHumSource, RelHumSourceVector)
from shyft.hydrology.repository.netcdf.utils import calculate_relative_humidity_tsv, calculate_pressure_tsv
from shyft.time_series import (TimeSeries, GeoPoint, POINT_INSTANT_VALUE, POINT_AVERAGE_VALUE, UtcPeriod, TimeAxisType,
                               derivative_method, Calendar, point_interpretation_policy)


HydrologySource = TemperatureSource | PrecipitationSource | RadiationSource | WindSpeedSource | RelHumSource
HydrologySourceVector = TemperatureSourceVector | PrecipitationSourceVector | RadiationSourceVector | \
                        WindSpeedSourceVector | RelHumSourceVector


@dataclass
class Variable:
    """
    Dataclass representing variables and the associated unit in the source database. time_series attribute is filled
    with the time series data for the variable, and is returned on call.
    """
    name: str
    unit: str
    time_series: TimeSeries = field(default_factory = TimeSeries)

    def get_timeseries(self) -> TimeSeries:
        """

        Returns: The time series of the variable

        """
        return self.time_series


class Method(ABC):
    def __init__(self, variables: list[Variable], source_input_name: str | None = None):
        """
        Base class for adding a processing method to one or several variables, and assigning a variable name. If no
        source input name is given, the first variable's name is used. A geo-point can also be assigned for
        location-specific processing. The method is applied to the variables on call.

        Args:
            variables: Required variables in the processing
            source_input_name: Name of the processed source variable
        """
        self.variables = variables
        self.source_input_name = source_input_name or self.variables[0].name
        self.geo_point: GeoPoint | None = None
        self.ts_type: point_interpretation_policy | None = None
        self.geo_ts: HydrologySource | None = None
        self.geo_tsv: HydrologySourceVector | None = None

    def set_geo_point(self, geo_point: GeoPoint):
        self.geo_point = geo_point

    def set_source(self, ts_type: point_interpretation_policy,
                   geo_ts: HydrologySource, geo_tsv: HydrologySourceVector):
        self.ts_type = ts_type
        self.geo_ts = geo_ts
        self.geo_tsv = geo_tsv

    @abstractmethod
    def get_timeseries(self) -> TimeSeries:
        """

        Returns: The processed time series

        """
        raise NotImplementedError

    @property
    def variable_names(self) -> list[str]:
        """
        Returns: Name of the variables for the processing method

        """
        return [v.name for v in self.variables]

    def create_source(self, clip_period: UtcPeriod | None = None) -> HydrologySource:
        """
        Create a hydrology geo-ts from the processed data, given by the geo-ts type. Requires that the geo-point and the
        source types has been set for the method. The time series can be clipped with the provided clip_period, which
        also requires that the time series can be evaluated.

        Args:
            clip_period: Clips the time series to the utc_period, if provided and within the data range

        Returns:

        """
        ts = self.get_timeseries()
        if self.geo_point is None:
            raise RuntimeError(f'Geo-point of method {self.source_input_name} not set')
        if self.ts_type is None:
            raise RuntimeError(f'Time series type of method {self.source_input_name} not set')
        if self.geo_ts is None:
            raise RuntimeError(f'Geo-ts source of method {self.source_input_name} not set')

        if not ts.needs_bind() and ts.point_interpretation() != self.ts_type:
            ts.set_point_interpretation(self.ts_type)

        if clip_period is not None:
            if ts.needs_bind():
                raise RuntimeError(f'Clipping is not possible with an unresolved time series')
            slice_period = clip_period.intersection(ts.total_period())
            slice_ix = ts.time_axis.index_of(slice_period.start)
            if ts.time_axis.timeaxis_type == TimeAxisType.FIXED:
                dt = ts.time_axis.fixed_dt.delta_t
                slice_n = int(slice_period.timespan() / dt)
            else:
                slice_end = ts.time_axis.index_of(slice_period.end)
                slice_n = slice_end - slice_ix

            pt_type_ext = int(self.ts_type == POINT_INSTANT_VALUE)
            if slice_ix > 0 or slice_ix + slice_n + pt_type_ext < len(ts):
                ts = ts.evaluate().slice(slice_ix, slice_n + pt_type_ext)

        return self.geo_ts(self.geo_point, ts)


class Get(Method):
    def __init__(self, variable: Variable, source_input_name: str | None = None):
        """
        Method to return variable data without any processing

        Args:
            variable:
            source_input_name:
        """
        super().__init__([variable], source_input_name)

    def get_timeseries(self) -> TimeSeries:
        return self.variables[0].get_timeseries()


class TemperatureShift(Method):
    def __init__(self, temp_variable: Variable, source_input_name: str | None = None):
        """
        Method to convert temperature from K to degrees Celsius

        Args:
            temp_variable:
            source_input_name:
        """
        if temp_variable.unit != 'K':
            raise RuntimeError(f'Unknown unit for converting to degrees: {temp_variable.unit}')
        super().__init__([temp_variable], source_input_name)
        self.zero_temperature = 273.15

    def get_timeseries(self) -> TimeSeries:
        return self.variables[0].get_timeseries() - self.zero_temperature


class PrecipitationDerivative(Method):
    def __init__(self, precip_variable: Variable, source_input_name: str | None = None):
        """
        Method to perform de-accumulation by derivation and scaling to obtain mm/hour from accumulated precipitation

        Args:
            precip_variable:
            source_input_name:
        """
        super().__init__([precip_variable], source_input_name)
        self.min_value = 0.
        self.max_value = 1000.

    def get_timeseries(self) -> TimeSeries:
        ts_derivative = self.variables[0].get_timeseries().derivative(derivative_method.FORWARD) * int(Calendar.HOUR)
        return ts_derivative.max(self.min_value).min(self.max_value)


class PrecipitationScale(Method):
    def __init__(self, precip_variable: Variable, source_input_name: str | None = None):
        """
        Method to perform scaling to obtain mm/hour from precipitation

        Args:
            precip_variable:
            source_input_name:
        """
        super().__init__([precip_variable], source_input_name)
        self.min_value = 0.
        self.max_value = 1000.

    def get_timeseries(self) -> TimeSeries:
        raise NotImplementedError(f'Untested solution, please verify suggestion below')
        # ta = self.variables[0].get_timeseries().time_axis
        # tsv = TsVector([self.variables[0]()])
        # if ta.timeaxis_type == TimeAxisType.FIXED:
        #     tsv_scaled = tsv * int(ta.fixed_dt.delta_t / Calendar.HOUR)
        # else:
        #     ta_hourly = TimeAxis(ta.time(0), Calendar.HOUR, int(ta.total_period().timespan() / Calendar.HOUR))
        #     tsv_scaled = tsv.average(ta_hourly)
        # return tsv_scaled[0].max(self.min_value).min(self.max_value)


class RadiationDerivative(Method):
    def __init__(self, radiation_variable: Variable, source_input_name: str | None = None):
        """
        Method to perform de-accumulation by derivation, to obtain radiation in W/m^2. One example is the variable
        integral_of_surface_downwelling_shortwave_flux_in_air_wrt_time

        Args:
            radiation_variable:
            source_input_name:
        """
        super().__init__([radiation_variable], source_input_name)
        self.min_value = 0.
        self.max_value = 5000.

    def get_timeseries(self) -> TimeSeries:
        tsv_derivative = self.variables[0].get_timeseries().derivative(derivative_method.FORWARD)
        return tsv_derivative.max(self.min_value).min(self.max_value)


class WindSpeed(Method):
    def __init__(self, x_var: Variable, y_var: Variable, source_input_name: str):
        """
        Method to calculate the wind speed from x- and y-components

        Args:
            x_var: variable for x-component
            y_var: variable for y_component
            source_input_name:
        """
        super().__init__([x_var, y_var], source_input_name)

    def get_timeseries(self) -> TimeSeries:
        return (self.variables[0].get_timeseries().pow(2.0) + self.variables[1].get_timeseries().pow(2.0)).pow(0.5)


class RelativeHumidity(Method):
    def __init__(self, temp_var: Variable, dew_temp_var: Variable, pressure_var: Variable, source_input_name: str):
        """
        Method to calculate relative humidity from temperature, dew temperature and pressure

        Args:
            temp_var:
            dew_temp_var:
            pressure_var:
            source_input_name:
        """
        super().__init__([temp_var, dew_temp_var, pressure_var], source_input_name)

    def get_timeseries(self) -> TimeSeries:
        return calculate_relative_humidity_tsv(self.variables[0].get_timeseries(),
                                               self.variables[1].get_timeseries(),
                                               self.variables[2].get_timeseries())


class RelativeHumiditySea(Method):
    def __init__(self, temp_var: Variable, dew_temp_var: Variable, pressure_var: Variable, source_input_name: str):
        """
        Method to calculate relative humidity from temperature, dew temperature and sea-level pressure. The pressure is
        calculated at the height of the geo-point, before calculating relative humidity.

        Args:
            temp_var:
            dew_temp_var:
            pressure_var:
            source_input_name:
        """
        super().__init__([temp_var, dew_temp_var, pressure_var], source_input_name)

    def get_timeseries(self) -> TimeSeries:
        if self.geo_point is None:
            raise RuntimeError(f'Geo point has not been set, cannot calculate pressure')
        pressure_ts_z = calculate_pressure_tsv([self.geo_point.z], [self.variables[2].get_timeseries()])[0]
        return calculate_relative_humidity_tsv(self.variables[0].get_timeseries(),
                                               self.variables[1].get_timeseries(),
                                               pressure_ts_z)


class HeightVariable:
    def __init__(self, data_variable_name: str, height_variable_name: str, height_index: int, unit: str):
        """
        Helper class when separating a data variable to several variables by different heights

        Args:
            data_variable_name:
            height_variable_name:
            height_index:
            unit:
        """
        self.data_variable_name = data_variable_name
        self.height_variable_name = height_variable_name
        self.height_index = height_index
        self.unit = unit


@dataclass
class SourceMethods:
    """
    Data class for keeping several methods associated with the same hydrology source geo-ts, hydrology source
    geo-ts-vector, and time series point interpretation. The methods are built up by hardcoded variables, which are
    matched up with the variable names of the input data.

    """
    methods: list[Method]
    source_point: HydrologySource
    source_vector: HydrologySourceVector
    ts_type: point_interpretation_policy

    def filter(self, all_variables: list[str]) -> list[Method]:
        """
        Returns all the methods that are available for the given variables

        Args:
            all_variables: list of data variables

        Returns:

        """
        methods = []
        for method in self.methods:
            if np.all([v.name in all_variables for v in method.variables]):
                method.set_source(self.ts_type, self.source_point, self.source_vector)
                methods.append(method)
        return methods

    @classmethod
    def height_variable(cls, variable_name: str, height_index: int, height: float) -> HeightVariable:
        raise NotImplementedError(f'Source method has no height-dependent variable splitting')


class TemperatureSources(SourceMethods):
    """
    Source methods for temperature variables
    """
    def __init__(self):
        methods = [Get(Variable('temperature', 'C')),
                   TemperatureShift(Variable('air_temperature_2m', 'K'), 'temperature'),
                   TemperatureShift(Variable('dew_point_temperature_2m', 'K'))]
        super().__init__(methods, TemperatureSource, TemperatureSourceVector, POINT_INSTANT_VALUE)


class PrecipitationSources(SourceMethods):
    """
    Source methods for precipitation variables
    """
    def __init__(self):
        methods = [Get(Variable('precipitation', 'mm/h')),
                   PrecipitationDerivative(Variable('precipitation_amount_acc', 'kg/m^2'), 'precipitation'),
                   PrecipitationScale(Variable('precipitation_amount', 'kg/m^2'), 'precipitation')]
        super().__init__(methods, PrecipitationSource, PrecipitationSourceVector, POINT_AVERAGE_VALUE)


class RadiationSources(SourceMethods):
    """
    Source methods for radiation variables
    """
    def __init__(self):
        methods = [Get(Variable('radiation', 'W/m^2')),
                   RadiationDerivative(Variable(
                       'integral_of_surface_downwelling_shortwave_flux_in_air_wrt_time', 'W s/m^2'), 'radiation')]
        super().__init__(methods, RadiationSource, RadiationSourceVector, POINT_AVERAGE_VALUE)


class WindSpeedSources(SourceMethods):
    """
    Source methods for wind speed variables
    """
    def __init__(self):
        methods = []
        for key in ['windspeed', 'wind_speed', 'windspeed_10m']:
            methods.append(Get(Variable(key, 'm/s'), 'wind_speed'))
        for key in ['windspeed_50m', 'wind_speed_50m']:
            methods.append(Get(Variable(key, 'm/s'), 'wind_speed_50m'))
        for key in ['windspeed_100m', 'wind_speed_100m']:
            methods.append(Get(Variable(key, 'm/s'), 'wind_speed_100m'))
        for key in ['x_wind', 'y_wind', 'x_wind_10m', 'y_wind_10m', 'x_wind_100m', 'y_wind_100m']:
            methods.append(Get(Variable(key, 'm/s')))

        methods.extend([WindSpeed(Variable('x_wind', 'm/s'), Variable('y_wind', 'm/s'), 'wind_speed'),
                        WindSpeed(Variable('x_wind_10m', 'm/s'), Variable('y_wind_10m', 'm/s'), 'wind_speed'),
                        WindSpeed(Variable('x_wind_100m', 'm/s'), Variable('y_wind_100m', 'm/s'), 'wind_speed_100m')])
        super().__init__(methods, WindSpeedSource, WindSpeedSourceVector, POINT_INSTANT_VALUE)

    @classmethod
    def height_variable(cls, variable_name: str, height_index: int, height: float) -> HeightVariable:
        height_variable_name = 'wind_speed' if int(height) == 10 else f'wind_speed_{int(height)}m'
        return HeightVariable(variable_name, height_variable_name, height_index, 'm/s')


class RelativeHumiditySources(SourceMethods):
    """
    Source methods for relative humidity variables
    """
    def __init__(self):
        methods = [Get(Variable('relative_humidity', '1'), 'relative_humidity'),
                   Get(Variable('relative_humidity_2m', '1'), 'relative_humidity'),
                   RelativeHumidity(Variable('air_temperature_2m', 'K'),
                                    Variable('dew_point_temperature_2m', 'K'),
                                    Variable('surface_air_pressure', 'Pa'), 'relative_humidity'),
                   RelativeHumiditySea(Variable('air_temperature_2m', 'K'),
                                       Variable('dew_point_temperature_2m', 'K'),
                                       Variable('sea_level_pressure', 'Pa'), 'relative_humidity')]
        super().__init__(methods, RelHumSource, RelHumSourceVector, POINT_INSTANT_VALUE)


class ConcatSourceVariables:
    def __init__(self):
        """
        Collection of all source methods available
        """
        self.temperature_sources = TemperatureSources()
        self.precipitation_sources = PrecipitationSources()
        self.radiation_sources = RadiationSources()
        self.wind_speed_sources = WindSpeedSources()
        self.relative_humidity_sources = RelativeHumiditySources()

    def get_methods(self, all_variables: list[str]) -> list[Method]:
        """
        Get all available source methods for the given variable names

        Args:
            all_variables: list of variable names

        Returns:

        """
        data_variables = []
        data_variables.extend(self.temperature_sources.filter(all_variables))
        data_variables.extend(self.precipitation_sources.filter(all_variables))
        data_variables.extend(self.radiation_sources.filter(all_variables))
        data_variables.extend(self.wind_speed_sources.filter(all_variables))
        data_variables.extend(self.relative_humidity_sources.filter(all_variables))
        return data_variables
