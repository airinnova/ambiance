import os

import numpy as np
import matplotlib.pyplot as plt
from ambiance import Atmosphere, CONST

HERE = os.path.abspath(os.path.dirname(__file__))
FILE_NAME = os.path.basename(__file__).replace('.py', '.png')
PATH_OUT = os.path.join(HERE, FILE_NAME)


def density_estimate(h):
    return 10**((h - 2.33e3)/-16.3e3)


# Make an atmosphere object
heights = np.linspace(-10e3, 90e3, num=1000)
rho_actual = Atmosphere(heights, check_bounds=False).density
rho_approx = density_estimate(heights)

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, tight_layout=True)
ax1.plot(rho_actual, heights/1000, label='Actual', c='blue')
ax1.plot(rho_approx, heights/1000, '--', label='Estimate', c='red')
ax1.set_xlabel("Density [kg/m^3]")
ax1.set_ylabel("Height [km]")
ax1.set_xscale("log")
ax1.grid()
ax1.legend()

for ax in (ax1, ax2):
    ax.axhline(y=CONST.h_min/1000, ls=':', color='black')
    ax.axhline(y=CONST.h_max/1000, ls=':', color='black')

rdiff = (rho_approx - rho_actual)/rho_actual
ax2.plot(rdiff*100, heights/1000, label='Relative error', c='red')
ax2.set_xlabel("Relative error [%]")
ax2.grid()

plt.savefig(PATH_OUT)
plt.show()
plt.clf()
