from larch.xafs import feffdat

from exafs_neo.pathObj import PathObject

"""
Construct individuals for the GA
"""


class Individual:
    def __init__(self, npaths, pathDictionary, pathrange_Dict, pathlists, e0, pathName):
        """
        Definition:
            npaths = number of paths
            pathDictionary = <dict> path name, and their corresponding paths.dat
            pathrange_Dict = <list> pathrange_limits
            path_lists = the paths lists (can be 2D depends on number of feff)
            e0 = quantum e0 of the individuals
            pathname = the paths identifier
        """
        self.npaths = npaths
        self.path_lists = pathlists
        self.pathname = pathName
        self.Population = []
        self.pathrange_Dict = pathrange_Dict
        self.pathDictionary = pathDictionary

        for pathrange in self.pathrange_Dict:
            self.Population.append(PathObject(pathrange, e0))

    def get(self):
        """Get all vars

        Returns:
            list of (npaths,4) 2D list
        """
        population = []
        for i in range(self.npaths):
            population.append(self.Population[i].get())
        return population

    def get_var(self):
        """Get all parameters except e0

        Returns:
            list of (npaths,3) 2D list
        """
        population = []
        for i in range(self.npaths):
            population.append(self.Population[i].get_var())
        return population

    def get_e0(self):
        """Get e0 of the individual
        Returns:
            int: e0 value
        """
        return self.Population[0].get_e0()

    def get_path(self, i):
        return self.Population[i].get()

    def verbose(self):
        """
        Print out the populations
        """
        for i in range(self.npaths):
            self.Population[i].verbose()

    def set_path(self, i, s02, sigma2, deltaR):
        """
        Set the specfic i-th paths
        @param int i: index of the paths
        @param float s02: s02 value
        @param float sigma2: sigma2 value
        @param float deltaR: deltaR value
        @return:
        """
        self.Population[i].set(s02, sigma2, deltaR)

    def set_allpath(self, pars_Arr):
        """Set the paths of all array given a input array
        @param np.array pars_Arr: numpy array containing all the paths parameters in (n_path,3)
        """
        assert pars_Arr.shape[0] == self.npaths
        assert pars_Arr.shape[1] == 3

        for i in range(self.npaths):
            self.Population[i].set(i, pars_Arr[i][0], pars_Arr[i][1], pars_Arr[i][2])

    def set_e0(self, e0):
        """
        Set e0 to a value
        @param float e0: value of e0
        @return:
        """
        for i in range(self.npaths):
            self.Population[i].set_e0(e0)

    def mutate_paths(self, chance):
        """
        Mutate Paths based on the input chance.
        @param float chance:
        @return:
        """
        for path in self.Population:
            path.mutate(chance)

    def verbose_yTotal(self, intervalk):
        """
        return the y total spectrum
        @param intervalk:
        @return:
        """
        yTotal = [0] * (401)
        for i in range(self.npaths):

            path = self.pathDictionary.get(self.pathname[i])
            Individual = self.get()
            path.e0 = Individual[i][1]
            path.s02 = Individual[i][0]
            path.sigma2 = Individual[i][2]
            path.deltar = Individual[i][3]
            feffdat.path2chi(path)
            y = path.chi
            for k in intervalk:
                yTotal[int(k)] += y[int(k)]

        return yTotal

    def __len__(self):
        """Return the number of independent parameters in the individual.
        """

        return int((3 * self.npaths) + 1)

    def __str__(self):
        return f"Individual with values of {self.get()}"
