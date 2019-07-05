"""Base data class to store messaged from OSC paths."""
import json
from collections import defaultdict


class TimeSeriesBundle():
    """ Bundles together different path identified time series.

    The bundle is a dictionary with the path names as the key.
    The values in the bundle are also dictionaries.
    They contain the timestamps and samples which are stored in lists.
    Timestamps is a list of floats.
    Samples is a list of lists since there could be many channels.
    Example:
        bundle = {
            'path/name':{
                'timestamps': [ 0,   1,   2,  ...],
                'samples':    [[0], [1], [2], ...]
            }
        }

    Keyword Args:
        file_name (string): Import from a file if name provided.
    """
    def __init__(self, file_name=None):
        self.bundle = dict()
        if file_name:
            self.from_json(file_name)

    def add_time_series(self, name, timestamps, samples):
        """Adds a time series identified by a path name.

        Creates a dictionary of timestamps and values recieved for each path.

        Args:
            name (string): OSC path name.
            timestamps (float): Timestamp saved when packet is received.
            samples (list): List of values received.
        """
        self.bundle[name] = {
            'timestamps': timestamps,
            'samples': samples
        }

    def to_json(self, file_name):
        """Saves the bundle to a json file.

        Saved to the directory the script is called on.

        Args:
            file_name (string): File name to save as.
        """
        with open(file_name, 'w') as save_file:
            json.dump(self.bundle, save_file, indent=2)

    def from_json(self, file_name):
        """Replaces the current bundle with with the bundle from the json file.

        Args:
            file_name (string): File name to open.
        """
        with open(file_name, 'r') as read_file:
            self.bundle = json.load(read_file)

    def to_timestamped_dict(self):
        """Returns a dict with the timestamps as the key for the dictionary.

        timestamped_bundle = {
            timestamp0:[
                [ /name0,   /name1, ...],
                [    [0],      [1], ...]
            ],
            timestamp0:[
                [ /name0,   /name1, ...],
                [    [0],      [1], ...]
            ]

        }

        Returns:
            [type]: [description]
        """
        timestamped_dict = defaultdict(list)
        for name, info in self.bundle.items():
            for timestamp, sample in zip(info['timestamps'], info['samples']):
                timestamped_dict[timestamp].append([name, sample])
        return timestamped_dict
