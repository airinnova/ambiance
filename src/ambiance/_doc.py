#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
List of properties for documentation purposes
"""


class V:
    def __init__(self, *, symb='', name='', unit=''):
        self.symb = symb
        self.name = name
        self.unit = unit


class P:
    def __init__(self, name, unit='', name_long='', *, log=False, symb='', eq=''):
        self.name = name
        self.unit = unit
        self.name_long = name_long if name_long else self.name.replace('_', ' ').capitalize()
        self.log = log
        self.symb = symb
        self.eq = eq


vars_const = (
    V(
        symb='g_0',
        name='Standard gravitational acceleration',
        unit='m/s²',
    ),
    V(
        symb='M_0',
        name='Sea level mean molar mass',
        unit='kg/mol',
    ),
    V(
        symb='N_A',
        name='Avogadro constant',
        unit='mol⁻¹',
    ),
    V(
        symb='P_0',
        name='Sea level atmospheric pressure',
        unit='Pa',
    ),
    V(
        symb='R^{*}',
        name='Universal gas constant',
        unit='J/(K·mol)',
    ),
    V(
        symb='R',
        name='Specific gas constant',
        unit='J/(K·kg)',
    ),
    V(
        symb='S',
        name='Sutherland\'s empirical constant in the equation for dynamic viscosity',
        unit='K',
    ),
    V(
        symb='T_i',
        name='Temperature of the ice point at mean sea level',
        unit='K',
    ),
    V(
        symb='T_0',
        name='Sea level temperature',
        unit='K',
    ),
    V(
        symb='t_i',
        name='Celsius temperature of the ice point at mean sea level',
        unit='°C',
    ),
    V(
        symb='t_0',
        name='Celsius sea level temperature',
        unit='°C',
    ),
    V(
        symb='\\beta_s',
        name='Sutherland\'s empirical constant in the equation for dynamic viscosity',
        unit='kg/(m·s·K^(1/2))',
    ),
    V(
        symb='\\kappa',
        name='Adiabatic index',
        unit='1',
    ),
    V(
        symb='\\rho_0',
        name='Sea level atmospheric density',
        unit='kg/m³',
    ),
    V(
        symb='\\sigma',
        name='Effective collision diameter of an air molecule',
        unit='m',
    ),
    V(
        symb='r',
        name='Nominal Earth\'s radius',
        unit='m',
    ),
)


props = (
    P(
        'collision_frequency',
        'Hz',
        log=True,
        symb='\\omega',
        eq='\\omega = 4 \\sigma^2 N_A \\left( \\frac{\\pi}{R^{*} M_0} \\right)^{1/2} \\frac{p}{\\sqrt{T}}',
    ),
    P(
        'density',
        'kg/m³',
        log=True,
        symb='\\rho',
        eq='\\rho = \\frac{p}{R T}'
    ),
    P(
        'dynamic_viscosity',
        'Pa·s',
        symb='\\mu',
        eq='\\mu = \\frac{\\beta_s T^{3/2}}{T + S}',
    ),
    P(
        'grav_accel',
        'm/s²',
        'Gravitational acceleration',
        symb='g',
        eq='g = g_0 \\left( \\frac{r}{r + h} \\right)^2'
    ),
    P(
        'kinematic_viscosity',
        'm²/s',
        log=True,
        symb='\\nu',
        eq='\\nu = \\frac{\\mu}{\\rho}',
    ),
    P(
        'mean_free_path',
        'm',
        log=True,
        symb='l',
        eq='l = \\frac{1}{\\sqrt{2} \\pi \\sigma^2 n}',
    ),
    P(
        'mean_particle_speed',
        'm/s',
        symb='\\bar{\\nu}',
        eq='\\bar{\\nu} = \\left( \\frac{8}{\\pi} R T \\right)^{1/2}',

    ),
    P(
        'number_density',
        'm⁻³',
        log=True,
        symb='n',
        eq='n = \\frac{N_A p}{R^{*} T}',
    ),
    P(
        'pressure',
        'Pa',
        log=True,
        symb='p',
        eq=(
          'p = p_b \\exp \\left[ - \\frac{g_0}{R T} (H - H_b) \\right] \\quad \\text{for} \\quad \\beta = 0',
          'p = p_b \\left[ 1 + \\frac{\\beta}{T_b} (H - H_b) \\right]^{-g_0 \\beta / R} \\quad \\text{for} \\quad \\beta \\neq 0',
        ),
    ),
    P(
        'pressure_scale_height',
        'm',
        symb='H_p',
        eq='H_p = \\frac{R T}{g}',
    ),
    P(
        'specific_weight',
        'N/m³',
        log=True,
        symb='\\gamma',
        eq='\\gamma = \\rho g',
    ),
    P(
        'speed_of_sound',
        'm/s',
        symb='a',
        eq='a = \\sqrt{\\kappa R T}',
    ),
    P(
        'temperature',
        'K',
        symb='T',
        eq='T = T_b + \\beta (H - H_b)',
    ),
    P(
        'temperature_in_celsius',
        '°C',
        'Temperature (Celsius)',
        symb='t',
        eq='t = T - T_i',
    ),
    P(
        'thermal_conductivity',
        'W/(m·K)',
        symb='\\lambda',
        eq='\\lambda = \\frac{2.648151 \\cdot 10^{-3} T^{3/2}}{T + (245.4 \\cdot 10^{-12/T})}'
    ),
)
