from typing import List, Tuple
import shyft.time_series as sa
from shyft.dashboard.time_series.state import Quantity, State, Unit
from shyft.dashboard.time_series.sources.ts_adapter import TsAdapter


def check_dtss_url(host_port: str) -> bool:
    """
    This function evaluates if the url belogns to a running dts server
    Parameters
    ----------
    host_port:
        url of dtss like localhost:20000

    Returns
    -------
    True if dtss reachable with given url, False if not
    """
    dtsc = sa.DtsClient(host_port)
    try:
        dtsc.reopen()
    except RuntimeError as e:
        return False
    finally:
        dtsc.close()
    return True


def try_dtss_connection(host_port: str) -> bool:
    """
    This function evaluates if the url belogs to a running dts server
    Parameters
    ----------
    host_port:
        url of dtss like localhost:20000

    Returns
    -------
    True if dtss reachable with given url

    Raises
    ------
    RuntimeError if no dtss can be found under given url
    """
    dtsc = sa.DtsClient(host_port)
    try:
        dtsc.reopen()
    finally:
        dtsc.close()
    return True


def detect_unit_of(url: str) -> str:
    """ Just a helper to illustrate multiple axis based on unit """
    if 'charge' in url: return 'm**3/s'
    if 'emperature' in url: return 'degC'
    if 'recip' in url: return 'mm/h'
    if 'speed' in url: return 'm/s'
    if 'swe' in url: return 'mm'
    return ''


def find_all_ts_names_and_url(*, host_port: str, container: str, pattern: str) -> List[Tuple[str, str]]:
    """
    This function returns a list of time series names and urls for each Time Series in the container of the
    dtss at the ts_url.

    Parameters
    ----------
    host_port:
        host_port to dtss
    container:
        dtss data container to search in
    pattern:
        what time-series to match, regular expression

    Returns
    -------
    List of Tuple with (ts_url, name) for each ts in the container

    Raises
    ------
    RuntimeError if no dtss can be found under given url
    """
    dtsc = sa.DtsClient(host_port)
    try:
        ts_infos = dtsc.find(sa.shyft_url(container, pattern))
    finally:
        dtsc.close()
    return [(sa.shyft_url(container, ti.name), f'{ti.name}:{ti.data_period}/{ti.delta_t}') for ti in ts_infos]


class DtssTsAdapter(TsAdapter):
    """
    A very primitive synchronous dtss adapter to keep it simple
    """

    def __init__(self, dtss_url: str, ts_url: str, unit: str = "") -> None:
        super().__init__()
        self.unit = unit if unit else detect_unit_of(dtss_url)
        self.dtsc = sa.DtsClient(dtss_url)
        self.tsv_request = sa.TsVector([sa.TimeSeries(ts_url)])

    def __call__(self, *, time_axis: sa.TimeAxis, unit: Unit) -> Quantity[sa.TsVector]:
        try:
            tsv = self.dtsc.evaluate(self.tsv_request.average(time_axis), time_axis.total_period())
        except RuntimeError as e:
            return sa.TsVector()
        finally:
            self.dtsc.close()
        # TODO compute from src unit to unit using pint.
        return State.Quantity(tsv, self.unit)
