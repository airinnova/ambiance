#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

from ambiance import Atmosphere


def main():
    # Make an atmosphere object
    heights = np.linspace(-5e3, 80e3, num=1000)
    atmos = Atmosphere(heights)

    # Make plot
    plt.plot(atmos.temperature_in_celsius, heights/1000)
    plt.ylabel('Height [km]')
    plt.xlabel('Temperature [°C]')
    plt.grid()
    plt.show()


if __name__ == '__main__':
    main()
