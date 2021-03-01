#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ======================================================================
# AMBIANCE -- A full implementation of the ICAO standard atmosphere 1993
#
#  Copyright 2019-2020 Aaron Dettmann
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ======================================================================

"""
Compute atmospheric properties for heights ranging from -5 km to 80 km.

The implementation is based on the ICAO standard atmosphere from 1993.

References:
===========

.. [ICAO93] International Civil Aviation Organization ; Manual Of The ICAO
            Standard Atmosphere -- 3rd Edition 1993 (Doc 7488) -- extended
            to 80 kilometres (262 500 feet)

.. [WISA19] Wikipedia ; International Standard Atmosphere ;
            https://en.wikipedia.org/wiki/International_Standard_Atmosphere
            Accessed: 2019-07-28
"""

from itertools import tee

import numpy as np
import scipy.optimize as opt

_EPS = 1e-9


def pairwise(iterable):
    """
    Iterate pairwise

    s -> (s0,s1), (s1,s2), (s2, s3), ...

    See: https://docs.python.org/3/library/itertools.html
    """

    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class CONST:
    """
    Constants defined in the ICAO standard atmosphere (1993)

    Notes:
        * All values are given in SI-units.

    Attributes:
        :g_0: Standard gravitational acceleration [m/s^2]
        :M_0: Sea level molar mass [kg/mol]
        :N_A: Avogadro constant [1/mol]
        :P_0: Sea level atmospheric pressure [Pa]
        :R_star: Universal gas constant [J/(K*mol)]
        :R: Specific gas constant [J/(K*kg)]
        :S: Sutherland's empirical constant in the equation for dynamic viscosity [K]
        :T_i: Temperature of the ice point at mean sea level [K]
        :T_0: Sea level temperature [K]
        :t_i: Celsius temperature of the ice point at mean sea level [degC]
        :t_0: Celsius sea level temperature [degC]
        :beta_s: Sutherland's empirical constant in the equation for dynamic viscosity [kg/(m*s*K**(1/2))]
        :kappa: Adiabatic index [-]
        :rho_0: Sea level atmospheric density [kg/m^3]
        :sigma: Effective collision diameter of an air molecule [m]
        :r: Nominal Earth's radius [m]

        :h_min: Lower boundary of acceptable geometric heights [m]
        :h_max: Upper boundary of acceptable geometric heights [m]
        :H_min: Lower boundary of acceptable geopotential heights [m]
        :H_max: Upper boundary of acceptable geopotential heights [m]
        :p_min: Lower boundary of acceptable pressures [Pa]
        :p_max: Upper boundary of acceptable pressures [Pa]

        :LAYER_SPEC_PROP: Table containing layer specific properties
        :LAYER_DICTS: Dictionary containing layer specific properties

    Notes on 'LAYER_SPEC_PROP':
         * Table with columns
               1. :H_b: geopotential base height [m]
               2. :T_b: base temperature [K]
               3. :beta: base temperature gradient [kg/(m*s*K^(1/2))]
               4. :p: base pressure [Pa]
               5. :layer name: string representation of layer name
         * Values for (1,2,3) from table D in [ICAO93]_
         * Values for (4) for pressure from [ICAO93]_
         * Values for (5) from [WISA19]_
    """

    # Primary constants (table A)
    g_0 = 9.80665
    M_0 = 28.964420e-3
    N_A = 602.257e21
    P_0 = 101.325e3
    R_star = 8314.32e-3
    R = 287.05287
    S = 110.4
    T_i = 273.15
    T_0 = 288.15
    t_i = 0.0
    t_0 = 15.0
    beta_s = 1.458e-6
    kappa = 1.4
    rho_0 = 1.225
    sigma = 0.365e-9

    # Additional constants
    r = 6_356_766

    # Geometric heights
    h_min = -5_004
    h_max = 81_020

    # Geopotential heights
    H_min = -5_000
    H_max = 80_000

    # Pressure limits (computed)
    p_min = 0.886216717024069
    p_max = 177837.4089432764

    _LAYER_NAME_a = 'troposphere'
    _LAYER_NAME_b = 'tropopause'
    _LAYER_NAME_c = 'stratosphere'
    _LAYER_NAME_d = 'stratopause'
    _LAYER_NAME_e = 'mesosphere'

    LAYER_SPEC_PROP = [
        [-5.0e3, 320.65, -6.5e-3, 1.77687e+5, _LAYER_NAME_a],
        [0.00e3, 288.15, -6.5e-3, 1.01325e+5, _LAYER_NAME_a],
        [11.0e3, 216.65,  0.0e-3, 2.26320e+4, _LAYER_NAME_b],
        [20.0e3, 216.65,  1.0e-3, 5.47487e+3, _LAYER_NAME_c],
        [32.0e3, 228.65,  2.8e-3, 8.68014e+2, _LAYER_NAME_c],
        [47.0e3, 270.65,  0.0e-3, 1.10906e+2, _LAYER_NAME_d],
        [51.0e3, 270.65, -2.8e-3, 6.69384e+1, _LAYER_NAME_e],
        [71.0e3, 214.65, -2.0e-3, 3.95639e+0, _LAYER_NAME_e],
        [80.0e3, 196.65, -2.0e-3, 8.86272e-1, _LAYER_NAME_e],
    ]

    # Number of first and last layer in atmosphere
    LAYER_NUM_FIRST = 1
    LAYER_NUM_LAST = len(LAYER_SPEC_PROP) - 1

    LAYER_DICTS = {}
    MAX_STR_LEN_LAYER_NAME = 0
    for i, layer_pair in enumerate(pairwise(LAYER_SPEC_PROP), start=LAYER_NUM_FIRST):
        # Layer properties from the base layer are valid from base to top
        H_base, T, beta, p, layer_name = layer_pair[0]
        H_top, _, _, _, _ = layer_pair[1]

        LAYER_DICTS[i] = {
            'H_base': H_base,
            'H_top': H_top,
            'T': T,
            'beta': beta,
            'p': p,
            'name': layer_name,
        }

        if len(layer_name) > MAX_STR_LEN_LAYER_NAME:
            MAX_STR_LEN_LAYER_NAME = len(layer_name)


class Atmosphere:
    """
    Representation of the ICAO standard atmosphere (1993)

    * All input and output is using SI units
    * The main constructor takes the geometric (actual) height as input
    * Single values, vectors or matrices are accepted as input

    Usage:

    Compute a properties such as pressure for a given height:

        >>> Atmosphere(0).pressure
        array([101325.])

    Values out of valid height range will not be computed:

        >>> Atmosphere(-6e3)
        Traceback (most recent call last):
            ...
        ValueError: Value out of bounds. Lower limit: -5004 m. Upper limit: 81020 m.

    Create an atmosphere object with given support points (heights in metre):

        >>> atmos = Atmosphere([0, 1000, 5000, 17777, 35e3, 80e3])
        >>>

    Compute basic properties such as density, temperature or pressure:

        >>> atmos.density
        array([1.22500002e+00, 1.11165967e+00, 7.36428613e-01, 1.25975595e-01,
               8.46333291e-03, 1.84578859e-05])

        >>> atmos.temperature
        array([288.15      , 281.65102237, 255.67554322, 216.65      ,
               236.51337209, 198.63857625])

        >>> atmos.pressure
        array([1.01325000e+05, 8.98762776e+04, 5.40482622e+04, 7.83442282e+03,
               5.74591263e+02, 1.05246447e+00])
    """

    def __init__(self, h, check_bounds=True):
        """Return a new instance from given geometric height(s)"""

        self.h = self._make_tensor(h)
        if check_bounds and ((self.h < CONST.h_min-_EPS).any() or (self.h > CONST.h_max+_EPS).any()):
            raise ValueError(
                "Value out of bounds." +
                f" Lower limit: {CONST.h_min:.0f} m." +
                f" Upper limit: {CONST.h_max:.0f} m."
            )

        self._H = self.geom2geop_height(self.h)
        self._layer_nums = self._get_layer_nums()

    @classmethod
    def from_pressure(cls, p):
        """Return a new instance for given pressure value(s)"""

        p = cls._make_tensor(p)
        if (p < CONST.p_min-_EPS).any() or (p > CONST.p_max+_EPS).any():
            raise ValueError(
                "Value out of bounds." +
                f" Lower limit: {CONST.p_min:.1f} Pa." +
                f" Upper limit: {CONST.p_max:.1f} Pa."
            )

        def f(ht):
            # * Use log() for faster convergence in Newton method
            # * Allow Newton method to 'overshoot', do not check bounds
            return np.log10(p/cls(ht, check_bounds=False).pressure)

        # Initial guess is based on noting that log10(pressure) vs. height is
        # approximately a straight line. Height can be roughly estimated from
        # h/1[m] = 80e3 - 16e3*log10(p/1[Pa]) (tweaked slightly below).
        return cls(h=opt.newton(f, x0=81e3-16e3*np.log10(p)))

    def __str__(self):
        return f'{self.__class__.__qualname__}({self.h!r})'

    def __repr__(self):
        return f'{self.__class__.__qualname__}({self.h!r})'

    def __hash__(self):
        return hash(tuple(self.h))

    @property
    def h(self):
        """Geometric heights :math:`h`"""
        return self._h

    @h.setter
    def h(self, h):
        self._h = h

    @property
    def H(self):
        """Geopotential heights :math:`H`"""
        return self._H

    @property
    def layer_nums(self):
        """Array of same shape as 'self.H' with layer numbers (int)"""
        return self._layer_nums

    @staticmethod
    def _make_tensor(t):
        """Return a 'tensor object' from given user input"""

        # Number-like or array-like input is accepted
        if isinstance(t, (int, float, list, tuple)):
            t = np.asarray(t, dtype=float)
            if t.ndim == 0:
                t = t[None]  # Make 1D array
        elif not isinstance(t, np.ndarray):
            raise TypeError("Input data type not accepted")

        if t.size == 0:
            raise ValueError("Input array is empty")

        # Always work with float
        return t.astype(dtype=float)

    @staticmethod
    def geom2geop_height(h):
        """
        Convert geometric height :math:`h` to geopotential height :math:`H`

        :math:`H = \\frac{r h}{r + h}`
        """
        h = __class__._make_tensor(h)
        return CONST.r*h/(CONST.r + h)

    @staticmethod
    def geop2geom_height(H):
        """
        Convert geopotential height :math:`H` to geometric height :math:`h`

        :math:`h = \\frac{r H}{r - H}`
        """
        H = __class__._make_tensor(H)
        return CONST.r*H/(CONST.r - H)

    @staticmethod
    def t2T(t):
        """
        Convert from temperature :math:`t` in degree Celsius to :math:`T` in Kelvin

        :math:`T = t + T_i`
        """
        return CONST.T_i + __class__._make_tensor(t)

    @staticmethod
    def T2t(T):
        """
        Convert from temperature :math:`T` in Kelvin to :math:`t` in degree Celsius

        :math:`t = T - T_i`
        """
        return __class__._make_tensor(T) - CONST.T_i

    def _get_layer_nums(self):
        """Return array of same shape as 'self.H' with corresponding layer numbers"""

        layers = CONST.LAYER_DICTS
        layer_nums = np.zeros_like(self.H)

        for i in layers.keys():
            pos_in_layer = (self.H >= layers[i]['H_base']) & (self.H < layers[i]['H_top'])
            layer_nums += pos_in_layer.astype(int)*i

        # Special case: geopotential height < -5000
        pos_in_layer = (self.H < CONST.H_min).astype(int)
        layer_nums += pos_in_layer*CONST.LAYER_NUM_FIRST

        # Special case: geopotential height > 80000
        pos_in_layer = (self.H >= CONST.H_max).astype(int)
        layer_nums += pos_in_layer*CONST.LAYER_NUM_LAST

        return layer_nums.astype(int)

    def _get_layer_params(self):
        """
        Get layer specific data for given geopotential height 'H'

        Returns:
            :(H_b, T_b, beta): (tuple) layer specific data
        """

        H_b = np.zeros_like(self.H)
        T_b = np.zeros_like(self.H)
        beta = np.zeros_like(self.H)
        p_b = np.zeros_like(self.H)

        for i, layer_dict in CONST.LAYER_DICTS.items():
            pos_in_layer = (self.layer_nums == i).astype(int)

            H_b += pos_in_layer*layer_dict['H_base']
            T_b += pos_in_layer*layer_dict['T']
            beta += pos_in_layer*layer_dict['beta']
            p_b += pos_in_layer*layer_dict['p']

        return (H_b, T_b, beta, p_b)

    @property
    def layer_name(self):
        """Get layer names as strings"""

        str_len = CONST.MAX_STR_LEN_LAYER_NAME
        layer_name = np.char.chararray(self.H.shape, itemsize=str_len, unicode=True)
        layer_name[:] = ''

        for i, layer_dict in CONST.LAYER_DICTS.items():
            this_layer = np.char.chararray(self.H.shape, itemsize=str_len, unicode=True)
            this_layer[:] = layer_dict['name']

            pos_in_layer = (self.layer_nums == i).astype(int)
            this_layer_filtered = np.char.multiply(this_layer, pos_in_layer)

            layer_name = np.char.add(layer_name, this_layer_filtered)

        return layer_name

    @property
    def grav_accel(self):
        """Gravitational acceleration :math:`g`"""
        return CONST.g_0*(CONST.r/(CONST.r + self.h))**2

    @property
    def temperature(self):
        """Air temperature :math:`T` in Kelvin"""
        H_b, T_b, beta, _ = self._get_layer_params()
        return T_b + beta*(self.H - H_b)

    @property
    def temperature_in_celsius(self):
        """Air temperature :math:`t` in Celsius"""
        return self.T2t(self.temperature)

    @property
    def pressure(self):
        """Air pressure :math:`p`"""
        H_b, T_b, beta, p_b = self._get_layer_params()

        # Note: Pressure is computed differently for beta = 0 and for beta != 0
        # Get a vector with positions where beta is 0
        beta_zero = beta == 0
        beta_zero = beta_zero.astype(int)

        beta_nonzero = 1 - beta_zero
        pressure = np.zeros_like(beta)

        # Pressure if beta == 0
        T = self.temperature
        pressue_beta_zero = p_b*np.exp((-CONST.g_0/(CONST.R*T))*(self.H - H_b))
        pressure = pressure + pressue_beta_zero*beta_zero

        # Pressure if beta != 0
        exponent = np.divide(1, beta, out=np.zeros_like(beta), where=beta != 0)
        pressue_beta_nozero = p_b*(1 + (beta/T_b)*(self.H - H_b))**(exponent*(-CONST.g_0/CONST.R))
        pressure = pressure + pressue_beta_nozero*beta_nonzero
        return pressure

    @property
    def density(self):
        """Air density :math:`\\rho`"""
        return self.pressure/(CONST.R*self.temperature)

    @property
    def specific_weight(self):
        """Specific weight :math:`\\gamma`"""
        return self.density*self.grav_accel

    @property
    def pressure_scale_height(self):
        """Pressure scale height :math:`H_p`"""
        return CONST.R*self.temperature/self.grav_accel

    @property
    def number_density(self):
        """Number density :math:`n`"""
        return CONST.N_A*self.pressure/(CONST.R_star*self.temperature)

    @property
    def mean_particle_speed(self):
        """Mean particle speed :math:`\\bar{\\nu}`"""
        T = self.temperature
        return np.sqrt((8/np.pi)*CONST.R*T)

    @property
    def mean_free_path(self):
        """Mean free path :math:`l`"""
        return 1/(np.sqrt(2)*np.pi*CONST.sigma**2*self.number_density)

    @property
    def collision_frequency(self):
        """Collision frequency :math:`\\omega`"""
        return 4*CONST.sigma**2*CONST.N_A * \
            (np.sqrt(np.pi/(CONST.R_star*CONST.M_0))) * \
            (self.pressure/np.sqrt(self.temperature))

    @property
    def speed_of_sound(self):
        """Speed of sound :math:`a`"""
        return np.sqrt(CONST.kappa*CONST.R*self.temperature)

    @property
    def dynamic_viscosity(self):
        """Dynamic viscosity :math:`\\mu`"""
        T = self.temperature
        return CONST.beta_s*T**1.5/(T + CONST.S)

    @property
    def kinematic_viscosity(self):
        """Kinematic viscosity :math:`\\nu`"""
        return self.dynamic_viscosity/self.density

    @property
    def thermal_conductivity(self):
        """Thermal conductivity :math:`\\lambda`"""
        T = self.temperature
        return 2.648151e-3*T**1.5/(T + (245.4*10**(-12/T)))
