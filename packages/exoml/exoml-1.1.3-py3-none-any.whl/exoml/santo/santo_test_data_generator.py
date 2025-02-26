import logging
import sys
from abc import ABC

import matplotlib.pyplot as plt
import random
from typing import Tuple
import ellc
import numpy as np
from numpy import ndarray
from numpy.random import default_rng
import astropy.units as u
import astropy.constants as ac
import timesynth


class FeaturesInjector(ABC):
    random_number_generator = default_rng()

    def __init__(self, time: ndarray, original_flux: ndarray):
        super().__init__()
        self.time = time
        self.original_flux = original_flux

    def inject(self) -> tuple[ndarray, ndarray]:
        pass

class RedNoiseInjector(FeaturesInjector):
    def __init__(self, time: ndarray, original_flux: ndarray, power: tuple[float, float], period: tuple[float, float], number_of_signals: int):
        super().__init__(time, original_flux)
        self.power = power
        self.period = period
        self.number_of_signals = number_of_signals

    def inject(self) -> tuple[ndarray, ndarray]:
        number_of_red_noise = random.uniform(0, 100)
        if number_of_red_noise < 50:
            number_of_red_noise = 0
        elif number_of_red_noise < 75:
            number_of_red_noise = 1
        elif number_of_red_noise < 90:
            number_of_red_noise = 2
        else:
            number_of_red_noise = int(random.uniform(0, self.number_of_signals))
        flux: ndarray = np.ones(len(self.time))
        for index in range(0, number_of_red_noise):
            red_noise_freq: float = self.random_number_generator.uniform(self.period[0], self.period[1])
            red_noise_power: float = self.random_number_generator.uniform(self.power[0], self.power[1])
            logging.info(f'Injecting red noise with power={red_noise_power} and freq={red_noise_freq}')
            red_noise = timesynth.noise.RedNoise(std=red_noise_power, tau=red_noise_freq)
            timeseries_rn: ndarray = np.zeros(len(self.original_flux))
            for time_index, value in enumerate(self.time):
                rn_value = red_noise.sample_next(value, None, None)
                rn_value = rn_value[0] if isinstance(rn_value, (list, np.ndarray)) else rn_value
                timeseries_rn[time_index] = rn_value
            flux = flux + timeseries_rn
        return self.original_flux + flux - 1, flux


class SinusoidalInjector(FeaturesInjector):
    def __init__(self, time: ndarray, original_flux: ndarray, amplitude: tuple[float, float], period: tuple[float, float], number_of_signals: int):
        super().__init__(time, original_flux)
        self.power = amplitude
        self.period = period
        self.number_of_signals = number_of_signals

    def inject(self) -> tuple[ndarray, ndarray]:
        number_of_signals = random.uniform(0, 100)
        if number_of_signals < 50:
            number_of_signals = 0
        elif number_of_signals < 75:
            number_of_signals = 1
        elif number_of_signals < 90:
            number_of_signals = 2
        else:
            number_of_signals = int(random.uniform(0, self.number_of_signals))
        flux: ndarray = np.ones(len(self.time))
        for index in range(0, number_of_signals):
            period: float = self.random_number_generator.uniform(self.period[0], self.period[1])
            amplitude: float = self.random_number_generator.uniform(self.power[0], self.power[1])
            logging.info(f'Injecting sinusoidal signal with power={amplitude} and freq={period}')
            flux = flux + amplitude * np.sin(2 * np.pi * self.time / period + random.uniform(0, 2 * np.pi))
        return self.original_flux + flux - 1, flux

class PseudoPeriodicInjector(FeaturesInjector):
    def __init__(self, time: ndarray, original_flux: ndarray, amplitude: tuple[float, float], period: tuple[float, float], amplitude_std: tuple[float, float], period_std: tuple[float, float],
                 number_of_signals: int):
        super().__init__(time, original_flux)
        self.power = amplitude
        self.period = period
        self.number_of_signals = number_of_signals
        self.power_std = amplitude_std
        self.period_std = period_std

    def inject(self) -> tuple[ndarray, ndarray]:
        number_of_signals = random.uniform(0, 100)
        if number_of_signals < 50:
            number_of_signals = 0
        elif number_of_signals < 75:
            number_of_signals = 1
        elif number_of_signals < 90:
            number_of_signals = 2
        else:
            number_of_signals = int(random.uniform(0, self.number_of_signals))
        flux: ndarray = np.ones(len(self.time))
        for index in range(0, number_of_signals):
            period: float = self.random_number_generator.uniform(self.period[0], self.period[1])
            amplitude: float = self.random_number_generator.uniform(self.power[0], self.power[1])
            period_std: float = self.random_number_generator.uniform(self.period_std[0], self.period_std[1])
            amplitude_std: float = self.random_number_generator.uniform(0, amplitude / 10)
            logging.info(f'Injecting pseudo-periodic signal with power={amplitude} and freq={period}')
            pseudo_periodic_signal = timesynth.signals.PseudoPeriodic(amplitude=amplitude, frequency=period, ampSD=amplitude_std, freqSD=0)
            timeseries_pp: ndarray = np.zeros(len(self.time))
            for time_index, value in enumerate(self.time):
                rn_value = pseudo_periodic_signal.sample_next(value, None, None)
                rn_value = rn_value[0] if isinstance(rn_value, (list, np.ndarray)) else rn_value
                timeseries_pp[time_index] = rn_value
            flux = flux + timeseries_pp
        return self.original_flux + flux - 1, flux


class TransitsInjector(FeaturesInjector):

    def __init__(self, time: ndarray, original_flux: ndarray, transit_period_avg_std: tuple[float, float], transit_depth_boundaries: tuple[float, float]):
        super().__init__(time, original_flux)
        self.transit_period_avg_std = transit_period_avg_std
        self.transit_depth_boundaries = transit_depth_boundaries

    def inject(self) -> tuple[ndarray, ndarray]:
        number_of_planets = random.uniform(0, 100)
        if number_of_planets < 50:
            number_of_planets = 1
        elif number_of_planets < 80:
            number_of_planets = 2
        else:
            number_of_planets = 3
        star_radius = 1
        star_mass = 1
        flux = np.ones(len(self.time))
        for index in range(0, number_of_planets):
            period = 0
            while period < 0.5:
                period = random.gauss(self.transit_period_avg_std[0], self.transit_period_avg_std[1])
            t0 = self.time[0] + period / random.uniform(0, 1)
            if t0 > self.time[-1]:
                t0 = np.random.uniform(self.time[0], self.time[-1])
            depth = random.uniform(self.transit_depth_boundaries[0], self.transit_depth_boundaries[1])
            planet_radius = np.sqrt(depth * (star_radius ** 2))
            logging.info(f'Injecting planet with P={period}, D={depth}')
            P1 = period * u.day
            a = np.cbrt((ac.G * star_mass * u.M_sun * P1 ** 2) / (4 * np.pi ** 2)).to(u.au)
            ld = [0.5, 0.5]
            planet_model = ellc.lc(
                t_obs=self.time,
                radius_1=(star_radius * u.R_sun).to(u.au) / a,  # star radius convert from AU to in units of a
                radius_2=(planet_radius * u.R_sun).to(u.au) / a,
                # convert from Rearth (equatorial) into AU and then into units of a
                sbratio=0,
                incl=90,
                light_3=0,
                t_zero=t0,
                period=period,
                a=None,
                q=planet_radius / star_radius * 0.1,
                f_c=None, f_s=None,
                ldc_1=ld, ldc_2=None,
                gdc_1=None, gdc_2=None,
                didt=None,
                domdt=None,
                rotfac_1=1, rotfac_2=1,
                hf_1=1.5, hf_2=1.5,
                bfac_1=None, bfac_2=None,
                heat_1=None, heat_2=None,
                lambda_1=None, lambda_2=None,
                vsini_1=None, vsini_2=None,
                t_exp=None, n_int=None,
                grid_1='default', grid_2='default',
                ld_1='quad', ld_2=None,
                shape_1='sphere', shape_2='sphere',
                spots_1=None, spots_2=None,
                exact_grav=False, verbose=1)
            flux = flux + planet_model - 1
        return self.original_flux + flux - 1, flux


class FlaresInjector(FeaturesInjector):
    ingress_param = 0.075
    egress_param = 0.15

    def __init__(self, time: ndarray, original_flux: ndarray, amplitude_avg_std: tuple[float, float], length_avg_std: tuple[float, float]):
        super().__init__(time, original_flux)
        self.amplitude_avg_std = amplitude_avg_std
        self.length_avg_std = length_avg_std

    def inject(self) -> tuple[ndarray, ndarray]:
        number_of_flares = random.uniform(0, 100)
        if number_of_flares < 50:
            number_of_flares = 1
        elif number_of_flares < 80:
            number_of_flares = 2
        else:
            number_of_flares = 3
        flux = np.ones(len(self.time))
        for index in range(0, number_of_flares):
            t0 = random.choice(self.time)
            amplitude = random.gauss(self.amplitude_avg_std[0], self.amplitude_avg_std[1])
            length = random.gauss(self.length_avg_std[0], self.length_avg_std[1])
            indexes = np.argwhere((self.time > t0 - length // 2) & (self.time < t0 + length // 2))
            for i in indexes:
                time_value = self.time[i]
                if flux[i] < 1 and time_value <= t0:
                    flux[i] = flux[i] + amplitude * np.exp(-((t0 - time_value) ** 2 / (2 * (self.ingress_param ** 2))))
                elif time_value > t0 and flux[i] < 1:
                    flux[i] = flux[i] + amplitude * np.exp((t0 - time_value) / self.egress_param)
        return self.original_flux + flux - 1, flux


class SantoTestDataGenerator:
    random_number_generator = default_rng()

    def __init__(self, output_dir: str, curves_len_boundaries: Tuple[int, int],
                 transit_depth_boundaries: Tuple[float, float],
                 transit_period_avg_std: Tuple[float, float],
                 white_noise_power_boundaries: Tuple[float, float],
                 red_noise_frequency_boundaries: Tuple[float, float],
                 red_noise_power_boundaries: Tuple[float, float],
                 sinusoid_frequency_boundaries: Tuple[float, float],
                 sinusoid_power_boundaries: Tuple[float, float],
                 pseudo_periodic_frequency_boundaries: Tuple[float, float],
                 pseudo_periodic_power_boundaries: Tuple[float, float],
                 pseudo_periodic_frequency_std_boundaries: Tuple[float, float],
                 pseudo_periodic_power_std_boundaries: Tuple[float, float],
                 flare_amplitude_avg_std: Tuple[float, float],
                 flare_length_avg_std: Tuple[float, float],
                 max_number_of_pseudo_periodic: int = 3,
                 max_number_of_sinusoid: int = 3,
                 max_number_of_red_noise: int = 5,
                 curves_count=10000, curves_cadence=120, only_plot=False):
        for curve_index in range(0, curves_count):
            curve_len: int = int(random.uniform(curves_len_boundaries[0], curves_len_boundaries[1]))
            flux: ndarray = np.ones((2, curve_len))
            curve_len_days: float = curve_len * curves_cadence / 3600 / 24
            time: ndarray = np.linspace(0, curve_len_days, curve_len)
            white_noise_std: float = random.uniform(white_noise_power_boundaries[0], white_noise_power_boundaries[1])
            flux[0] = flux[0] + np.random.normal(loc=0, scale=white_noise_std, size=curve_len)
            flux[0], flux[1] = RedNoiseInjector(time, flux[0], red_noise_power_boundaries, red_noise_frequency_boundaries, max_number_of_red_noise).inject()
            #flux[0] = SinusoidalInjector(time, flux[0], sinusoid_power_boundaries, sinusoid_frequency_boundaries, max_number_of_sinusoid).inject()
            flux[0], flux[1] = PseudoPeriodicInjector(time, flux[0], pseudo_periodic_power_boundaries, pseudo_periodic_frequency_boundaries,
                                             pseudo_periodic_power_std_boundaries, pseudo_periodic_frequency_std_boundaries, max_number_of_pseudo_periodic).inject()
            flux[0], flux[1] = FlaresInjector(time, flux[0], flare_amplitude_avg_std, flare_length_avg_std).inject()
            flux[0], flux[1] = TransitsInjector(time, flux[0], transit_period_avg_std, transit_depth_boundaries).inject()
            #plt.scatter(time, flux[0])
            #plt.show()
            np.savetxt(f'{output_dir}/{curve_index}_model.csv', flux, delimiter=',')

