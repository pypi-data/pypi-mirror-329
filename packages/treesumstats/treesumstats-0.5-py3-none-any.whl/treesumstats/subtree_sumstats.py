import re
from collections import defaultdict

import numpy as np
import scipy

from treesumstats import FeatureCalculator, BASIC_METRIC2FUN, BASIC_METRIC2HELP, BASIC_ARRAY_METRICS, EPSILON
from treesumstats.tree_manager import annotate_forest_with_time, TIME

OTHER_CONFIGURATION_LABEL = 'O'

TIP_TOPOLOGY_LABELS = ['2', '3U', '3L', '4U', '4U3U1', '4U211', '4L', '4B', 'O']
INODE_LABELS = ['I']
TOPOLOGY_LABELS = TIP_TOPOLOGY_LABELS + INODE_LABELS

TIP = 1

CHERRY = (TIP, TIP)

TRIPLET_UNRESOLVED = (TIP, TIP, TIP)
TRIPLET_LADDER = (CHERRY, TIP)

QUARTET_UNRESOLVED = (TIP, TIP, TIP, TIP)
QUARTET_TRIPLET_UNRESOLVED_TIP = (TRIPLET_UNRESOLVED, TIP)
QUARTET_CHERRY_TIP_TIP = (CHERRY, TIP, TIP)
QUARTET_LADDER = (TRIPLET_LADDER, TIP)
QUARTET_BALANCED = (CHERRY, CHERRY)

OTHER = 2

CONFIG_ORDER = [TIP, CHERRY, TRIPLET_UNRESOLVED, TRIPLET_LADDER,
                QUARTET_UNRESOLVED, QUARTET_TRIPLET_UNRESOLVED_TIP, QUARTET_CHERRY_TIP_TIP, QUARTET_LADDER, QUARTET_BALANCED,
                OTHER]

TOPOLOGY_LABEL2KEY = {'2': CHERRY, '3U': TRIPLET_UNRESOLVED, '3L': TRIPLET_LADDER, '4U': QUARTET_UNRESOLVED,
                      '4U3U1': QUARTET_TRIPLET_UNRESOLVED_TIP, '4U211': QUARTET_CHERRY_TIP_TIP,
                      '4L': QUARTET_LADDER, '4B': QUARTET_BALANCED, 'O': 2, 'I': -1}

KEY2TOPOLOGY_LABEL = {v: k for (k, v) in TOPOLOGY_LABEL2KEY.items()}

TOPOLOGY_LABEL2N = {'2': 2, '3U': 3, '3L': 3, '4U': 4,
                    '4U3U1': 4, '4U211': 4,
                    '4L': 4, '4B': 4, 'O': 1}

TOPOLOGY_LABEL2NAME = {'2': 'cherries', '3U': 'unresolved triplets', '3L': 'resolved triplets',
                       '4U': 'fully unresolved quartets',
                       '4U3U1': 'partially resolved quartets with an unresolved triplet and a tip as children',
                       '4U211': 'partially resolved quartets with a cherry and two tips as three children',
                       '4L': 'ladderized fully resolved quartets',
                       '4B': 'balanced quartets (with two cherries as children)',
                       'I': 'cherries or fully unresolved n-tip subtrees (n > 2) whose external nodes were internal in the global forest'}


TIP_TIME_PERCENTILES = [1, 5, 10, 25, 75, 90, 95, 99]


def get_config2tips(forest):
    topo2tips = defaultdict(list)
    feature = 'configuration'
    for tree in forest:
        for n in tree.traverse('postorder'):
            if n.is_leaf():
                if not n.is_root():
                    n.add_feature(feature, TIP)
                continue

            if len(n) > 4:
                topo2tips[OTHER].extend(_ for _ in n.children if _.is_leaf())
            else:
                config = tuple(
                    sorted([getattr(c, feature) for c in n.children], key=lambda _: -CONFIG_ORDER.index(_)))
                n.add_feature(feature, config)
                topo2tips[config].append(list(n.iter_leaves()))

            for c in n.children:
                c.del_feature(feature)
    return topo2tips


def pick_siblings(forest, include_polytomies=True):
    """
    Picks internal sibling motifs in the given forest.

    :param include_polytomies: bool, whether to include nodes with > 2 children into consideration.
    :param forest: list(ete3.Tree), the forest of interest
    :return: iterator of Motif motifs
    """
    result = []
    for tree in forest:
        for root in tree.traverse():
            if root.is_leaf() or not include_polytomies and len(root.children) != 2:
                continue
            siblings = [_ for _ in root.children if not _.is_leaf()]
            if len(siblings) < 2:
                continue
            result.append(siblings)
    return result


def get_reshuffled_configs(real_configs, all_tips_sorted):
    """
    Creates reshuffled configs. For each real config a reshuffled one is constructed by
        (1) keeping one tip from the real config
        (2) for each other tip from the real config picking a tip such that
            (2a) the time at the beginning of its branch is as close as possible to the time at the beginning of the real tip's branch,
            (2b) all the tips in the reshuffled config are different
            and (2c) there are no two tips in the reshuffled config that used to belong to the sam real config
                    (unless there are not enough tips, e.g., 8 tips in total and 2 4-tip configs)

    :param real_configs: an array of tip arrays representing real configs
    :param all_tips_sorted: an array of all tips in the forest, sorted by the time at the beginning of their branches (ascending order)
    :return: an array of tip arrays representing reshuffled configs
    """
    if not len(real_configs):
        return real_configs

    tip2config = {t: i for i, conf in enumerate(real_configs) for t in conf}

    def get_start_time(tip):
        return getattr(tip, TIME) - tip.dist

    n_tips = len(all_tips_sorted)

    def get_closest_tip(tip, is_ok=lambda _: True):
        j = all_tips_sorted.index(tip)
        tip_stime = get_start_time(tip)

        next_tip = next((all_tips_sorted[_] for _ in range(j + 1, n_tips) if is_ok(all_tips_sorted[_])), None)
        prev_tip = next((all_tips_sorted[_] for _ in range(j - 1, -1, -1) if is_ok(all_tips_sorted[_])), None)
        if prev_tip is None and next_tip is None:
            return tip
        return min([_ for _ in (next_tip, prev_tip) if not _ is None], key=lambda t: np.abs(get_start_time(t) - tip_stime))

    reshuffled_confs = []
    for i, conf in enumerate(real_configs):
        config_len = len(conf)
        fixed_tip = np.random.choice(conf, size=1, replace=False)[0]
        used_tips = []
        used_configs = {i}

        def is_ok(tip):
            return (tip not in used_tips) \
                and (tip not in tip2config or tip2config[tip] not in used_configs \
                     or (len(used_configs) * config_len + (len(used_tips) - len(used_configs)) == n_tips))

        for other_tip in conf:
            tip = other_tip if other_tip == fixed_tip else get_closest_tip(other_tip, is_ok)
            used_tips.append(tip)
            if tip in tip2config:
                used_configs.add(tip2config[tip])
        reshuffled_confs.append(used_tips)

    return reshuffled_confs


def get_avg_time_diff(times):
    n = len(times)
    diff_sum = 0
    for i in range(n - 1):
        time_i = times[i]
        for j in range(i + 1, n):
            diff_sum += np.abs(time_i - times[j])
    return 2 * diff_sum / n / (n - 1)


class SubtreeFeatureCalculator(FeatureCalculator):
    """Computes tree topology-related summary statistics."""

    def __init__(self):
        self._topo2tips_random = None
        self._n_inodes = None
        self._sibling_inodes = None
        self._topo2diffs = None
        self._topo2diffs_random = None
        self._all_tips = None
        self._forest = None
        self._topo2tips = None
        self._n_tips = None
        self._sibling_inodes_random = None
        self._topo2inodes_random = None
        self._all_inodes = None

    def help(self, feature_name, *args, **kwargs):
        if 'tips_in_' in feature_name:
            conf = feature_name[feature_name.find('tips_in_') + len('tips_in_'):]
            measure = 'fraction' if feature_name.startswith('frac') else 'number'
            if 'O' == conf:
                return f'{measure} of forest tips that are not part of any subtree of size 2, 3 or 4.'
            return f'{measure} of forest tips that are found in {TOPOLOGY_LABEL2NAME[conf]}.'

        if 'inodes_with_sibling_inodes' in feature_name:
            measure = 'fraction' if feature_name.startswith('frac') else 'number'
            return f'{measure} of forest non-root internal nodes that have internal node siblings.'
        if 'inodes_without_sibling_inodes' in feature_name:
            measure = 'fraction' if feature_name.startswith('frac') else 'number'
            return f'{measure} of forest non-root internal nodes that do not have internal node siblings.'

        if feature_name.startswith('time_diff_in_'):
            conf = feature_name[feature_name.find('time_diff_in_') + len('time_diff_in_'):].split('_')[0]
            is_real='real' in feature_name

            reshuffling_expl = '(To construct a reshuffled subtree of a certain kind from a real one we keep one of its (randomly chosen) locally external (with respect to the subtree) nodes, ' \
                               'while for each of its other locally external node we replace it with a node of the same global type (internal or external, with respect to the global forest), for which:' \
                               '(i) the time at the beginning of its branch is as close as possible to the time at the beginning of the real locally external node\'s branch, ' \
                               '(ii) while all the locally external nodes in the reshuffled subtree are different ' \
                               'and (iii) there are no two locally external nodes in the reshuffled subtree that used to belong to the same real subtree of this kind ' \
                               '(unless there were not enough such nodes, e.g., 8 tips in total and only 2 4-tip subtrees in the forest).'

            flavour = feature_name.split('_')[-1]
            if flavour in BASIC_METRIC2FUN or 'perc' in flavour:
                res = f'{BASIC_METRIC2HELP[flavour]}' if flavour in BASIC_METRIC2FUN \
                    else f'{re.findall(r'\d+', flavour)[0]}th percentile'
                res += f' of average of all external node pair sampling time differences in a {TOPOLOGY_LABEL2NAME[conf]} among all {'' if is_real else 'reshuffled'}' \
                       f'{TOPOLOGY_LABEL2NAME[conf]} in the forest.'
                if not is_real:
                    res += reshuffling_expl
                return res
            else:
                if 'random_vs_real_n_' in feature_name:
                    less_or_more = 'smaller' if 'less' == feature_name.split('_')[-1] else 'larger'
                    return f'number of {TOPOLOGY_LABEL2NAME[conf]}, ' \
                           f'for which their average external node sampling time difference is {less_or_more} in real subtrees than ' \
                           f'in the corresponding reshuffled ones. {reshuffling_expl}'
                elif 'random_vs_real_frac_' in feature_name:
                    less_or_more = 'smaller' if 'less' == feature_name.split('_')[-1] else 'larger'
                    return f'fraction of {TOPOLOGY_LABEL2NAME[conf]}, ' \
                           f'for which their average external node sampling time difference is {less_or_more} in real subtrees than ' \
                           f'in the corresponding reshuffled ones. {reshuffling_expl}'
                elif 'random_vs_real_pval_' in feature_name:
                    less_or_more = 'smaller' if 'less' == feature_name.split('_')[-1] else 'larger'
                    return f'p-value of the sign test checking that for {TOPOLOGY_LABEL2NAME[conf]}, ' \
                           'their average external node sampling time differences are indistinguishable in real subtrees and ' \
                           f'in the corresponding reshuffled ones ' \
                           f'(the alternative hypothesis is that some real ones are {less_or_more}). {reshuffling_expl}'

        return None

    def feature_names(self):
        return [f'frac_tips_in_{conf}' for conf in TIP_TOPOLOGY_LABELS] \
            + [f'n_tips_in_{conf}' for conf in TIP_TOPOLOGY_LABELS] \
            + [f'frac_inodes_{wwo}_sibling_inodes' for wwo in ('with', 'without')] \
            + [f'n_inodes_{wwo}_sibling_inodes' for wwo in ('with', 'without')] \
            + [f'time_diff_in_{conf}_{type}_{flavour}' for type in ('real', 'random') for flavour in BASIC_ARRAY_METRICS for conf in TOPOLOGY_LABELS if conf != OTHER_CONFIGURATION_LABEL] \
            + [f'time_diff_in_{conf}_{type}_perc{p}' for type in ('real', 'random') for p in TIP_TIME_PERCENTILES for conf in TOPOLOGY_LABELS if conf != OTHER_CONFIGURATION_LABEL] \
            + [f'time_diff_in_{conf}_random_vs_real_{metric}_{how}' for metric in ('n', 'frac', 'pval') for conf in TOPOLOGY_LABELS if conf != OTHER_CONFIGURATION_LABEL for how in ('less', 'more')]

    def set_forest(self, forest, **kwargs):
        self._forest = forest
        annotate_forest_with_time(self._forest)
        self._topo2tips = None
        self._n_tips = None
        self._all_tips = None
        self._all_inodes = None
        self._sibling_inodes_random = None
        self._topo2diffs = None
        self._topo2diffs_random = None
        self._sibling_inodes = None
        self._topo2inodes_random = None
        self._n_inodes = None
        self._topo2tips_random = None

    @property
    def n_tips(self):
        if self._n_tips is None:
            self._n_tips = sum(len(tree) for tree in self._forest)
        return self._n_tips

    @property
    def n_inodes(self):
        if self._n_inodes is None:
            self._n_inodes = sum(sum(1 for n in tree.traverse() if not n.is_leaf() and not n.is_root()) for tree in self._forest)
        return self._n_inodes

    def conf2tips(self, config_type, is_real=True):
        if is_real:
            if self._topo2tips is None:
                self._topo2tips = get_config2tips(self._forest)
            return self._topo2tips[config_type]

        if self._topo2tips_random is None:
            self._topo2tips_random = dict()
        if config_type not in self._topo2tips_random:
            self._topo2tips_random[config_type] = get_reshuffled_configs(self.conf2tips(config_type, is_real=True),
                                                                              self.all_tips)
        return self._topo2tips_random[config_type]


    def sibling_inodes(self, is_real=True):
        if is_real:
            if self._sibling_inodes is None:
                self._sibling_inodes = pick_siblings(self._forest)
            return self._sibling_inodes

        if self._sibling_inodes_random is None:
            self._sibling_inodes_random = []
        self._sibling_inodes_random = get_reshuffled_configs(self.sibling_inodes(is_real=True), self.all_inodes)
        return self._sibling_inodes_random

    def conf2time_diffs(self, config_type, is_real=True):
        is_tip_config = KEY2TOPOLOGY_LABEL[config_type] in TIP_TOPOLOGY_LABELS
        if is_real:
            if self._topo2diffs is None:
                self._topo2diffs = {}
            if config_type not in self._topo2diffs:
                confs_real = self.conf2tips(config_type, is_real=True) if is_tip_config else self.sibling_inodes(is_real=True)
                self._topo2diffs[config_type] = np.array([get_avg_time_diff([getattr(_, TIME) for _ in c]) for c in confs_real])
            return self._topo2diffs[config_type]
        if self._topo2diffs_random is None:
            self._topo2diffs_random = {}
        if config_type not in self._topo2diffs_random:
            confs_real = self.conf2tips(config_type, is_real=True) if is_tip_config else self.sibling_inodes(is_real=True)
            confs_random = self.conf2tips(config_type, is_real=False) if is_tip_config else self.sibling_inodes(is_real=False)
            self._topo2diffs_random[config_type] = np.array([get_avg_time_diff([getattr(t, TIME) - t.dist + tr.dist
                                                                                for t, tr in zip(c, cr)])
                                                             for c, cr in zip(confs_real, confs_random)])
        return self._topo2diffs_random[config_type]

    @property
    def all_tips(self):
        if self._all_tips is None:
            self._all_tips = sorted([t for tree in self._forest for t in tree], key=lambda _: getattr(_, TIME) - _.dist)
        return self._all_tips

    @property
    def all_inodes(self):
        if self._all_inodes is None:
            self._all_inodes = sorted([n for tree in self._forest for n in tree.traverse() if not n.is_leaf() and not n.is_root()],
                                     key=lambda _: getattr(_, TIME) - _.dist)
        return self._all_inodes

    def calculate(self, feature_name, **kwargs):
        if 'tips_in_' in feature_name:
            conf = feature_name[feature_name.find('tips_in_') + len('tips_in_'):]
            denominator = self.n_tips if feature_name.startswith('frac') else 1
            return len(self.conf2tips(TOPOLOGY_LABEL2KEY[conf], is_real=True)) * TOPOLOGY_LABEL2N[conf] / denominator

        if 'inodes_with_sibling_inodes' in feature_name:
            denominator = max(self.n_inodes, EPSILON) if feature_name.startswith('frac') else 1
            return sum(len(_) for _ in self.sibling_inodes(is_real=True)) / denominator
        if 'inodes_without_sibling_inodes' in feature_name:
            denominator = max(self.n_inodes, EPSILON) if feature_name.startswith('frac') else 1
            return (self.n_inodes - sum(len(_) for _ in self.sibling_inodes(is_real=True))) / denominator

        if feature_name.startswith('time_diff_in_'):
            conf = feature_name[feature_name.find('time_diff_in_') + len('time_diff_in_'):].split('_')[0]
            is_real = 'real' in feature_name
            time_diffs = self.conf2time_diffs(TOPOLOGY_LABEL2KEY[conf], is_real=is_real)

            flavour = feature_name.split('_')[-1]
            n = len(time_diffs)
            if flavour in BASIC_METRIC2FUN:
                return BASIC_METRIC2FUN[flavour](time_diffs) if n else 0
            elif 'perc' in flavour:
                perc = int(re.findall(r'\d+', flavour)[0])
                return np.percentile(time_diffs, perc) if n else 0
            else:
                time_diffs_random = self.conf2time_diffs(TOPOLOGY_LABEL2KEY[conf], is_real=False)
                is_less = 'less' == feature_name.split('_')[-1]
                n_random_vs_real = ((time_diffs_random < time_diffs) if is_less else (time_diffs_random > time_diffs)).sum()
                if 'random_vs_real_n_' in feature_name:
                    return n_random_vs_real
                elif 'random_vs_real_frac_' in feature_name:
                    return n_random_vs_real / n if n else 0.5
                elif 'random_vs_real_pval_' in feature_name:
                    return scipy.stats.binomtest(n_random_vs_real, n=n, p=0.5, alternative='less').pvalue if n else 0.5

