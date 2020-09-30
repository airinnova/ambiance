import os

import numpy as np
import matplotlib.pyplot as plt
from ambiance import Atmosphere, CONST

HERE = os.path.abspath(os.path.dirname(__file__))
FILE_NAME = os.path.basename(__file__).replace('.py', '.png')
PATH_OUT = os.path.join(HERE, FILE_NAME)


def pressure_estimate(h):
    return 10**(5 - h/16e3)


# Make an atmosphere object
heights = np.linspace(-10e3, 90e3, num=1000)
p_actual = Atmosphere(heights, check_bounds=False).pressure
p_approx = pressure_estimate(heights)

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, tight_layout=True)
ax1.plot(p_actual, heights/1000, label='Actual', c='blue')
ax1.plot(p_approx, heights/1000, '--', label='Estimate', c='red')
ax1.set_xlabel("Pressure [Pa]")
ax1.set_ylabel("Height [km]")
ax1.set_xscale("log")
ax1.grid()
ax1.legend()

for ax in (ax1, ax2):
    ax.axhline(y=CONST.h_min/1000, ls=':', color='black')
    ax.axhline(y=CONST.h_max/1000, ls=':', color='black')

rdiff = (p_approx - p_actual)/p_actual
ax2.plot(rdiff*100, heights/1000, label='Relative error', c='red')
ax2.set_xlabel("Relative error [%]")
ax2.grid()

plt.savefig(PATH_OUT)
plt.clf()
