import unittest

from exafs_neo.exafs_pop import NeoPopulations
from exafs_neo.neoPars import NeoPars


class MyTestCase(unittest.TestCase):

    def test_neoPars(self):
        inputs_pars = {'data_file': 'tests/cu_test_files/cu_paths/cu_10k.xmu',
                       'output_file': '',
                       'feff_file': 'tests/cu_test_files/cu_paths/path_75/feff',
                       'kmin': 0.95,
                       'kmax': 9.775,
                       'kweight': 3.0, 'pathrange': [1, 2, 3, 4, 5],
                       'deltak': 0.05, 'rbkg': 1.1, 'bkgkw': 1.0, 'bkgkmax': 15.0}
        exafs_NeoPars = NeoPars()
        exafs_NeoPars.read_inputs(inputs_pars)
        neo_population = NeoPopulations(exafs_NeoPars)
        neo_population.initialize_populations()
        self.assertIsInstance(neo_population[0], tuple)
        # self.assertIsInstance(neo_population[0][0], exafs_test.individual.Individual)


if __name__ == '__main__':
    unittest.main()
