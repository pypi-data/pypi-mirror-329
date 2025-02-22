import itertools
from typing import List, Optional
import bokeh.models
import bokeh.layouts
from bokeh.palettes import Category20c as Palette  # @UnresolvedImport

from shyft.dashboard.time_series.view_container.figure import Figure
from shyft.dashboard.time_series.view_container.table import Table
from shyft.dashboard.time_series.axes import YAxis, YAxisSide

from shyft.dashboard.base.ports import Receiver, Sender
from shyft.dashboard.base.app import update_value_factory, LayoutComponents
from shyft.dashboard.apps.dtss_viewer.dtsc_helper_functions import check_dtss_url, find_all_ts_names_and_url, \
    DtssTsAdapter, detect_unit_of
from shyft.dashboard.base.selector_model import SelectorModelBase, processing_wrapper
from shyft.dashboard.base.selector_presenter import SelectorPresenter
from shyft.dashboard.time_series.sources.source import DataSource
from shyft.dashboard.time_series.view import Line, TableView
from shyft.dashboard.time_series.ds_view_handle import DsViewHandle
from shyft.dashboard.time_series.state import State


class ContainerPathReceiver:

    def __init__(self, dtss_host: Optional[str] = '', dtss_port: Optional[int] = 20000,
                 dtss_container: Optional[str] = '') -> None:
        dtss_host: str = dtss_host or 'localhost'
        dtss_port: int = dtss_port or 20000
        dtss_container: str = dtss_container or 'test'
        self.send_event_message = Sender(parent=self, name="Container path event messenger", signal_type=str)
        self.send_dtss_url = Sender(parent=self, name="DTSS url sender", signal_type=str)
        self.send_shyft_container = Sender(parent=self, name="shyft container name sender", signal_type=str)
        self.send_pattern = Sender(parent=self, name="shyft pattern name sender", signal_type=str)

        default_url = f"{dtss_host}:{dtss_port}"
        self.dtss_url_text_input = bokeh.models.TextInput(title="DTSS url",
                                                          value=default_url,
                                                          placeholder=default_url,
                                                          width=150)
        self.shyft_container_text_input = bokeh.models.TextInput(title="Shyft container name",
                                                                 value=dtss_container,
                                                                 placeholder="test", width=150)
        self.shyft_ts_pattern_input = bokeh.models.TextInput(title="Ts reg.expr.",
                                                             value="change-me.*",
                                                             placeholder="reg expr", width=150)

        self.dtss_url_text_input.on_change('value', self.changed_value_dtss_url)
        self.shyft_container_text_input.on_change('value', self.changed_value_shyft_container)
        self.shyft_ts_pattern_input.on_change('value', self.changed_pattern)
        self.set_dtss_text = update_value_factory(self.dtss_url_text_input, 'value')
        self.set_shyft_container_text = update_value_factory(self.shyft_container_text_input, 'value')

        self._layout = bokeh.layouts.column(bokeh.layouts.row(self.dtss_url_text_input),
                                            bokeh.layouts.row(self.shyft_container_text_input),
                                            bokeh.layouts.row(self.shyft_ts_pattern_input), margin=(5, 5, 5, 5))

    @property
    def layout(self) -> bokeh.layouts.column:
        return self._layout

    @property
    def layout_components(self) -> LayoutComponents:
        return {'widgets': [self.dtss_url_text_input, self.shyft_container_text_input, self.shyft_ts_pattern_input],
                'figures': []}

    def changed_value_dtss_url(self, attr, old, new) -> None:
        if check_dtss_url(new):
            self.send_event_message(f"DTSSR: Received valid url: {new}")
            self.send_dtss_url(new)
            self.send_shyft_container(self.shyft_container_text_input.value)
        else:
            self.send_event_message(f"DTSSR: Invalid url: {new}")

    def changed_pattern(self, attr, old, new) -> None:
        if new:
            self.send_event_message(f"DTSSR: pattern changed {new}")
            self.send_pattern(new)
        else:
            self.send_event_message(f"DTSSR: Invalid pattern: {new}")

    def changed_value_shyft_container(self, attr, old, new) -> None:
        self.send_event_message(f"SCNR: Received shyft container name: {new}")
        self.send_shyft_container(new)


class TsSelector(SelectorModelBase):

    def __init__(self, presenter: SelectorPresenter) -> None:
        super().__init__(presenter=presenter)

        self.url = None
        self.container = None
        self.pattern = None
        self.ts_list = None

        self.send_event_message = Sender(parent=self, name="TS selector event messenger", signal_type=str)
        self.send_selected_time_series = Sender(parent=self, name="send_selected_time_series", signal_type=List[str])

        self.receive_url = Receiver(parent=self, name='receive url', func=self._receive_url, signal_type=str)
        self.receive_container = Receiver(parent=self, name='receive container', func=self._receive_container,
                                          signal_type=str)
        self.receive_pattern = Receiver(parent=self, name='receive pattern', func=self._receive_pattern,
                                        signal_type=str)

    def _receive_url(self, text: str) -> None:
        self.url = text
        if self.container and self.pattern:
            self.update_list()

    def _receive_container(self, text: str) -> None:
        self.container = text
        if self.url and self.pattern:
            self.update_list()

    def _receive_pattern(self, text: str) -> None:
        self.pattern = text
        if self.url and self.container:
            self.update_list()

    @processing_wrapper
    def get_options(self):
        try:
            return find_all_ts_names_and_url(host_port=self.url, container=self.container, pattern=self.pattern)
        except RuntimeError as e:
            self.send_event_message(f"TSS: could not retrieve data")
            return []

    def update_list(self):
        self.send_event_message(f"TSS: updating TS list")
        self.ts_list = self.get_options()
        self.presenter.set_selector_options(options=self.ts_list, callback=False,
                                            selected_value=["shyft://test/ts-0"],
                                            sort=True)

    def on_change_selected(self, selected_values: List[str]) -> None:
        self.send_event_message(f"TSS: received {len(selected_values)} Time Series")
        self.send_selected_time_series(selected_values)


class TsViewDemo:
    def __init__(self, figure: Figure, table: Table) -> None:
        self.figure: Figure = figure
        self.table: Table = table
        self.color_line = itertools.cycle(Palette[10])
        self.line_styles = itertools.cycle(['solid', 'dashed', 'dotted', 'dotdash', 'dashdot'])
        self.url_str = ''
        self.send_event_message = Sender(parent=self, name="TsView event messenger", signal_type=str)
        self.receive_dtss_url = Receiver(parent=self, name="send_selected_time_series", func=self._set_url,
                                         signal_type=str)
        self.view_handles = []
        self.receive_time_series = Receiver(parent=self, name="send_selected_time_series", func=self._add_time_series,
                                            signal_type=List[str])
        self.send_selected = Sender(parent=self, name="ts_selected", signal_type=List[DsViewHandle])

    def _set_url(self, url: str):
        self.url_str = url

    def find_y_axis_for_unit(self, unit: str) -> YAxis:
        self.send_event_message(f'Find axis for {unit}')
        for y in self.figure.y_axes:
            if y.unit == unit:
                self.send_event_message(f'Found y-axis for it')
                return y
        self.send_event_message("using default")
        return self.figure.default_y_axis

    def _add_time_series(self, ts_names: List[str]):

        self.view_handles = []
        self.send_event_message(f"Add time-series {ts_names}")
        if len(ts_names) != 1:
            raise RuntimeError(f'This demo only handles series one by one')
        ts_name = ts_names[0]
        unit = detect_unit_of(ts_name)
        self.send_event_message(f'unit of {ts_name} detected to "{unit}"')
        ts_adapter = DtssTsAdapter(self.url_str, ts_name, unit)
        ds = DataSource(ts_adapter=ts_adapter, unit=unit, tag=ts_name)
        view = Line(view_container=self.figure,
                    color=next(self.color_line),
                    label=ts_name,
                    unit=unit,
                    index=0,
                    line_width=0.7,
                    y_axis=self.find_y_axis_for_unit(unit)
                    )

        table_view = TableView(view_container=self.table, columns={0: '|'}, label=ts_name.split("/")[-1], unit=unit)
        view_handle = DsViewHandle(
            data_source=ds,
            views=[view, table_view],
            tag=ts_name,
            unit_registry=State.unit_registry
        )
        self.view_handles.append(view_handle)

        self.send_selected(self.view_handles)
