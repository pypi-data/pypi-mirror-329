import numpy as np
import scipy
from scipy.stats import linregress

from treesumstats.tree_manager import TIME, annotate_forest_with_time

TARGET_AVG_BL = 1

CHERRY_PERCENTILES = [0, 1, 5, 10, 25, 50, 75, 100]
INCUBATION_PERIOD_PERCENTILES = [0, 5, 10, 25, 50, 75, 90, 95, 100]




def get_cherry_metrics(forest):
    """
    Computes the following metrics on tree cherries:
    0th (min), 1st, 5th, 10th, 25th, 50th, 75th and 100th (max) percentiles of cherry tip differences
    0th (min), 1st, 5th, 10th, 25th, 50th, 75th and 100th (max) percentiles of cherry tip differences in reshuffled cherries
    mean and var of tip branch len differences
    mean and var of tip branch len differences in reshuffled cherries
    cherry test value

    :param forest: list(ete3.Tree), forest of trees on which these metrics are computed
    :return: tuple of the above metrics in the above order
    """
    all_cherries = []
    for tree in forest:
        all_cherries.extend(pick_cherries(tree, include_polytomies=True))
    all_cherries = sorted(all_cherries, key=lambda _: getattr(_.root, TIME))

    if all_cherries:
        num_cherries = len(all_cherries)
        random_diffs, real_diffs = get_real_vs_reshuffled_diffs(all_cherries)
        pval = scipy.stats.binomtest((random_diffs < real_diffs).sum(), n=num_cherries, p=0.5, alternative='less').pvalue

        return (*np.percentile(real_diffs, q=CHERRY_PERCENTILES),
                *np.percentile(random_diffs, q=CHERRY_PERCENTILES),
                np.mean(real_diffs), np.var(real_diffs),
                np.mean(random_diffs), np.var(random_diffs), pval)
    else:
        return *np.zeros(len(CHERRY_PERCENTILES)), *np.zeros(len(CHERRY_PERCENTILES)), 0, 0, 0, 0, 1


def get_incubation_metrics(forest):
    """
    Computes the following metrics on tree internal sibling branches:
    percentage of internal nodes that have an internal sibling among all internal nodes
    0th (min), 5th, 10th, 25th, 50th, 75th, 90th, 95th and 100th (max) percentiles of sibling branch len differences
    mean and var of sibling branch len differences
    sibling test value

    :param forest: list(ete3.Tree), forest of trees on which these metrics are computed
    :return: tuple of the above metrics in the above order
    """
    all_siblings = []
    for tree in forest:
        all_siblings.extend(pick_siblings(tree, include_polytomies=True))
    all_siblings = sorted(all_siblings, key=lambda _: getattr(_.root, TIME))

    if all_siblings:
        n_siblings = len(all_siblings)
        random_diffs, real_diffs = get_real_vs_reshuffled_diffs(all_siblings)
        pval = (scipy.stats.binomtest((random_diffs < real_diffs).sum(), n=n_siblings, p=0.5, alternative='greater')
                .pvalue)

        nodes_in_siblings = sum(len(_) for _ in all_siblings)
        num_internal_nodes = sum(sum(1 for _ in tree.traverse() if not _.is_leaf()) for tree in forest)

        return (nodes_in_siblings / num_internal_nodes,
                *np.percentile(real_diffs, q=INCUBATION_PERIOD_PERCENTILES),
                np.mean(real_diffs), np.var(real_diffs), pval)
    else:
        return 0, *np.zeros(len(INCUBATION_PERIOD_PERCENTILES)), 0, 0, 1

def calc_summary_statistics(forest):
    """Calculates the summary statistics for a given forest of trees.

    :param forest: list(ete3.Tree), forest of trees on which statistics are computed

    :return: dict of summary statistics
    """
    annotate_forest_with_time(forest)

    # compute summary statistics based on branch lengths
    summaries = {}



    # compute summary statistics based on cherries:
    summaries.update(zip([f'perc{i}_cdiff' for i in CHERRY_PERCENTILES]
                         + [f'perc{i}_cdiff_random' for i in CHERRY_PERCENTILES]
                         + ['mean_cdiff', 'var_cdiff', 'mean_cdiff_random', 'var_cdiff_random', 'ctest'],
                         get_cherry_metrics(forest)))

    # compute summary statistics based on incubation period:
    summaries.update(zip(['IS_nodes']
                         + [f'perc{i}_sdiff' for i in INCUBATION_PERIOD_PERCENTILES]
                         + ['mean_sdiff', 'var_sdiff', 'stest'],
                         get_incubation_metrics(forest)))



    return summaries




