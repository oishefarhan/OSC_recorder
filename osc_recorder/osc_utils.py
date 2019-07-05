"""
OSC input/output utility.
Server implementation to capture OSC.
Function implementation to replay OSC.
"""
import time
import logging
import numpy as np

import liblo

from .base import TimeSeriesBundle
from .collector import Collector

log = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)


# *********************************SERVER CLASS**********************************

class CaptureOSCServer(liblo.ServerThread):
    """OSC server to capture OSC data and store.

        Args:
            port (int): Port to listen on.

        Keyword Args:
            debug (bool): Set to True to log captures.
    """

    def __init__(self, port, debug=False):
        super().__init__(port)
        if debug:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)
        log.info("Server started on port %d", port)
        self.collector = Collector()
        self.start_time = None
        self.first_message_captured = False

    @liblo.make_method(None, None)
    def catch_all_callback(self, path, args):
        """Executes when capturing any OSC message.

        Uses Collector to format and store.

        Args:
            path (string): OSC path captured on.
            args (list): list of values to capture.
        """
        log.debug("%s, %s", path, str(args))
        if not self.first_message_captured:
            self.first_message_captured = True
            self.start_time = time.time()
        timestamp = time.time() - self.start_time
        self.collector.collect_samples(path, timestamp, args)

    def get_time_series(self):
        """Converts captured OSC messages to time series bundle format.

        Returns:
            (TimeSeriesBundle): All outputs are TimeSeriesBundles.
        """
        log.info("Converting Data...")
        return self.collector.to_time_series_bundle()


def replay_osc(data, address='127.0.0.1', port=9000, loop=False, debug=False):
    """Replay TimeSeriesBundle data via OSC by waiting.

    Calculates wait time between OSC messages and waits to send message.

    Args:
        data (TimeSeriesBundle): TimeSeriesBundle data.

    Keyword Args:
        address (str): IP address to send to.
        port (int): port to send to.
        loop (bool): set to True to repeat infinitely.
        debug (bool): set to True to print messages.

    """
    try:
        output_thread = liblo.Address(address, port)
        print(f'Replaying OSC to {address}:{port}')
    except liblo.AddressError as err:
        print(str(err))

    if not isinstance(data, TimeSeriesBundle):
        raise "Data type not supported."

    ts_dict = data.to_timestamped_dict()
    timestamps = sorted(ts_dict.keys())
    wait_times = np.diff(timestamps, append=0)

    run_once = True  # guarantee the selection runs once
    while run_once or loop:  # if loop selected, repeat the full replay
        run_once = False

        overhead_time_start = time.time()
        for i, timestamp in enumerate(timestamps):
            msg_list = list()
            for info in ts_dict[timestamp]:
                name = info[0]
                samples = info[1]
                if debug:
                    print("%s:%d -- %f %s %s" %
                          (address, port, timestamp, name, str(samples)))
                msg_list.append(liblo.Message(name, *samples))

            liblo.send(output_thread, *msg_list)

            overhead_time = time.time() - overhead_time_start
            # Avoids discontinous jumps in timestamps
            if wait_times[i] > overhead_time and wait_times[i] < 50:
                # NOTE:
                    # The wait time is still too slow
                    # Manual decrease in wait time
                    # check corresponding jupyter notebook
                time.sleep((wait_times[i] - overhead_time)* 0.8)
            # Starting overhead time immidiately after last call.
            overhead_time_start = time.time()

def replay_osc_time_bundle(data, address='127.0.0.1', port=9000, loop=False, debug=False):
    """Replay TimeSeriesBundle data via OSC. Doesn't wait.

    Sends all the packets at once with the appropriate wait times added to each time tag.
    Supported by many osc libraries that implemented the latest osc protocol update.
    The client can send packets with future timestamps. The server will wait till the
    correct time to actually call the callback functions.

    Args:
        data (TimeSeriesBundle): TimeSeriesBundle data.

    Keyword Args:
        address (str): IP address to send to.
        port (int): port to send to.
        loop (bool): set to True to repeat infinitely.
        debug (bool): set to True to print messages.

    """
    try:
        output_thread = liblo.Address(address, port)
        print(f'Replaying OSC to {address}:{port}')
    except liblo.AddressError as err:
        print(str(err))

    if not isinstance(data, TimeSeriesBundle):
        raise "Data type not supported."

    ts_dict = data.to_timestamped_dict()
    timestamps = sorted(ts_dict.keys())
    start_timestamp = timestamps[0]

    run_once = True  # guarantee the selection runs once
    while run_once or loop:  # if loop selected, repeat the full replay
        run_once = False

        bundle_list = list()
        start_time = liblo.time()
        for timestamp in timestamps:
            msg_list = list()
            for info in ts_dict[timestamp]:
                name = info[0]
                samples = info[1]
                if debug:
                    print("%s:%d -- %f %s %s" %
                          (address, port, timestamp, name, str(samples)))
                msg_list.append(liblo.Message(name, *samples))
            wait_time = timestamp - start_timestamp
            bundle = liblo.Bundle(start_time + wait_time, *msg_list)
            bundle_list.append(bundle)
        liblo.send(output_thread, *bundle_list)
