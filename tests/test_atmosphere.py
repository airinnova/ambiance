#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Aaron Dettmann

from collections import defaultdict

import pytest
from pytest import approx, main
import numpy as np

from ambiance import Atmosphere, CONST

from table_data import table_data


def test_version():
    from ambiance.__version__ import __version__
    print(__version__)


def test_repr():
    assert repr(Atmosphere(0)) == 'Atmosphere([0.0])'
    assert repr(Atmosphere([1, 100, 1000])) == 'Atmosphere([1.0, 100.0, 1000.0])'


def test_str():
    assert str(Atmosphere(0)) == 'Atmosphere([0.0])'
    assert str(Atmosphere([1, 100, 1000])) == 'Atmosphere([1.0, 100.0, 1000.0])'


def test_hash():
    assert isinstance(hash(Atmosphere(0)), int)
    a1 = Atmosphere(0)
    a2 = Atmosphere([1e0, 1e1, 1e2, 1e3, 1e4])
    d = {a1: 'sealevel', a2: 'range'}
    assert d[a1] == 'sealevel'
    assert d[a2] == 'range'


def test_invalid_inputs():
    """
    Do not allow strange input
    """

    with pytest.raises(TypeError):
        Atmosphere()

    type_errors = [
        None,
        dict,
        str,
    ]

    value_errors = [
        [],
        (),
        [[]],
        [1, [2, 3]]
    ]

    for invalid_input in type_errors:
        with pytest.raises(TypeError):
            Atmosphere(invalid_input)

    for invalid_input in value_errors:
        with pytest.raises(ValueError):
            Atmosphere(invalid_input)


def test_out_of_bounds_error():
    """
    Assert that errors are raised when height is too low or too high
    """

    # Minimal and maximal heights
    min_height = CONST.h_min
    max_height = CONST.h_max

    # Make exact values of min and max heights don't raise errors
    for boundary_height in [min_height, max_height]:
        try:
            Atmosphere(boundary_height)
        except ValueError:
            pytest.fail(f"ValueError for height {boundary_height} m...")

    invalid_inputs = [
        min_height-1,
        max_height+1,
        [1, 2, 3, min_height-1],
        [1, 2, 3, min_height-1, 50],
        [1, 2, 3, max_height+1],
        [1, 2, 3, max_height+1, 50],
    ]

    for invalid_input in invalid_inputs:
        with pytest.raises(ValueError):
            Atmosphere(invalid_input)


def test_sealevel():
    """
    Test sealevel conditions
    """

    sealevel = Atmosphere(0)

    # Geopotential and geometric height are equal
    assert sealevel.H == sealevel.h == 0

    # Table 1
    assert sealevel.temperature == 288.15
    assert sealevel.temperature_in_celsius == 15
    assert sealevel.pressure == 1.01325e5
    assert sealevel.density == approx(1.225)
    assert sealevel.grav_accel == 9.80665

    # Table 2
    assert sealevel.speed_of_sound == approx(340.294)
    assert sealevel.dynamic_viscosity == approx(1.7894e-5, 1e-4)
    assert sealevel.kinematic_viscosity == approx(1.4607e-5, 1e-4)
    assert sealevel.thermal_conductivity == approx(2.5343e-2, 1e-4)

    # Table 3
    assert sealevel.pressure_scale_height == approx(8434.5, 1e-4)
    assert sealevel.specific_weight == approx(1.2013e1, 1e-4)
    assert sealevel.number_density == approx(2.5471e25, 1e-4)
    assert sealevel.mean_particle_speed == approx(458.94, 1e-4)
    assert sealevel.collision_frequency == approx(6.9193e9, 1e-4)
    assert sealevel.mean_free_path == approx(6.6328e-8, 1e-4)


def test_table_data_single_value_input():
    """
    Test that data corresponds to tabularised data from "Doc 7488/3"
    """

    for h, entry in table_data.property_dict.items():
        print("="*80)
        print(f"Testing {h} m ...")
        for prop_name, value in entry.items():
            computed = float(getattr(Atmosphere(h), prop_name))
            # print(f"--> ({prop_name}) computed: {computed:.5e}")
            # print(f"--> ({prop_name}) expected: {value:.5e}")
            assert computed == approx(value, 1e-3)


def test_table_data_vector_input():
    """
    Test that vector can be passed as input (instead of single values)
    """

    # "Sorted" vectors
    heights, properties = table_data.get_vectors()
    atmos = Atmosphere(heights)

    for prop_name, exp_values in properties.items():
        computed_values = getattr(atmos, prop_name)
        # print(computed_values)
        # print(exp_values)
        assert np.testing.assert_allclose(computed_values, exp_values, rtol=1e-3) is None

    # Random vectors
    heights, properties = table_data.get_vectors(return_random=True)
    atmos = Atmosphere(heights)
    print(heights)

    for prop_name, exp_values in properties.items():
        computed_values = getattr(atmos, prop_name)
        assert np.testing.assert_allclose(computed_values, exp_values, rtol=1e-3) is None


def test_table_data_matrix_input():
    """
    Test that matrix can be passed as input (instead of single values)
    """

    # "Sorted" matrices
    heights, properties = table_data.get_matrices()
    atmos = Atmosphere(heights)

    for prop_name, exp_values in properties.items():
        computed_values = getattr(atmos, prop_name)
        assert np.testing.assert_allclose(computed_values, exp_values, rtol=1e-3) is None

    # Random matrices
    heights, properties = table_data.get_matrices(return_random=True)
    atmos = Atmosphere(heights)

    for prop_name, exp_values in properties.items():
        computed_values = getattr(atmos, prop_name)
        print(prop_name)
        print(computed_values)
        print()
        print(exp_values)
        print("--------------")
        assert np.testing.assert_allclose(computed_values, exp_values, rtol=1e-3) is None

    # "Differently shaped" matrices
    heights, properties = table_data.get_matrices(shape=(4, 5))
    atmos = Atmosphere(heights)

    for prop_name, exp_values in properties.items():
        computed_values = getattr(atmos, prop_name)
        print(prop_name)
        print(computed_values)
        print()
        print(exp_values)
        print("--------------")
        assert np.testing.assert_allclose(computed_values, exp_values, rtol=1e-3) is None


def test_data_types():
    """
    Test that input of different data types consistently produces same output

    See: https://github.com/aarondettmann/ambiance/issues/1
    """

    # ------------------------------
    # ----- Single value input -----
    # ------------------------------
    height = 11000
    entry = table_data.property_dict[height]

    h_types = [
        int(height),
        float(height),
        [int(height)],
        np.array(height, dtype=int),
        np.array(height, dtype=float),
    ]

    for h in h_types:
        print(repr(h))
        for prop_name, value in entry.items():
            computed = getattr(Atmosphere(h), prop_name)
            assert computed == approx(value, 1e-3)

    # -----------------------------------
    # ----- Vector-like value input -----
    # -----------------------------------
    heights = [11000, 20000, 75895]
    entries = [table_data.property_dict[height] for height in heights]

    exp_values = defaultdict(list)
    for entry in entries:
        for prop_name in table_data.PROPERTY_NAMES:
            exp_values[prop_name].append(entry[prop_name])

    h_types = [
        list(int(height) for height in heights),
        tuple(int(height) for height in heights),
        list(float(height) for height in heights),
        tuple(float(height) for height in heights),
        np.array(heights, dtype=int),
        np.array(heights, dtype=float),
    ]

    for h in h_types:
        print(repr(h))
        for prop_name, value in exp_values.items():
            computed = getattr(Atmosphere(h), prop_name)
            assert computed == approx(value, 1e-3)


def test_layer_names():
    """
    Test layer names
    """

    # Converter (layer boundaries are defined based on geopotential height)
    H2h = Atmosphere.geop2geom_height
    eps = 1e-6

    # Single value input
    assert Atmosphere(H2h(-3e3)).layer_name[0] == 'troposphere'
    assert Atmosphere(H2h(0)).layer_name[0] == 'troposphere'

    assert Atmosphere(H2h(11e3 + eps)).layer_name[0] == 'tropopause'
    assert Atmosphere(H2h(15e3)).layer_name[0] == 'tropopause'

    assert Atmosphere(H2h(20e3 + eps)).layer_name[0] == 'stratosphere'
    assert Atmosphere(H2h(25e3)).layer_name[0] == 'stratosphere'
    assert Atmosphere(H2h(32e3)).layer_name[0] == 'stratosphere'

    assert Atmosphere(H2h(47e3 + eps)).layer_name[0] == 'stratopause'
    assert Atmosphere(H2h(50e3)).layer_name[0] == 'stratopause'

    assert Atmosphere(H2h(51e3 + eps)).layer_name[0] == 'mesosphere'
    assert Atmosphere(H2h(75e3)).layer_name[0] == 'mesosphere'
    assert Atmosphere(H2h(80e3)).layer_name[0] == 'mesosphere'

    # Test matrix
    h = np.array([[0, 12, 22],
                 [30, 49, 75]])*1e3
    expected = np.char.array([['troposphere', 'tropopause', 'stratosphere'],
                             ['stratosphere', 'stratopause', 'mesosphere']])

    computed = Atmosphere(h).layer_name
    assert np.testing.assert_array_equal(computed, expected) is None


def test_kelvin_celsius_conversion():
    """
    Test conversion between temperature in degrees Celsius and Kelvin
    """

    # See: https://www.wolframalpha.com/input/?i=-30.00%C2%B0C+in+Kelvin
    # See: https://www.wolframalpha.com/input/?i=236.00%C2%B0C+in+Kelvin
    # See: https://www.wolframalpha.com/input/?i=555.24%C2%B0C+in+Kelvin
    celsius = [-30.00, 236.00, 555.24]
    kelvins = [243.15, 509.15, 828.39]

    # Test single inputs
    for degC, kel in zip(celsius, kelvins):
        assert Atmosphere.t2T(degC) == approx(kel)
        assert Atmosphere.T2t(kel) == approx(degC)

    # Test vector input
    assert Atmosphere.t2T(celsius) == approx(kelvins)
    assert Atmosphere.t2T(celsius[::-1]) == approx(kelvins[::-1])
    assert Atmosphere.T2t(kelvins) == approx(celsius)
    assert Atmosphere.T2t(kelvins[::-1]) == approx(celsius[::-1])

    # Make sure "back and forth" conversion works
    for t in np.arange(-200, 1000, 30):
        assert t == approx(Atmosphere.T2t(Atmosphere.t2T(t)))

    for T in np.arange(0, 1000, 30):
        assert T == approx(Atmosphere.t2T(Atmosphere.T2t(T)))


def test_geom_geop_height_conversion():
    """
    Test conversion between geometric and geopotential height
    """

    # Test different inputs
    inputs = [
        np.arange(-5e3, 80e3, 1e3),
        (-5e3, 80e3, 1e3),
        [-5e3, 80e3, 1e3],
        -5000,
    ]

    for in_data in inputs:
        geom_height_in = np.arange(-5e3, 80e3, 1e3)

        geop_height_out = Atmosphere.geom2geop_height(geom_height_in)
        geom_height_out = Atmosphere.geop2geom_height(geop_height_out)

        assert np.testing.assert_allclose(geom_height_out, geom_height_in) is None


if __name__ == '__main__':
    main()
