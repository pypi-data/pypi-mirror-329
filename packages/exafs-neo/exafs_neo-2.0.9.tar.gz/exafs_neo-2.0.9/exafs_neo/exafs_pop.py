import copy
import operator

import numpy as np
from attrs import define, field
from larch.xafs import feffdat

from exafs_neo.individual import Individual
from exafs_neo.neoPars import NeoPars


def fitness(exafs_neo_pars, ind_obj, return_tot=False):
    """
    Evaluate fitness of a individual
    """
    loss = 0
    y_total = np.zeros(401)
    intervalK = exafs_neo_pars.exafsPars.intervalK
    larch = exafs_neo_pars.exafsPathPars.mylarch
    kweight = exafs_neo_pars.exafsPars.kweight
    for i in range(exafs_neo_pars.exafsPars.npath):
        pathname = exafs_neo_pars.exafsPathPars.pathname[i]
        pathdictionary = exafs_neo_pars.exafsPathPars.pathDictionary
        path = pathdictionary.get(pathname)
        path.e0 = ind_obj.get_e0()
        path.s02 = ind_obj.get_path(i)[0]
        path.sigma2 = ind_obj.get_path(i)[2]
        path.deltar = ind_obj.get_path(i)[3]
        feffdat.path2chi(path, _larch=larch)
        y = path.chi
        for k in intervalK:
            y_total[int(k)] += y[int(k)]
    # compute loss function
    for j in intervalK:
        loss = loss + (y_total[int(j)] * exafs_neo_pars.exafsPathPars.g.k[int(j)] ** kweight -
                       exafs_neo_pars.exafsPathPars.exp[int(j)] * exafs_neo_pars.exafsPathPars.g.k[
                           int(j)] ** kweight) ** 2
    if return_tot:
        return loss, y_total
    else:
        return loss


@define
class NeoPopulations:
    exafs_NeoPars: NeoPars = None
    population: list = field(factory=list)
    population_sorted: list = field(factory=list)
    population_score: list = field(factory=list)
    population_perf: dict = field(factory=dict)
    next_population: list = field(factory=list)

    def generate_individual(self):
        if not self.exafs_NeoPars.runPars.secondHalf:
            e0 = np.random.choice(self.exafs_NeoPars.exafsRangePars.rangeE0)
        else:
            e0 = self.exafs_NeoPars.bestFitPars.bestE0
        ind = Individual(self.exafs_NeoPars.exafsPars.npath,
                         self.exafs_NeoPars.exafsPathPars.pathDictionary,
                         self.exafs_NeoPars.exafsRangePars.pathrange_pars,
                         self.exafs_NeoPars.exafsPathPars.path_lists,
                         e0,
                         self.exafs_NeoPars.exafsPathPars.pathname)
        return ind

    def eval_population(self, replace=True, sorting=True):
        score = []
        population_perf = {}

        for i, individual in enumerate(self.population):
            temp_score = fitness(self.exafs_NeoPars, individual)
            score.append(temp_score)

            population_perf[individual] = temp_score
        if sorting:
            self.population_sorted = sorted(
                population_perf.items(), key=operator.itemgetter(1), reverse=False)
        if replace:
            # self.currBestFit = list(self.population_sorted[0])
            self.__replace_bestfit()
        return score

    def initialize_populations(self):
        """
        Initialize populations
        :return:
        """
        for i in range(self.exafs_NeoPars.fixedPars.nPops):
            self.population.append(self.generate_individual())

        self.eval_population()

    def __getitem__(self, item):
        return self.population_sorted[item]

    def __replace_bestfit(self):
        self.exafs_NeoPars.bestFitPars.currBestInd = self.population_sorted[0][0]
        self.exafs_NeoPars.bestFitPars.currBestVal = self.population_sorted[0][1]

        delta = np.abs(self.exafs_NeoPars.bestFitPars.currBestVal - self.exafs_NeoPars.bestFitPars.globBestVal)
        if delta > 0.01:
            self.exafs_NeoPars.bestFitPars.bestDiff = delta
        else:
            self.exafs_NeoPars.bestFitPars.bestDiff = 0

        if self.exafs_NeoPars.bestFitPars.currBestVal < self.exafs_NeoPars.bestFitPars.globBestVal:
            self.exafs_NeoPars.bestFitPars.globBestInd = self.exafs_NeoPars.bestFitPars.currBestInd
            self.exafs_NeoPars.bestFitPars.globBestVal = self.exafs_NeoPars.bestFitPars.currBestVal

    def optimize_e0(self):
        # TODO: Revist this
        #  if mess == None:
        #      self.logger.info(
        #          "Finished First Half of Generation, Optimizing E0...")
        #  else:
        #      self.logger.info(mess)

        curr_ind = copy.deepcopy(self.exafs_NeoPars.bestFitPars.globBestInd)
        curr_score = copy.deepcopy(self.exafs_NeoPars.bestFitPars.globBestVal)
        curr_e0 = curr_ind.get_e0()
        for i in self.exafs_NeoPars.exafsRangePars.rangeE0_large:
            curr_ind.set_e0(i)
            fit_score = fitness(self.exafs_NeoPars, curr_ind)
            if fit_score < curr_score:
                curr_e0 = i
                curr_score = fit_score
            # listOfX.append(i)
            # listOfY.append(fit)
        # self.logger.info("Continue With E0= " + str(round(curr_e0, 3)))
        new_e0 = curr_e0
        self.exafs_NeoPars.bestFitPars.bestE0 = new_e0
        # TODO: revisit this!
        #  Reset Mutation Chance??
        #  self.mut_chance_e0 = 0
        self.exafs_NeoPars.bestFitPars.globBestInd.set_e0(new_e0)
        self.exafs_NeoPars.bestFitPars.globBestVal = curr_score

        for i in self.population:
            i.set_e0(new_e0)


if __name__ == "__main__":
    inputs_pars = {'data_file': '../path_files/Cu/cu_10k.xmu', 'output_file': '',
                   'feff_file': '../path_files/Cu/path_75/feff', 'kmin': 0.95,
                   'kmax': 9.775,
                   'kweight': 3.0, 'pathrange': [1, 2, 3, 4, 5],
                   'deltak': 0.05, 'rbkg': 1.1, 'bkgkw': 1.0, 'bkgkmax': 15.0}
    exafs_NeoPars = NeoPars()
    exafs_NeoPars.read_inputs(inputs_pars)
    neo_population = NeoPopulations(exafs_NeoPars)

    neo_population.initialize_populations()
