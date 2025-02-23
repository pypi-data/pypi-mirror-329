import datetime
import logging
import pathlib
import sys

import numpy as np
from exafs_neo.helper import time_call
from exafs_neo.utils_mapping import neocrossover_int2str, neomutator_int2str, neoselector_int2str

def raise_error(msg='Error'):
    raise Exception(msg)



def checkKey(key, dictionary, alt_value=None, logger=None, verbose=False):
    # TODO: Raise checker for alternative response
    if key not in dictionary:
        if verbose:
            warn_str = f'{key} not found! Using default value of {key}: {alt_value}'
            if logger is None:
                print(warn_str)
            else:
                logger.warn(warn_str)
        return alt_value
    else:
        return dictionary[key]


class NeoLogger:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger('')
        # file_handler = logging.FileHandler()
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.log_path = None
        self.logging_level = logging.DEBUG

    def initialize_logging(self, log_path=None, log_format='%(message)s'):
        self.log_path = log_path
        formatter = logging.Formatter(log_format)

        if log_path is not None:
            file_handler = logging.FileHandler(
                self.log_path, mode='a+', encoding='utf-8')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(self.logging_level)
            self.logger.addHandler(file_handler)

        stdout_handler = logging.StreamHandler(stream=sys.stdout)
        stdout_handler.setLevel(self.logging_level)
        stdout_handler.setFormatter(formatter)
        self.logger.addHandler(stdout_handler)
        self.logger.setLevel(self.logging_level)

    def set_loglevel(self, loglevel):
        # TODO: change each of the handler to the level
        self.logging_level = loglevel
        self.logger.setLevel(loglevel)

    def print(self, message: str):
        self.logger.debug(message)

    def __call__(self, message):
        self.logger.debug(message)


def check_if_exists(path_file):
    """
    Check if the directory exists
    """
    pathFile = pathlib.Path(path_file)
    if pathFile.is_file():
        pathFile.unlink()
    # Make Directory when its missing
    pathFile.parent.mkdir(parents=True, exist_ok=True)


class STRColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def logger_print_based_on_verbose_lvl(logger,
                                          string: str,
                                          current_verbose_lvl: int,
                                          designated_verbose_lvl: int) -> None:
        if current_verbose_lvl >= designated_verbose_lvl:
            logger.print(string)

    # TODO: Implement verbose_lvl argument that detects if jupyter is running...
    @staticmethod
    def run_verbose_start(logger, exafs_NeoPars, verbose_lvl=5):
        """
        Visualize the verbose start place
        """
        # logger.print(banner())
        if exafs_NeoPars.fixedPars.debug_mode:
            STRColors.logger_print_based_on_verbose_lvl(logger, f"{STRColors.BOLD}DEBUG-MODE{STRColors.ENDC}",
                                                        verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger, "------------Inputs File Stats--------------",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Data File{STRColors.ENDC}: {exafs_NeoPars.neoFilePars.data_path}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Feff File{STRColors.ENDC}: {exafs_NeoPars.neoFilePars.front}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Output File{STRColors.ENDC}: {exafs_NeoPars.neoFilePars.output_path}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Log File{STRColors.ENDC}: {exafs_NeoPars.neoFilePars.log_path}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Paths Range File{STRColors.ENDC}: {exafs_NeoPars.neoFilePars.feff_file}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}CSV series{STRColors.ENDC}: {exafs_NeoPars.neoFilePars.multi_data_toggle}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger, "--------------Populations------------------",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Population{STRColors.ENDC}: {exafs_NeoPars.fixedPars.nPops}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Num Gen{STRColors.ENDC}: {exafs_NeoPars.fixedPars.nGen}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Best Individuals{STRColors.ENDC}: {exafs_NeoPars.selPars.nBestSample}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Lucky Survivor{STRColors.ENDC}: {exafs_NeoPars.selPars.nLuckSample}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger, "-----------------Paths---------------------",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Individual Path{STRColors.ENDC}: {exafs_NeoPars.exafsPathPars.individual_paths}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Num Path{STRColors.ENDC}: {exafs_NeoPars.exafsPathPars.npaths}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Paths {STRColors.ENDC}: {exafs_NeoPars.exafsPathPars.path_lists}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Path Optimize{STRColors.ENDC}: {exafs_NeoPars.fixedPars.pathOptimize}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Path Optimize Percent{STRColors.ENDC}: {exafs_NeoPars.fixedPars.pathOptimizePercent}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Path Optimize Only{STRColors.ENDC}: {exafs_NeoPars.fixedPars.pathOptimizeOnly}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger, "-----------------Solvers-------------------",
                                                    verbose_lvl, 5)
        # STRColors.logger_print_based_on_verbose_lvl(logger,
        #                                             f"{STRColors.BOLD}Solver Options{STRColors.ENDC}: {exafs_NeoPars.mutPars.}",
        #                                             verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger, "----------------Mutations------------------",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Mutations{STRColors.ENDC}: {exafs_NeoPars.mutPars.mutChance}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}E0 Mutations{STRColors.ENDC}: {exafs_NeoPars.mutPars.mutChanceE0}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Mutation Options{STRColors.ENDC}: {neomutator_int2str(exafs_NeoPars.mutPars.mutOpt)}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Selection Options{STRColors.ENDC}: {neoselector_int2str(exafs_NeoPars.selPars.selOpt)}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Crossover Options{STRColors.ENDC}: {neocrossover_int2str(exafs_NeoPars.crossPars.croOpt)}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger, "---------------Larch Paths-----------------", verbose_lvl,
                                                    5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Kmin{STRColors.ENDC}: {exafs_NeoPars.exafsPars.kmin}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Kmax{STRColors.ENDC}: {exafs_NeoPars.exafsPars.kmax}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Kweight{STRColors.ENDC}: {exafs_NeoPars.exafsPars.kweight}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Delta k{STRColors.ENDC}: {exafs_NeoPars.exafsPars.dk}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}RBKG{STRColors.ENDC}: {exafs_NeoPars.exafsPars.rbkg}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}BKG Kw{STRColors.ENDC}: {exafs_NeoPars.exafsPars.bkgkw}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}BKG Kmax{STRColors.ENDC}: {exafs_NeoPars.exafsPars.bkgkmax}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger, "-------------------------------------------", verbose_lvl,
                                                    5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Steady State{STRColors.ENDC}: {exafs_NeoPars.fixedPars.steadyState}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Print Graph{STRColors.ENDC}: {exafs_NeoPars.fixedPars.printGraph}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger, "-------------------------------------------", verbose_lvl,
                                                    5)

    @staticmethod
    def run_verbose_gen(logger, exafs_NeoPars, neo_population, verbose_lvl=5):
        """
        Verbose generation
        """
        st = time_call()
        population_sorted = neo_population.population_sorted
        STRColors.logger_print_based_on_verbose_lvl(logger, "---------------------------------------------------------",
                                                    verbose_lvl, 1)
        STRColors.logger_print_based_on_verbose_lvl(logger, datetime.datetime.fromtimestamp(st).strftime(
            '%H:%M:%S') + f"{STRColors.BOLD} Gen: {STRColors.ENDC}{exafs_NeoPars.runPars.currGen}", verbose_lvl, 1)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"Best Fit: {STRColors.BOLD}{population_sorted[0][1].round(3)}{STRColors.ENDC}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"Best Fit: {STRColors.BOLD}{population_sorted[0][1].round(3)}{STRColors.ENDC}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"2nd Fit: {STRColors.BOLD}{population_sorted[1][1].round(3)}{STRColors.ENDC}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"3rd Fit: {STRColors.BOLD}{population_sorted[2][1].round(3)}{STRColors.ENDC}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"4th Fit: {STRColors.BOLD}{population_sorted[0][1].round(3)}{STRColors.ENDC}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"Last Fit: {STRColors.BOLD}{population_sorted[-1][1].round(3)}{STRColors.ENDC}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"Different from last best fit: {exafs_NeoPars.bestFitPars.bestDiff:.4f}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger, STRColors.BOLD + "Best fit: " + STRColors.OKBLUE + str(
            np.round(exafs_NeoPars.bestFitPars.currBestVal, 3)) + STRColors.ENDC, verbose_lvl, 5)
        CurrchiR = np.round(exafs_NeoPars.bestFitPars.currBestVal / (
                    len(exafs_NeoPars.exafsPars.intervalK) - 3 * exafs_NeoPars.exafsPars.npath + 1), 3)
        STRColors.logger_print_based_on_verbose_lvl(logger, STRColors.BOLD + "Best fit ChiR: " + STRColors.OKBLUE + str(
            CurrchiR) + STRColors.ENDC, verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger, STRColors.BOLD + "History Best: " + STRColors.OKBLUE + str(
            np.round(exafs_NeoPars.bestFitPars.globBestVal, 4)) + STRColors.ENDC, verbose_lvl, 1)
        GlobchiR = exafs_NeoPars.bestFitPars.globBestVal / (
                    len(exafs_NeoPars.exafsPars.intervalK) - 3 * exafs_NeoPars.exafsPars.npath + 1)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    STRColors.BOLD + "History Best ChiR: " + STRColors.OKBLUE + str(
                                                        np.round(GlobchiR, 4)) + STRColors.ENDC, verbose_lvl, 1)
        STRColors.logger_print_based_on_verbose_lvl(logger, "DiffCounter: " + str(exafs_NeoPars.runPars.diffCounter),
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"Diff %: {(exafs_NeoPars.runPars.diffCounter / exafs_NeoPars.runPars.currGen):.3f}",
                                                    verbose_lvl, 5)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"Mutation Chance: {100 * exafs_NeoPars.mutPars.mutChance:.2f}%",
                                                    verbose_lvl, 5)
        # if exafs_NeoPars.mutPars.mutOpt == 4:
        #     STRColors.logger_print_based_on_verbose_lvl(logger, "Mutation Percentage" + str(np.round(exafs_NeoPars.self.nmutate_success / self.nmutate, 4)),verbose_lvl,5)

        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    "Time: " + str(round(exafs_NeoPars.runPars.currGen_tt, 5)) + "s",
                                                    verbose_lvl, 5)

    @staticmethod
    def run_verbose_end(logger, exafs_NeoPars, verbose_lvl=5):
        """
        Verbose end
        """

        STRColors.logger_print_based_on_verbose_lvl(logger, "-----------Output Stats---------------", verbose_lvl, 1)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Total Time(s){STRColors.ENDC}: {round(exafs_NeoPars.runPars.tt, 4)}",
                                                    verbose_lvl, 1)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}File{STRColors.ENDC}: {exafs_NeoPars.neoFilePars.data_path}",
                                                    verbose_lvl, 1)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Path{STRColors.ENDC}: {exafs_NeoPars.exafsPathPars.path_lists}",
                                                    verbose_lvl, 1)
        STRColors.logger_print_based_on_verbose_lvl(logger,
                                                    f"{STRColors.BOLD}Final Fittness Score{STRColors.ENDC}: {exafs_NeoPars.bestFitPars.globBestVal:.2f}",
                                                    verbose_lvl, 1)
        STRColors.logger_print_based_on_verbose_lvl(logger, "-------------------------------------------", verbose_lvl,
                                                    1)
        if exafs_NeoPars.fixedPars.printGraph:
            # TODO: Reimplement this
            pass
            # self.verbose_graph()


if __name__ == "__main__":
    # Testing Logger
    # logger = NeoLogger()
    # logger.initialize_logging('Test.csv')
    # logger.set_loglevel(logging.DEBUG)

    # Test Str Print
    pass
