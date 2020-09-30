.. _sec_user_guide:

User guide
==========

Creating an Atmosphere object
-----------------------------

|name| provides a class called ``Atmosphere`` from which atmospheric properties can be derived. An instance of ``Atmosphere`` can be created with the altitudes at which atmospheric properties are to be evaluated.

**Example** If you wanted to compute some properties at, say, :math:`0\,\textrm{m}`, :math:`1000\,\textrm{m}` and :math:`10\,000\,\textrm{m}`, all you need to do is to call `Atmosphere` with these altitudes.

.. code:: python

    >>> from ambiance import Atmosphere

    >>> atmosphere = Atmosphere([0, 1000, 10000])

.. hint::

    `Atmosphere` takes the **geometric height** (altitude above mean sea level) as input. The geometric height is not to be confused with the **geopotential height**.

    * https://en.wikipedia.org/wiki/Geopotential_height

    `Atmosphere` will keep track of both geometric and geopotential height:

    .. code:: python

        >>> atmosphere.h  # Geometric height
        array([    0.,  1000., 10000.])
        >>> atmosphere.H  # Geopotential height
        array([   0.        ,  999.84271205, 9984.29343877])

    The ``Atmosphere`` class does only take *geometric* heights as input as this is the typical use. However, if you really wanted to request properties based on the *geopotential* height, you can convert the geopotential height to geometric height, and then call `Atmosphere`.

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

``Atmosphere`` provides attributes with atmospheric properties of interest. For instance, *pressure*, *gravitational acceleration* and *speed of sound* can be retrieved with:

.. code:: python

    >>> atmosphere.pressure
    array([101325.        ,  89874.56291622,  26436.24259269])
    >>> atmosphere.grav_accel
    array([9.80665   , 9.80356482, 9.77582006])
    >>> atmosphere.speed_of_sound
    array([340.29398803, 336.43397149, 299.46316487])


.. hint::

    All properties will be returned in `SI units`_ (or SI derived units). In the above example, *pressure* is given in :math:`N/m^2`, *gravitational acceleration* in :math:`m/s^2` and *speed of sound* in :math:`m/s`.

**List of available atmospheric properties**

* Collision frequency (``collision_frequency``)
* Density (``density``)
* Dynamic viscosity (``dynamic_viscosity``)
* Geometric height above `MSL <https://en.wikipedia.org/wiki/Sea_level>`_ (``h``)
* Geopotential height (``H``)
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

``Atmosphere`` also provides a special attribute called ``layer_name`` which returns the layer name(s) corresponding to the input height(s). Example:

.. code:: python

    >>> Atmosphere(0).layer_name
    array(['troposphere'], dtype='<U31')

    >>> Atmosphere([[30000, 80000], [-5000, 22000]]).layer_name
    array([['stratosphere', 'mesosphere'],
           ['troposphere', 'stratosphere']], dtype='<U53')

The attribute ``layer_name`` returns a *NumPy* string array which can be further manipulated in many ways.

.. seealso::

    **NumPy string operations:** https://docs.scipy.org/doc/numpy/reference/routines.char.html

Input data
----------

The height data passed to ``Atmosphere`` can be a single value (integer, float), a vector (list, tuple, *NumPy* vector) or a matrix (iterable of an iterable, *NumPy* matrix). The heights do not have to be ordered in any specific way.

.. code:: python

    >>> # ===== Single value input =====
    >>> Atmosphere(1729).grav_accel
    array([9.80131748])

    >>> # ===== Vector input =====
    >>> Atmosphere([3000, 12000, 36000]).grav_accel
    array([9.79740029, 9.76972952, 9.69651134])

    >>> # ===== Matrix input =====
    >>> Atmosphere([3000, 12000, 36000]).grav_accel
    array([9.79740029, 9.76972952, 9.69651134])
    >>> Atmosphere([[3000, 12000], [0, -3000]]).grav_accel
    array([[9.79740029, 9.76972952],
           [9.80665   , 9.81591282]])

Instantiating from given pressure
---------------------------------

An ``Atmosphere`` object can also be instantiated from given ambient pressure. To do so you can use the ``Atmosphere.from_pressure()`` method. This method takes pressure values in :math:`Pa = N/m^2` as input. Scalar, vector- and matrix-like input is accepted. ``Atmosphere.from_pressure()`` returns a new atmosphere instance which lets you easily check other atmospheric properties too, like temperature.

.. code:: python

    # Pressure at sea level
    >>> atmos = Atmosphere.from_pressure(101325)

    >>> # Geometric altitude
    >>> atmos.h
    array([1.6616131e-12])

    >>> # Temperature
    >>> atmos.temperature
    array([288.15])

    >>> # You can also pass in multiple pressure values at once...
    >>> atmos = Atmosphere.from_pressure([1e5, 1e4, 1e3, 1e2, 1e1, 1e0])
    >>> atmos.h
    array([  110.88636257, 16220.98996248, 31207.06116863, 48182.51841281,
           65617.3058236 , 80304.40565541])

``Atmosphere.from_pressure()`` uses SciPy's `Newton method <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.newton.html>`_ to find approximate atmospheric altitudes. The method uses the default tolerance settings from ``scipy.optimize.newton()`` when determining the altitude. The initial guess for the altitude is zero for all pressure values.

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
