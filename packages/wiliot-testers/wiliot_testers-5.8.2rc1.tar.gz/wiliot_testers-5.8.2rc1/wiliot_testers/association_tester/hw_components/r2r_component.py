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
import serial

from wiliot_tools.test_equipment.test_equipment import serial_ports


ARDUINO_BAUD = 1000000
ARDUINO_NAME = 'Williot R2R GPIO 1.0'


class R2R(object):
    def __init__(self, logger_name, counter_start_idx=0):
        self.logger = logging.getLogger(logger_name)

        # connect to the r2r/arduino:
        self.r2r = None
        self.port = ''
        self.connected = False
        self.counter = int(counter_start_idx)
        self.connect()
        if not self.connected:
            raise Exception('Could not connect to arduino!')

    def connect(self):
        baud_rate = ARDUINO_BAUD
        if self.port:
            ports_list = [self.port]
        else:
            ports_list = serial_ports()
        for p in ports_list:
            try:
                self.r2r = serial.Serial(p, baud_rate, timeout=0.1)
                time.sleep(1)
                if self.r2r.isOpen():
                    rsp = self.r2r.readline().decode()
                    if ARDUINO_NAME in rsp:
                        self.port = p
                        self.connected = True
                        self.logger.warning(f'Connect to R2R port {p}')
                        return
            except Exception as e:
                self.logger.warning(f'Could not connect to port {p} due to {e}, check the next port')

    def write(self, cmd):
        if not self.r2r.isOpen():
            self.connected = False
            self.connect()

        self.r2r.write(cmd.encode())
        time.sleep(0.5)
        rsp = self.r2r.readline()
        return rsp.decode()

    def move(self):
        rsp = self.write('T')
        self.logger.info(f'R2R responded with {rsp}')
        self.counter += 1

    def disconnect(self):
        self.connected = False
        if not self.r2r.isOpen():
            self.r2r.close()

    def get_counter(self):
        return self.counter
