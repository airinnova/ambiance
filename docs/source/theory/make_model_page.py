#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

HERE = os.path.abspath(os.path.dirname(__file__))
os.chdir(HERE)

sys.path.insert(0, os.path.abspath('../../../src/ambiance'))

from _doc import props, vars_const

URL_PLOTS = 'https://raw.githubusercontent.com/airinnova/ambiance/master/tests/plots/props/'

UNDERLINE_SECTION = {
    0: "=",
    1: "-",
    2: "~",
    3: "^",
}


def get_header(string, level=0):
    """
    See model-framework
    """

    return f"{string}\n{UNDERLINE_SECTION[level]*len(string)}\n\n"


def add_plot(name):
    """
    See model-framework
    """

    rst = ""
    rst += f".. image:: {URL_PLOTS}/{name}.png\n"
    rst += f"   :align: left\n"
    rst += f"   :alt: {name}\n"
    rst += "\n"
    return rst


def add_descr(p):
    rst = "\n**Equation:** "
    if isinstance(p.eq, tuple):
        rst += "\n"
        for eq in p.eq:
            rst += f'\n:math:`{eq}`\n'
    else:
        rst += f':math:`{p.eq}`\n'

    rst += "\n"
    return rst


rst = ""
rst += get_header("Model overview", 0)

rst += get_header("Constants", 1)
for v in vars_const:
    rst += f"* :math:`{v.symb}`: {v.name} [{v.unit}]\n"
rst += "\n"

rst += get_header("Variables", 1)
for p in props:
    rst += f"* :math:`{p.symb}`: {p.name_long} [{p.unit}]\n"
rst += "\n"

rst += get_header("Plots and equations", 1)
for p in props:
    rst += get_header(p.name_long, 2)
    rst += add_plot(p.name)
    rst += add_descr(p)

with open('model.rst', 'w') as fp:
    fp.write(rst)
