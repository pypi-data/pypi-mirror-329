import numpy as np

from skq.constants import *


def photon_energy(frequency):
    return PLANCK_CONSTANT * frequency


def blackbody_radiance(frequency, temperature):
    return (2 * PLANCK_CONSTANT * frequency**3 / SPEED_OF_LIGHT**2) / (np.exp(PLANCK_CONSTANT * frequency / (BOLTZMANN_CONSTANT * temperature)) - 1)


def hydrogen_energy_level(n):
    return -(REDUCED_PLANCK_CONSTANT**2 * SPEED_OF_LIGHT * ELECTRON_CHARGE**4) / (8 * np.pi**2 * PERMITTIVITY_OF_FREE_SPACE**2 * REDUCED_PLANCK_CONSTANT**2 * n**2)


def coulomb_force(q1, q2, r):
    return (1 / (4 * np.pi * PERMITTIVITY_OF_FREE_SPACE)) * (q1 * q2) / r**2


def test_photon_energy():
    frequency = 1e14
    expected_energy = 6.62607015e-20
    calculated_energy = photon_energy(frequency)
    assert np.isclose(calculated_energy, expected_energy, rtol=1e-9), f"Photon energy is incorrect: {calculated_energy} != {expected_energy}"


def test_blackbody_radiance():
    frequency = 1e14
    temperature = 300
    expected_radiance = 3.74177e-19 / (np.exp(4.799243073e-02) - 1)
    calculated_radiance = blackbody_radiance(frequency, temperature)
    assert np.isclose(calculated_radiance, expected_radiance, rtol=1e-9), f"Blackbody radiance is incorrect: {calculated_radiance} != {expected_radiance}"


def test_permittivity_and_permeability_of_free_space():
    expected_speed_of_light = 1 / np.sqrt(PERMEABILITY_OF_FREE_SPACE * PERMITTIVITY_OF_FREE_SPACE)
    assert np.isclose(expected_speed_of_light, SPEED_OF_LIGHT, rtol=1e-9), f"Calculated speed of light is incorrect: {expected_speed_of_light} != {SPEED_OF_LIGHT}"


def test_hydrogen_energy_level():
    expected_energy = -2.1798723611035e-18
    calculated_energy = hydrogen_energy_level(1)
    assert np.isclose(calculated_energy, expected_energy, rtol=1e-9), f"Hydrogen energy level is incorrect: {calculated_energy} != {expected_energy}"


def test_coulomb_force():
    expected_force = 2.307077551e-8
    calculated_force = coulomb_force(ELECTRON_CHARGE, ELECTRON_CHARGE, 1e-10)
    assert np.isclose(calculated_force, expected_force, rtol=1e-9), f"Coulomb force is incorrect: {calculated_force} != {expected_force}"
