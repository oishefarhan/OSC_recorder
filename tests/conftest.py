#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `osc_recorder` package."""

import pytest

from osc_recorder import TimeSeriesBundle

pytest_plugins = 'pytester'

@pytest.fixture()
def ts_bundle():
    """Loads a time series bundle for test use."""
    return TimeSeriesBundle('tests/sine60.json')
