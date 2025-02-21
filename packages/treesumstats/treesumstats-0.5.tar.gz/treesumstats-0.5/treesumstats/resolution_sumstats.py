import numpy as np

from treesumstats import BASIC_METRIC2HELP, BASIC_ARRAY_METRICS, BASIC_METRIC2FUN, FeatureCalculator

FRACTION_RESOLVED_NON_ZERO = "frac_inodes_resolved_non_zero"

FRACTION_RESOLVED = "frac_inodes_resolved"

N_RESOLVED_NON_ZERO = "n_inodes_resolved_non_zero"

N_RESOLVED = "n_inodes_resolved"

N_CHILDREN_PREFIX = "n_children"


class ResolutionFeatureCalculator(FeatureCalculator):
    """Computes tree resolution-related summary statistics."""

    def __init__(self):
        self._n_resolved_max = None
        self._n_resolved_nz = None
        self._n_resolved = None
        self._forest = None
        self._n_children = None

    def feature_names(self):
        return ([f'{N_CHILDREN_PREFIX}_{flavour}' for flavour in BASIC_ARRAY_METRICS] +
                [N_RESOLVED, N_RESOLVED_NON_ZERO, FRACTION_RESOLVED, FRACTION_RESOLVED_NON_ZERO])

    def set_forest(self, forest, **kwargs):
        self._forest = forest
        self._n_children = None
        self._n_resolved = None
        self._n_resolved_nz = None
        self._n_resolved_max = None

    @property
    def n_children(self):
        if self._n_children is None:
            n_children = []
            for tree in self._forest:
                n_children.extend(len(n.children) for n in tree.traverse() if not n.is_leaf())
            self._n_children =  np.array(n_children, dtype=int)
        return self._n_children

    @property
    def n_resolved(self):
        if self._n_resolved is None:
            self._n_resolved = 0
            self._n_resolved_nz = 0
            for tree in self._forest:
                for n in tree.traverse():
                    if 2 == len(n.children):
                        self._n_resolved += 1
                        if n.is_root() or n.dist:
                            if all(_.dist > 0 for _ in n.children):
                                self._n_resolved_nz += 1
        return self._n_resolved

    @property
    def n_resolved_binary(self):
        if self._n_resolved_max is None:
            self._n_resolved_max = sum(len(tree) for tree in self._forest) - len(self._forest)
        return self._n_resolved_max

    @property
    def n_resolved_nz(self):
        assert self.n_resolved >= 0
        return self._n_resolved_nz

    def calculate(self, feature_name, **kwargs):
        if feature_name.startswith(N_CHILDREN_PREFIX):
            return BASIC_METRIC2FUN[feature_name[len(N_CHILDREN_PREFIX) + 1:]](self.n_children)
        if N_RESOLVED == feature_name:
            return self.n_resolved
        if FRACTION_RESOLVED == feature_name:
            return self.n_resolved / self.n_resolved_binary
        if N_RESOLVED_NON_ZERO == feature_name:
            return self.n_resolved_nz
        return self.n_resolved_nz / self.n_resolved_binary

    def help(self, feature_name, *args, **kwargs):
        if feature_name.startswith(N_CHILDREN_PREFIX):
            return (f'{BASIC_METRIC2HELP[feature_name[len(N_CHILDREN_PREFIX) + 1:]]} '
                    f'of the number of children per internal node of forest trees.')
        if N_RESOLVED == feature_name:
            return 'number of resolved (i.e., with exactly 2 children) nodes in the forest.'
        if N_RESOLVED_NON_ZERO == feature_name:
            return ('number of resolved (i.e., with exactly 2 children) forest nodes '
                    'that are either root nodes or have non-zero branch length.')
        if FRACTION_RESOLVED == feature_name:
            return ('fraction of resolved (i.e., with exactly 2 children) nodes in the forest '
                    'with respect to the number of internal nodes in this forest '
                    'if all its trees were fully resolved (i.e., binary).')
        if FRACTION_RESOLVED_NON_ZERO == feature_name:
            return ('fraction of resolved (i.e., with exactly 2 children) forest nodes '
                    'that are either root nodes or have non-zero branch length '
                    'with respect to the number of internal nodes in this forest '
                    'if all its trees were fully resolved (i.e., binary).')
        return None
