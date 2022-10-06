Model overview
==============

Constants
---------

* :math:`g_0`: Standard gravitational acceleration [m/s²]
* :math:`M_0`: Sea level mean molar mass [kg/mol]
* :math:`N_A`: Avogadro constant [mol⁻¹]
* :math:`P_0`: Sea level atmospheric pressure [Pa]
* :math:`R^{*}`: Universal gas constant [J/(K·mol)]
* :math:`R`: Specific gas constant [J/(K·kg)]
* :math:`S`: Sutherland's empirical constant in the equation for dynamic viscosity [K]
* :math:`T_i`: Temperature of the ice point at mean sea level [K]
* :math:`T_0`: Sea level temperature [K]
* :math:`t_i`: Celsius temperature of the ice point at mean sea level [°C]
* :math:`t_0`: Celsius sea level temperature [°C]
* :math:`\beta_s`: Sutherland's empirical constant in the equation for dynamic viscosity [kg/(m·s·K^(1/2))]
* :math:`\kappa`: Adiabatic index [1]
* :math:`\rho_0`: Sea level atmospheric density [kg/m³]
* :math:`\sigma`: Effective collision diameter of an air molecule [m]
* :math:`r`: Nominal Earth's radius [m]
* :math:`\beta`: Temperature gradient (layer-specific) [K/m]

Variables
---------

* :math:`\omega`: Collision frequency [Hz]
* :math:`\rho`: Density [kg/m³]
* :math:`\mu`: Dynamic viscosity [Pa·s]
* :math:`g`: Gravitational acceleration [m/s²]
* :math:`\nu`: Kinematic viscosity [m²/s]
* :math:`l`: Mean free path [m]
* :math:`\bar{\nu}`: Mean particle speed [m/s]
* :math:`n`: Number density [m⁻³]
* :math:`p`: Pressure [Pa]
* :math:`H_p`: Pressure scale height [m]
* :math:`\gamma`: Specific weight [N/m³]
* :math:`a`: Speed of sound [m/s]
* :math:`T`: Temperature [K]
* :math:`t`: Temperature (Celsius) [°C]
* :math:`\lambda`: Thermal conductivity [W/(m·K)]

Plots and equations
-------------------

Collision frequency
~~~~~~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/airinnova/ambiance/master/tests/plots/props//collision_frequency.png
   :align: left
   :alt: collision_frequency


**Equation:** :math:`\omega = 4 \sigma^2 N_A \left( \frac{\pi}{R^{*} M_0} \right)^{1/2} \frac{p}{\sqrt{T}}`

Density
~~~~~~~

.. image:: https://raw.githubusercontent.com/airinnova/ambiance/master/tests/plots/props//density.png
   :align: left
   :alt: density


**Equation:** :math:`\rho = \frac{p}{R T}`

Dynamic viscosity
~~~~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/airinnova/ambiance/master/tests/plots/props//dynamic_viscosity.png
   :align: left
   :alt: dynamic_viscosity


**Equation:** :math:`\mu = \frac{\beta_s T^{3/2}}{T + S}`

Gravitational acceleration
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/airinnova/ambiance/master/tests/plots/props//grav_accel.png
   :align: left
   :alt: grav_accel


**Equation:** :math:`g = g_0 \left( \frac{r}{r + h} \right)^2`

Kinematic viscosity
~~~~~~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/airinnova/ambiance/master/tests/plots/props//kinematic_viscosity.png
   :align: left
   :alt: kinematic_viscosity


**Equation:** :math:`\nu = \frac{\mu}{\rho}`

Mean free path
~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/airinnova/ambiance/master/tests/plots/props//mean_free_path.png
   :align: left
   :alt: mean_free_path


**Equation:** :math:`l = \frac{1}{\sqrt{2} \pi \sigma^2 n}`

Mean particle speed
~~~~~~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/airinnova/ambiance/master/tests/plots/props//mean_particle_speed.png
   :align: left
   :alt: mean_particle_speed


**Equation:** :math:`\bar{\nu} = \left( \frac{8}{\pi} R T \right)^{1/2}`

Number density
~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/airinnova/ambiance/master/tests/plots/props//number_density.png
   :align: left
   :alt: number_density


**Equation:** :math:`n = \frac{N_A p}{R^{*} T}`

Pressure
~~~~~~~~

.. image:: https://raw.githubusercontent.com/airinnova/ambiance/master/tests/plots/props//pressure.png
   :align: left
   :alt: pressure


**Equation:** 

:math:`p = p_b \exp \left[ - \frac{g_0}{R T} (H - H_b) \right] \quad \text{for} \quad \beta = 0`

:math:`p = p_b \left[ 1 + \frac{\beta}{T_b} (H - H_b) \right]^{-g_0/(\beta R)} \quad \text{for} \quad \beta \neq 0`

Pressure scale height
~~~~~~~~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/airinnova/ambiance/master/tests/plots/props//pressure_scale_height.png
   :align: left
   :alt: pressure_scale_height


**Equation:** :math:`H_p = \frac{R T}{g}`

Specific weight
~~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/airinnova/ambiance/master/tests/plots/props//specific_weight.png
   :align: left
   :alt: specific_weight


**Equation:** :math:`\gamma = \rho g`

Speed of sound
~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/airinnova/ambiance/master/tests/plots/props//speed_of_sound.png
   :align: left
   :alt: speed_of_sound


**Equation:** :math:`a = \sqrt{\kappa R T}`

Temperature
~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/airinnova/ambiance/master/tests/plots/props//temperature.png
   :align: left
   :alt: temperature


**Equation:** :math:`T = T_b + \beta (H - H_b)`

Temperature (Celsius)
~~~~~~~~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/airinnova/ambiance/master/tests/plots/props//temperature_in_celsius.png
   :align: left
   :alt: temperature_in_celsius


**Equation:** :math:`t = T - T_i`

Thermal conductivity
~~~~~~~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/airinnova/ambiance/master/tests/plots/props//thermal_conductivity.png
   :align: left
   :alt: thermal_conductivity


**Equation:** :math:`\lambda = \frac{2.648151 \cdot 10^{-3} T^{3/2}}{T + (245.4 \cdot 10^{-12/T})}`

