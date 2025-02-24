"""
Copyright (c) 2016- 2024, Wiliot Ltd. All rights reserved.

Redistribution and use of the Software in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

  1. Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.

  2. Redistributions in binary form, except as used in conjunction with
  Wiliot's Pixel in a product or a Software update for such product, must reproduce
  the above copyright notice, this list of conditions and the following disclaimer in
  the documentation and/or other materials provided with the distribution.

  3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
  may be used to endorse or promote products or services derived from this Software,
  without specific prior written permission.

  4. This Software, with or without modification, must only be used in conjunction
  with Wiliot's Pixel or with Wiliot's cloud service.

  5. If any Software is provided in binary form under this license, you must not
  do any of the following:
  (a) modify, adapt, translate, or create a derivative work of the Software; or
  (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
  discover the source code or non-literal aspects (such as the underlying structure,
  sequence, organization, ideas, or algorithms) of the Software.

  6. If you create a derivative work and/or improvement of any Software, you hereby
  irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
  royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
  right and license to reproduce, use, make, have made, import, distribute, sell,
  offer for sale, create derivative works of, modify, translate, publicly perform
  and display, and otherwise commercially exploit such derivative works and improvements
  (as applicable) in conjunction with Wiliot's products and services.

  7. You represent and warrant that you are not a resident of (and will not use the
  Software in) a country that the U.S. government has embargoed for use of the Software,
  nor are you named on the U.S. Treasury Department’s list of Specially Designated
  Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
  You must not transfer, export, re-export, import, re-import or divert the Software
  in violation of any export or re-export control laws and regulations (such as the
  United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
  and use restrictions, all as then in effect

THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
(SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
(A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
(B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
(C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
"""

import logging
import time
import threading
import pandas as pd
from enum import Enum

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output
from werkzeug.serving import make_server
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from wiliot_core import set_logger


class LevelType(Enum):
    ADVA = 'adv. address'
    EXTERNAL_ID = 'external id'


GREEN_BUTTON_STYLE = {'background-color': 'green',
                      'color': 'white',
                      'height': '50px',
                      'width': '200px'}

RED_BUTTON_STYLE = {'background-color': 'red',
                    'color': 'white',
                    'height': '50px',
                    'width': '200px'}



class YieldPlotting(object):

    def __init__(self, get_data, get_sensors_data, cmd_q, user_config, logger=None, stop_event=None, tester_name='Yield Tester'):
        """
        :param data_q data queue contains DecryptedTagCollection elements
        :type data_q multiprocessing.Manager().Queue
        """
        if logger is None:
            _, self.logger = set_logger(app_name='YieldPlotting')
        else:
            self.logger = logger
        
        self.tester_name = tester_name.replace('_', ' ').title()
        self.stop_event = stop_event
        self.get_live_df = get_data
        self.cmd_q = cmd_q
        self.user_config = user_config
        self.cur_state = {}
        self.live_df = {}
        self.dash_app = None
        self.server = None
        self.level_type = LevelType.ADVA
        self.get_sensors_data = get_sensors_data
        self.sensors_data = {}
        self.update_sensors()
        self.is_run = True

        self.init_live_plot()
        self.logger.info('start application')

    def init_live_plot(self):
        self.logger.info('Starting server connection')
        self.dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
        self.generate_monitor_inlay()
        self.server = self.dash_app.server
        self.init_callbacks()
        self.logger.info('complete init callbacks')

    def init_callbacks(self):

        @self.dash_app.callback(
            Output('placeholder-data_type_switch', 'children'),
            Input("data_type_switch", "value")
        )
        def update_data_type_switch(value):
            self.logger.info('update_data_type_switch')
            try:
                self.level_type = LevelType(value)
                self.logger.info(f'data_type was changed to {self.level_type}')
            except Exception as e:
                self.logger.warning(f'cannot change level type due to {e}')
                raise dash.exceptions.PreventUpdate
            
        @self.dash_app.callback(
            Output('placeholder-window-size', 'children'),
            Input('window-size', 'value')
        )
        def update_plot_mode(value):
            self.user_config['window_size'] = value
            self.logger.info(f'window_size was changed to {value}')
            return None
        
        @self.dash_app.callback(
            [Output('start-stop-btn', 'children'),
             Output('start-stop-btn', 'color'),],
            Input('start-stop-btn', 'n_clicks')
        )
        def start_stop_run(n_clicks):
            if n_clicks > 0:
                self.is_run = not self.is_run
                if self.cmd_q.full():
                    self.logger.warning(f'start_stop_run: cmd_q is full, discard: {self.cmd_q.get()}')
                self.cmd_q.put('start' if self.is_run else 'pause')
            if self.is_run:
                str_print = 'Run Started'
                style_out = 'danger'
                value = 'Pause Run'
            else: 
                str_print = 'Run Stopped'
                style_out = 'success'
                value = 'Start Run'
            self.logger.info(f'{str_print}')
            return value, style_out

        @self.dash_app.callback(
            [Output('upload-btn', 'children'),
             Output('upload-btn', 'color'),],
            Input('upload-btn', 'n_clicks')
        )
        def upload_and_finish_run(n_clicks):
            style_out = 'secondary'
            value = 'Stop and Upload Data'
            if n_clicks > 0:
                self.logger.info('User stop the application')
                style_out = 'light'
                value = 'Uploading...'
                if self.cmd_q.full():
                    self.logger.warning(f'upload_and_finish_run: cmd_q is full, discard: {self.cmd_q.get()}')
                self.cmd_q.put('stop')
            return value, style_out

        @self.dash_app.callback(
            [Output('graph', 'figure'),
             Output('num-tags-text', 'children'),
             Output('num-adva-text', 'children'),
             Output('num-ex-id-text', 'children'),
             ] + [Output(f'{sensor_name}-sense', 'children') for sensor_name in self.sensors_data.keys()],
            Input('interval-component', 'n_intervals')
        )
        def update_graphs(_):
            data = self.get_live_df()
            if 0 in data.index:
                data = data.drop(index=0)
            
            if data.empty:
                raise dash.exceptions.PreventUpdate
            sensors_out = self.update_sensors()
            figure_out = self.generate_figures(data)
            n_tags = html.H2(str(data.index[-1] * int(self.user_config.get('matrix_size', 1))), className="card-title")
            n_adva = html.H2(str(data['matrix_advas'].sum()), className="card-title")
            n_ex_id = html.H2(str(data['matrix_external_ids'].sum()), className="card-title")
            return figure_out + [n_tags, n_adva, n_ex_id] + sensors_out

    def update_sensors(self):
        self.sensors_data = self.get_sensors_data()
        if 'temperature' in self.sensors_data.keys() and self.user_config.get('temperature_type', 'C') == 'F':
            self.sensors_data['temperature'] = (self.sensors_data['temperature'] * (9 / 5)) + 32

        sensors_cards = []
        for sensor_type, sensor_data in self.sensors_data.items():
            color = 'black' if float(self.user_config.get(f'min_{sensor_type}', -float('inf'))) <= sensor_data <= float(self.user_config.get(f'max_{sensor_type}', float('inf'))) else 'danger'
            sensors_cards.append(html.P(f'{sensor_data}', className=f"text-{color}"))
        
        return sensors_cards
    
    def generate_figures(self, new_df):       
        matrix_num = new_df.index
        if self.level_type == LevelType.EXTERNAL_ID:
            n_passed = new_df['matrix_external_ids']
        elif self.level_type == LevelType.ADVA:
            n_passed = new_df['matrix_advas']
        else:
            self.logger.warning(f'data type is not supported: {self.level_type}')
            raise dash.exceptions.PreventUpdate

        window_size = int(self.user_config.get('window_size', 1))
        matrix_size = int(self.user_config.get('matrix_size', 1))

        n_tags = matrix_num * int(self.user_config.get('matrix_size', 1))
        yield_all = (n_passed.cumsum() / n_tags) * 100
        yield_current = (n_passed.rolling(window_size).sum() / (window_size * matrix_size)) * 100
        
        # all fig
        fig = make_subplots(rows=1, cols=2, subplot_titles=['Moving Mean Yield', 'Cumulative Yield'],
                            horizontal_spacing=0.1
        )
        # current:
        fig.add_trace(go.Scatter(x=matrix_num.to_list(), y=yield_current.to_list(), mode='lines+markers', marker=dict(color='blue')), row=1, col=1)
        fig.add_trace(go.Scatter(x=matrix_num.to_list(), y=[int(self.user_config.get('red_line_current', 0))] * len(matrix_num), mode='lines', line_color='red', fill='tozeroy'), row=1, col=1)
        fig.update_xaxes(title_text='Number of Matrices', row=1, col=1)
        # all
        fig.add_trace(go.Scatter(x=n_tags.to_list(), y=yield_all.to_list(), mode='lines+markers', marker=dict(color='blue')), row=1, col=2)
        fig.add_trace(go.Scatter(x=n_tags.to_list(), y=[int(self.user_config.get('red_line_cumulative', 0))] * len(n_tags), mode='lines',line_color='red', fill='tozeroy'), row=1, col=2)
        fig.update_xaxes(title_text='Number of Tags', row=1, col=2)

        fig.update_yaxes(title_text='%')
        fig.update_layout(uirevision=1, showlegend=False)

        return [fig]
    
    def generate_monitor_inlay(self):
        def header(name, app):
            title = html.H2(name, className='mt-2')
            logo = html.Img(
                src='https://www.wiliot.com/src/uploads/Wiliotlogo.png', style={"float": "right", "height": 50}
            )

            return dbc.Row([dbc.Col(title, md=9), dbc.Col(logo, md=3)])
        
        start_stop_button = html.Div(
            [dbc.Button("Pause Run", id="start-stop-btn",n_clicks=0, color='danger', 
                        style={'height': '50px', 'width': '200px'})]
            )
        upload_button = html.Div(
            [dbc.Button("Stop and Upload Data", id="upload-btn",n_clicks=0, color='secondary', 
                        style={'height': '50px', 'width': '400px'})]
            )

        radio_button_style = {'font-size': 15, 'padding-left': 10, 'padding-right': 40}

        # Card components
        cards_stat = [
            dbc.Card(
                [
                    html.Div(id='num-tags-text'),
                    html.P("Tested Tags", className="card-text"),
                ],
                body=True,
                color="light",
                id='num-tags-card',
            ),
            dbc.Card(
                [
                    html.Div(id='num-adva-text'),
                    html.P("Unique Adv. Address", className="card-text"),
                ],
                body=True,
                color="info",
                inverse=True,
            ),
            dbc.Card(
                [
                    html.Div(id='num-ex-id-text'),
                    html.P("Unique External Ids", className="card-text"),
                ],
                body=True,
                color="primary",  # "#0d6efd"
                inverse=True,
            ),
        ]
        sensors_labels = html.P(children=[
            html.Div('nan', id='temperature-sense'), self.user_config.get('temperature_type', 'C'),  html.I(className='bi bi-thermometer-half me-2'), 
            html.P('|',className='px-3'),
            html.Div('nan', id='humidity-sense'), ' %', html.I(className='bi bi-droplet-half me-2'), 
            html.P('|',className='px-3'),
            html.Div('nan', id='light_intensity-sense'), ' Lux', html.I(className='bi bi-lightbulb me-2'),
            ],
            className='col fw-bold', style=dict(display='flex', width='150%')
                                )
        plot_options = [
            html.Div(
                [
                    dcc.RadioItems(id='data_type_switch', 
                                    options=[
                                        {'label': html.Span(LevelType.ADVA.name, style=radio_button_style), 'value': LevelType.ADVA.value},
                                        {'label': html.Span(LevelType.EXTERNAL_ID.name, style=radio_button_style), 'value': LevelType.EXTERNAL_ID.value},
                                        ], 
                                    value=LevelType.EXTERNAL_ID.value, inline=True),
                ],
                className='col fw-bold', style=dict(display='flex', width='100%')
            ),
            html.Div(
                [
                    html.P('Window Size:',className='me-4'),
                    daq.NumericInput(id='window-size', value=int(self.user_config.get('window_size', 1)),
                                     min=0, max=1000),
                ],
                className='col fw-bold', style=dict(display='flex', width='100%')
            ),
            html.Div(id='placeholder-data_type_switch'),
            html.Div(id='placeholder-window-size'),
        ]
        plot_style = {'margin': 0,
                      'display': 'flex',
                      'height': '60vh'}
        graph = dcc.Graph(id=f"graph", style=plot_style)

        self.dash_app.layout = dbc.Container(
            [
                header(f"Wiliot {self.tester_name}", self.dash_app),
                html.Hr(className='vw-100'),
                dbc.Row([dbc.Col(card) for card in cards_stat], className='vw-100'),
                html.Br(),
                dbc.Row([dbc.Col(sensors_labels), dbc.Col(start_stop_button), dbc.Col(upload_button)], className='vw-100'),
                html.Br(),
                dbc.Row([dbc.Col(op) for op in plot_options], className='vw-100'),
                dbc.Row(dbc.Col(graph), className='vw-100'),
                dcc.Interval(
                    id='interval-component',
                    interval=1 * 1000,  # in milliseconds
                    n_intervals=0),
            ],
            fluid=True,
        )

    def run(self, host=None, port=None):
        host = self.user_config['host'] if host is None else host
        port = int(self.user_config['port'] if port is None else port)
        self.server = make_server(host, port, self.dash_app.server)
        self.logger.info(f"http://{host}:{port}/")
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
        if self.stop_event is None:
            self.server.serve_forever()
        else:
            all_threads_handles = {}
            server_thread = threading.Thread(target=self.server.serve_forever)
            server_thread.start()
            all_threads_handles['server'] = server_thread
            while not self.stop_event.is_set():
                time.sleep(1)
            self.server.shutdown()
            for handler_name, handler in all_threads_handles.items():
                handler.join(5)
                if handler.is_alive():
                    self.logger.warning(f'failed to stop the {handler_name}')
                else:
                    self.logger.info(f'{handler_name} was stopped')


if __name__ == '__main__':
    from queue import Queue
    my_df = pd.DataFrame()
    x = 0

    def get_data():
        global my_df
        my_df = pd.concat([my_df, pd.DataFrame({'matrix_advas': 1, 'matrix_external_ids': 10, 'trigger_time': 0.0}, index=[0])], ignore_index=True)
        return my_df
    def get_sensors_data():
        global x
        x +=1
        return {'temperature': x, 'humidity': 10*x, 'light_intensity': x*100}
    cmd_q = Queue(maxsize=100)
    stop_event = threading.Event()

    user_config={'port': 8008, 'host': '127.0.0.3',
                 'red_line_current': 50, 'red_line_cumulative': 10,
                 "max_temperature": "40",
                 "min_temperature": "10",
                 "temperature_type": "C",
                 "min_humidity": "20",
                 "max_humidity": "90",
                 "min_light_intensity": "0",
                 "max_light_intensity": "1500",
    }
    
    p = YieldPlotting(get_data=get_data, get_sensors_data=get_sensors_data, cmd_q=cmd_q, user_config=user_config, stop_event=stop_event)
    p.run()
