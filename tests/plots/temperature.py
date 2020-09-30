#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

HERE = os.path.abspath(os.path.dirname(__file__))
FILE_NAME = os.path.basename(__file__).replace('.py', '.png')
PATH_OUT = os.path.join(HERE, FILE_NAME)

# ==================================================

import numpy as np
import matplotlib.pyplot as plt

from ambiance import Atmosphere


# Make an atmosphere object
heights = np.linspace(-5e3, 80e3, num=1000)
atmosphere = Atmosphere(heights)

# Make plot
plt.plot(atmosphere.temperature_in_celsius, heights/1000)
plt.ylabel('Height [km]')
plt.xlabel('Temperature [°C]')
plt.grid()
plt.show()

# ==================================================

plt.savefig(PATH_OUT)
plt.clf()
