from typing import Optional, Dict, Any
from concurrent.futures import ThreadPoolExecutor
import bokeh
import bokeh.layouts
import bokeh.models

import shyft.time_series as sa

from shyft.dashboard.time_series.axes import YAxis, YAxisSide

from shyft.dashboard.time_series.ds_view_handle_registry import DsViewHandleRegistryApp
from shyft.dashboard.time_series.renderer import LineRenderer
from shyft.dashboard.time_series.state import State
from shyft.dashboard.time_series.tools.figure_tools import ResetYRange, WheelZoomDirection, \
    HoverToolToggleDropdown
from shyft.dashboard.time_series.tools.ts_viewer_tools import ResetTool
from shyft.dashboard.time_series.view_container.figure import Figure

from shyft.dashboard.time_series.ts_viewer import TsViewer

from shyft.dashboard.base.selector_presenter import SelectorPresenter
from shyft.dashboard.base.selector_views import FilterMultiSelect

from shyft.dashboard.base.app import AppBase
from shyft.dashboard.apps.dtss_viewer.widgets import (ContainerPathReceiver,
                                                      TsSelector, TsViewDemo)

from shyft.dashboard.base.ports import connect_ports
from shyft.dashboard.time_series.view_container.table import Table
from shyft.dashboard.widgets.logger_box import LoggerBox
from shyft.dashboard.widgets.message_viewer import MessageViewer

from shyft.dashboard.time_series.tools.figure_tools import HoverTool


class DtssViewerApp(AppBase):

    def __init__(self, thread_pool: Optional[ThreadPoolExecutor] = None,
                 app_kwargs: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(thread_pool=thread_pool)
        a = app_kwargs or {}
        self.default_host: str = a.get('dtss_host', 'localhost')
        self.default_port: int = a.get('dtss_port', 20000)
        self.default_container: str = a.get('dtss_container', 'test')

    @property
    def name(self) -> str:
        """
        This property returns the name of the app
        """
        return "DTSS Viewer App"

    def get_layout(self, doc: 'bokeh.document.Document', logger: Optional[LoggerBox] = None) -> bokeh.models.LayoutDOM:
        """
        This function returns the full page layout for the app
        """
        std_width = 800
        doc.title = self.name
        event_messenger = MessageViewer(title='Log:', rows=6, width=std_width, height=100, title_hight=15,
                                        show_time=True, time_zone='Europe/Oslo')

        container_path_input = ContainerPathReceiver(dtss_host=self.default_host, dtss_port=self.default_port,dtss_container=self.default_container)
        multi_select_view = FilterMultiSelect(title='Time Series in DTSS', height=200, width=std_width, size=40,
                                              padding=20)
        multi_select_presenter = SelectorPresenter(name='Ts', view=multi_select_view)
        ts_selector = TsSelector(multi_select_presenter)
        utc = sa.Calendar()
        time_range = sa.UtcPeriod(utc.time(2000, 1, 1), utc.time(2024, 1, 1))

        time_step_restrictions = [sa.Calendar.HOUR, sa.Calendar.HOUR * 3, sa.Calendar.DAY, sa.Calendar.WEEK,
                                  sa.Calendar.MONTH, sa.Calendar.QUARTER, sa.Calendar.YEAR]

        reset_tool = ResetTool(logger=logger)
        reset_y_range_tool = ResetYRange(logger=logger)

        wheel_zoom = WheelZoomDirection(logger=logger)
        ts_viewer = TsViewer(bokeh_document=doc,
                             title="Ts Viewer", padding=10, height=50,
                             unit_registry=State.unit_registry,
                             thread_pool_executor=self.thread_pool,
                             tools=[reset_tool],
                             init_view_range=time_range,
                             time_step_restrictions=time_step_restrictions,
                             reset_time_axis=False
                             )
        # TODO rather use auto axis when adding time-series
        ax_any = YAxis(label="any", unit='', side=YAxisSide.LEFT)
        ax_mmh = YAxis(label="precipitation", unit='mm/h', side=YAxisSide.RIGHT)
        ax_m3s = YAxis(label="flow", unit='m**3/s', side=YAxisSide.LEFT, color='green')
        ax_tmp = YAxis(label="temperature", unit='degC', side=YAxisSide.RIGHT, color='magenta')
        ax_swe = YAxis(label="swe", unit='mm', side=YAxisSide.RIGHT, color='blue')
        hover = HoverTool(
            point_policy='follow_mouse',
            tooltips=[("label", "@label"), ("value", "$y"), ("time", "$x{%d-%m-%Y %H:%M}")],
            formatters={'$x': 'datetime'}
        )
        hover_tool_toggle = HoverToolToggleDropdown([hover])

        fig = Figure(viewer=ts_viewer,
                     width=std_width, height=600,
                     init_renderers={LineRenderer: 6},
                     tools=[reset_y_range_tool, wheel_zoom, hover]
                     , y_axes=[ax_any, ax_mmh, ax_m3s, ax_swe, ax_tmp]
                     )
        table1 = Table(viewer=ts_viewer, width=std_width, height=400)
        ts_view = TsViewDemo(figure=fig, table=table1)
        dsviewhandle_registry = DsViewHandleRegistryApp()

        connect_ports(container_path_input.send_event_message, event_messenger.receive_message)
        connect_ports(ts_selector.send_event_message, event_messenger.receive_message)
        connect_ports(ts_view.send_event_message, event_messenger.receive_message)

        connect_ports(container_path_input.send_dtss_url, ts_selector.receive_url)
        connect_ports(container_path_input.send_shyft_container, ts_selector.receive_container)
        connect_ports(container_path_input.send_pattern, ts_selector.receive_pattern)
        connect_ports(container_path_input.send_dtss_url, ts_view.receive_dtss_url)
        connect_ports(ts_selector.send_selected_time_series, ts_view.receive_time_series)

        connect_ports(ts_view.send_selected, dsviewhandle_registry.receive_ds_view_handles_to_register)
        connect_ports(dsviewhandle_registry.send_ds_view_handles_to_add, ts_viewer.receive_ds_view_handles_to_add)
        connect_ports(dsviewhandle_registry.send_ds_view_handles_to_remove, ts_viewer.receive_ds_view_handles_to_remove)

        # ensure we get a flying start sending suitable start values to the container
        container_path_input.send_dtss_url(f'{self.default_host}:{self.default_port}')
        container_path_input.send_shyft_container(self.default_container)
        sizing_mode="stretch_width"
        return bokeh.layouts.column(bokeh.layouts.row(event_messenger.layout, sizing_mode=sizing_mode),
                                    bokeh.layouts.row(
                                        bokeh.layouts.column(
                                            bokeh.layouts.row(container_path_input.layout_components["widgets"][0],
                                                              container_path_input.layout_components["widgets"][1],
                                                              container_path_input.layout_components["widgets"][2]
                                                              ),
                                            multi_select_view.layout_components['widgets'][1],
                                            bokeh.layouts.row(dsviewhandle_registry.layout_components['widgets'][1],
                                                              dsviewhandle_registry.layout_components['widgets'][0]
                                                              )

                                        ), sizing_mode=sizing_mode
                                    ),
                                    bokeh.layouts.row(
                                        bokeh.layouts.column(
                                            bokeh.layouts.row(
                                                ts_viewer.layout_components['widgets'],
                                                reset_y_range_tool.layout,
                                                wheel_zoom.layout,
                                                reset_tool.layout,
                                                hover_tool_toggle.layout
                                             , sizing_mode=sizing_mode
                                            ),
                                            fig.layout,
                                            table1.layout)
                                        , sizing_mode=sizing_mode
                                    )
                                    )
