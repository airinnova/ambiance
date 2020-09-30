#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import numpy as np
import matplotlib.pyplot as plt

from ambiance import Atmosphere, CONST


HERE = os.path.abspath(os.path.dirname(__file__))


class P:
    def __init__(self, name, unit='', name_long='', log=False):
        self.name = name
        self.unit = unit
        self.name_long = name_long if name_long else self.name.replace('_', ' ').capitalize()
        self.log = log


props = (
    P('collision_frequency', 'Hz', log=True),
    P('density', 'kg/m³', log=True),
    P('dynamic_viscosity', 'Pa·s'),
    P('grav_accel', 'm/s²', 'Gravitational acceleration'),
    P('kinematic_viscosity', 'm²/s', log=True),
    P('mean_free_path', 'm', log=True),
    P('mean_particle_speed', 'm/s'),
    P('number_density', 'm$^{-3}$', log=True),
    P('pressure', 'Pa', log=True),
    P('pressure_scale_height', 'm'),
    P('specific_weight', 'N/m³', log=True),
    P('speed_of_sound', 'm/s'),
    P('temperature', 'K'),
    P('temperature_in_celsius', '°C'),
    P('thermal_conductivity', 'W/(m·K)'),
)


def make_plots():
    h = np.linspace(CONST.h_min, CONST.h_max, num=1000)
    a = Atmosphere(h)
    hs = h/1000

    lw = 2
    cp1 = 'black'
    cp2 = 'red'

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
