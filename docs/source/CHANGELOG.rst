Changelog
=========

Changelog for |name_bold|. Version numbers try to follow `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[0.3.2] -- 2020-03-14
---------------------

* Remove unnecessary aliases of atmospheric properties when deriving new ones

[0.3.1] -- 2019-12-30
---------------------

Changed
~~~~~~~

* Transfer of repository ownership
* Repository moved from ``aarondettmann/ambiance`` to ``airinnova/ambiance``

[0.3.0] -- 2019-08-03
---------------------

Added
~~~~~

* Added `Atmosphere.layer_name` which returns a string array with layer names corresponding to the input heights

Changed
~~~~~~~

* Renamed the class `ambiance.Constant` to `ambiance._Const`/`ambiance.CONST`
    * Clearer indication that this class is meant to be "private"/constant

[0.2.1] -- 2019-08-03
---------------------

Fixed
~~~~~

* `int` and `float` input reported to produce different values
    * See https://github.com/aarondettmann/ambiance/issues/1

[0.2.0] -- 2019-07-28
---------------------

Added
~~~~~

* Added support for input in matrix form
* Added test cases for input in matrix form

Changed
~~~~~~~

* Made `Atmosphere` attributes `h` and `H` @property to indicate 'read-only'
* Made converter between geometric and geopotential heights @staticmethod

[0.1.0] -- 2019-07-26
---------------------

Added
~~~~~

* Added test cases for full test coverage
* Integration with `CI <https://en.wikipedia.org/wiki/Continuous_integration>`_ service
* Updated the documentation

Changed
~~~~~~~

* Minor changes in the |name| module

[0.0.1] -- 2019-07-11
---------------------

Added
~~~~~

* Initial release
    - Basic implementation of the ICAO 1993 atmosphere
    - Single values and arrays can be processed
    - Basic test cases included
