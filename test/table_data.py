#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Aaron Dettmann

# --> Should check geopotential rather geometric

# ===== LAYER CHANGES =====
# OK --> -5.0e3
# OK -2500
# OK --> 0.00e3
# OK 2000
# OK --> 11.0e3
# OK 15000
# OK --> 20.0e3
# OK 25000
# *OK --> 32.0e3
# *OK 41_000
# *OK --> 47.0e3
# *OK 50_000
# *OK --> 51.0e3
# *OK 61_000
# *OK --> 71.0e3
# *OK 75_000
# *OK --> 80.0e3


from collections import defaultdict
import random


class TableData:
    """
    Tabularised data from standard atmosphere
    """

    PROPERTY_NAMES = [
            # Table 1
            "geom_height",
            "geop_height",
            "temperature",
            "temperature_in_celsius",
            "pressure",
            "density",
            "grav_accel",

            # Table 2
            "speed_of_sound",
            "dynamic_viscosity",
            "kinematic_viscosity",
            "thermal_conductivity",

            # Table 3
            "pressure_scale_height",
            "specific_weight",
            "number_density",
            "mean_particle_speed",
            "collision_frequency",
            "mean_free_path",
            ]

    def __init__(self):
        self.property_dict = {}

    def add_entry(self, h, entry):
        # Dictionary: h (geometric height) --> property dict
        self.property_dict[h] = entry

    def get_vectors(self, return_random=False, list_len=10):
        height = []
        properties = defaultdict(list)

        # -------------------------------------------------------------------
        # Random list
        # -------------------------------------------------------------------
        if return_random:
            for _ in range(list_len):
                h, entry_dict = random.choice(list(self.property_dict.items()))
                height.append(h)

                for prop_name, value in entry_dict.items():
                    properties[prop_name].append(value)
        # -------------------------------------------------------------------
        # Sorted
        # -------------------------------------------------------------------
        else:
            for h, entry_dict in self.property_dict.items():
                height.append(h)

                for prop_name, value in entry_dict.items():
                    properties[prop_name].append(value)

        return height, properties


table_data = TableData()

table_data.add_entry(
        h=-5000,
        entry={
            "H": -5004,
            "temperature": 320.676,
            "temperature_in_celsius": 47.526,
            "pressure": 1.77762e5,
            "density": 1.93113,
            "grav_accel": 9.8221,
            # ----------
            "speed_of_sound": 358.986,
            "dynamic_viscosity": 1.9422e-5,
            "kinematic_viscosity": 1.0058e-5,
            "thermal_conductivity": 2.7861e-2,
            # ----------
            "pressure_scale_height": 9371.8,
            "specific_weight": 1.8968e1,
            "number_density": 4.0154e25,
            "mean_particle_speed": 484.15,
            "collision_frequency": 1.1507e10,
            "mean_free_path": 4.2075e-8,
            }
        )

table_data.add_entry(
        h=-2500,
        entry={
            "H": -2501,
            "temperature": 304.406,
            "temperature_in_celsius": 31.265,
            "pressure": 1.35205e5,
            "density": 1.54731,
            "grav_accel": 9.8144,
            # ----------
            "speed_of_sound": 349.761,
            "dynamic_viscosity": 1.8668e-5,
            "kinematic_viscosity": 1.2065e-5,
            "thermal_conductivity": 2.6611e-2,
            # ----------
            "pressure_scale_height": 8903.3,
            "specific_weight": 1.5186e1,
            "number_density": 3.2173e25,
            "mean_particle_speed": 471.71,
            "collision_frequency": 8.9830e9,
            "mean_free_path": 5.2512e-8,
            }
        )

table_data.add_entry(
        h=0,
        entry={
            "H": 0,
            "temperature": 288.15,
            "temperature_in_celsius": 15,
            "pressure": 1.01325e5,
            "density": 1.225,
            "grav_accel": 9.80665,
            # ----------
            "speed_of_sound": 340.294,
            "dynamic_viscosity": 1.7894e-5,
            "kinematic_viscosity": 1.4607e-5,
            "thermal_conductivity": 2.5343e-2,
            # ----------
            "pressure_scale_height": 8434.5,
            "specific_weight": 1.2013e1,
            "number_density": 2.5471e25,
            "mean_particle_speed": 458.94,
            "collision_frequency": 6.9193e9,
            "mean_free_path": 6.6328e-8,
            }
        )

table_data.add_entry(
        h=1000,
        entry={
            "H": 1000,
            "temperature": 281.651,
            "temperature_in_celsius": 8.501,
            "pressure": 8.98763e4,
            "density": 1.11166,
            "grav_accel": 9.8036,
            # ----------
            "speed_of_sound": 336.435,
            "dynamic_viscosity": 1.7579e-5,
            "kinematic_viscosity": 1.5813e-5,
            "thermal_conductivity": 2.4830e-2,
            # ----------
            "pressure_scale_height": 8246.9,
            "specific_weight": 1.0898e1,
            "number_density": 2.3115e25,
            "mean_particle_speed": 453.74,
            "collision_frequency": 6.2079e9,
            "mean_free_path": 7.3090e-8,
            }
        )

table_data.add_entry(
        h=2000,
        entry={
            "H": 1999,
            "temperature": 275.154,
            "temperature_in_celsius": 2.004,
            "pressure": 7.95014e4,
            "density": 1.00655,
            "grav_accel": 9.8005,
            # ----------
            "speed_of_sound": 332.532,
            "dynamic_viscosity": 1.7260e-5,
            "kinematic_viscosity": 1.7147e-5,
            "thermal_conductivity": 2.4314e-2,
            # ----------
            "pressure_scale_height": 8059.2,
            "specific_weight": 9.8647,
            "number_density": 2.0929e25,
            "mean_particle_speed": 448.48,
            "collision_frequency": 5.5558e9,
            "mean_free_path": 8.0723e-8,
            }
        )

table_data.add_entry(
        h=11_000,
        entry={
            "H": 10981,
            "temperature": 216.774,
            "temperature_in_celsius": -56.376,
            "pressure": 2.26999e4,
            "density": 3.64801e-1,
            "grav_accel": 9.7728,
            # ----------
            "speed_of_sound": 295.154,
            "dynamic_viscosity": 1.4223e-5,
            "kinematic_viscosity": 3.8988e-5,
            "thermal_conductivity": 1.9528e-2,
            # ----------
            "pressure_scale_height": 6367.2,
            "specific_weight": 3.5651,
            "number_density": 7.5853e24,
            "mean_particle_speed": 398.07,
            "collision_frequency": 1.7872e9,
            "mean_free_path": 2.2273e-7,
            }
        )

table_data.add_entry(
        h=15_000,
        entry={
            "H": 14965,
            "temperature": 216.650,
            "temperature_in_celsius": -56.500,
            "pressure": 1.21118e4,
            "density": 1.94755e-1,
            "grav_accel": 9.7605,
            # ----------
            "speed_of_sound": 295.069,
            "dynamic_viscosity": 1.4216e-5,
            "kinematic_viscosity": 7.2995e-5,
            "thermal_conductivity": 1.9518e-2,
            # ----------
            "pressure_scale_height": 6371.6,
            "specific_weight": 1.9009,
            "number_density": 4.0495e24,
            "mean_particle_speed": 397.95,
            "collision_frequency": 9.5386e8,
            "mean_free_path": 4.1720e-7,
            }
        )

table_data.add_entry(
        h=20_000,
        entry={
            "H": 19937,
            "temperature": 216.650,
            "temperature_in_celsius": -56.500,
            "pressure": 5.52929e3,
            "density": 8.89097e-2,
            "grav_accel": 9.7452,
            # ----------
            "speed_of_sound": 295.069,
            "dynamic_viscosity": 1.4216e-5,
            "kinematic_viscosity": 1.5989e-4,
            "thermal_conductivity": 1.9518e-2,
            # ----------
            "pressure_scale_height": 6381.6,
            "specific_weight": 8.6645e-1,
            "number_density": 1.8487e24,
            "mean_particle_speed": 397.95,
            "collision_frequency": 4.3546e8,
            "mean_free_path": 9.1387e-7,
            }
        )

table_data.add_entry(
        h=25_000,
        entry={
            "H": 24902,
            "temperature": 221.552,
            "temperature_in_celsius": -51.598,
            "pressure": 2.54921e3,
            "density": 4.00837e-2,
            "grav_accel": 9.7300,
            # ----------
            "speed_of_sound": 298.389,
            "dynamic_viscosity": 1.4484e-5,
            "kinematic_viscosity": 3.6135e-4,
            "thermal_conductivity": 1.9930e-2,
            # ----------
            "pressure_scale_height": 6536.2,
            "specific_weight": 3.9001e-1,
            "number_density": 8.3346e23,
            "mean_particle_speed": 402.43,
            "collision_frequency": 1.9853e8,
            "mean_free_path": 2.0270e-6,
            }
        )

table_data.add_entry(
        h=32_162,
        entry={
            "H": 32000,
            "temperature": 228.650,
            "temperature_in_celsius": -44.500,
            "pressure": 8.68014e2,
            "density": 1.32249e-2,
            "grav_accel": 9.7082,
            # ----------
            "speed_of_sound": 303.131,
            "dynamic_viscosity": 1.4868e-5,
            "kinematic_viscosity": 1.1242e-3,
            "thermal_conductivity": 2.0523e-2,
            # ----------
            "pressure_scale_height": 6760.8,
            "specific_weight": 1.2839e-1,
            "number_density": 2.7499e23,
            "mean_particle_speed": 408.82,
            "collision_frequency": 6.6542e7,
            "mean_free_path": 6.1438e-6,
            }
        )

table_data.add_entry(
        h=41_266,
        entry={
            "H": 41000,
            "temperature": 253.850,
            "temperature_in_celsius": -19.300,
            "pressure": 2.42394e2,
            "density": 3.32646e-3,
            "grav_accel": 9.6806,
            # ----------
            "speed_of_sound": 319.399,
            "dynamic_viscosity": 1.6189e-5,
            "kinematic_viscosity": 4.8668e-3,
            "thermal_conductivity": 2.2599e-2,
            # ----------
            "pressure_scale_height": 7527.3,
            "specific_weight": 3.2202e-2,
            "number_density": 6.9167e22,
            "mean_particle_speed": 430.76,
            "collision_frequency": 1.7636e7,
            "mean_free_path": 2.4426e-5,
            }
        )

table_data.add_entry(
        h=47_350,
        entry={
            "H": 47000,
            "temperature": 270.650,
            "temperature_in_celsius": -2.500,
            "pressure": 1.10906e2,
            "density": 1.42752e-3,
            "grav_accel": 9.6622,
            # ----------
            "speed_of_sound": 329.799,
            "dynamic_viscosity": 1.7037e-5,
            "kinematic_viscosity": 1.1934e-2,
            "thermal_conductivity": 2.3954e-2,
            # ----------
            "pressure_scale_height": 8040.7,
            "specific_weight": 1.3793e-2,
            "number_density": 2.9683e22,
            "mean_particle_speed": 444.79,
            "collision_frequency": 7.8146e6,
            "mean_free_path": 5.6918e-5,
            }
        )

table_data.add_entry(
        h=50_396,
        entry={
            "H": 50000,
            "temperature": 270.650,
            "temperature_in_celsius": -2.500,
            "pressure": 7.59443e1,
            "density": 9.77519e-4,
            "grav_accel": 9.6530,
            # ----------
            "speed_of_sound": 329.799,
            "dynamic_viscosity": 1.7037e-5,
            "kinematic_viscosity": 1.7429e-2,
            "thermal_conductivity": 2.3954e-2,
            # ----------
            "pressure_scale_height": 8048.4,
            "specific_weight": 9.4360e-3,
            "number_density": 2.0326e22,
            "mean_particle_speed": 444.79,
            "collision_frequency": 5.3512e6,
            "mean_free_path": 8.3120e-5,
            }
        )

table_data.add_entry(
        h=51_412,
        entry={
            "H": 51000,
            "temperature": 270.650,
            "temperature_in_celsius": -2.500,
            "pressure": 6.69384e1,
            "density": 8.61600e-4,
            "grav_accel": 9.6499,
            # ----------
            "speed_of_sound": 329.799,
            "dynamic_viscosity": 1.7037e-5,
            "kinematic_viscosity": 1.9773e-2,
            "thermal_conductivity": 2.3954e-2,
            # ----------
            "pressure_scale_height": 8050.9,
            "specific_weight": 8.3144e-3,
            "number_density": 1.7915e22,
            "mean_particle_speed": 444.79,
            "collision_frequency": 4.7166e6,
            "mean_free_path": 9.4303e-5,
            }
        )

table_data.add_entry(
        h=61_591,
        entry={
            "H": 61000,
            "temperature": 242.650,
            "temperature_in_celsius": -30.500,
            "pressure": 1.76605e1,
            "density": 2.53548e-4,
            "grav_accel": 9.6193,
            # ----------
            "speed_of_sound": 312.274,
            "dynamic_viscosity": 1.5610e-5,
            "kinematic_viscosity": 6.1565e-2,
            "thermal_conductivity": 2.1683e-2,
            # ----------
            "pressure_scale_height": 7241.0,
            "specific_weight": 2.4390e-3,
            "number_density": 5.2720e21,
            "mean_particle_speed": 421.15,
            "collision_frequency": 1.3142e6,
            "mean_free_path": 3.2046e-4,
            }
        )

table_data.add_entry(
        h=71_802,
        entry={
            "H": 71000,
            "temperature": 214.650,
            "temperature_in_celsius": -58.500,
            "pressure": 3.95639e0,
            "density": 6.42105e-5,
            "grav_accel": 9.5888,
            # ----------
            "speed_of_sound": 293.704,
            "dynamic_viscosity": 1.4106e-5,
            "kinematic_viscosity": 2.1968e-1,
            "thermal_conductivity": 1.9349e-2,
            # ----------
            "pressure_scale_height": 6425.8,
            "specific_weight": 6.1570e-4,
            "number_density": 1.3351e21,
            "mean_particle_speed": 396.11,
            "collision_frequency": 3.1303e5,
            "mean_free_path": 1.2654e-3,
            }
        )

table_data.add_entry(
        h=75_895,
        entry={
            "H": 75000,
            "temperature": 206.650,
            "temperature_in_celsius": -66.500,
            "pressure": 2.06790e0,
            "density": 3.48604e-5,
            "grav_accel": 9.5766,
            # ----------
            "speed_of_sound": 288.179,
            "dynamic_viscosity": 1.3661e-5,
            "kinematic_viscosity": 3.9188e-1,
            "thermal_conductivity": 1.8671e-2,
            # ----------
            "pressure_scale_height": 6194.2,
            "specific_weight": 3.3384e-4,
            "number_density": 7.2485e20,
            "mean_particle_speed": 388.66,
            "collision_frequency": 1.6675e5,
            "mean_free_path": 2.3308e-3,
            }
        )

table_data.add_entry(
        h=81_020,
        entry={
            "H": 80000,
            "temperature": 196.650,
            "temperature_in_celsius": -76.500,
            "pressure": 8.86272e-1,
            "density": 1.57004e-5,
            "grav_accel": 9.5614,
            # ----------
            "speed_of_sound": 281.120,
            "dynamic_viscosity": 1.3095e-5,
            "kinematic_viscosity": 8.3402e-1,
            "thermal_conductivity": 1.7817e-2,
            # ----------
            "pressure_scale_height": 5903.9,
            "specific_weight": 1.5012e-4,
            "number_density": 3.2646e20,
            "mean_particle_speed": 379.14,
            "collision_frequency": 7.3262e4,
            "mean_free_path": 5.1751e-3,
            }
        )
