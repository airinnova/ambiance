User Guide
==========

Creating an Atmosphere object
-----------------------------

|name| provides a class called `Atmosphere` from which aerodynamic properties can be derived. An instance of `Atmosphere` can be instantiated with the altitudes at which aerodynamic properties are to be evaluated. If you wanted to know some properties at, say, *0 m*, *1000 m* and *10000 m*, all you need to do is to call `Atmosphere` with these altitudes.

.. code:: python

    >>> from ambiance import Atmosphere

    >>> atmosphere = Atmosphere([0, 1e3, 1e4])

.. hint::

    `Atmosphere` takes the **geometric height** (altitude above mean sea level). The geometric height is not to be confused with the **geopotential height**.

    * https://en.wikipedia.org/wiki/Geopotential_height

    The `Atmosphere` will actually keep track of both geometric and geopotential height:

    .. code:: python

        >>> atmosphere.h  # Geometric height
        [    0.  1000. 10000.]
        >>> atmosphere.H  # Geopotential height
        [   0.          999.84271205 9984.29343877]


Computing atmospheric properties
--------------------------------

`Atmosphere` provides attributes with the atmospheric properties of interest. For instance, *pressure*, *gravitational acceleration* and *speed of sound* can be retrieved with:

.. code:: python

    >>> atmosphere.pressure
    array([101325.        ,  89876.27760234,  26499.8731228 ])
    >>> atmosphere.grav_accel
    array([9.80665   , 9.80356531, 9.77586844])
    >>> atmosphere.speed_of_sound
    array([340.29398803, 336.4345821 , 299.53166026])


.. hint::

    All properties will be returned in SI units (or SI derived units). In the above example, pressure is given in *[newton/ meter²]*, gravitational acceleration in *[meter/second²]* and speed of sound in *[meter/second]*.

    * https://en.wikipedia.org/wiki/International_System_of_Units

TODO: full list...

TODO: converters
