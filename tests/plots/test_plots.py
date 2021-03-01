#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import pytest


if not sys.platform.lower().startswith("linux"):
    pytest.skip("Skip plot tests", allow_module_level=True)


def test_plots():
    from . import pressure_estimate
    from . import temperature

    from .props import props
    props.make_plots()
