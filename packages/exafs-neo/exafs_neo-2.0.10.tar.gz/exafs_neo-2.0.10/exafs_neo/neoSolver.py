import numpy as np

from exafs_neo.exafs_pop import NeoPopulations
from exafs_neo.neoPars import NeoPars





class NeoSolverBase:
    def __init__(self, exafs_pars, logger):
        """
        Initialize the selector base class
        :param exafs_pars:
        :param logger:
        """
        self.logger = logger
        self.exafs_pars = exafs_pars

        self.sol_list = []

    def solve(self, pops, selector, crossover, mutator, exafs_pars):
        pass

    def __str__(self):
        # return f"Top Percentage: {100 * self.nBest_Percent}%, Lucky: {100 * self.nLucky_Percent}%"
        return f"Neo Solver"


class NeoSolver_GA(NeoSolverBase):
    """
    Standard GA algorithm solver
    """

    def __init__(self, exafs_pars, logger):
        super().__init__(exafs_pars, logger)
        self.solver_type = 0
        self.solver_operator = "Genetic Algorithm"

    def solve(self, pops, selector, crossover, mutator,exafs_pars):
        selector.select(pops)
        crossover.crossover(pops)
        mutator.mutate(pops)
        pops.eval_population()


class NeoSolver_GA_Rechenberg(NeoSolverBase):
    """
    Standard GA with Rechenberg addition
    """

    def __init__(self, exafs_pars, logger):
        super().__init__(exafs_pars, logger)
        self.solver_type = 1
        self.solver_operator = "Genetic Algorithm with Rechenberg"

    def solve(self, pops, selector, crossover, mutator, exafs_pars):
        selector.select(pops)
        crossover.crossover(pops)
        self.rechenberg_mutation(exafs_pars)
        mutator.mutate(pops)
        pops.eval_population()

    def rechenberg_mutation(self, exafs_pars):
        # Recehenberg mutation
        diffCounter = exafs_pars.runPars.diffCounter
        if exafs_pars.runPars.currGen > 20:
            if diffCounter < 0.1:
                diffCounter += 1
            else:
                diffCounter -= 1

            if (abs(diffCounter) / float(exafs_pars.runPars.currGen)) > 0.2:
                exafs_pars.mutPars.mutChance += 0.025
                exafs_pars.mutPars.mutChance = abs(exafs_pars.mutPars.mutChance)
            elif (abs(diffCounter) / float(exafs_pars.runPars.currGen)) < 0.2:
                if (exafs_pars.mutPars.mutChance - 0.025) > 0:
                    exafs_pars.mutPars.mutChance -= 0.025
                    exafs_pars.mutPars.mutChance = abs(exafs_pars.mutPars.mutChance)

            # Clip between 0 and 100%
            exafs_pars.mutPars.mutChance = np.clip(exafs_pars.mutPars.mutChance, 0, 100)


class NeoSolver_DE(NeoSolverBase):
    """
    Standard Differential Evolution
    """

    def __init__(self, exafs_pars, logger):
        super().__init__(exafs_pars, logger)
        self.solver_type = 2
        self.solver_operator = "Differential Evolution"

    def solve(self, pops, selector, crossover, mutator, exafs_pars):
        pass


class NeoSolver:

    def __init__(self, logger=None):
        """
        Neo Selector
        :param NeoLogger logger: logger for Neo
        """
        self.solver_operator = None
        self.logger = logger
        self.solver_type = None
        self.exafs_pars = None

    def initialize(self, exafs_pars):
        """
        Initialize the Selector
        :param exafs_pars:
        :return:
        """
        self.exafs_pars = exafs_pars
        # self.solver_type = exafs_pars.selPars.selOpt
        self.solver_type = exafs_pars.solPars.solOpt
        if self.solver_type == 0:
            self.solver_operator = NeoSolver_GA(exafs_pars, logger=self.logger)
        elif self.solver_type == 1:
            self.solver_operator = NeoSolver_GA_Rechenberg(exafs_pars, logger=self.logger)
        elif self.solver_type == 2:
            self.solver_operator = NeoSolver_DE(exafs_pars, logger=self.logger)
        else:
            self.solver_operator = NeoSolverBase(exafs_pars, logger=self.logger)
            raise ValueError("Invalid selector type, returning standard selector type.")

    def solve(self, pops, selector, crossover, mutator, exafs_pars):
        """
        Perform the actual selection
        :param exafs_pars:
        :param selector:
        :param mutator:
        :param crossover:
        :param NeoPopulation pops:
        :return:
        """
        if self.solver_operator is None:
            raise ValueError("Solver is not initialized")
        else:
            return self.solver_operator.solve(pops, selector, crossover, mutator, exafs_pars)

    def __str__(self):
        if self.solver_operator is None:
            return "None Mutator selected"
        else:
            return f"Selector Type: {self.solver_type}, {self.solver_operator}"


if __name__ == "__main__":
    inputs_pars = {'data_file': '../path_files/Cu/cu_10k.xmu', 'output_file': '',
                   'feff_file': '../path_files/Cu/path_75/feff', 'kmin': 0.95,
                   'kmax': 9.775,
                   'kweight': 3.0, 'pathrange': [1, 2, 3, 4, 5],
                   'deltak': 0.05, 'rbkg': 1.1, 'bkgkw': 1.0, 'bkgkmax': 15.0,
                   'solver_type': 1}
    exafs_NeoPars = NeoPars()
    exafs_NeoPars.read_inputs(inputs_pars)

    neo_population = NeoPopulations(exafs_NeoPars)
    neo_population.initialize_populations()

    exafs_solver = NeoSolver()
    exafs_solver.initialize(exafs_pars=exafs_NeoPars)
    # exafs_selector.solve(neo_population)
    print(exafs_solver)
