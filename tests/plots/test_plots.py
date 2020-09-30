#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def test_plots():
    from . import pressure_estimate
    from . import temperature

    from .props import props
    props.make_plots()
