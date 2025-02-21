import numpy as np

from treesumstats import BASIC_METRIC2HELP, BASIC_ARRAY_METRICS, BASIC_METRIC2FUN, FeatureCalculator, NORMALIZED
from treesumstats.tree_manager import annotate_forest_with_time, TIME


class EventTimeFeatureCalculator(FeatureCalculator):
    """Computes tree event time-related summary statistics."""

    def __init__(self):
        self._max_time = None
        self._tip_times = None
        self._forest = None
        self._inode_times = None

    def feature_names(self):
        return [f'{TIME}_tip_{flavour}' for flavour in BASIC_ARRAY_METRICS] \
            +  [f'{TIME}_inode_{flavour}' for flavour in BASIC_ARRAY_METRICS] \
            +  [f'{TIME}_tip_{NORMALIZED}_{flavour}' for flavour in BASIC_ARRAY_METRICS] \
            + [f'{TIME}_inode_{NORMALIZED}_{flavour}' for flavour in BASIC_ARRAY_METRICS]

    def set_forest(self, forest, **kwargs):
        self._forest = forest
        annotate_forest_with_time(self._forest)
        self._tip_times = None
        self._inode_times = None
        self._max_time = None

    @property
    def tip_times(self):
        if self._tip_times is None:
            self._tip_times = np.array([getattr(t, TIME) for tree in self._forest for t in tree])
        return self._tip_times

    @property
    def max_time(self):
        if self._max_time is None:
            self._max_time = np.max(self.tip_times)
        return self._max_time

    @property
    def inode_times(self):
        if self._inode_times is None:
            self._inode_times \
                = np.array([getattr(n, TIME) for tree in self._forest for n in tree.traverse() if not n.is_leaf()])
        return self._inode_times

    def calculate(self, feature_name, **kwargs):
        if feature_name.startswith(TIME):
            is_internal = 'inode' in feature_name
            is_normalized = NORMALIZED in feature_name
            flavour = feature_name.split('_')[-1]
            return BASIC_METRIC2FUN[flavour]((self.inode_times if is_internal else self.tip_times)
                                             / (self.max_time if is_normalized else 1))

        return None

    def help(self, feature_name, *args, **kwargs):
        if feature_name.startswith(TIME):
            is_internal = 'inode' in feature_name
            node = 'internal node' if is_internal else 'tip'
            is_normalized = NORMALIZED in feature_name
            flavour = feature_name.split('_')[-1]
            res = f'{BASIC_METRIC2HELP[flavour]} of the times of forest {node}s.'
            if is_normalized:
                res += ' We normalize the times by dividing them by the last tip\'s time.'
            return res
        return None