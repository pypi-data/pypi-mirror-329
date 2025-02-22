# This file is part of Shyft. Copyright 2015-2018 SiH, JFB, OS, YAS, Statkraft AS
# See file COPYING for more details **/
from os import path
import numpy as np

from ....time_series import (TimeAxis, UtcTimeVector, DtsClient, StringVector, GeoEvalArgs, time, GeoQuery, utctime_now)
from ....hydrology import (TemperatureSource, PrecipitationSource, RelHumSource, RadiationSource, WindSpeedSource, TemperatureSourceVector,
                           PrecipitationSourceVector, WindSpeedSourceVector, RelHumSourceVector, RadiationSourceVector)

from .. import interfaces


class CFERA5GdbDataRepositoryError(Exception):
    pass


class CFERA5GdbDataRepository(interfaces.GeoTsRepository):
    """
    Repository for geo located timeseries stored in netCDF files.

    """

    def __init__(self, epsg, port, padding=5000.):
        self.client = DtsClient(f'localhost:{port}')

        self.forcings = StringVector(
            ['temperature', 'precipitation', 'relative_humidity', 'shortwave_radiation', 'wind'])
        self.allow_subset = True  # allow_subset

        self.shyft_cs = f"+init=EPSG:{epsg}"

    def get_timeseries(self, input_source_types, utc_period, geo_location_criteria=None):
        """
        see interfaces.GeoTsRepository
        """

        return self._get_data_from_gdb(self.client)

    def _get_data_from_gdb(self, client):

        # Get the configuration from the server
        geos = client.get_geo_db_ts_info()  # get the configurations from  the server
        gdb = None
        gcc = None
        for geo in geos:
            if geo.name == 'era5-snowmip-fc':
                gdb = geo
            elif geo.name == 'era5-snowmip-cc':
                gcc = geo
        if not (gdb and gcc):
            raise RuntimeError('db-server must have gdb and gcc setup')
        # ta_t0 = TimeAxis(utc.time(2021, 7, 1), time(3600*6), 4*(10))
        # print(f'Read in all available forecast')  # {repr(ta_t0)}')
        #  this is only chunk of data
        # this is all data concatenated on the fly
        fc_cc_ea = GeoEvalArgs(geo_ts_db_id=gdb.name, variables=gdb.variables, ensembles=[0],
                                   time_axis=gdb.t0_time_axis,
                                   ts_dt=time(0),
                                   geo_range=GeoQuery(), concat=True, cc_dt0=time(0))
        t0 = utctime_now()
        cc0 = client.cache_stats
        geo_ts_matrix = client.geo_evaluate(eval_args=fc_cc_ea, use_cache=True, update_cache=True)
        cc1 = client.cache_stats

        self.shyft_cs = f"+init=EPSG:{gdb.grid.epsg}"

        #TODO: add bounding box to slice!

        varixs = []
        for variable in self.forcings:
            variable_ix = [s for s in gdb.variables].index(variable)
            varixs.append(variable_ix)

            # ['temperature', 'precipitation', 'relative_humidity', 'shortwave_radiation', 'wind']
        # ixs should be: 0, 1,                  2                   3                    4
        t_srs_all = []
        p_srs_all = []
        rh_srs_all = []
        sw_srs_all = []
        w_srs_all = []
        for grid_point in gdb.grid.points:
            geo_point = geo_ts_matrix.get_geo_point(0, 0, 0, grid_point)
            # print(f'Evaluating point at ({geo_point.x}, {geo_point.y}, {geo_point.z})')
            ts_var_t = geo_ts_matrix.get_ts(0, 0, 0, grid_point)
            ts_tmp = ts_var_t.min_max_check_linear_fill(v_min=-40, v_max=40)  # qac by internal tool
            ts_var_p = geo_ts_matrix.get_ts(0, 1, 0, grid_point)
            ts_prec = ts_var_p.min_max_check_linear_fill(v_min=-10, v_max=200)  # qac by internal tool
            ts_var_rh = geo_ts_matrix.get_ts(0, 2, 0, grid_point)
            ts_rh = ts_var_rh.min_max_check_linear_fill(v_min=0, v_max=1)  # qac by internal tool
            ts_var_sw = geo_ts_matrix.get_ts(0, 3, 0, grid_point)
            ts_sw = ts_var_sw.min_max_check_linear_fill(v_min=0, v_max=1300)  # qac by internal tool
            ts_var_w = geo_ts_matrix.get_ts(0, 4, 0, grid_point)
            ts_ws = ts_var_w.min_max_check_linear_fill(v_min=-20, v_max=20)  # qac by internal tool
            # print(f'Time-series of temperature at point: {repr(ts_var_t.time_axis)} {str(ts_var_t.v)}')
            #print(f'Time-series of temperature at point: {repr(ts_var_t.time_axis)} {str(ts_var_t.v)}')

            # print(f"Read data={utctime_now() - t0}, id_count={cc1.id_count} hits-delta={cc1.hits - cc0.hits} misses-delta={cc1.misses - cc0.misses}")
            # t_srs_all.append(api.TemperatureSource(geo_point, ts_var_t))
            # p_srs_all.append(api.PrecipitationSource(geo_point, ts_var_p))
            # rh_srs_all.append(api.RelHumSource(geo_point, ts_var_rh))
            # sw_srs_all.append(api.RadiationSource(geo_point, ts_var_sw))
            # w_srs_all.append(api.WindSpeedSource(geo_point, ts_var_w))
            t_srs_all.append(TemperatureSource(geo_point, ts_tmp))
            p_srs_all.append(PrecipitationSource(geo_point, ts_prec))
            rh_srs_all.append(RelHumSource(geo_point, ts_rh))
            sw_srs_all.append(RadiationSource(geo_point, ts_sw))
            w_srs_all.append(WindSpeedSource(geo_point, ts_ws))


        t_srs_vec = TemperatureSourceVector(t_srs_all)
        p_srs_vec = PrecipitationSourceVector(p_srs_all)
        ws_srs_vec = WindSpeedSourceVector(w_srs_all)
        rh_srs_vec = RelHumSourceVector(rh_srs_all)
        r_srs_vec = RadiationSourceVector(sw_srs_all)

        sources = {"temperature": t_srs_vec,
                   "precipitation": p_srs_vec,
                   "wind_speed": ws_srs_vec,
                   "relative_humidity": rh_srs_vec,
                   "radiation":r_srs_vec}


        return sources

