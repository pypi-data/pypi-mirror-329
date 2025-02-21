import numpy as np

from treesumstats import BASIC_METRIC2HELP, BASIC_METRIC2FUN, FeatureCalculator, MEAN, MED, VAR, EPSILON
from treesumstats.tree_manager import annotate_forest_with_time, TIME

BRLEN = 'brlen'

class BranchFeatureCalculator(FeatureCalculator):
    """Computes tree branch-related summary statistics."""

    def __init__(self):
        self._edists_top = None
        self._idists_top = None
        self._edists_bottom = None
        self._idists_bottom = None
        self._edists_middle = None
        self._idists_middle = None
        self._max_time = None
        self._idists = None
        self._edists = None
        self._forest = None

    def feature_names(self):
        return [f'{BRLEN}_inode_{flavour}' for flavour in [MEAN, MED, VAR]] \
            + [f'{BRLEN}_tip_{flavour}' for flavour in [MEAN, MED, VAR]] \
            + [f'{BRLEN}_inode_top_{flavour}' for flavour in [MEAN, MED, VAR]] \
            + [f'{BRLEN}_tip_top_{flavour}' for flavour in[MEAN, MED, VAR]]\
            + [f'{BRLEN}_inode_middle_{flavour}' for flavour in [MEAN, MED, VAR]] \
            + [f'{BRLEN}_tip_middle_{flavour}' for flavour in[MEAN, MED, VAR]] \
            + [f'{BRLEN}_inode_bottom_{flavour}' for flavour in [MEAN, MED, VAR]] \
            + [f'{BRLEN}_tip_bottom_{flavour}' for flavour in[MEAN, MED, VAR]] \
            + [f'frac_{BRLEN}_inode_{flavour}_by_{BRLEN}_tip_{flavour}' for flavour in [MEAN, MED, VAR]] \
            + [f'frac_{BRLEN}_inode_top_{flavour}_by_{BRLEN}_tip_top_{flavour}' for flavour in [MEAN, MED, VAR]] \
            + [f'frac_{BRLEN}_inode_middle_{flavour}_by_{BRLEN}_tip_middle_{flavour}' for flavour in [MEAN, MED, VAR]] \
            + [f'frac_{BRLEN}_inode_bottom_{flavour}_by_{BRLEN}_tip_bottom_{flavour}' for flavour in [MEAN, MED, VAR]]


    def set_forest(self, forest, **kwargs):
        self._forest = forest
        annotate_forest_with_time(self._forest)
        self._idists = None
        self._edists = None
        self._edists_top = None
        self._idists_top = None
        self._edists_middle = None
        self._idists_middle = None
        self._edists_bottom = None
        self._idists_bottom = None
        self._max_time = None


    @property
    def max_time(self):
        if self._max_time is None:
            self._max_time = max(getattr(_, TIME) for tree in self._forest for _ in tree)
        return self._max_time

    @property
    def idists(self):
        if self._idists is None:
            self._idists, self._edists = self._get_branch_lengths()
        return self._idists

    @property
    def edists(self):
        if self._edists is None:
            self._idists, self._edists = self._get_branch_lengths()
        return self._edists

    @property
    def idists_top(self):
        if self._idists_top is None:
            self._idists_top, self._edists_top = self._get_branch_lengths(max_time=self.max_time / 3)
        return self._idists_top

    @property
    def edists_top(self):
        if self._edists_top is None:
            self._idists_top, self._edists_top = self._get_branch_lengths(max_time=self.max_time / 3)
        return self._edists_top

    @property
    def idists_middle(self):
        if self._idists_middle is None:
            self._idists_middle, self._edists_middle = \
                self._get_branch_lengths(min_time=self.max_time / 3, max_time=2 * self.max_time / 3)
        return self._idists_middle

    @property
    def edists_middle(self):
        if self._edists_middle is None:
            self._idists_middle, self._edists_middle = \
                self._get_branch_lengths(min_time=self.max_time / 3, max_time=2 * self.max_time / 3)
        return self._edists_middle

    @property
    def idists_bottom(self):
        if self._idists_bottom is None:
            self._idists_bottom, self._edists_bottom = self._get_branch_lengths(min_time=2 * self.max_time / 3)
        return self._idists_bottom

    @property
    def edists_bottom(self):
        if self._edists is None:
            self._idists_bottom, self._edists_bottom = self._get_branch_lengths(min_time=2 * self.max_time / 3)
        return self._edists_bottom

    def _get_branch_lengths(self, min_time=-np.inf, max_time=np.inf):
        internal_dists, external_dists = [], []

        for tree in self._forest:
            for n in tree.traverse():
                n_time = getattr(n, TIME)
                if n_time <= min_time or n_time > max_time:
                    continue

                dist = min(n.dist, n_time - min_time)

                if n.is_leaf():
                    external_dists.append(dist)
                else:
                    internal_dists.append(dist)
        return internal_dists, external_dists


    def calculate(self, feature_name, **kwargs):
        if feature_name.startswith(BRLEN):
            is_internal = 'inode' in feature_name
            flavour = feature_name.split('_')[-1]
            if is_internal:
                data = self.idists_top if 'top' in feature_name \
                    else (self.idists_middle if 'middle' in feature_name \
                              else (self.idists_bottom if 'bottom' in feature_name else self.idists))
            else:
                data = self.edists_top if 'top' in feature_name \
                    else (self.edists_middle if 'middle' in feature_name \
                              else (self.edists_bottom if 'bottom' in feature_name else self.edists))
            return BASIC_METRIC2FUN[flavour](data) if len(data) else 0
        if feature_name.startswith('frac'):
            feature_name_1, feature_name_2 = feature_name[len('frac_'): ].split('_by_')
            val1, val2 = self.calculate(feature_name_1), self.calculate(feature_name_2)
            return val1 / max(val2, EPSILON)
        return None

    def help(self, feature_name, *args, **kwargs):
        if feature_name.startswith(BRLEN):
            is_internal = 'inode' in feature_name
            flavour = feature_name.split('_')[-1]
            res = f'{BASIC_METRIC2HELP[flavour]} ' \
                  f'of the branch lengths of the forest {'internal nodes' if is_internal else 'tips'}.'
            part = 'top' if 'top' in feature_name \
                else ('middle' if 'middle' in feature_name else ('bottom' if 'bottom' in feature_name else ''))
            if part:
                res += f' Only branches finishing in the {part} third of the forest are considered. Their start time is cut to the start of the interval if they started before.' \
                       f'(The total time between the earliest forest tree start and the last sampled tip '\
                       'is split into three equal parts.)'
            return res
        if feature_name.startswith('frac'):
            feature_name_1, feature_name_2 = feature_name[len('frac_'):].split('_by_')
            return f'fraction of two values. The dividend is {self.help(feature_name_1).split('.')[0]}. '\
                   f'The divisor is {self.help(feature_name_2)}'
        return None