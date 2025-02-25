from . import _cupy_numpy as xp
from io import open
import configparser
from pkg_resources import resource_filename

from ._interpolator_3D import regular_grid_interp

class AbundanceGetter:
    def __init__(self, include_condensation=True):
        config = configparser.ConfigParser()
        config.read(resource_filename(__name__, "data/abundances/properties.cfg"))
        properties = config["DEFAULT"]
        self.min_temperature = float(properties["min_temperature"])
        self.logZs = xp.linspace(float(properties["min_logZ"]),
                                 float(properties["max_logZ"]),
                                 int(properties["num_logZ"]))
        self.CO_ratios = xp.array(eval(properties["CO_ratios"]))
        self.included_species = eval(properties["included_species"])

        if include_condensation:
            filename = "with_condensation.npy"
        else:
            filename = "gas_only.npy"

        abundances_path = "data/abundances/{}".format(filename)

        self.log_abundances = xp.log10(xp.load(
            resource_filename(__name__, abundances_path)))
                 
        
    def get(self, logZ, CO_ratio=0.53):
        '''Get an abundance grid at the specified logZ and C/O ratio.  This
        abundance grid can be passed to TransitDepthCalculator, with or without
        modifications.  The end user should not need to call this except in
        rare cases.

        Returns
        -------
        abundances : dict of xp.ndarray
            A dictionary mapping species name to a 2D abundance array, specifying
            the number fraction of the species at a certain temperature and
            pressure.'''
        interp_log_abund = 10**regular_grid_interp(self.logZs, self.CO_ratios, self.log_abundances, xp.float32(logZ), xp.float32(CO_ratio))

        abund_dict = {}
        for i, s in enumerate(self.included_species):
            abund_dict[s] = interp_log_abund[i]

        return abund_dict

    def is_in_bounds(self, logZ, CO_ratio, T):
        '''Check to see if a certain metallicity, C/O ratio, and temperature
        combination is within the supported bounds'''
        if T <= self.min_temperature:
            return False
        if logZ <= self.logZs.min() or logZ >= self.logZs.max():
            return False
        if CO_ratio <= self.CO_ratios.min() or \
           CO_ratio >= self.CO_ratios.max():
            return False
        return True

    @staticmethod
    def from_file(filename):
        '''Reads abundances file in the ExoTransmit format (called "EOS" files
        in ExoTransmit), returning a dictionary mapping species name to an
        abundance array of dimension'''
        line_counter = 0

        species = None
        temperatures = []
        pressures = []
        compositions = []
        abundance_data = dict()

        with open(filename) as f:
            for line in f:
                elements = line.split()
                if line_counter == 0:
                    assert(elements[0] == 'T')
                    assert(elements[1] == 'P')
                    species = elements[2:]
                elif len(elements) > 1:
                    elements = xp.array([float(e) for e in elements])
                    temperatures.append(elements[0])
                    pressures.append(elements[1])
                    compositions.append(elements[2:])

                line_counter += 1

        temperatures = xp.array(temperatures)
        pressures = xp.array(pressures)
        compositions = xp.array(compositions)

        N_temperatures = len(xp.unique(temperatures))
        N_pressures = len(xp.unique(pressures))

        for i in range(len(species)):
            c = compositions[:, i].reshape((N_pressures, N_temperatures)).T
            # This file has decreasing temperatures and pressures; we want
            # increasing temperatures and pressures
            c = c[::-1, ::-1]
            abundance_data[species[i]] = c
        return abundance_data
