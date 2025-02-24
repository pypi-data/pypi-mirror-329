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
import logging
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

from wiliot_testers.failure_analysis_tester.configs_gui import TEST_CONFIG, OUTPUT_DIR, TESTER_NAME, TIME_NOW
from wiliot_testers.wiliot_tester_log import WiliotTesterLog
from wiliot_test_equipment.visa_test_equipment.gpio_router import GPIORouter
from wiliot_test_equipment.visa_test_equipment.smu import SMU

RELAY_CONFIG = {
    'HARVESTER_SUB1': '0000',
    'HARVESTER_24': '0100',
    'TX': '1100',
    'VDD_CAP': '1110',
    # 'LC': '1111',
}


class FailureAnalysisTester:
    def __init__(self):
        self.set_logger()
        self.gpio_router = GPIORouter(logger=self.logger)
        self.smu = SMU(visa_addr=TEST_CONFIG['visa_addr'], logger=self.logger)
        self.df = pd.DataFrame()

    def set_logger(self):
        run_name = 'failure_analysis_' + TIME_NOW
        self.log_obj = WiliotTesterLog(run_name=run_name)
        self.log_obj.set_logger(tester_name=TESTER_NAME, log_path=OUTPUT_DIR)
        self.logger = self.log_obj.logger

    def run_test(self):
        for key in RELAY_CONFIG.keys():
            self.test_field(key)
        self.df.to_csv(OUTPUT_DIR / f'output_{TIME_NOW}.csv')

    def test_field(self, field):
        self.gpio_router.set_gpio_state(RELAY_CONFIG[field])
        kwargs = TEST_CONFIG[field]
        self.smu.configure_current_sweep(**kwargs)
        self.smu.run()
        time_list_float, current_A_list_float, voltage_V_list_float = self.smu.read_sweep()
        current_uA_list_float = [x * 1e6 for x in current_A_list_float]
        self.df[field + ' time'] = time_list_float
        self.df[field + ' current_uA'] = current_uA_list_float
        self.df[field + ' voltage_V'] = voltage_V_list_float
        plot = self.get_plot_field(
            field, current_uA_list_float, voltage_V_list_float)
        plot.savefig(OUTPUT_DIR / f'{field}.png')

    @staticmethod
    def get_plot_field(field, current, voltage):
        config = TEST_CONFIG[field]
        fig = plt.figure(figsize=(10, 6))
        plt.plot(current, voltage, 'o-')
        plt.title(field)
        plt.xlabel('Current [uA]')
        plt.ylabel('Voltage [V]')
        plt.xlim([config['start_current_uA'], config['stop_current_uA']])
        plt.ylim([- config['voltage_limit_V'], config['voltage_limit_V']])
        plt.minorticks_on()
        plt.grid(True, which='both')
        return fig


def plot_from_csv(csv_path: str):
    csv_path = Path(csv_path)
    df = pd.read_csv(csv_path)
    for key in RELAY_CONFIG.keys():
        plt = FailureAnalysisTester.get_plot_field(
            key, df[key + ' current_uA'], df[key + ' voltage_V'])
        plt.savefig(csv_path.parent / f'{key}.png')


if __name__ == '__main__':
    FAT = FailureAnalysisTester()
    FAT.run_test()
