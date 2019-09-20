User Guide
==========

Creating an Atmosphere object
-----------------------------

|name| provides a class called `Atmosphere` from which atmospheric properties can be derived. An instance of `Atmosphere` can be created with the altitudes at which atmospheric properties are to be evaluated.

**Example** If you wanted to know some properties at, say, *0 m*, *1000 m* and *10000 m*, all you need to do is to call `Atmosphere` with these altitudes.

.. code:: python

    >>> from ambiance import Atmosphere

    >>> atmosphere = Atmosphere([0, 1000, 10000])

.. hint::

    `Atmosphere` takes the **geometric height** (altitude above mean sea level) as input. The geometric height is not to be confused with the **geopotential height**.

    * https://en.wikipedia.org/wiki/Geopotential_height

    `Atmosphere` will keep track of both geometric and geopotential height:

    .. code:: python

        >>> atmosphere.h  # Geometric height
        [    0.  1000. 10000.]
        >>> atmosphere.H  # Geopotential height
        [   0.          999.84271205 9984.29343877]

    The `Atmosphere` class does only take *geometric* heights as input as this is the typical use. However, if you really wanted to request properties based on the *geopotential* height, you can convert the geopotential height to geometric height, and then call `Atmosphere`.

    .. code:: python

        >>> # Convert from geopotential to geometric heights
        >>> h = Atmosphere.geop2geom_height([0, 1000, 10000])
        >>> atmosphere = Atmosphere(h)

        >>> atmosphere.h
        array([    0.        ,  1000.15733745, 10015.75605592])
        >>> atmosphere.H
        array([    0.,  1000., 10000.])

Computing atmospheric properties
--------------------------------

`Atmosphere` provides attributes with atmospheric properties of interest. For instance, *pressure*, *gravitational acceleration* and *speed of sound* can be retrieved with:

.. code:: python

    >>> atmosphere.pressure
    array([101325.        ,  89876.27760234,  26499.8731228 ])
    >>> atmosphere.grav_accel
    array([9.80665   , 9.80356531, 9.77586844])
    >>> atmosphere.speed_of_sound
    array([340.29398803, 336.4345821 , 299.53166026])


.. hint::

    All properties will be returned in `SI units`_ (or SI derived units). In the above example, pressure is given in *[newton/ meter²]*, gravitational acceleration in *[meter/second²]* and speed of sound in *[meter/second]*.

**List of available atmospheric properties**

* Collision frequency (``collision_frequency``)
* Density (``density``)
* Dynamic viscosity (``dynamic_viscosity``)
* Gravitational acceleration (``grav_accel``)
* Kinematic viscosity (``kinematic_viscosity``)
* Layer names (``layer_name``) [string array]
* Mean free path (``mean_free_path``)
* Mean particle speed (``mean_particle_speed``)
* Number density (``number_density``)
* Pressure (``pressure``)
* Pressure scale height (``pressure_scale_height``)
* Specific weight (``specific_weight``)
* Speed of sound (``speed_of_sound``)
* Temperature (``temperature``, ``temperature_in_celsius``)
* Thermal conductivity (``thermal_conductivity``)

**Layer names**

`Atmosphere` also provides a special attribute called `layer_name` which returns the layer name(s) corresponding to the input height(s). Example:

.. code:: python

    >>> Atmosphere(0).layer_name
    array(['troposphere'], dtype='<U31')

    >>> Atmosphere([[30000, 80000], [-5000, 22000]]).layer_name
    array([['stratosphere', 'mesosphere'],
           ['troposphere', 'stratosphere']], dtype='<U53')

The attribute `layer_name` returns a *Numpy* string array which can be further manipulated in many ways.

.. seealso::

    **Numpy string operations:** https://docs.scipy.org/doc/numpy/reference/routines.char.html

Input data
----------

The height data passed to `Atmosphere` can be a single value (integers, floats), a vector (list, tuple, *Numpy* vector) or a matrix (iterable of an iterable, *Numpy* matrix). The heights do not have to be ordered in any specific way.

.. code:: python

    >>> # ===== Single value input =====
    >>> Atmosphere(1729).grav_accel
    array([9.80131748])

    >>> # ===== Vector input =====
    >>> Atmosphere([3000, 12000, 36000]).grav_accel
    array([9.79740029, 9.76972952, 9.69651134])

    >>> # ===== Matrix input =====
    >>> Atmosphere([3000, 12000, 36000]).grav_accel
    >>> Atmosphere([[3000, 12000], [0, -3000]]).grav_accel
    array([[9.79740029, 9.76972952],
           [9.80665   , 9.81591282]])

Converting units
----------------

|name| also provides functions to convert between different units.

Kelvin and degree Celsius
~~~~~~~~~~~~~~~~~~~~~~~~~

Convert from a temperature in degree Celsius to a temperature in Kelvin:

.. code:: python

    >>> Atmosphere.t2T(0)
    273.15

    >>> Atmosphere.t2T([0, 10, 30.5])
    array([273.15, 283.15, 303.65])

Convert from a temperature in Kelvin to a temperature in Celsius:

.. code:: python

    >>> Atmosphere.T2t(273.15)
    0.0

    >>> Atmosphere.T2t([273.15, 283.15, 303.65])
    array([ 0. , 10. , 30.5])

Geometric and geopotential height
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Convert from a *geometric* to a *geopotential* height.

.. code:: python

    >>> Atmosphere.geom2geop_height(10000)
    9984.293438772525

    Convert from a *geopotential* to a *geometric* height.

    >>> Atmosphere.geop2geom_height(9984.293438772525)
    10000.0
