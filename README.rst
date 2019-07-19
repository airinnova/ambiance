.. image:: https://raw.githubusercontent.com/aarondettmann/ambiance/master/docs/source/_static/images/logo/logo001.svg?sanitize=true
   :alt: Ambiance
   :width: 100 px
   :scale: 50 %

.. image:: https://img.shields.io/pypi/v/ambiance.svg?style=flat
   :target: https://pypi.org/project/ambiance/
   :alt: Latest PyPI version

.. image:: https://readthedocs.org/projects/ambiance/badge/?version=latest
    :target: https://ambiance.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/license-Apache%202-blue.svg
    :target: https://github.com/aarondettmann/ambiance/blob/master/LICENSE.txt
    :alt: License

*Ambiance* is a full implementation of the ICAO standard atmosphere 1993 written in Python.

* `International Standard Atmosphere (Wikipedia) <https://en.wikipedia.org/wiki/International_Standard_Atmosphere>`_
* `Manual Of The ICAO Standard Atmosphere - 3rd Edition 1993 (Doc 7488) <https://store.icao.int/manual-of-the-icao-standard-atmosphere-extended-to-80-kilometres-262-500-feet-doc-7488-quadrilingual-printed.html>`_

Usage
=====

Atmospheric properties are computed from an "Atmosphere object" which takes the altitude (geometric height) as input. For instance, to simply retrieve sea level properties, you can write:

.. code:: python

    >>> from ambiance import Atmosphere
    >>> sealevel = Atmosphere(0)
    >>>
    >>> sealevel.temperature
    array([288.15])
    >>>
    >>> sealevel.pressure
    array([101325.])
    >>>
    >>> sealevel.kinematic_viscosity
    array([1.46071857e-05])

*Ambiance* also handles list-like input (list, tuples, *Numpy* arrays). The following code demonstrates how to produce a temperature plot with *Matplotlib*. In the example, *Numpy*'s `linspace()` function is used to produce an array with altitudes.

.. code:: python

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

The output is

.. image:: https://raw.githubusercontent.com/aarondettmann/ambiance/master/tests/temperature_plot.png
   :alt: Temperature plot

For all functionality see the `complete documentation <https://ambiance.readthedocs.io/en/latest/>`_.

Installation
============

*Ambiance* is available on `PyPi <https://pypi.org/project/ambiance/>`_ and may simply be installed with

.. code::

    pip install ambiance

Requirements
============

Using *Ambiance* requires

* *Python 3.6* or higher
* *Numpy*

*For developers*: Recommended packages may be installed with the `requirements.txt`.

.. code::

    pip install -r "requirements.txt"

License
=======

**License:** Apache-2.0
