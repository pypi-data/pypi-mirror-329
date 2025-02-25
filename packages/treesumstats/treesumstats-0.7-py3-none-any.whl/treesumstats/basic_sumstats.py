from treesumstats import FeatureCalculator


class BasicFeatureCalculator(FeatureCalculator):
    """Computes tree height-related summary statistics."""

    def __init__(self):
        self._forest = None

    def feature_names(self):
        return ['n_trees', 'n_tips', 'n_inodes', 'len_forest']

    def set_forest(self, forest, **kwargs):
        self._forest = forest

    def calculate(self, feature_name, **kwargs):
        if 'n_trees' == feature_name:
            return len(self._forest)
        if 'n_tips' == feature_name:
            return sum(len(tree) for tree in self._forest)
        if 'n_inodes' == feature_name:
            return sum(1 for tree in self._forest for n in tree.traverse() if not n.is_leaf())
        if 'len_forest' == feature_name:
            return sum(_.dist for tree in self._forest for _ in tree.traverse())
        return None

    def help(self, feature_name, *args, **kwargs):
        if 'n_trees' == feature_name:
            return 'number of trees in the forest.'
        if 'n_tips' == feature_name:
            return 'number of tips in the forest.'
        if 'n_inodes' == feature_name:
            return 'number of internal nodes in the forest.'
        if 'len_forest' == feature_name:
            return 'sum of forest branch lengths.'
        return None
