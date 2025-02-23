import os

from exafs_neo.neoMutator import NeoMutator
from exafs_neo.exafs_pop import NeoPopulations
from exafs_neo.neoPars import NeoPars
from exafs_neo.helper import banner
from exafs_neo.utils import NeoLogger, STRColors
from exafs_neo.neoCrossOver import NeoCrossover
from exafs_neo.neoSelector import NeoSelector
from exafs_neo.neoResult import NeoResult
from exafs_neo.ini_parser import validate_input_file
from exafs_neo.parser import InputParamsParser
from exafs_neo.neoSolver import NeoSolver


class ExafsNeo:

    def __init__(self, verbose_lvl=5):
        """
        Initialize Params:

        """

        print(banner())
        self.logger = NeoLogger()
        self.exafs_neo_pars = NeoPars()
        self.mutator = NeoMutator(logger=self.logger)
        self.selector = NeoSelector(logger=self.logger)
        self.crossOver = NeoCrossover(logger=self.logger)
        self.solver = NeoSolver(logger=self.logger)
        self.neo_population = None
        self.verbose_lvl = verbose_lvl
        self.result = NeoResult(logger=self.logger)
        self.input_parameters = None

    def exafs_read(self, filepath=None, input_parameters=None):
        """
        Read the input file into exafs parameters
        @param str filepath: file path to the ini file
        @param dict input_parameters: Dictionary of input parameters
        """
        if filepath is not None:
            file_path = os.path.join(os.getcwd(), filepath)
            input_params = InputParamsParser()
            input_params.read_input_file(file_path, verbose=False)
            input_params.input_dict = validate_input_file(input_params.input_dict)

            self.input_parameters = input_params.export_input_dict()

        if input_parameters is not None:
            self.input_parameters = input_parameters

        if self.input_parameters is None:
            raise ValueError("No input parameters are given")

    def exafs_setup(self):
        """
        Setup EXAFS run subroutine
        :return:
        """
        # TODO:
        #  1. At mid point, do a E0 optimization
        self.exafs_neo_pars.read_inputs(self.input_parameters)
        self.logger.initialize_logging(self.exafs_neo_pars.neoFilePars.log_path)
        self.neo_population = NeoPopulations(self.exafs_neo_pars)
        self.neo_population.initialize_populations()
        self.result.initialize(self.exafs_neo_pars)
        # Initialize all the operators
        self.selector.initialize(self.exafs_neo_pars)
        self.crossOver.initialize(self.exafs_neo_pars)
        self.mutator.initialize(self.exafs_neo_pars)
        self.solver.initialize(self.exafs_neo_pars)

    def run(self):
        """
        Initialize a EXAFS Run
        :return: result class 
        """
        STRColors.run_verbose_start(self.logger, self.exafs_neo_pars, verbose_lvl=self.verbose_lvl)

        for currGen in range(self.exafs_neo_pars.fixedPars.nGen):
            self.exafs_neo_pars.runPars.start_gen()

            self.solver.solve(self.neo_population, self.selector, self.crossOver, self.mutator, self.exafs_neo_pars)

            # End of generation verbose
            STRColors.run_verbose_gen(self.logger, self.exafs_neo_pars, self.neo_population,
                                      verbose_lvl=self.verbose_lvl)
            self.result.collect(self.neo_population, self.exafs_neo_pars)

            # self.exafs_neo_pars.runPars.end_gen(self.neo_population)
            self.exafs_neo_pars.end_gen(self.neo_population)
        # End of run verbose
        STRColors.run_verbose_end(self.logger, self.exafs_neo_pars, verbose_lvl=self.verbose_lvl)
        return self.result


if __name__ == "__main__":
    initializer_override = {
        'printGraph': False
    }

    exafs_temp = ExafsNeo(verbose_lvl=5)

    input_dict = {
        'data_file': '../path_files/Cu/cu_10k.xmu',
        'output_file': 'test.csv',
        'feff_file': '../path_files/Cu/path_75/feff',
        'nGen': 20,
        'kmin': 0.95,
        'kmax': 9.775,
        'kweight': 3.0,
        'deltak': 0.05,
        'rbkg': 1.1,
        'bkgkw': 1.0,
        'bkgkmax': 15.0,
        'printGraph': False,
        'pathrange': [1, 2, 3, 4, 5],
        'solver_type': 1,
    }
    exafs_temp.exafs_read(input_parameters=input_dict)
    exafs_temp.exafs_setup()

    result = exafs_temp.run()
    print(result)
