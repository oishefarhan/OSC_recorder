#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `osc_recorder` package."""

# import pytest

from osc_recorder import TimeSeriesBundle

def test_time_series_bundle_format(ts_bundle):
    """Testing TimeSeriesBundle is in the correct format."""
    assert isinstance(ts_bundle, TimeSeriesBundle)
    for name, info in ts_bundle.bundle.items():
        assert isinstance(name, str)
        assert isinstance(info, dict)
        assert isinstance(info['timestamps'], list)
        assert isinstance(info['samples'], list)


def test_bundle_to_timestamped_dict(ts_bundle):
    """Testing TimeSeriesBundle conversion to timestampled_dict"""
    ts_dict = ts_bundle.to_timestamped_dict()

    for name, info in ts_bundle.bundle.items():
        timestamps = info['timestamps']
        samples = info['samples']
        for i, timestamp in enumerate(timestamps):
            sample = samples[i]
            assert timestamp in ts_dict
            assert [name, sample] in ts_dict[timestamp]
