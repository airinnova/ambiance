#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ======================================================================
# AMBIANCE -- A full implementation of the ICAO standard atmosphere 1993
#
#  Copyright 2019 Aaron Dettmann
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

The implementation is based on the ICAO standard atmosphere from 1993:

    | International Civil Aviation Organization
    | Manual Of The Icao Standard Atmosphere -- 3rd Edition 1993 (Doc 7488)
    | -- extended to 80 kilometres (262 500 feet)

See:
    https://store.icao.int/manual-of-the-icao-standard-atmosphere-extended
    -to- 80-kilometres-262-500-feet-doc-7488-quadrilingual-printed.html
"""

from itertools import tee

import numpy as np


def pairwise(iterable):
    """
    Iterate pairwise

    s -> (s0,s1), (s1,s2), (s2, s3), ...

    See: https://docs.python.org/3/library/itertools.html
    """

    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class Constant:
    """
    Constants defined in the ICAO standard atmosphere (1993)

    Notes:
        * All values are given in SI-units.

    Attributes:
        :g_0: Standard gravitational acceleration [m/s^2]
        :M_0: Sea level molar mass [kg/mol]
        :N_A: Avogadro constant [1/mol]
        :P_0: Sea level atmospheric pressure [Pa]
        :R_star: Universal gas constant [J/K*mol]
        :R: Specific gas constant [J/K*kg]
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
        :LAYER_SPECIFIC_PROPERTIES: Table containing layer specific properties
    """

    # Table A: primary constants
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

    # Table D (pressure was added)
    # H_b [m] | T_b [K] | beta [kg/(m*s*K^(1/2))] | p [Pa]
    LAYER_SPEC_PROP = [
        [-5.0e3, 320.65, -6.5e-3, 1.77687e+5],
        [0.00e3, 288.15, -6.5e-3, 1.01325e+5],
        [11.0e3, 216.65,  0.0e-3, 2.26320e+4],
        [20.0e3, 216.65,  1.0e-3, 5.47487e+3],
        [32.0e3, 228.65,  2.8e-3, 8.68014e+2],
        [47.0e3, 270.65,  0.0e-3, 1.10906e+2],
        [51.0e3, 270.65, -2.8e-3, 6.69384e+1],
        [71.0e3, 214.65, -2.0e-3, 3.95639e+0],
        [80.0e3, 196.65, -2.0e-3, 8.86272e-1],
        ]


class Atmosphere:
    """
    Representation of the ICAO standard atmosphere (1993)

    * All input and output is using the basic SI-units
    * Input for computation of atmospheric properties is generally the GEOMETRIC (actual) height
    * Either a single value or a height range can be given as input

    Usage:

    Compute a properties such as pressure for a given height:

        >>> Atmosphere(0).pressure
        array([101325.])

    Values out of valid height range will not be computed:

        >>> Atmosphere(-6e3)
        Traceback (most recent call last):
            ...
        ValueError: ('Value out of bounds.', 'Lower limit: -5004 m, ', 'Upper limit: 81020 m')

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

    def __init__(self, h):
        # Store the geometric and geopotential height.
        # All other properties are computed on demand.
        self.h = h
        self._parse_height()
        self.H = self.geom2geop_height()

    def __str__(self):
        return f'{self.__class__.__name__}({list(self.h)})'

    def __repr__(self):
        return f'{self.__class__.__name__}({list(self.h)})'

    def _parse_height(self):
        """
        Check and return correct representation of geometric height 'h'

        For internal use. Not intended to be called by the user.
        """

        # Number-like or array-like input is accepted
        if isinstance(self.h, (int, float, list, tuple)):
            self.h = np.asarray(self.h)

            if self.h.ndim == 0:
                self.h = self.h[None]  # Make 1D array

        elif not isinstance(self.h, np.ndarray):
            raise TypeError('Input data type not accepted')

        if self.h.size == 0:
            raise ValueError("Input array is empty")

        # Check that input height is in correct range
        if any([(height < Constant.h_min or height > Constant.h_max) for height in self.h]):
            raise ValueError(
                    'Value out of bounds.',
                    f'Lower limit: {Constant.h_min:.0f} m, ',
                    f'Upper limit: {Constant.h_max:.0f} m')

    def geom2geop_height(self):
        """Convert geometric height 'h' to geopotential height 'H'"""

        return Constant.r*self.h/(Constant.r + self.h)

    def geop2geom_height(self):
        """Convert geopotential height 'H' to geometric height 'h'"""

        return Constant.r*self.H/(Constant.r - self.H)

    @staticmethod
    def t2T(t):
        """Convert from temperature 't' in degree Celsius to 'T' in Kelvin"""

        return Constant.T_i + np.asarray(t)

    @staticmethod
    def T2t(T):
        """Convert from temperature 'T' in Kelvin to 't' in degree Celsius"""

        return np.asarray(T) - Constant.T_i

    def _get_layer_params(self):
        """Get layer specific data for given geopotential height 'H'

        For internal use. Not intended to be called by the user.

        Return:
            :(H_b, T_b, beta): (tuple) layer specific data
        """

        prop = Constant.LAYER_SPEC_PROP

        H_b = np.array([])
        T_b = np.array([])
        beta = np.array([])
        p_b = np.array([])

        for H in self.H:
            for row1, row2 in pairwise(prop):
                H_layer1 = row1[0]
                H_layer2 = row2[0]

                if H_layer1 <= H < H_layer2 or H < -5000:
                    H_b = np.append(H_b, [row1[0]])
                    T_b = np.append(T_b, [row1[1]])
                    beta = np.append(beta, [row1[2]])
                    p_b = np.append(p_b, [row1[3]])
                    break

                # Last layer
                elif H > 80_000 and H_layer2 == 80_000:
                    H_b = np.append(H_b, [row2[0]])
                    T_b = np.append(T_b, [row2[1]])
                    beta = np.append(beta, [row2[2]])
                    p_b = np.append(p_b, [row2[3]])
                    break

        return (H_b, T_b, beta, p_b)

    @property
    def grav_accel(self):
        """Compute gravitational acceleration 'g' for given geometric height 'h'"""

        return Constant.g_0*(Constant.r/(Constant.r + self.h))**2

    @property
    def temperature(self):
        """Compute the air temperature :T: for given geometric height 'h'"""

        H_b, T_b, beta, _ = self._get_layer_params()
        return T_b + beta*(self.H - H_b)

    @property
    def temperature_in_celsius(self):
        """Compute the air temperature 'T' in Celsius for given geometric height 'h'"""

        return self.T2t(self.temperature)

    @property
    def pressure(self):
        """Compute the air pressure 'p' for given geometric height 'h'"""

        H_b, T_b, beta, p_b = self._get_layer_params()

        # Note: Pressure is computed differently for beta = 0 and for beta != 0
        # Get a vector with positions where beta is 0
        beta_zero = beta == 0
        beta_zero = beta_zero.astype(int)

        beta_nonzero = 1 - beta_zero
        pressure = np.zeros_like(beta)

        # Pressure if beta == 0
        T = self.temperature
        pressue_beta_zero = p_b*np.exp((-Constant.g_0/(Constant.R*T))*(self.H - H_b))
        pressure = pressure + pressue_beta_zero*beta_zero

        # Pressure if beta != 0
        exponent = np.divide(1, beta, out=np.zeros_like(beta), where=beta!=0)
        pressue_beta_nozero = p_b*(1 + (beta/T_b)*(self.H - H_b))**(exponent*(-Constant.g_0/Constant.R))
        pressure = pressure + pressue_beta_nozero*beta_nonzero

        return pressure

    @property
    def density(self):
        """Compute the air density 'rho' for given geometric height 'h'"""

        p = self.pressure
        T = self.temperature
        return p/(Constant.R*T)

    @property
    def specific_weight(self):
        """Compute the specific weight 'gamma' for given geometric height 'h'"""

        return self.density*self.grav_accel

    @property
    def pressure_scale_height(self):
        """Compute the pressure scale height 'H_p' for given geometric height 'h'"""

        T = self.temperature
        g = self.grav_accel
        return Constant.R*T/g

    @property
    def number_density(self):
        """Compute the number density :n: for given geometric height 'h'"""

        p = self.pressure
        T = self.temperature
        return Constant.N_A*p/(Constant.R_star*T)

    @property
    def mean_particle_speed(self):
        """Compute the mean particle speed :nu_bar: for given geometric height 'h'"""

        T = self.temperature
        return np.sqrt((8/np.pi)*Constant.R*T)

    @property
    def mean_free_path(self):
        """Compute the mean free path :l: for given geometric height 'h'"""

        n = self.number_density
        return 1/(np.sqrt(2)*np.pi*Constant.sigma**2*n)

    @property
    def collision_frequency(self):
        """Compute the collision frequency 'omega' for given geometric height 'h'"""

        p = self.pressure
        T = self.temperature
        return 4*Constant.sigma**2*Constant.N_A*(np.sqrt(np.pi/(Constant.R_star*Constant.M_0)))*(p/np.sqrt(T))

    @property
    def speed_of_sound(self):
        """Compute the speed of sound 'a' for given geometric height 'h'"""

        T = self.temperature
        return np.sqrt(Constant.kappa*Constant.R*T)

    @property
    def dynamic_viscosity(self):
        """Compute the dynamic viscosity 'mu' for given geometric height 'h'"""

        T = self.temperature
        return Constant.beta_s*T**(3.0/2)/(T + Constant.S)

    @property
    def kinematic_viscosity(self):
        """Compute the kinematic viscosity 'nu' for given geometric height 'h'"""

        mu = self.dynamic_viscosity
        rho = self.density
        return mu/rho

    @property
    def thermal_conductivity(self):
        """Compute the thermal conductivity 'lambda' for given geometric height 'h'"""

        T = self.temperature
        return 2.648151e-3*T**(3/2)/(T + (245.4*10**(-12/T)))
