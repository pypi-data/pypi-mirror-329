#!/usr/bin/env python3
# Copyright (C) 2024 Dr. Matthias Kesenheimer - All Rights Reserved.
# This file is based on TAoFI-FaultLib which is released under the GPL3 license.
# Go to https://github.com/raelize/TAoFI-FaultLib/LICENSE for full license details.
#
# You should have received a copy of the GPL3 license with this file.
# If not, please write to: m.kesenheimer@gmx.net.

"""
Findus is a Python library to perform fault-injection attacks on embedded devices. It was developed for the Pico Glitcher, however, the ChipWhisperer Pro and the ChipWhisperer Husky is also supported.

This is the documentation of the findus module and all its classes.
"""

import sqlite3
import time
import ast
import serial
import sys
import datetime
import os
import glob
from . import pyboard
from enum import Enum
from .GlitchState import ErrorType, WarningType, OKType, ExpectedType, SuccessType
try:
    from rd6006 import RD6006
    rd6006_available = True
except Exception as _:
    print("[-] Warning: Library RD6006 not installed. Functions to control the external power supply not available.")
    rd6006_available = False
from importlib.metadata import version
import random
import matplotlib.pyplot as plt
import numpy as np

class Database():
    """
    Database class managing access to the SQLite databases to store results from a glitching campaign.
    The parameter points stored in these databases are used to render an overview of the scanned parameter point via a web application.
    The web application and data analyzer can be run separately from the glitcher scripts by the following command:

        analyzer --directory databases

    Example usage:

        # import Database from findus
        from findus import Database
        ...
        database = Database(argv=argv)
        ...
        database.insert(experiment_id, delay, length, color, response)

    Example usage for multi-dimensional parameter space:

        # import Database from findus
        from findus import Database
        ...
        database = Database(argv=argv, column_names=["delay", "length", "t1"])
        ...
        database.insert(experiment_id, delay, length, t1, color, response)

    If you want to plot the `(length, t1)`-slice, you can call the `analyzer` script as follows:

        analyzer --directory databases -x length -y t1

    If `dbname` is not provided, a name will automatically generated based on `argv`.

    Methods:
        __init__: Default constructor.
        insert: Method to insert datapoints into the SQLite database.
        get_parameters_of_experiment: Get the parameters of a dataset by experiment_id.
        remove: Remove a parameter point from the database by experiment_id.
        cleanup: Remove all parameter points with a given color.
        get_number_of_experiments: Get the total number of performed experiments (number of datasets in the database).
        get_latest_experiment_id: Get the latest experiment_id.
        get_base_experiments_count: [Deprecated] Get the total number of performed experiments (number of datasets in the database).
        close: Close the connection to the database.
    """

    def __init__(self, argv: list[str], dbname: str = None, resume: bool = False, nostore: bool = False, column_names = None):
        """
        Default constructor of the Database class.

        Parameters:
            argv: Arguments that were supplied to the main-script. These arguments are stored as metadata when the database is instantiated.
            dbname: Name of the database to be generated.
            resume: Resume a previous run and write the results into the previously generated database
            nostore: Do not store the results in a database (can be used for debugging).
        """
        self.nostore = nostore
        if not os.path.isdir('databases'):
            os.mkdir("databases")

        if resume and dbname is None:
            list_of_files = glob.glob('databases/*.sqlite')
            latest_file = max(list_of_files, key=os.path.getctime)[10:]
            print(f"[+] Resuming previous database {latest_file}")
            self.dbname = latest_file
        elif dbname is None:
            script_name = os.path.basename(sys.argv[0])
            self.dbname = f"{script_name}_%s.sqlite" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        else:
            self.dbname = dbname

        self.con = sqlite3.connect("databases/" + self.dbname)
        self.cur = self.con.cursor()
        self.argv = argv
        self.column_names = column_names
        if column_names is None:
            self.column_names = ["delay", "length"]
        if not resume and dbname is None:
            columns = ", ".join(f"{col} integer" for col in self.column_names)
            self.cur.execute(f"CREATE TABLE experiments(id integer, {columns}, color text, response blob)")
            self.cur.execute("CREATE TABLE metadata (stime_seconds integer, argv blob)")

        self.base_row_count = self.get_latest_experiment_id()
        if self.base_row_count is None:
            self.base_row_count = 0
        if resume or dbname is not None:
            print(f"[+] Number of experiments in previous database: {self.base_row_count}")

    def insert(self, *dataset):
        """
        Method to insert datapoints into the SQLite database.

        Parameters:
            dataset: Dataset consisting of experiment_id, delay, length, [additional parameters, ...], color and response.
                - experiment_id: ID of the experiment to insert into the database.
                - delay: Time from trigger until the glitch is set (in nano seconds).
                - length: Length of glitch (in nano seconds).
                - color: Color with which the parameter point (delay, length) is to be displayed in the graph.
                - response: Byte string of target response. 
        """
        if len(dataset) < 4:
            raise Exception("Database.insert: Too less arguments given.")
        experiment_id = dataset[0]
        if not self.nostore:
            if (experiment_id + self.base_row_count) == 0:
                s_argv = ' '.join(self.argv[1:])
                self.cur.execute("INSERT INTO metadata (stime_seconds,argv) VALUES (?,?)", [int(time.time()), s_argv])
            parameters = dataset[1:-2]
            color = dataset[-2]
            response = dataset[-1]
            #print(f"{experiment_id}, {parameters}, {color}, {response}")
            columns = ",".join(f"{col}" for col in self.column_names)
            values = [experiment_id + self.base_row_count, color, response]
            # insert the parameters after position 1
            values[1:1] = parameters
            #print(values)
            qmarks = ",".join("?" for _ in range(len(values)))
            #print(qmarks)
            #print(f"INSERT INTO experiments (id,{columns},color,response) VALUES ({qmarks})")
            self.cur.execute(f"INSERT INTO experiments (id,{columns},color,response) VALUES ({qmarks})", values)
            self.con.commit()

    def get_parameters_of_experiment(self, experiment_id: int) -> list:
        """
        Get the parameters of a dataset by experiment_id.

        Parameters:
            experiment_id: ID of the experiment to insert into the database.

        Returns:
            List of parameters.
        """
        self.cur.execute("SELECT * FROM experiments WHERE id = (?);", [experiment_id + self.base_row_count])
        self.con.commit()
        return next(self.cur, [None])

    def remove(self, experiment_id: int):
        """
        Remove a parameter point from the database by experiment_id.

        Parameters:
            experiment_id: ID of the experiment to insert into the database.
        """
        self.cur.execute("DELETE FROM experiments WHERE id = (?);", [experiment_id + self.base_row_count])
        self.con.commit()

    def cleanup(self, color):
        """
        Remove all parameter points with a given color.
        """
        self.cur.execute("DELETE FROM experiments WHERE color = (?);", [color])
        #self.cur.execute("DELETE FROM experiments WHERE length >= (?);", [color])
        self.con.commit()

    def get_number_of_experiments(self) -> int:
        """
        Get the total number of performed experiments (number of datasets in the database).

        Returns:
            Number of experiments performed so far in the current database.
        """
        self.cur.execute("SELECT count(id) FROM experiments")
        result = self.cur.fetchone()
        row_count = result[0]
        return row_count

    def get_latest_experiment_id(self) -> int:
        """
        Get the latest experiment_id.

        Returns:
            Experiment ID.
        """
        self.cur.execute("SELECT * FROM experiments WHERE id=(SELECT max(id) FROM experiments);")
        self.con.commit()
        return next(self.cur, [None])[0]

    def get_base_experiments_count(self) -> int:
        """
        [Deprecated] Get the total number of performed experiments (number of datasets in the database).

        Returns:
            Number of experiments performed so far in the current database.
        """
        return self.base_row_count

    def close(self):
        """
        Close the connection to the database.
        """
        self.con.close()

class Serial():
    r"""
    Class to manage serial connections more easily.
    Example usage:

        # import Serial from findus
        from findus import Serial
        ser = Serial(port="/dev/ttyUSB0")
        ser.write(b'\x7f')
        ...
        result = ser.read(3)

    Methods:
        __init__: Default constructor.
        write: Write data out via the serial interface.
        read: Read data from the serial interface.
        reset: Reset target via DTR pin and flush data lines.
        flush: Flush data buffers.
        flush_v2: Flush serial data buffers with timeout.
        close: Close serial connection.
    """
    def __init__(self, port:str = "/dev/ttyUSB0", baudrate:int = 115200, timeout:float = 0.1, bytesize:int = 8, parity:str = 'N', stopbits:int = 1):
        """
        __init__: Default constructor.

        Parameters:
            port: Port identifier of the serial connection.
            baudrate: Baudrate of the serial connection.
            timeout: Timeout after the serial connection stops listening.
            bytesize: Number of bytes per payload.
            parity: Even ('E') or Odd ('O') parity.
            stopbits: Number of stop bits.
        """
        self.ser = None
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.init()

    def init(self):
        """
        Initializes the serial connection. Can be called again, if the connection was closed previously.
        """
        try:
            self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout, bytesize=self.bytesize, parity=self.parity, stopbits=self.stopbits)
        except Exception as _:
            print("[-] Serial device not found. Aborting")
            sys.exit(-1)

    def write(self, message: bytes) -> int:
        """
        Write the bytes data to the port. This should be of type `bytes` (or compatible such as `bytearray` or `memoryview`). Unicode strings must be encoded (e.g. `'hello'.encode('utf-8')`.

        Parameters:
            message: Data to send
        Returns:
            Number of bytes written.
        """
        return self.ser.write(message)

    def read(self, length: int) -> bytes:
        """
        Read `length` bytes from the serial port. If a timeout is set it may return fewer characters than requested. With no timeout it will block until the requested number of bytes is read.

        Parameters:
            length: Number of bytes to read.
        Returns:
            Bytes read from the port.
        """
        response = self.ser.read(length)
        return response
    
    def readline(self) -> bytes:
        r"""
        Read up to one line, including the \n at the end.

        Returns:
            The line received from the target.
        """
        response = self.ser.readline()
        return response

    def reset(self, debug:bool = False) -> bool:
        """
        Reset target via DTR pin and flush data lines. Can be used alternatively to the reset lines of the Pico Glitcher (or ChipWhisperer Husky, or ChipWhisperer Pro) to reset the target.

        Parameters:
            debug: If set to true, garbage on the serial interface is plotted to tty.
        """
        print("[+] Resetting target...")
        self.ser.dtr = True
        time.sleep(0.1)
        self.ser.dtr = False
        response = self.ser.read(4096)
        if debug:
            for line in response.splitlines():
                print('\t', line.decode())

    def flush(self):
        """
        Flush serial data buffers.
        """
        self.ser.reset_input_buffer()

    def flush_v2(self, timeout:float = 0.01):
        """
        Flush serial data buffers with timeout.

        Parameters:
            timeout: Timeout after the serial connection stops listening. Can be tweaked to make sure all data is flushed.
        """
        self.ser.timeout = timeout
        self.ser.read(8192)
        self.ser.timeout = self.timeout

    def close(self):
        """
        Close serial connection.
        """
        self.ser.close()

class MicroPythonScript():
    def __init__(self, port:str = '/dev/ttyACM1', debug:bool = False):
        self.port   = None
        self.pyb    = None
        self.debug = debug

    def init(self, port:str, micropy_script:str, debug:bool = False):
        self.port = port
        try:
            self.pyb = pyboard.Pyboard(self.port)
        except Exception as _:
            print("[-] Pico Glitcher not found. Aborting")
            sys.exit(-1)
        self.pyb.enter_raw_repl()
        self.pyb.exec(f'import {micropy_script}')
        self.pyb.exec(f'mp = {micropy_script}.{micropy_script}()')

# inherit functionality and overwrite some functions
class PicoGlitcherInterface(MicroPythonScript):
    def get_firmware_version(self):
        version_bytes = self.pyb.exec('mp.get_firmware_version()')
        decoded_str = version_bytes.decode('utf-8').strip()
        return ast.literal_eval(decoded_str)

    def set_trigger(self, mode:str, pin_trigger:str):
        self.pyb.exec(f'mp.set_trigger("{mode}", "{pin_trigger}")')

    def set_frequency(self, frequency:int):
        self.pyb.exec(f'mp.set_frequency({frequency})')

    def get_frequency(self):
        return self.pyb.exec('mp.get_frequency()')

    def set_baudrate(self, baud:int):
        self.pyb.exec(f'mp.set_baudrate({baud})')

    def set_number_of_bits(self, number_of_bits:int):
        self.pyb.exec(f'mp.set_number_of_bits({number_of_bits})')

    def set_pattern_match(self, pattern:int):
        self.pyb.exec(f'mp.set_pattern_match({pattern})')

    def power_cycle_target(self, power_cycle_time:float):
        self.pyb.exec(f'mp.power_cycle_target({power_cycle_time})')

    def arm(self, delay:int, length:int):
        self.pyb.exec(f'mp.arm({delay}, {length})')

    def arm_multiplexing(self, delay:int, mul_config:dict):
        return self.pyb.exec(f'mp.arm_multiplexing({delay}, {mul_config})')

    def arm_pulseshaping_from_config(self, delay:int, ps_config:list[list[int]]):
        return self.pyb.exec(f'mp.arm_pulseshaping_from_config({delay}, {ps_config})')

    def arm_pulseshaping_from_spline(self, delay:int, xpoints:list[int], ypoints:list[float]):
        return self.pyb.exec(f'mp.arm_pulseshaping_from_spline({delay}, {xpoints}, {ypoints})')

    def arm_pulseshaping_from_lambda(self, delay:int, ps_lambda:str, pulse_number_of_points:int):
        return self.pyb.exec(f'mp.arm_pulseshaping_from_lambda({delay}, {ps_lambda}, {pulse_number_of_points})')

    def arm_pulseshaping_from_list(self, delay:int, pulse:list[int]):
        return self.pyb.exec(f'mp.arm_pulseshaping_from_list({delay}, {pulse})')

    def reset_target(self):
        self.pyb.exec('mp.reset_target()')

    def release_reset(self):
        self.pyb.exec('mp.release_reset()')

    def disable_vtarget(self):
        self.pyb.exec('mp.disable_vtarget()')

    def enable_vtarget(self):
        self.pyb.exec('mp.enable_vtarget()')

    def reset(self, reset_time:float):
        self.pyb.exec(f'mp.reset({reset_time})')

    def block(self, timeout:float):
        self.pyb.exec(f'mp.block({timeout})')

    def get_sm1_output(self) -> str:
        return self.pyb.exec('mp.get_sm1_output()')

    def set_lpglitch(self):
        self.pyb.exec('mp.set_lpglitch()')

    def set_hpglitch(self):
        self.pyb.exec('mp.set_hpglitch()')

    def set_multiplexing(self):
        self.pyb.exec('mp.set_multiplexing()')

    def set_pulseshaping(self, vinit=1.8):
        self.pyb.exec(f'mp.set_pulseshaping({vinit})')

    def do_calibration(self, vhigh:float):
        self.pyb.exec(f'mp.do_calibration({vhigh})')

    def apply_calibration(self, vhigh:float, vlow:float, store:bool = True):
        self.pyb.exec(f'mp.apply_calibration({vhigh}, {vlow}, {store})')

    def waveform_generator(self, frequency:int, gain:float, waveid:int):
        return self.pyb.exec(f'mp.waveform_generator({frequency}, {gain}, {waveid})')

    def set_dead_zone(self, dead_time:float, pin_condition:str):
        self.pyb.exec(f'mp.set_dead_zone({dead_time}, "{pin_condition}")')

    def change_config_and_reset(self, key, value) -> str:
        return self.pyb.exec(f'mp.change_config_and_reset("{key}", "{value}")')

    def arm_adc(self):
        self.pyb.exec('mp.arm_adc()')

    def get_adc_samples(self) -> list[int]:
        return self.pyb.exec('mp.get_adc_samples()')

    def configure_adc(self, number_of_samples:int = 1024, sampling_freq:int = 500_000):
        self.pyb.exec(f'mp.configure_adc({number_of_samples}, {sampling_freq})')

    def stop_core1(self):
        self.pyb.exec('mp.stop_core1()')

    def hard_reset(self):
        self.pyb.exec('mp.hard_reset()')

class ExternalPowerSupply:
    """
    Wrapper class for the RD6006 voltage supply to align function names with the rest of the library.
    Example usage:
    
        from findus import ExternalPowerSupply
        power_supply = ExternalPowerSupply(port="/dev/ttyACM0")
        power_supply.set_voltage(ext_power_voltage)
        print(power_supply.status())
        power_supply.power_cycle_target(power_cycle_time)

    Methods:
        __init__: Default constructor.
        status: Get the status of the voltage supply.
        set_voltage: Set the voltage.
        enable_vtarget: Enable voltage output.
        disable_vtarget: Disable voltage output
        power_cycle_target: Power cycle the target (disables output, waits a certain time, enables voltage output again).
    """

    def __init__(self, port:str):
        """
        Default constructor.
        
        Parameters:
            port: Port identifier of the voltage supply.
        """
        self.port = port
        self.r = RD6006(self.port)

    def status(self) -> str:
        """
        Get the status of the voltage supply.

        Returns:
            Status message of the voltage supply.
        """
        return self.r.status()

    def set_voltage(self, voltage:float):
        """
        Set the voltage of the power supply.
        
        Parameters:
            voltage: Desired output voltage.
        """
        try:
            self.r.voltage = voltage
            self.r.enable = True
        except Exception as _:
            pass

    def enable_vtarget(self):
        """
        Enable voltage output.
        """
        self.r.enable = True

    def disable_vtarget(self):
        """
        Disable voltage output.
        """
        self.r.enable = False

    def power_cycle_target(self, power_cycle_time:float = 0.2):
        """
        Power cycle the target (disables output, waits a certain time, enables voltage output again).
        
        Parameters:
            power_cycle_time: Time to wait between disabling and enabling the voltage output again.
        """
        self.r.enable = False
        time.sleep(power_cycle_time)
        self.r.enable = True

class Glitcher():
    """
    Glitcher template class. This class defines a common anchestor from which other glitcher modules should inherit from.

    Methods:
        __init__: Default constructor. Does nothing in this case.
        classify: Template method to classify an output state.
        colorize: Returns a colored string depending on a color identifier (G, Y, R, M, C, B).
        get_speed: Calculate and return the average speed of the glitching campaign (glitches per second).
    """
    def __init__(self):
        """
        Default constructor. Does nothing in this case.
        """
        pass

    def classify(self, state:type(Enum)) -> str:
        """
        Template method to classify an output state. Overload this class if you want to customize the targets response classification. Alternatively, use the built-in class `GlitchState` to characterize the targets responses. Remember to define certain response states depending on the possible responses. See class `BootloaderCom` for an example.

            from findus import PicoGlitcher
            from findus.BootloaderCom import BootloaderCom, GlitchState
            glitcher = PicoGlitcher()
            ...
            bootcom = BootloaderCom(port="/dev/ttyACM1")
            ...
            response = bootcom.init_bootloader()
            ...
            glitcher.classify(response)
        """
        if issubclass(type(state), ExpectedType):
            color = 'G'
        elif issubclass(type(state), SuccessType):
            color = 'R'
        elif issubclass(type(state), OKType):
            color = 'M'
        elif issubclass(type(state), ErrorType):
            color = 'Y'
        elif issubclass(type(state), WarningType):
            color = 'C'
        return color

    def colorize(self, s:str, color:str) -> str:
        """
        Returns a colorized string depending on a color identifier (G, Y, R, M, C, B, O, Z).
        
        Parameters:
            s: The string you want to colorize.
            color: Color identifier, one of 'G', 'Y', 'R', 'M', 'C', 'B', 'O', 'Z' (black).
        Returns:
            Returns the colorized string.
        """
        colors = {
            'G': [182, 214, 168],
            'Y': [232, 237, 164],
            'R': [228, 145, 167],
            'M': [234, 192, 226],
            'C': [113, 198, 177],
            'B': [109, 174, 217],
            'O': [197, 148, 124],
            'Z': [31, 31, 31]
        }
        #colors = {
        #    'G': [0, 255, 0],
        #    'Y': [255, 255, 0],
        #    'R': [170, 0, 0],
        #    'M': [255, 0, 255],
        #    'C': [0, 255, 255],
        #    'B': [0, 0, 255],
        #    'O': [255, 100, 50],
        #    'Z': [0, 0, 0]
        #}
        r = colors[color][0]
        g = colors[color][1]
        b = colors[color][2]
        return f"\033[38;2;{r};{g};{b}m{s}\033[0m"

    def get_speed(self, start_time:int, number_of_experiments:int) -> int:
        """
        Calculate and return the average speed of the glitching campaign (glitches per second).
        
        Parameters:
            start_time: Start time of the glitching campaign in seconds.
            number_of_experiments: Number of experiments carried out so far.
        Returns:
            Returns the average number of experiments per second.
        """
        elapsed_time = int(time.time()) - start_time
        if elapsed_time == 0:
            return 'NA'
        else:
            return number_of_experiments // elapsed_time

class PicoGlitcher(Glitcher):
    """
    Class giving access to the functions of the Pico Glitcher. Derived from Glitcher class.
    For an example, connect the Pico Glitcher as follows:

    - Remove any capacitors on your target device that could infere with the glitch.
    - Set the desired output voltage `VTARGET` with the micro switch.
    - Connect `VTARGET` with the voltage input of your target (`VCC`).
    - Connect the `GLITCH` output (either the SMA connector or the pin header) to an appropriate target pin, for example `VCC`.
    - Connect the `RESET` output with the target's reset input.
    - Connect the `RESET` line with the `TRIGGER` input.
    
    Code snippet:

        from findus import PicoGlitcher
        glitcher = PicoGlitcher()
        glitcher.init(port="/dev/ttyACM0", ext_power="/dev/ttyACM1", ext_power_voltage=3.3)
        # set up database, define delay and length
        ...
        # one shot glitching
        glitcher.arm(delay, length)
        # reset target for 0.01 seconds (the rising edge on reset line triggers the glitch)
        glitcher.reset(0.01)
        # read the response from the device (for example UART, SWD, etc.)
        response = ...
        # classify the response and put into database
        color = glitcher.classify(response)
        database.insert(experiment_id, delay, length, color, response)

    Methods:
        __init__: Default constructor. Does nothing in this case.
        init: Default initialization procedure.
        arm: Arm the Pico Glitcher and wait for trigger condition.
        block: Block the main script until trigger condition is met. Times out.
        reset: Reset the target via the Pico Glitcher's `RESET` output.
        release_reset: Release the reset to the target via the Pico Glitcher's `RESET` output.
        power_cycle_target: Power cycle the target via the Pico Glitcher `VTARGET` output.
        power_cycle_reset: Power cycle and reset the target via the Pico Glitcher `RESET` and `VTARGET` output.
        reset_and_eat_it_all: Reset the target and flush the serial buffers.
        reset_wait: Reset the target and read from serial.
        set_lpglitch: Enable low-power MOSFET for glitch generation.
        set_hpglitch: Enable high-power MOSFET for glitch generation.
        rising_edge_trigger: Configure the Pico Glitcher to trigger on a rising edge on the `TRIGGER` line.
        uart_trigger: Configure the Pico Glitcher to trigger when a specific byte pattern is observed on the `TRIGGER` line.
        set_cpu_frequency: Set the CPU frequency of the Raspberry Pi Pico.
        get_cpu_frequency: Get the current CPU frequency of the Raspberry Pi Pico.
        __del__: Default deconstructor. Disconnects Pico Glitcher.
    """
    def __init__(self):
        """
        Default constructor. Does nothing in this case.
        """
        self.pico_glitcher = None

    def __del__(self):
        print("[+] Terminating gracefully.")
        try:
            self.stop_core1()
            self.hard_reset()
        except Exception as _:
            pass

    def init(self, port:str, ext_power:str = None, ext_power_voltage:float = 3.3):
        """
        Default initialization procedure of the Pico Glitcher. Default configuration is:

        - Set the trigger input to rising-edge trigger on `TRIGGER` input and assume triggering when the reset is released.
        - Set a dead time that prohibits triggering within a certain time (trigger rejection). This is intended to exclude false trigger conditions.
        - Use the high-power crowbar MOSFET.

        Parameters:
            port: Port identifier of the Pico Glitcher.
            ext_power: Port identifier of the external power supply (RD6006). If None, target is assumed to be supplied by `VTARGET` of the Pico Glitcher.
            ext_power_voltage: Supply voltage of the external power supply. Must be used in combination with `ext_power`. You can not control the supply voltage `VTARGET` of the Pico Glitcher with this parameter.
        """
        self.pico_glitcher = PicoGlitcherInterface()
        self.pico_glitcher.init(port, 'PicoGlitcher')

        # check compatibility
        try:
            pg_fw_version = self.pico_glitcher.get_firmware_version()
            fi_fw_version = list(map(int, version("findus").split('.')))
            print(f"[+] Version of Pico Glitcher: {pg_fw_version}")
            print(f"[+] Version of findus: {fi_fw_version}")
            # check only major and minor version, but not the build number
            if pg_fw_version[:2] != fi_fw_version[:2]:
                raise Exception("Version mismatch")
        except Exception as _:
            print("[-] Fatal error: Versions of findus and Pico Glitcher do not match.")
            print("[*] Update the Pico Glitcher firmware and findus software. See README.md.")
            print("[*] pip install --upgrade findus")
            print("[*] cd .venv/lib/python3.xx/site-packages/findus/firmware")
            print("[*] upload --port /dev/tty.<rpi-tty-port> --files AD910X.py FastADC.py PicoGlitcher.py PulseGenerator.py Spline.py <config-version>/config.json")
            sys.exit(-1)

        self.pico_glitcher.set_trigger("tio", "default")
        self.pico_glitcher.set_dead_zone(0, "default")
        self.pico_glitcher.set_frequency(200_000_000)
        self.pico_glitcher.set_hpglitch()
        if rd6006_available and ext_power is not None:
            self.pico_glitcher.disable_vtarget()
            self.power_supply = ExternalPowerSupply(port=ext_power)
            self.power_supply.set_voltage(ext_power_voltage)
            print(self.power_supply.status())
        else:
            self.pico_glitcher.enable_vtarget()
            self.power_supply = None

    def arm(self, delay:int, length:int):
        """
        Arm the Pico Glitcher and wait for the trigger condition. The trigger condition can either be when the reset on the target is released or when a certain pattern is observed in the serial communication.

        Parameters:
            delay: Glitch is emitted after this time. Given in nano seconds. Expect a resolution of about 5 nano seconds.
            length: Length of the glitch in nano seconds. Expect a resolution of about 5 nano seconds.
        """
        self.pico_glitcher.arm(delay, length)

    def arm_multiplexing(self, delay:int, mul_config:dict):
        """
        Arm the Pico Glitcher and wait for the trigger condition. The trigger condition can either be when the reset on the target is released or when a certain pattern is observed in the serial communication. Only available for hardware revision 2 and later.

        Parameters:
            delay: Glitch is emitted after this time. Given in nano seconds. Expect a resolution of about 5 nano seconds.
            mul_config: The dictionary for the multiplexing profile with pairs of identifiers and values. For example, this could be `{"t1": 10, "v1": "GND", "t2": 20, "v2": "1.8", "t3": 30, "v3": "GND", "t4": 40, "v4": "1.8"}`. Meaning that when triggered, a GND-voltage pulse with duration of `10ns` is emitted, followed by a +1.8V step with duration of `20ns` and so on.
        """
        self.pico_glitcher.arm_multiplexing(delay, mul_config)

    def arm_pulseshaping_from_config(self, delay:int, ps_config:list[list[int]]):
        """
        Arm the Pico Glitcher and wait for the trigger condition. The trigger condition can either be when the reset on the target is released or when a certain pattern is observed in the serial communication. Only available for hardware revision 2 and later. Additionally, the Pulse Shaping Expansion board is needed.

        Parameters:
            delay: Glitch is emitted after this time. Given in nano seconds. Expect a resolution of about 5 nano seconds.
            ps_config: The pulse configuration given as a list of time deltas and voltage values.

        Example:

            ps_config = [[4*length, 1.8], [4*length, 0.95], [length, 0.0]]
            glitcher.arm_pulseshaping_from_config(delay, ps_config)
        """
        return self.pico_glitcher.arm_pulseshaping_from_config(delay, ps_config)

    def arm_pulseshaping_from_spline(self, delay:int, xpoints:list[int], ypoints:list[float]):
        """
        Arm the Pico Glitcher and wait for the trigger condition. The pulse definition is given by time and voltage points. Intermediate values are interpolated.

        Parameters:
            delay: Glitch is emitted after this time. Given in nano seconds. Expect a resolution of about 5 nano seconds.
            xpoints: A list of time points (in nanoseconds) where voltage changes occur.
            ypoints: The corresponding voltage levels at each time point.

        Example:

            xpoints = [0,   100, 200, 300, 400, 500, 515, 520]
            ypoints = [3.0, 2.1, 2.0, 2.0, 1.7, 0.0, 2.0, 3.0]
            glitcher.arm_pulseshaping_from_spline(delay, xpoints, ypoints)
        """
        return self.pico_glitcher.arm_pulseshaping_from_spline(delay, xpoints, ypoints)

    def arm_pulseshaping_from_lambda(self, delay:int, ps_lambda:str, pulse_number_of_points:int):
        """
        Arm the Pico Glitcher and wait for the trigger condition. Generate the pulse from a lambda function depending on the time.

        Parameters:
            delay: Glitch is emitted after this time. Given in nano seconds. Expect a resolution of about 5 nano seconds.
            ps_lambda: A lambda function that defines the glitch at certain times. Must be given as string which is processed by the Pico Glitcher at runtime.
            pulse_number_of_points: The approximate length of the pulse. This is needed to constrain the pulse and to save computing time.

        Example:

            ps_lambda = f"lambda t:-1.0/({2*length})*t+3.0 if t<{2*length} else 2.0 if t<{4*length} else 0.0 if t<{5*length} else 3.0"
            glitcher.arm_pulseshaping_from_lambda(delay, ps_lambda, 6*length)
        """
        return self.pico_glitcher.arm_pulseshaping_from_lambda(delay, ps_lambda, pulse_number_of_points)

    def arm_pulseshaping_from_list(self, delay:int, pulse:list[int]):
        """
        Arm the Pico Glitcher and wait for the trigger condition. Genereate the pulse from a raw array of values.

        Parameters:
            delay: Glitch is emitted after this time. Given in nano seconds. Expect a resolution of about 5 nano seconds.
            pulse: A raw list of points that define the pulse. No calibration and no constraints are applied to the list. The list is forwarded directly to the DAC.

        Example:

            pulse = [-0x1fff] * 50 + [-0x0fff] * 50 + [-0x07ff] * 50 + [0x0000] * 50
            glitcher.arm_pulseshaping_from_list(delay, pulse)
        """
        return self.pico_glitcher.arm_pulseshaping_from_list(delay, pulse)

    def block(self, timeout:float = 1.0):
        """
        Block until trigger condition is met. Raises an exception if times out.
        
        Parameters:
            timeout: Time after the block is released.
        """
        self.pico_glitcher.block(timeout)

    def get_sm1_output(self) -> str:
        return self.pico_glitcher.get_sm1_output()

    def reset(self, reset_time:float = 0.2):
        """
        Reset the target via the Pico Glitcher's `RESET` output.
        
        Parameters:
            reset_time: Time how long the target is held in reset.
        """
        self.pico_glitcher.reset(reset_time)

    def release_reset(self):
        """
        Release the reset to the target via the Pico Glitcher's `RESET` output.
        """
        self.pico_glitcher.release_reset()

    def power_cycle_target(self, power_cycle_time:float = 0.2):
        """
        Power cycle the target via the Pico Glitcher `VTARGET` output.
        If available, target is power-cycled by the external power supply RD6006.
        
        Parameters:
            power_cycle_time: Time how long the power supply is cut. If `ext_power` is defined, the external power supply (RD6006) is cycled.
        """
        if self.power_supply is not None:
            self.power_supply.power_cycle_target(power_cycle_time)
        else:
            self.pico_glitcher.power_cycle_target(power_cycle_time)

    def power_cycle_reset(self, power_cycle_time:float = 0.2):
        """
        Power cycle and reset the target via the Pico Glitcher `VTARGET` and `RESET` output. Can also be used to define sharper trigger conditions via the `RESET` line.
        
        Parameters:
            power_cycle_time: Time how long the power supply is cut. If `ext_power` is defined, the external power supply is cycled.
        """
        if self.power_supply is not None:
            self.power_supply.disable_vtarget()
            self.pico_glitcher.reset_target()
            time.sleep(power_cycle_time)
            self.power_supply.enable_vtarget()
            self.pico_glitcher.release_reset()
        else:
            self.pico_glitcher.disable_vtarget()
            self.pico_glitcher.reset_target()
            time.sleep(power_cycle_time)
            self.pico_glitcher.enable_vtarget()
            self.pico_glitcher.release_reset()

    def reset_and_eat_it_all(self, target:serial.Serial, target_timeout:float = 0.3):
        """
        Reset the target via the Pico Glitcher's `RESET` output and flush the serial buffers.
        
        Parameters:
            target: Serial communication object (usually defined as `target = serial.Serial(...)`).
            target_timeout: Time-out of the serial communication. After this time, reading from the serial connection is canceled and it is assumed that there is no more garbage on the line.
        """
        self.pico_glitcher.reset_target()
        target.ser.timeout = target_timeout
        target.read(4096)
        target.ser.timeout = target.timeout
        self.pico_glitcher.release_reset()

    def reset_wait(self, target:serial.Serial, token:bytes, reset_time:float = 0.2, debug:bool = False) -> bytes:
        """
        Reset the target via the Pico Glitchers's `RESET` output and wait until the target responds (read from serial).

        Parameters:
            target: Serial communication object (usually defined as `target = serial.Serial(...)`).
            token: Expected response from target. Read from serial multiple times until target responds.
            reset_time:  Time how long the target is held under reset.
            debug: If `true`, more output is given.

        Returns:
            Returns the target's response.
        """
        self.pico_glitcher.reset_target()
        time.sleep(reset_time)
        self.pico_glitcher.release_reset()
        response = target.read(4096)
        for _ in range(0, 5):
            if token in response:
                break
            response += target.read(4096)
        if debug:
            for line in response.splitlines():
                print('\t', line.decode())
        return response

    def set_lpglitch(self):
        """
        Enable the low-power crowbar MOSFET for glitch generation.

        The glitch output is an SMA-connected output line that is normally connected to a target's power rails. If this setting is enabled, a low-powered MOSFET shorts the power-rail to ground when the glitch module's output is active.
        """
        self.pico_glitcher.set_lpglitch()

    def set_hpglitch(self):
        """
        Enable the high-power crowbar MOSFET for glitch generation.
        
        The glitch output is an SMA-connected output line that is normally connected to a target's power rails. If this setting is enabled, a high-powered MOSFET shorts the power-rail to ground when the glitch module's output is active.
        """
        self.pico_glitcher.set_hpglitch()

    def set_multiplexing(self):
        """
        Enables the multiplexing mode of the Pico Glitcher version 2 to quickly switch between different voltage levels.
        """
        self.pico_glitcher.set_multiplexing()

    def set_pulseshaping(self, vinit:float=1.8):
        """
        Enables the pulse-shaping mode of the Pico Glitcher version 2 to apply a voltage profile to the target's supply voltage.

        Parameters:
            vinit: The initial voltage (voltage offset) to base the calculations on. This does not change the output voltage of the pulse shaping expansion board. However, this parameter is used to calculate the correct offsets and scaling of the pulse.
        """
        self.pico_glitcher.set_pulseshaping(vinit)

    def do_calibration(self, vhigh:float):
        """
        Emit a calibration pulse with the Pico Glitcher Pulse Shaping expansion board to determine `vhigh` and `vlow`. These parameters are used to calculate the offset and gain parameters of the DAC.

        Parameters:
            vhigh: The initial voltage to perform the calibration with. Default is `1V`.
        """
        self.pico_glitcher.do_calibration(vhigh)

    def apply_calibration(self, vhigh:float, vlow:float, store:bool = True):
        """
        Calculate and store the offset and gain parameters that were determined by the calibration routine. These values are stored in `config.json` and must be re-calculated if the config is overwritten.

        Parameters:
            vhigh: The maximum voltage of the calibration voltage trace.
            vlow: The minimum voltage of the calibration voltage trace.
            store: wether to store the offset and gain factor in the Pico Glitcher configuration.
        """
        self.pico_glitcher.apply_calibration(vhigh, vlow, store)

    def rising_edge_trigger(self, pin_trigger:str = "default", dead_time:float = 0, pin_condition:str = "default"):
        """
        Configure the Pico Glitcher to trigger on a rising edge on the `TRIGGER` line.
        
        Parameters:
            pin_trigger: The trigger pin to use. Can either be "default" (default `TRIGGER` input) or "alt" (alternative trigger input `TRIGGER1`). For hardware version 2 options "ext1" or "ext2" are also available.
            dead_time: Set a dead time that prohibits triggering within a certain time (trigger rejection). This is intended to exclude false trigger conditions. Can also be set to 0 to disable this feature.
            pin_condition: The rejection time is generated internally by measuring the state of the `power` or `reset` pin of the Pico Glitcher. If you want to trigger on the reset condition, set `pin_condition = 'reset'`, else if you want to trigger on the target power set `pin_condition = 'power'`. If `dead_time` is set to zero and `pin_condition = 'default'`, this parameter is ignored.
        """
        self.pico_glitcher.set_trigger("tio", pin_trigger)
        self.pico_glitcher.set_dead_zone(dead_time, pin_condition)

    def uart_trigger(self, pattern:int, baudrate:int = 115200, number_of_bits:int = 8, pin_trigger:str = "default"):
        """
        Configure the Pico Glitcher to trigger when a specific byte pattern is observed on the `TRIGGER` line.
        
        Parameters:
            pattern: Byte pattern that is transmitted on the serial lines to trigger on. For example `0x11`.
            baudrate: The baudrate of the serial communication.
            number_of_bits: The number of bits of the UART payload.
            pin_trigger: The trigger pin to use. Can be either "default" or "alt". For hardware version 2 options "ext1" or "ext2" can also be chosen.
        """
        self.pico_glitcher.set_trigger("uart", pin_trigger)
        self.pico_glitcher.set_baudrate(baudrate)
        self.pico_glitcher.set_number_of_bits(number_of_bits)
        self.pico_glitcher.set_pattern_match(pattern)

    def set_cpu_frequency(self, frequency:int = 200_000_000):
        """
        Set the CPU frequency of the Raspberry Pi Pico.
        
        Parameters:
            frequency: the CPU frequency.
        """
        self.pico_glitcher.set_frequency(frequency)

    def get_cpu_frequency(self) -> int:
        """
        Get the current CPU frequency of the Raspberry Pi Pico.
        
        Returns:
            Returns the CPU frequency.
        """
        return self.pico_glitcher.get_frequency()

    def change_config_and_reset(self, key:str, value:int|float|str):
        """
        Change the content of the configuration file `config.json`. Note that the value to be changed must already exist. After calling this function, the Pico Glitcher must be re-initialized.

        Parameters:
            key: Key of value to be replacedl.
            value: Value to be set.
        """
        return self.pico_glitcher.change_config_and_reset(key, value)

    def waveform_generator(self, frequency:int, gain:float, waveid:int):
        """
        The Pulse Shaping expansion board of the Pico Glitcher v2 can be used to generate arbitrary and continous waveforms as well.

        Parameters:
            frequency: The frequency of the signal.
            gain: The gain (overall amplitude) of the signal.
            waveid: This determines the signal type, that is, what signal should be generated.

        - sine wave: `waveid = 0`
        - cosine wave: `waveid = 1`
        - triangle: `waveid = 2`
        - positive sawtooth: `waveid = 3`
        - negative sawtooth: `waveid = 4`
        """
        self.pico_glitcher.waveform_generator(frequency, gain, waveid)

    def arm_adc(self):
        """
        Arm the ADC on pin 26 and capture ADC samples if the trigger condition is met. On Pico Glitcher hardware version 1, the separate SMA connector labeled `Analog` can be used to measure analog voltage traces. On revision 2, the analog input is directly connected to the `GLITCH` line.
        """
        self.pico_glitcher.arm_adc()

    def get_adc_samples(self) -> list[int]:
        """
        Read back the captured ADC samples.
        """
        samples = self.pico_glitcher.get_adc_samples()
        #print(samples)
        decoded_str = samples.decode().strip()
        num_str = decoded_str.split("[")[1].split("]")[0]
        int_list = [int(x) for x in num_str.split(",")]
        return int_list

    def configure_adc(self, number_of_samples:int = 1024, sampling_freq:int = 500_000):
        """
        Configure the onboard ADC of the Pico Glitcher.

        Parameters:
            number_of_samples: The number of samples to capture after triggering.
            sampling_freq: The sampling frequency of the ADC. `500 kSPS` is the maximum.
        """
        self.pico_glitcher.configure_adc(number_of_samples, sampling_freq)

    def stop_core1(self):
        """
        Stop execution on the second core of the Pico Glitcher (Raspberry Pi Pico).
        """
        self.pico_glitcher.stop_core1()

    def hard_reset(self):
        """
        Perform a hard reset of the Pico Glitcher (Raspberry Pi Pico).
        """
        try:
            self.pico_glitcher.hard_reset()
        except Exception as _:
            pass

class Helper():
    """
    Helper class that provides useful functions.
    Example usage:
    
        from findus import Helper as helper
        filename = f"{helper.timestamp()}_memory_dump.bin"

    Methods:
        timestamp: Provides the current timestamp in a file-friendly format.
    """
    def timestamp() -> str:
        """
        Provides the current timestamp in a file-friendly format.
        
        Returns:
            Returns the current timestamp in the format %Y-%m-%d_%H-%M-%S.
        """
        return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

class Parameterspace():
    def __init__(self, parameter_boundaries:list[tuple[float, float]], parameter_divisions:list[int]):
        # sanity checks
        if len(parameter_boundaries) != len(parameter_divisions):
            raise Exception(f"Error: parameter_boundaries and parameter_divisions have different lengths ({len(parameter_boundaries)} vs. {len(parameter_divisions)}).")
        for tup in parameter_boundaries:
            if tup[0] > tup[1]:
                raise Exception(f"Error: Upper bound {tup[1]} is lower than lower bound {tup[0]}.")
        self.parameter_boundaries = parameter_boundaries
        self.parameter_divisions = parameter_divisions
        self.cardinality = 1
        for num in self.parameter_divisions:
            self.cardinality *= num
        self.weights_per_bin = [0 for x in range(self.cardinality)]

    def get_cardinality(self):
        return self.cardinality

    def get_bin_assignment(self, *parameter:float) -> list[int]:
        fact = 1
        bina = 0
        for i in range(len(self.parameter_divisions)):
            division =  self.parameter_divisions[i]
            # xdelta = (xmax - xmin) / xdiv
            delta = (self.parameter_boundaries[i][1] - self.parameter_boundaries[i][0]) / division
            bin_number = int((parameter[i] - self.parameter_boundaries[i][0]) / delta)
            #print(f"par = {parameter[i]}, delta = {delta}, bina = {bin_number}")
            if i > 0:
                fact *= self.parameter_divisions[i - 1]
            bina += fact * bin_number
        return bina

    def add_experiment(self, weight:int, *parameter:float):
        for i in range(len(self.parameter_divisions)):
            if parameter[i] < self.parameter_boundaries[i][0] or parameter[i] >= self.parameter_boundaries[i][1]:
                print("[-] Error: parameter out of bounds. Skipping.")
                print(f"[-] Dimension: {i}, lower = {self.parameter_boundaries[i][0]}, upper = {self.parameter_boundaries[i][1]}, parameter = {parameter[i]}")
                return
        bina = self.get_bin_assignment(*parameter)
        self.weights_per_bin[bina] += weight

    def get_weights(self) -> list[int]:
        return self.weights_per_bin

    def get_bin_numbers_sorted_by_weights(self) -> list[int]:
        return sorted(range(len(self.weights_per_bin)), key=lambda i: self.weights_per_bin[i])

    def get_coordinates(self, bin_assignment:int) -> list[int]:
        bin_numbers = []
        reversed_parameter_divisions = list(reversed(self.parameter_divisions))
        fact = self.cardinality
        if bin_assignment > fact:
            raise Exception("Error: bin number exceeds total number of bins.")
        for div in reversed_parameter_divisions:
            c = (fact / div)
            b = int(bin_assignment / c)
            #print(f"bin_assignment = {bin_assignment}, fact = {fact}, div = {div}, (fact / div) = {c}, bin_number = {b}")
            bin_numbers.append(b)
            fact /= div
            bin_assignment -= int(b * c)
        return list(reversed(bin_numbers))

    def get_boundaries_from_coordinates(self, coordinates:list[float]) -> list[tuple[float, float]]:
        boundaries = []
        for i in range(len(self.parameter_divisions)):
            division =  self.parameter_divisions[i]
            delta = (self.parameter_boundaries[i][1] - self.parameter_boundaries[i][0]) / division
            lower = self.parameter_boundaries[i][0] + delta * coordinates[i]
            upper = self.parameter_boundaries[i][0] + delta * (coordinates[i] + 1)
            tup = (lower, upper)
            boundaries.append(tup)
        return boundaries

    def get_boundaries(self, bin_assignment:int) -> list[tuple[float, float]]:
        bin_numbers = self.get_coordinates(bin_assignment)
        return self.get_boundaries_from_coordinates(bin_numbers)

class Individual():
    def __init__(self, parameters:list[int], max_age:int = 10):
        self.parameters = parameters
        self.health = 0
        self.max_age = max_age
        self.age = 0

    def set_genom(self, parameters:list[int]):
        self.parameters = parameters

    def get_genom(self) -> list[int]:
        return self.parameters

    def set_health(self, health:int):
        self.health = health

    def get_health(self) -> int:
        return self.health

    def get_age(self) -> int:
        return self.age

    def get_max_age(self) -> int:
        return self.max_age

    def increase_age(self):
        self.age += 1

class Population():
    def __init__(self, number_of_individuals:int, length_of_genom:int):
        if number_of_individuals < 10:
            raise Exception("Error: Population too small.")

        self.number_of_individuals = number_of_individuals
        self.length_of_genom = length_of_genom

        self.population = [None] * self.number_of_individuals
        for i in range(self.number_of_individuals):
            self.population[i] = self.generate_random_individual()

    def get_number_of_individuals(self) -> int:
        return self.number_of_individuals

    def get_length_of_genom(self) -> int:
        return self.length_of_genom

    def generate_random_individual(self) -> Individual:
        genom = [0] * self.length_of_genom
        for i in range(self.length_of_genom):
            genom[i] = random.uniform(0, 1)
        return Individual(genom)

    def get_individuals(self) -> list[Individual]:
        return self.population

    def set_individuals(self, individuals:list[Individual]):
        self.population = individuals

    def sort_by_health(self):
        self.population = sorted(self.population, key=lambda ind: ind.get_health())

    def update_health(self, health_function):
        for ind in self.population:
            ind.set_health(health_function(ind.get_genom()))
            #print(ind.get_health())

    def breed(self, i:int, j:int) -> Individual:
        geni = self.population[i].get_genom().copy()
        genj = self.population[j].get_genom().copy()
        for k in range(len(geni)):
            select = random.randint(0, 1)
            if select == 1:
                geni[k] = genj[k]
        return Individual(geni)

    def mutate(self, i:int) -> Individual:
        gene = random.randint(0, self.length_of_genom - 1)
        self.population[i].get_genom()[gene] = random.uniform(0, 1)

    def replace(self, i:int, individual:Individual):
        self.population[i] = individual

    def replace_with_random(self, i:int):
        self.population[i] = self.generate_random_individual()

    def kill_and_replace(self):
        for i in range(len(self.population)):
            if self.population[i].get_age() > self.population[i].get_max_age():
                self.population[i] = self.generate_random_individual()

    def increase_age_of_population(self):
        for i in range(len(self.population)):
            self.population[i].increase_age()

class GeneticAlgorithm:
    def __init__(self, parameterspace:Parameterspace, population:Population, health_malus_factor:float = 1):
        self.parameterspace = parameterspace
        self.population = population
        self.health_malus_factor = health_malus_factor

    def get_bins_from_genom(self, parameters:list[int]) -> list[int]:
        bins = [int(x * self.parameterspace.get_cardinality()) for x in parameters]
        return bins

    def health_function(self, parameters:list[int]) -> int:
        bins = self.get_bins_from_genom(parameters)
        """
        Calculates the health of a individual:

            health = Sum(weight_i) - factor * malus * Sum(weight_i)
            health = (1 - factor * malus) * Sum(weight_i)
        """
        # sum up the weights in each bin
        health = 0
        weights = self.parameterspace.get_weights()
        for b in bins:
            health += weights[b]

        # for every bin that occurs more than once, reduce health
        # (forces the algorithm to look into separate bins)
        # malus can maximal be the number of genoms (=bins),
        # therefore it is reasonable to choose health_malus_factor < (1 / number_of_bins)
        counts = {}
        for item in bins:
            counts[item] = counts.get(item, 0) + 1
        malus = 0
        for c in counts:
            if counts[c] > 1:
                malus += counts[c] - 1
        health -= (self.health_malus_factor * malus * health)

        return health

    def get_max_health(self) -> int:
        genom_length = self.population.get_length_of_genom()
        return max(self.parameterspace.get_weights()) * genom_length

    def step(self) -> list[Individual]:
        self.population.increase_age_of_population()
        self.population.update_health(self.health_function)
        self.population.sort_by_health()

        # Step 1: breeding
        number_of_individuals = self.population.get_number_of_individuals()
        child12 = self.population.breed(number_of_individuals - 1, number_of_individuals - 2)
        child21 = self.population.breed(number_of_individuals - 2, number_of_individuals - 1)
        child34 = self.population.breed(number_of_individuals - 3, number_of_individuals - 4)
        child43 = self.population.breed(number_of_individuals - 4, number_of_individuals - 3)
        # replace the individuals with bad health
        self.population.replace(0, child12)
        self.population.replace(1, child21)
        self.population.replace(2, child34)
        self.population.replace(3, child43)

        # Step 2: mutate
        self.population.mutate(0)
        self.population.mutate(2)

        # Step 3: replace weak individuals with random ones
        self.population.replace_with_random(4)
        self.population.replace_with_random(5)

        # Step 4: Kill old individuals
        self.population.kill_and_replace()

        self.population.update_health(self.health_function)
        self.population.sort_by_health()

        return self.population.get_individuals()

    def run(self, threshold:float) -> list[int]:
        maxhealth = self.get_max_health()
        while True:
            individuals = self.step()
            for ind in individuals:
                print(f"health of ind {ind}: {ind.get_health()}")
            print()
            if individuals[0].get_health() >= maxhealth * threshold:
                parameters = individuals[0].get_genom()
                return self.get_bins_from_genom(parameters)

    def get_population(self) -> Population:
        return self.population

    def get_parameterspace(self) -> Parameterspace:
        return self.parameterspace

class OptimizationController():
    """
    Wrapper class for initializing parameter space binning and using the genetic algorithm to search for optimal paramters.

    Methods:
        __init__: Constructor of the OptimizationController. Parameter boundaries and parameter divisions must be provided. Parameters for the genetic algorithm are optional.
        print_best_performing_bins: Output the best performing parameter space bins. In these bins a successful glitch is assumed.
        step: Perform the next step of the genetic algorithm; should be called before every experiment.
        add_experiment: Add the parameters and the outcome (weights) to the parameter space.
    """

    def __init__(self, parameter_boundaries:list[tuple[int, int]], parameter_divisions:list[int], number_of_individuals:int = 10, length_of_genom:int = 20, malus_factor_for_equal_bins:float = 1):
        """
        Constructor of the OptimizationController. Parameter boundaries and parameter divisions must be provided. Parameters for the genetic algorithm are optional.

        Parameters:
            parameter_boundaries: Boundaries of all parameters to look into, for example `[(s_delay, e_delay), (s_t1, e_t1), (s_length, e_length)]`.
            parameter_divisions: Number of how many bins the individual parameter ranges should be divided into, for example `[10, 10, 5]`. Bigger values mean division into smaller bins which increases accuracy at the expense of performance (longer glitching campaign duration).
            number_of_individuals: Number of individuals used simultaneously in the genetic algorithm. Increasing this number improves accuracy at the expense of performance (longer glitching campaign duration).
            length_of_genom: Number of bins to track per individual. The larger the parameter space, the higher this number should be.
            malus_factor_for_equal_bins: Can be used to punish individuals that look into the same bin multiple times. Must be in range [0, 1]. A bigger value means a greater penalty.
        """
        self.par = Parameterspace(parameter_boundaries, parameter_divisions)
        self.pop = Population(number_of_individuals, length_of_genom)
        # renorm the malus factor to the maximum number of genoms,
        # thus malus_factor_for_equal_bins can be chosen between 0 and 1.
        if malus_factor_for_equal_bins > 1 or malus_factor_for_equal_bins < 0:
            print("[-] Error: malus_factor_for_equal_bins must be in range [0, 1].")
            sys.exit(-1)
        factor = malus_factor_for_equal_bins / length_of_genom
        self.opt = GeneticAlgorithm(self.par, self.pop, factor)
        self.i_current_individual = 0
        self.i_current_bin = 0
        self.number_of_individuals = self.pop.get_number_of_individuals()
        self.length_of_genom = self.pop.get_length_of_genom()

    def print_best_performing_bins(self):
        """
        Method that prints an overview of the best performing bins of the parameterspace. Can be called from time to time to obtain an overview of the optimization process.
        """
        number_of_individuals = self.pop.get_number_of_individuals()
        ind0 = self.pop.get_individuals()[number_of_individuals - 1]
        print(f"[+] Individual health = {ind0.get_health()}, age = {ind0.get_age()}")
        print("[+] Best performing bins:")
        genom = ind0.get_genom()
        bins = self.opt.get_bins_from_genom(genom)
        boundaries = []
        for i in range(len(bins)):
            boundary = self.par.get_boundaries(bins[i])
            print(f"    bin = {bins[i]}: {boundary}")
            boundaries.append(boundary)

    def step(self) -> list[int]:
        """
        Perform the next step in the optimization process. Should be called before the next experiment.

        Returns:
            A list of the parameters for the next experiment.
        """
        individuals = self.pop.get_individuals()
        parameters = individuals[self.i_current_individual].get_genom()
        bins = self.opt.get_bins_from_genom(parameters)
        boundaries = self.par.get_boundaries(bins[self.i_current_bin])

        random_numbers = []
        for b in boundaries:
            random_numbers.append(random.uniform(b[0], b[1]))

        # next bin
        self.i_current_bin += 1
        if self.i_current_bin >= self.length_of_genom:
            self.i_current_bin = 0
            # next individual
            self.i_current_individual += 1
            if self.i_current_individual >= self.number_of_individuals:
                self.i_current_individual = 0
                # next age step
                self.pop.set_individuals(self.opt.step())

        return random_numbers

    def add_experiment(self, weight:int, *parameter:int):
        """
        Method to add the parameters and the outcome (weights) to the parameter space. Can be used similarly to the method `Database.insert()`.

        Parameters:
            weight: Weight of the outcome of the experiment. Higher values mean a better performing bin and a better health of the individuals that track that bin.
            parameter: list of parameters that were used for the experiment.
        """
        self.par.add_experiment(weight, *parameter)

class AnalogPlot():
    """
    Class to easily plot captured voltage traces with the ADC.

    Example usage:

        glitcher.configure_adc(number_of_samples=1024, sampling_freq=450_000)
        plotter = AnalogPlot(number_of_samples=1024, sampling_freq=450_000)
        ...
        glitcher.arm_adc()
        ...
        samples = glitcher.get_adc_samples()
        plotter.update_curve(samples)
    """
    def __init__(self, number_of_samples:int, vref:float = 3.3, sampling_freq = 500_000):
        self.number_of_samples = number_of_samples
        self.vref = vref
        self.sampling_freq = sampling_freq

        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.3)

        self.curve_line, = self.ax.plot([], [], label="Analog measurement", color="blue")

        x_end = 1_000_000_000 * self.number_of_samples / self.sampling_freq
        self.xpoints = np.linspace(0, x_end, self.number_of_samples)
        self.ypoints = np.zeros(self.number_of_samples)

        # Set axis limits and finer ticks
        self.ax.set_xlim(-1, x_end)
        self.ax.set_ylim(-0.2, 3.5)
        self.ax.set_xticks(np.arange(0, x_end, x_end / 10))
        self.ax.set_yticks(np.arange(0, 3.4, 0.5))

        self.ax.set_xlabel("Time [ns]")
        self.ax.set_ylabel("Voltage [V]")
        self.ax.legend()
        self.ax.grid(True)

        self.update_curve(self.ypoints)

    def show(self):
        plt.show(block=False)
        plt.pause(0.001)

    def update_curve(self, y:list):
        self.ypoints = np.array(y) / 4096 * self.vref
        self.curve_line.set_data(self.xpoints, self.ypoints)
        self.show()
