"""
Example of how to use Bokeh's range tool.

For this we need two figures showing the same data but with different
time periods - the main figure is zoomed in on the selected period and the second figure shows the full time
period.

This goes against the standard TsViewer usage and requires that 2 identical DataSources and TsViewers are created.

"""

from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Dict, Any

import bokeh
from bokeh.layouts import row, column
from bokeh.models import RangeTool

from shyft.dashboard.base.app import AppBase
from shyft.dashboard.examples.test_data_generator import ExampleTsAdapterSine
from shyft.dashboard.time_series.axes import YAxis, YAxisSide
from shyft.dashboard.time_series.axes_handler import DsViewTimeAxisType
from shyft.dashboard.time_series.ds_view_handle import DsViewHandle
from shyft.dashboard.time_series.sources.source import DataSource
from shyft.dashboard.time_series.state import State
from shyft.dashboard.time_series.ts_viewer import TsViewer
from shyft.dashboard.time_series.view import Line
from shyft.dashboard.time_series.view_container.figure import Figure
from shyft.dashboard.widgets.logger_box import LoggerBox
from shyft.time_series import UtcPeriod, Calendar


class RangeToolExample(AppBase):

    def __init__(self, thread_pool, app_kwargs: Optional[Dict[str, Any]] = None):
        super().__init__(thread_pool=thread_pool)
        self.logger = None

    @property
    def name(self) -> str:
        """
        This property returns the name of the app
        """
        return "range_tool_example"

    def get_layout(self, doc: bokeh.document.Document, logger: Optional[LoggerBox] = None) -> bokeh.layouts.LayoutDOM:
        """
        This function returns the full page layout for the app
        """
        # PRE RUNTIME
        doc.title = self.name
        figure_width = 800

        # Set up async thread pool
        async_on = True
        thread_pool_executor = ThreadPoolExecutor(5)  # self.thread_pool

        # Create our viewer1 app
        viewer1 = TsViewer(bokeh_document=doc, unit_registry=State.unit_registry,
                           tools=[],
                           time_step_restrictions=[Calendar.HOUR * 3, Calendar.DAY, Calendar.WEEK],
                           thread_pool_executor=thread_pool_executor, logger=logger)

        # Create our viewer2 app
        viewer2 = TsViewer(bokeh_document=doc, unit_registry=State.unit_registry,
                           tools=[],
                           time_step_restrictions=[Calendar.HOUR * 3, Calendar.DAY, Calendar.WEEK],
                           thread_pool_executor=thread_pool_executor, logger=logger)

        # Create view containers

        # set up additional y-axes
        ax1_fig1 = YAxis(label="left nonsens axes", unit='MW', side=YAxisSide.LEFT)
        # create first figure with all additional y-axes

        ''' Define the x range initially selected by the range tool '''
        select_start = -2376000000.0
        select_end = 2376000000.0
        fig1 = Figure(viewer=viewer1, tools=[],
                      width=figure_width, x_range=(select_start, select_end),
                      y_axes=[ax1_fig1], init_renderers={Line: 20}.items(),
                      logger=logger)

        # Initialise a data source
        time_range = UtcPeriod(-3600 * 24 * 100, 3600 * 24 * 100)
        example_data = ExampleTsAdapterSine(unit_to_decorate='MW', time_range=time_range, async_on=async_on)
        data_source = DataSource(ts_adapter=example_data,
                                 unit='MW', request_time_axis_type=DsViewTimeAxisType.padded_view_time_axis,
                                 time_range=time_range)

        data_source2 = DataSource(ts_adapter=example_data,
                                  unit='MW', request_time_axis_type=DsViewTimeAxisType.padded_view_time_axis,
                                  time_range=time_range)

        select = Figure(viewer=viewer2, tools=[],
                        height=130, width=800,
                        # y_range=p.y_range,
                        # y_axes=[ax1_fig1],
                        init_renderers={Line: 20}.items(),
                        logger=logger)

        # Initialise views

        # create line view
        line_view_select = Line(color='blue', unit='MW', label='select  line', visible=True, view_container=select,
                                index=1)

        # create line view
        line_view = Line(color='blue', unit='MW', label='test adapter line', visible=True, view_container=fig1, index=1,
                         y_axis=ax1_fig1)

        # Connecting the views and a data source through a DsViewHandle
        ds_view_handle = DsViewHandle(data_source=data_source, views=[line_view])
        ds_view_handle2 = DsViewHandle(data_source=data_source2, views=[line_view_select])

        # Adding the ds_view_handle to the app
        viewer1.add_ds_view_handles(ds_view_handles=[ds_view_handle])
        viewer2.add_ds_view_handles(ds_view_handles=[ds_view_handle2])

        # IN RUNTIME
        bokeh_fig1 = fig1.bokeh_figure

        range_tool = RangeTool(x_range=bokeh_fig1.x_range)
        range_tool.overlay.fill_color = "navy"
        range_tool.overlay.fill_alpha = 0.2

        select.bokeh_figure.add_tools(range_tool)

        layout = column(fig1.layout, select.layout)
        return layout
