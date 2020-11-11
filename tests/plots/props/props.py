#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import numpy as np
import matplotlib.pyplot as plt

from ambiance import Atmosphere, CONST
from ambiance._doc import props

HERE = os.path.abspath(os.path.dirname(__file__))


def make_plots():
    h = np.linspace(CONST.h_min, CONST.h_max, num=1000)
    a = Atmosphere(h)
    hs = h/1000

    lw = 1.5
    cp1 = 'blue'
    cp2 = 'green'

    for p in props:
        fig, ax1 = plt.subplots()

        data = getattr(a, p.name)

        ax1.plot(data, hs, lw=lw, c=cp1)
        ax1.set_ylabel('Height [km]')
        ax1.tick_params(axis='x', labelcolor=cp1)
        ax1.grid()

        ax1.set_xlabel(f"{p.name_long} [{p.unit}]")

        if p.log:
            ax2 = ax1.twiny()
            ax2.plot(data, hs, '--', lw=lw, c=cp2)
            ax2.set_xscale('log')
            ax2.tick_params(axis='x', labelcolor=cp2)
            ax2.grid()

        fig.tight_layout()

        fname = p.name + '.png'
        print(fname)
        plt.savefig(os.path.join(HERE, fname))

        plt.cla()
        plt.close('all')
        plt.clf()


if __name__ == '__main__':
    make_plots()
