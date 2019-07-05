"""A collector with simple storage for efficient callbacks during OSC packet capture."""
import copy
from collections import defaultdict

from .base import TimeSeriesBundle


class Collector():
    """Collector with a callback function to receive and store OSC packets."""
    def __init__(self):
        self._samples = defaultdict(list)
        self._timestamps = defaultdict(list)

    def collect_samples(self, name, timestamp, sample):
        """Callback function to collect samples from incoming OSC.

        Args:
            name (str): OSC path name.
            timestamp (float): timing information for each packet.
            sample (list, np.ndarray or scalar): values to collect.
        """
        self._timestamps[name].append(timestamp)
        self._samples[name].append(copy.deepcopy(sample))

    def to_time_series_bundle(self):
        """Converts OSC packets stored into the TimeSeriesBundle format.

        Returns:
            (TimeSeriesBundle): TimeSeriesBundleObject.
        """
        bundle = TimeSeriesBundle()
        for name in self._timestamps:
            bundle.add_time_series(name, self._timestamps[name], self._samples[name])
        return bundle
