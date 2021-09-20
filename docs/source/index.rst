Welcome to |name|'s documentation!
==================================

.. image:: _static/images/logo/logo.png
   :width: 250 px
   :alt: Logo
   :align: right

|name_bold| is a full implementation of the ICAO standard atmosphere 1993 written in Python. |name| allows you to create an ``Atmosphere`` object from which atmospheric properties can be easily derived in a human-readable form.

.. code:: python

    from ambiance import Atmosphere

    sealevel = Atmosphere(0)
    sealevel.pressure     # --> 101325 Pascal
    sealevel.temperature  # --> 288.15 Kelvin

.. toctree::
   :maxdepth: 1
   :caption: User guide

   user_guide/installation
   user_guide/detailed_user_guide
   user_guide/extending

.. toctree::
   :maxdepth: 1
   :caption: Theory

   theory/model
   theory/references

.. toctree::
   :maxdepth: 1
   :caption: API documentation

   dev_doc/modules

.. toctree::
   :maxdepth: 1
   :caption: Changelog

   CHANGELOG.md

:Author:
    |author1|

:Licence:
    |license|
