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

import datetime
import os
import json
import threading
import multiprocessing
import time
import pandas as pd
import webbrowser
import requests
from queue import Queue

from wiliot_core import set_logger, GetApiKey, InlayTypes
from wiliot_tools.utils.wiliot_gui.wiliot_gui import *
from wiliot_tools.association_tool.association_configs import is_wiliot_code, is_asset_code
from wiliot_testers.association_tester.hw_components.scanner_component import Scanner
from wiliot_testers.association_tester.modules.performance_module import ReelVerification
from wiliot_testers.association_tester.modules.association_module import TagAssociation
from wiliot_testers.association_tester.modules.gui_module import AssociationAndVerificationGUI

pd.options.mode.chained_assignment = None  # default='warn'

GUI_USER_INPUT_PATH = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = 'association_and_verification_gui_user_inputs.json'
GUI_FILE = os.path.abspath(os.path.join(GUI_USER_INPUT_PATH, 'configs', FILE_NAME))
RUN_PARAMS_FILE = os.path.abspath(os.path.join(GUI_USER_INPUT_PATH, 'configs', 'last_run_params.json'))
INLAY_TYPE = InlayTypes.TIKI_121.name
DEFAULT_VALUES = {
    'min_test_time': '1.5',
    'max_test_time': '5',
    'time_to_move': '0.5',
    'need_to_associate': 'no',
    'is_step_machine': 'yes',
    'asset_location': 'last',
    'owner_id': 'wiliot-ops',
    'category_id': '86fd9f07-38b0-466f-b717-2e285b803f5c',
    'energy_pattern': '51',
    'time_profile': '5,15',
    'ble_power': '22', 'sub1g_power': '29', 'sub1g_freq': '925000',
    'scan_ch': '37',
    'is_listen_bridge': 'yes',
    'env': 'prod',
    'scanner_type': 'Cognex',
    'sc_min_location': '30',
    'sc_association': '90',
    'sc_scanning': '90',
    'sc_responding': '90',
    'sc_n_no_scan': '2',
    'run_name': 'test'
}

DEFAULT_RUN_PARAM = {"last_run_name": "test", "last_location": 0, "last_asset_id": "", "last_asset_location": 0}

TITLE_FONT = ("Helvetica", 14, "bold")
SECTION_FONT = ("Helvetica", 12, "bold")


def get_params(file_path, default_values):
    if os.path.isfile(file_path):
        out = json.load(open(file_path, "rb"))
        for k in default_values.keys():
            if k not in out.keys():
                out[k] = default_values[k]
    else:
        out = default_values
    return out


def get_user_inputs():
    """
    opens GUI for selecting a file and returns it
    """
    # upload config
    default_values = get_params(GUI_FILE, DEFAULT_VALUES)
    run_params = get_params(RUN_PARAMS_FILE, DEFAULT_RUN_PARAM)

    params_dict = {

        # Setup Button
        'check_setup': {
            'text': 'Check Setup',
            'value': '',
            'widget_type': 'button',
            'group': 'Label Location'
        },

        # Label Location Section
        'run_name': {
            'text': 'Run name',
            'value': default_values['run_name'],
            'widget_type': 'entry',
            'group': 'Label Location'
        },
        'generate_run_name': {
            'text': 'Generate Run Name',
            'value': '',
            'widget_type': 'button',
            'group': 'Label Location'
        },
        'first_location': {
            'text': 'Start label location',
            'value': 0,
            'widget_type': 'entry',
            'group': 'Label Location'
        },
        'last_tested': {
            'value': f'last tested run name was: {run_params["last_run_name"]}\n'
                     f'last tested location was: {run_params["last_location"]}\n'
                     f'last scanned asset id was: {run_params["last_asset_id"]} '
                     f'at location: {run_params["last_asset_location"]}',
            'text': '',
            'widget_type': 'label',
            'group': 'Label Location'
        },

        # Tag-GW Configuration Section

        'min_test_time': {
            'text': 'Minimal wait time per location [sec]',
            'value': default_values['min_test_time'],
            'widget_type': 'entry',
            'group': 'Tag-GW Configuration'
        },
        'max_test_time': {
            'text': 'Maximal wait time per location [sec]',
            'value': default_values['max_test_time'],
            'widget_type': 'entry',
            'group': 'Tag-GW Configuration'
        },
        'energy_pattern': {
            'text': 'Energy Pattern',
            'value': default_values['energy_pattern'],
            'widget_type': 'entry',
            'group': 'Tag-GW Configuration'
        },
        'time_profile': {
            'text': 'Time Profile',
            'value': default_values['time_profile'],
            'widget_type': 'entry',
            'group': 'Tag-GW Configuration'
        },
        'ble_power': {
            'text': 'BLE Power[dBm]',
            'value': default_values['ble_power'],
            'widget_type': 'entry',
            'group': 'Tag-GW Configuration'
        },
        'sub1g_power': {
            'text': 'Sub1G Power[dBm]',
            'value': default_values['sub1g_power'],
            'widget_type': 'entry',
            'group': 'Tag-GW Configuration'
        },
        'sub1g_freq': {
            'text': 'Sub1G frequency[kHz]',
            'value': default_values['sub1g_freq'],
            'widget_type': 'entry',
            'group': 'Tag-GW Configuration'
        },
        'is_listen_bridge': {
            'text': 'listen to Bridge?',
            'value': default_values['is_listen_bridge'],
            'options': ('yes', 'no'),
            'widget_type': 'combobox',
            'group': 'Tag-GW Configuration'
        },

        # Scanner Section
        'scanner_type': {
            'text': 'Scanner Type',
            'value': default_values['scanner_type'],
            'options': ('Cognex', ''),
            'widget_type': 'combobox',
            'group': 'Scanner'
        },
        'asset_location': {
            'text': 'Asset location with respect to Wiliot code',
            'value': default_values['asset_location'],
            'options': ('first', 'last'),
            'widget_type': 'combobox',
            'group': 'Scanner'
        },

        # Reel-to-Reel Section
        'is_step_machine': {
            'text': 'Is step machine?',
            'value': default_values['is_step_machine'],
            'options': ('yes', 'no'),
            'widget_type': 'combobox',
            'group': 'Reel-to-Reel'
        },
        'time_to_move': {
            'text': 'Movement time [sec]',
            'value': default_values['time_to_move'],
            'widget_type': 'entry',
            'group': 'Reel-to-Reel'
        },

        # Association Section
        'need_to_associate': {
            'text': 'Do association?',
            'value': default_values['need_to_associate'],
            'options': ('yes', 'no'),
            'widget_type': 'combobox',
            'group': 'Association'
        },
        'owner_id': {
            'text': 'Owner id',
            'value': default_values['owner_id'],
            'widget_type': 'entry',
            'group': 'Association'
        },
        'env': {
            'text': 'Environment',
            'value': default_values['env'],
            'widget_type': 'entry',
            'group': 'Association'
        },
        'category_id': {
            'text': 'Asset category id',
            'value': default_values['category_id'],
            'widget_type': 'entry',
            'group': 'Association'
        },

        # Stop Criteria Section
        'sc_min_location': {
            'text': 'Minimum tags to test before applying "yield-stop-criteria"',
            'value': default_values['sc_min_location'],
            'widget_type': 'entry',
            'group': 'Stop Criteria'
        },
        'sc_association': {
            'text': 'Stop if association yield is lower than [%]',
            'value': default_values['sc_association'],
            'widget_type': 'entry',
            'group': 'Stop Criteria'
        },
        'sc_scanning': {
            'text': 'Stop if scanning yield is lower than [%]',
            'value': default_values['sc_scanning'],
            'widget_type': 'entry',
            'group': 'Stop Criteria'
        },
        'sc_responding': {
            'text': 'Stop if responding yield is lower than [%]',
            'value': default_values['sc_responding'],
            'widget_type': 'entry',
            'group': 'Stop Criteria'
        },
        'sc_n_no_scan': {
            'text': 'Stop if N successive labels are failed to be scanned',
            'value': default_values['sc_n_no_scan'],
            'widget_type': 'entry',
            'group': 'Stop Criteria'
        },

        # Run Button
        'run_button': {
            'text': 'Run',
            'value': '',
            'widget_type': 'button',
            'columnspan': 2

        },
    }
    scanner = None
    is_setup_valid = False
    scanned_codes = ['test']

    def on_check_setup():
        values = gui.get_all_values()
        nonlocal scanner
        is_setup_valid, scanner, scanned_codes = is_valid_setup(values, scanner, gui)

    def on_generate_run_name():
        scanned_codes.sort(reverse=True)
        gui.update_widget(widget_key='run_name', new_value='_'.join(scanned_codes))

    def on_run():
        values = gui.get_all_values()
        nonlocal scanner
        if not is_setup_valid:
            is_valid, scanner, scanned_codes = is_valid_setup(values, scanner, gui)
            if not is_valid:
                pass
        for k, v in values.items():
            default_values[k] = v
        with open(GUI_FILE, 'w') as f:
            json.dump(default_values, f)
        with open(RUN_PARAMS_FILE, 'w') as f:
            json.dump(run_params, f)

        if scanner is not None:
            scanner.disconnect()
        return default_values

    gui = WiliotGui(params_dict, do_button_config=False, height_offset=-50, title='Association and Verification tester')
    gui.widgets['last_tested'].configure(anchor="w", justify='left')
    gui.add_event(widget_key='generate_run_name', command=on_generate_run_name, event_type='button')
    gui.add_event(widget_key='check_setup', command=on_check_setup, event_type='button')
    gui.add_event(widget_key='run_button', command=on_run, event_type='button')
    gui.run()


def is_valid_setup(values, scanner, gui):
    # check scanner
    is_valid = 'yes'
    scanned_codes = ['test']
    if values['scanner_type'].lower() == 'cognex':
        if scanner is None:
            scanner = Scanner()
        scanned_codes = scanner.scan()
        yes_or_no_layout = {
            'question': {
                'value': f'Starting location was set to: {values["first_location"]}\n'
                         f'The scanned codes are:\n{scanned_codes}\n'
                         f'Is the starting location is correct?\n'
                         f'Are those the codes of the first label?\n\n'
                         f'If not, please click on No, try to re-position scanner and try again',
                'text': '',
                'widget_type': 'label',
            },
            'yes_button': {
                'text': 'Yes',
                'value': '',
                'widget_type': 'button',
            },
            'no_button': {
                'text': 'No',
                'value': '',
                'widget_type': 'button',
            },
        }

        def on_no_button():
            print('re-positioning the scanner and try again')
            yes_or_no_gui.layout.destroy()
            return False, scanner, scanned_codes

        def on_yes_button():
            client_types = ['asset', None]
            for client_type in client_types:
                g = GetApiKey(gui_type='ttk',
                              env=values['env'],
                              owner_id=values['owner_id'],
                              client_type=client_type
                              )
                api_key = g.get_api_key()
                if not api_key:
                    file_path = g.get_config_path()
                    popup_message(
                        f'Could not found an api key for owner id {values["owner_id"]} and env {values["env"]}'
                        f'at path: {file_path}')
                    yes_or_no_gui.layout.destroy()
                    return False, scanner, scanned_codes
            yes_or_no_gui.layout.destroy()
            return True, scanner, scanned_codes

        yes_or_no_gui = WiliotGui(params_dict=yes_or_no_layout, parent=gui.layout, do_button_config=False,
                                  title='Valid Setup Association and Verification')
        yes_or_no_gui.add_event(widget_key='no_button', command=on_no_button, event_type='button')
        yes_or_no_gui.add_event(widget_key='yes_button', command=on_yes_button, event_type='button')
        yes_or_no_gui.run()


class AssociationAndVerificationTester(object):
    def __init__(self, user_input):
        start_time = datetime.datetime.now()
        common_run_name = f"{user_input['run_name']}_{start_time.strftime('%Y%m%d_%H%M%S')}"
        self.logger_path, self.logger = set_logger(app_name='AssociationAndVerificationTester',
                                                   common_run_name=common_run_name)
        self.run_data = {'common_run_name': common_run_name,
                         'tester_type': 'association_and_verification',
                         'inlay_type': INLAY_TYPE,
                         'station_name': os.environ['testerStationName']
                         if 'testerStationName' in os.environ else 'testStation',
                         'run_start_time': start_time}
        stop_event = multiprocessing.Event()
        exception_q = Queue(maxsize=100)
        self.app_running = True
        self.performance = ReelVerification(user_input=user_inputs,
                                            stop_event=stop_event,
                                            is_app_running=self.is_app_running,
                                            logger_name=self.logger.name,
                                            logger_path=self.logger_path,
                                            exception_q=exception_q)
        self.association = TagAssociation(user_input=user_inputs,
                                          stop_event=stop_event,
                                          is_app_running=self.is_app_running,
                                          logger_name=self.logger.name,
                                          logger_path=self.logger_path,
                                          exception_q=exception_q,
                                          run_param_file=RUN_PARAMS_FILE)

        self.gui = AssociationAndVerificationGUI(logger_name=self.logger.name,
                                                 get_data_func=self.get_data,
                                                 get_stat_func=self.get_stat,
                                                 common_run_name=common_run_name)
        self.user_inputs = user_input
        self.stop_event = stop_event
        self.exception_q = exception_q
        self.results_df = pd.DataFrame()
        self.current_stat = {'n_locations': '0',
                             'scan_success': '0%', 'association_success': '0%', 'responding_rate': '0%',
                             'n_success': '0', 'success_rate': '0%'}
        self.duplicated_code = pd.DataFrame()
        self.neglected_duplication = pd.DataFrame()
        self.performance_thread = None
        self.association_thread = None
        self.gui_thread = None

    def run(self):
        self.performance_thread = threading.Thread(target=self.performance.run_app, args=())
        self.association_thread = threading.Thread(target=self.association.run_app, args=())
        self.gui_thread = threading.Thread(target=self.gui.run_app, args=())
        self.performance_thread.start()
        self.association_thread.start()
        self.gui_thread.start()
        webbrowser.open(self.gui.get_url())

        self.run_app()

    def run_app(self):
        while True:
            try:
                time.sleep(1)
                if self.gui.is_stopped_by_user():
                    self.logger.info('run stopped by user')
                    break
                elif self.app_running != self.gui.is_app_running():
                    self.logger.info(f'run was {"paused" if self.app_running else "continued"} by user')
                    self.app_running = not self.app_running

                if not self.exception_q.empty():
                    self.app_running = False
                    self.logger.warning('got exception during run, pause the app')
                    self.handle_exceptions()

                if self.app_running:
                    df_ass = self.association.get_locations_df()
                    df_per = self.performance.get_packets_df()
                    self.merge_results(location_df=df_ass, packets_df=df_per)
                    self.current_stat = self.calc_stat()
                    self.handle_stop_criteria()
                    # save data:
                    self.save_location_data()
                    self.save_run_data()
                else:
                    time.sleep(1)
            except Exception as e:
                self.logger.warning(f'got exception during run: {e}')
                if not self.exception_q.full():
                    self.exception_q.put(f'Main: {e}')

        # stop run
        self.stop()

    def is_app_running(self):
        return self.app_running

    def handle_stop_criteria(self):
        if int(self.current_stat['n_successive_bad_scan']) >= int(self.user_inputs['sc_n_no_scan']):
            raise Exception(f"{self.current_stat['n_successive_bad_scan']} successive bad scanning were detected. "
                            f"Check if machine is stuck")

        if self.current_stat['is_duplicated']:
            self.neglected_duplication = self.duplicated_code.copy()
            raise Exception(f"{self.duplicated_code.values} codes duplications were detected. "
                            f"Check if machine is stuck")

        if int(self.current_stat['n_locations']) < int(self.user_inputs['sc_min_location']):
            return
        if self.user_inputs['need_to_associate'].lower() == 'yes':
            if float(self.current_stat['association_success'].replace('%', '')) < float(
                    self.user_inputs['sc_association']):
                self.user_inputs['sc_association'] = 0  # pop only once
                raise Exception(f"association yield of {self.current_stat['association_success']} was detected")
        if float(self.current_stat['scan_success'].replace('%', '')) < float(self.user_inputs['sc_scanning']):
            self.user_inputs['sc_scanning'] = 0  # pop only once
            raise Exception(f"scan yield of {self.current_stat['scan_success']} was detected")
        if float(self.current_stat['responding_rate'].replace('%', '')) < float(self.user_inputs['sc_responding']):
            self.user_inputs['sc_responding'] = 0  # pop only once
            raise Exception(f"responding yield of {self.current_stat['responding_rate']} was detected")

    def handle_exceptions(self):
        n_exceptions = self.exception_q.qsize()
        exceptions_str = []
        for _ in range(n_exceptions):
            exceptions_str.append(self.exception_q.get())
        self.logger.warning('\n'.join(exceptions_str))
        popup_message('\n'.join(exceptions_str))

    def print_run(self):  # for debug
        t_i = time.time()
        while time.time() - t_i < 60:
            try:
                time.sleep(2)
                df_ass = self.association.get_locations_df()
                print(f'n unique locations: {len(df_ass)}')
                df_per = self.performance.get_packets_df()
                print(f'n unique adva: {len(df_per)}')
                self.merge_results(location_df=df_ass, packets_df=df_per)
                print(f'n all results: {len(self.results_df)}')
                stat = self.calc_stat()
                print(stat)
            except Exception as e:
                self.logger.warning(f'got exception during print_run: {e}')

        # stop run
        self.stop_event.set()
        self.stop()

    def calc_stat(self):
        stat_out = {}
        rel_data = self.results_df.loc[~(self.results_df['location'].isna()) & ~(self.results_df['location'] == '')]
        n_location = len(rel_data)
        stat_out['n_locations'] = str(n_location)
        stat_out['n_tags_outside_test'] = str(len(self.results_df) - n_location)
        if n_location > 0:
            stat_out['scan_success'] = f'{round(rel_data["scan_status"].sum() / n_location * 100, 2)}%'
            ass_valid = rel_data["is_associated"][rel_data["associate_status_code"] != '']
            stat_out['association_success'] = f'{round(ass_valid.sum() / max([ass_valid.count(), 1]) * 100, 2)}%'
            if 'n_packets' in rel_data.keys():
                respond_valid = rel_data["n_packets"][rel_data["wiliot_code"] != '']
                stat_out['responding_rate'] = f'{round(respond_valid.notna().sum() / len(respond_valid) * 100, 2)}%'
            else:
                stat_out['responding_rate'] = '0%'
            stat_out['n_successive_bad_scan'] = \
                rel_data['location'].iloc[-1] - rel_data['location'][rel_data['scan_status']].iloc[-1] \
                    if any(rel_data['scan_status']) else n_location

            df_per_loc = rel_data.drop_duplicates(subset=['location'])
            self.duplicated_code = pd.concat([
                df_per_loc['asset_code'].loc[
                    (df_per_loc.duplicated(subset=['asset_code']) & (df_per_loc['asset_code'] != ''))],
                df_per_loc['wiliot_code'].loc[
                    (df_per_loc.duplicated(subset=['wiliot_code'])) & (df_per_loc['wiliot_code'] != '')]
            ], axis=0)
            stat_out['is_duplicated'] = len(self.duplicated_code) > len(self.neglected_duplication)
            if 'is_success' in rel_data.keys():
                stat_out['n_success'] = f'{rel_data["is_success"].sum()}'
                stat_out['success_rate'] = f'{round(rel_data["is_success"].sum() / n_location * 100, 2)}%'
            else:
                stat_out['n_success'] = '0'
                stat_out['success_rate'] = '0%'
        else:
            stat_out['scan_success'] = '0%'
            stat_out['association_success'] = '0%'
            stat_out['responding_rate'] = '0%'
            stat_out['n_successive_bad_scan'] = 0
            stat_out['is_duplicated'] = False
            stat_out['n_success'] = '0'
            stat_out['success_rate'] = '0%'

        return stat_out

    def shutdown_server(self):
        try:
            requests.post(f'{self.gui.get_url()}shutdown')
        except Exception as e:
            pass

    def stop(self):
        self.stop_event.set()
        self.shutdown_server()

        self.performance_thread.join(15)
        if self.performance_thread.is_alive():
            self.logger.warning('performance thread is still running')
        self.association_thread.join(15)
        if self.association_thread.is_alive():
            self.logger.warning('association thread is still running')
        self.gui_thread.join(15)
        if self.gui_thread.is_alive():
            self.logger.warning('GUI thread is still running')

        # summary
        df_ass = self.association.get_locations_df()
        df_per = self.performance.get_packets_df()
        self.merge_results(location_df=df_ass, packets_df=df_per)
        self.current_stat = self.calc_stat()

        self.save_location_data()
        self.save_run_data()

        # handle exceptions:
        if not self.exception_q.empty():
            self.handle_exceptions()

        # show results:
        stat_out_str = "\n".join([f'{k}: {v}' for k, v in self.current_stat.items()])
        popup_message(f'{self.run_data["common_run_name"]}\n\n{stat_out_str}')

    def save_run_data(self):
        df_path = os.path.join(os.path.dirname(self.logger_path), f'{self.run_data["common_run_name"]}@run_data.csv')
        print(f'saving run config at: {df_path}')
        data_to_save = pd.DataFrame({**self.run_data, **{'end_run_time': datetime.datetime.now()}, **self.current_stat,
                                     **self.user_inputs}, index=[0])
        data_to_save.to_csv(df_path, index=False)

    def save_location_data(self):
        df_path = os.path.join(os.path.dirname(self.logger_path),
                               f'{self.run_data["common_run_name"]}@packets_data.csv')
        print(f'saving data at: {df_path}')
        data_to_save = self.results_df.loc[~self.results_df['location'].isna()]
        data_to_save.sort_values(by='location', inplace=True)
        data_to_save.to_csv(df_path, index=False)

    def get_data(self):
        return self.results_df

    def get_stat(self):
        return self.current_stat

    def merge_results(self, location_df, packets_df):
        if packets_df.empty and location_df.empty:
            return

        merged_df = None
        if packets_df.empty:
            merged_df = location_df
        else:
            packets_df.index = packets_df.index.set_names(['adv_address'])
            packets_df = packets_df.reset_index()

        if location_df.empty:
            merged_df = packets_df
            merged_df.insert(loc=0, column='location', value='')
            if 'n_packets' not in merged_df.keys():
                merged_df.insert(loc=0, column='n_packets', value=0)

        if merged_df is None:
            merged_df = pd.merge(location_df, packets_df, left_on='wiliot_code', right_on='external_id', how='outer')
            if 'n_packets' in merged_df.keys():
                is_responded = merged_df['n_packets'].apply(lambda x: int(x) > 0 if not pd.isnull(x) else False)
            else:
                is_responded = pd.Series([False] * merged_df.shape[0])
            if self.user_inputs['need_to_associate'].lower() == 'yes':
                is_success = pd.DataFrame([merged_df['scan_status'], merged_df['is_associated'], is_responded]).all()
            else:
                is_success = pd.DataFrame([merged_df['scan_status'], is_responded]).all()
            merged_df.insert(loc=len(merged_df.columns), column='is_success', value=is_success)
            merged_df.insert(loc=0, column='common_run_name', value=self.run_data['common_run_name'])

        self.results_df = merged_df


if __name__ == '__main__':
    user_inputs = get_user_inputs()
    print(user_inputs)

    av = AssociationAndVerificationTester(user_input=user_inputs)
    av.run()

    print('done')
