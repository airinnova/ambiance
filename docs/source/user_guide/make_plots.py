#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

HERE = os.path.abspath(os.path.dirname(__file__))
os.chdir(HERE)

sys.path.insert(0, os.path.abspath('../../../tests/plots/props'))

from props import props

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


rst = ""
rst += get_header("Plots", 0)

for p in props:
    rst += get_header(p.name_long, 1)
    rst += add_plot(p.name)

with open('plots.rst', 'w') as fp:
    fp.write(rst)
