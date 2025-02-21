from collections import Counter

import numpy as np
from scipy.special import digamma

from treesumstats import FeatureCalculator, NORMALIZED

IMBALANCE_AVG = 'imbalance_avg'

DEPTH_MAX = 'depth_max'

WIDTH_DELTA = 'width_delta'

WIDTH_DEPTH_RATIO = 'width_depth_ratio'

WIDTH_MAX = 'width_max'

SACKIN = 'sackin'

COLLESS = 'colless'

DEPTH = "depth"

class BalanceFeatureCalculator(FeatureCalculator):
    """Computes tree balance-related summary statistics."""

    def __init__(self):
        self._in_ladder = None
        self._max_ladder_norm = None
        self._max_ladder = None
        self._n_inodes = None
        self._max_width = None
        self._max_depth = None
        self._sackin = None
        self._colless = None
        self._forest = None
        self._n_tips = None
        self._delta_w = None
        self._avg_imbalance = None
        self._n_imbalanced = None

    def help(self, feature_name, *args, **kwargs):
        if feature_name.startswith(COLLESS):
            res = f'sum (over internal nodes) of absolute differences of numbers of tips in their left and right subtrees [Colless 1982].'
            if feature_name.endswith(NORMALIZED):
                res += ' We normalize it by dividing it by this metric for a forest of a ladder and all the other trees only having 1 tip: '\
                       '(n_tips - n_trees - 1) (n_tips - n_trees) / 2.'
            return res
        if feature_name.startswith(SACKIN):
            res = f'sum (over tips) of the number of internal nodes separating them from the root [Sackin 1972].'
            if feature_name.endswith(NORMALIZED):
                res += ' We normalize it by dividing it the value of this metric for a forest of a ladder and all the other trees only having 1 tip: '\
                       '(n_tips - n_trees) (n_tips - n_trees + 1) / 2 - 1.'
            return res

        if feature_name.startswith(DEPTH_MAX):
            res = "maximum node depth (i.e., number of branches separating a node from its tree root) [Colijn et al. 2014]."
            if feature_name.endswith(NORMALIZED):
                res += ' We normalize it by dividing it by the value of this metric for a forest of a ladder and all the other trees only having 1 tip: '\
                       '(n_tips - n_trees).'
            return res
        if feature_name.startswith(WIDTH_MAX):
            res = 'maximum width, where the width is defined as the number of nodes that are at the same depth, '\
                  'and node depth as the number of branches separating a node from its tree root [Colijn et al. 2014].'
            if feature_name.endswith(NORMALIZED):
                res += ' We normalize it by dividing it by the value of this metric for a forest of the same number of balanced trees with the same total number of tips.'
            return res
        if feature_name.startswith(WIDTH_DEPTH_RATIO):
            res = 'maximum width to maximum depth ratio, where the width is defined as the number of nodes that are at the same depth, '\
                  'and node depth as the number of branches separating a node from its tree root [Colijn et al. 2014].'
            if feature_name.endswith(NORMALIZED):
                res += ' We normalize it by dividing it by the value of this metric for a forest of the same number of balanced trees with the same total number of tips.'
            return res
        if feature_name.startswith(WIDTH_DELTA):
            res = 'maximum width difference between neighbouring depths, ' \
                  'where the width is defined as the number of nodes that are at the same depth, ' \
                  'and node depth as the number of branches separating a node from its tree root [Colijn et al. 2014].'
            if feature_name.endswith(NORMALIZED):
                res += (' We normalize it by dividing it by the value of this metric for a forest of the same '
                        'number of balanced trees and last two layers reorganised to increase the delta (tips at the last layer are grouped into one ladderized subtree).')
            return res
        if 'ladder' in feature_name:
            if 'inodes_in' in feature_name:
                measure = 'fraction' if feature_name.startswith('frac') else 'number'
                return f'{measure} of forest internal nodes that are resolved and have a tip descendant [Colijn et al. 2014].'
            elif 'max' in feature_name:
                res = 'maximum number of connected internal nodes with a single tip descendant [Colijn et al. 2014].'
                if feature_name.endswith(NORMALIZED):
                    res += ' We calculate it separately on each forest\'s tree and divide it by the number of tips in that tree. '\
                           'The maximum of these values is then reported.'
                return res
        if 'imbalanced' in feature_name:
            measure = 'fraction' if feature_name.startswith('frac') else 'number'
            return f'{measure} of internal nodes that have different number of tips ' \
                   f'in their smallest and their largest child subtrees [Colijn et al. 2014].'
        if IMBALANCE_AVG == feature_name:
            return 'mean ratio of min-to-max subtree sizes over all internal nodes [Colijn et al. 2014].'
        return None

    def feature_names(self):
        return [COLLESS, f'{COLLESS}_{NORMALIZED}'] \
            + [SACKIN, f'{SACKIN}_{NORMALIZED}'] \
            + [WIDTH_MAX, f'{WIDTH_MAX}_{NORMALIZED}'] \
            + [DEPTH_MAX, f'{DEPTH_MAX}_{NORMALIZED}'] \
            + [WIDTH_DEPTH_RATIO, f'{WIDTH_DEPTH_RATIO}_{NORMALIZED}'] \
            + [WIDTH_DELTA, f'{WIDTH_DELTA}_{NORMALIZED}'] \
            + ['frac_inodes_in_ladder', 'n_inodes_in_ladder',
               'len_ladder_max', f'len_ladder_max_{NORMALIZED}'] \
            + ['frac_inodes_imbalanced', 'n_inodes_imbalanced'] \
            + [IMBALANCE_AVG]

    def set_forest(self, forest, **kwargs):
        self._forest = forest
        self._n_tips = None
        self._colless = None
        self._sackin = None
        self._max_depth = None
        self._max_width = None
        self._delta_w = None
        self._n_inodes = None
        self._max_ladder_norm = None
        self._max_ladder = None
        self._in_ladder = None
        self._avg_imbalance = None
        self._n_imbalanced = None

    @property
    def n_tips(self):
        if self._n_tips is None:
            self._n_tips = sum(len(tree) for tree in self._forest)
        return self._n_tips

    @property
    def n_inodes(self):
        """Number of internal nodes in the forest"""
        if self._n_inodes is None:
            self._n_inodes = sum(sum(1 for _ in tree.traverse() if not _.is_leaf()) for tree in self._forest)
        return self._n_inodes


    @property
    def colless(self):
        if self._colless is None:
            self._colless = 0

            for tree in self._forest:
                for node in tree.traverse():
                    if not node.is_leaf():
                        if len(node.children) == 2:
                            child1, child2 = node.children
                            self._colless += abs(len(child1) - len(child2))
                        else:
                            scores = []
                            for j in range(len(node.children)):
                                for k in range(j + 1, len(node.children)):
                                    scores.append(abs(len(node.children[j]) - len(node.children[k])))
                            self._colless += np.average(scores)
        return self._colless

    def _annotate_depth(self):
        if not hasattr(self._forest[0], DEPTH):
            for tree in self._forest:
                for node in tree.traverse('preorder'):
                    parent_depth = -1 if node.is_root() else getattr(node.up, DEPTH)
                    node.add_feature(DEPTH, parent_depth + 1)

    @property
    def sackin(self):
        if self._sackin is None:
            self._annotate_depth()
            self._sackin = sum(sum(getattr(tip, DEPTH) - 1 for tip in tree if not tip.is_root())
                               for tree in self._forest)
        return self._sackin

    @property
    def max_depth(self):
        if self._max_depth is None:
            self._annotate_depth()
            self._max_depth = max(max(getattr(tip, DEPTH) for tip in tree) for tree in self._forest)
        return self._max_depth

    def _set_depth_delta(self):
        self._annotate_depth()
        width_d = Counter(getattr(node, DEPTH) for tree in self._forest for node in tree.traverse())
        self._max_width = width_d.most_common(n=1)[0][1]

        if self._max_depth is None:
            self._max_depth = max(width_d.keys())

        self._delta_w = 0
        for d in range(1, self._max_depth + 1):
            self._delta_w = max(np.abs(width_d[d] - width_d[d - 1]), self._delta_w)

    @property
    def max_width(self):
        if self._max_width is None:
            self._set_depth_delta()
        return self._max_width

    @property
    def delta_w(self):
        if self._delta_w is None:
            self._set_depth_delta()
        return self._delta_w

    def max_width_depth_balanced(self):
        # we distribute leaves equally into n_forest balanced trees
        # and compare the number of nodes at the second-but-last and the last levels to calculate the max width
        n_trees = len(self._forest)
        n_nodes = 2 * self.n_tips - n_trees
        l = np.floor(np.log2(self.n_tips / n_trees))
        nodes_in_second_but_last_level = n_trees * np.power(2, l)
        nodes_in_all_but_last_levels = n_trees * (np.power(2, l + 1) - 1)
        nodes_in_last_level = n_nodes - nodes_in_all_but_last_levels
        mw = max(nodes_in_second_but_last_level, nodes_in_last_level)
        md = l + 1 if nodes_in_last_level else l
        # to calculate the max_delta we take the level with the max_width
        # and (if it was not the last one) ladderize the leaves that belonged to the last level (hence leaving only two leaves there);
        # or (otherwise) removing a cherry from the last level and regrafting it on top of one of its existing tips
        # (hence removing two leaves from that level and adding two to the next one)
        if n_nodes == n_trees:
            delta = 0
        else:
            if not nodes_in_last_level:
                delta = max(nodes_in_second_but_last_level - 4,
                            nodes_in_second_but_last_level - nodes_in_second_but_last_level / 2)
            else:
                delta = max(np.abs(nodes_in_last_level - nodes_in_second_but_last_level),
                            nodes_in_second_but_last_level - 2,
                            nodes_in_last_level - 4)
        return mw, md, delta

    @property
    def in_ladder(self):
        if self._in_ladder is None:
            self._set_ladder()
        return self._in_ladder

    @property
    def max_ladder(self):
        if self._max_ladder is None:
            self._set_ladder()
        return self._max_ladder

    @property
    def max_ladder_norm(self):
        if self._max_ladder_norm is None:
            self._set_ladder()
        return self._max_ladder_norm

    def _set_imbalance(self):
        self._n_imbalanced = 0
        self._avg_imbalance = 0

        for tree in self._forest:
            for node in tree.traverse():
                if not node.is_leaf():
                    c_lens = sorted([len(c) for c in node.children])
                    if c_lens[0] != c_lens[-1]:
                        self._n_imbalanced += 1
                    self._avg_imbalance += c_lens[0] / c_lens[-1]
        self._avg_imbalance /= self.n_inodes

    @property
    def n_imbalanced(self):
        if self._n_imbalanced is None:
            self._set_imbalance()
        return self._n_imbalanced

    @property
    def avg_imbalanced(self):
        if self._avg_imbalance is None:
            self._set_imbalance()
        return self._avg_imbalance


    def _set_ladder(self):
        self._max_ladder = 0
        self._max_ladder_norm = 0
        self._in_ladder = 0
        for tree in self._forest:
            cur_ladder = 0
            for node in tree.traverse('preorder'):
                if 2 == len(node.children) and next((True for c in node.children if c.is_leaf()), False):
                    self._in_ladder += 1
                    parent_ladder_len = 0 if node.is_root() else getattr(node.up, 'ladder', 0)
                    ladder_len = 1 + parent_ladder_len
                    node.add_feature('ladder', ladder_len)
                    cur_ladder = max(cur_ladder, ladder_len)
            for node in set(_.up for _ in tree if not _.is_root()):
                node.del_feature('ladder')
            self._max_ladder = max(cur_ladder, self._max_ladder)
            self._max_ladder_norm = max(cur_ladder / len(tree), self._max_ladder_norm)



    def calculate(self, feature_name, **kwargs):
        n_trees = len(self._forest)
        if feature_name.startswith(COLLESS):
            denominator = (self.n_tips - n_trees - 1) * (self.n_tips - n_trees) / 2 \
                if feature_name.endswith(NORMALIZED) else 1
            return self.colless / denominator
        if feature_name.startswith(SACKIN):
            denominator = (self.n_tips - n_trees) * (self.n_tips - n_trees + 1) / 2 - 1 \
                if feature_name.endswith(NORMALIZED) else 1
            return self.sackin / denominator
        if feature_name.startswith(DEPTH_MAX):
            denominator = (self.n_tips - n_trees) if feature_name.endswith(NORMALIZED) else 1
            return self.max_depth / denominator
        if feature_name.startswith(WIDTH_MAX):
            denominator = self.max_width_depth_balanced()[0] if feature_name.endswith(NORMALIZED) else 1
            return self.max_width / denominator
        if feature_name.startswith(WIDTH_DEPTH_RATIO):
            mw, md, _ = self.max_width_depth_balanced()
            denominator = mw / md if feature_name.endswith(NORMALIZED) else 1
            return self.max_width / self.max_depth / denominator
        if feature_name.startswith(WIDTH_DELTA):
            denominator = self.max_width_depth_balanced()[-1] if feature_name.endswith(NORMALIZED) else 1
            return self.delta_w / denominator
        if 'ladder' in feature_name:
            if 'inodes_in' in feature_name:
                denominator = self.n_inodes if feature_name.startswith('frac') else 1
                return self.in_ladder / denominator
            elif 'max' in feature_name:
                return self.max_ladder_norm if feature_name.endswith(NORMALIZED) else self.max_ladder
        if 'imbalanced' in feature_name:
            denominator = self.n_inodes if feature_name.startswith('frac') else 1
            return self.n_imbalanced / denominator
        if IMBALANCE_AVG == feature_name:
            return self.avg_imbalanced
        return None


def min_avg_stair(n):
    return digamma(n + 1) + np.euler_gamma