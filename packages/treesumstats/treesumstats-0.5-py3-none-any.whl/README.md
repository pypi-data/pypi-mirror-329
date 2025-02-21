# treesumstats

Representing phylogenetic trees (or forests of such trees) as summary statistics.



[//]: # ([![DOI:10.1093/sysbio/syad059]&#40;https://zenodo.org/badge/DOI/10.1093/sysbio/syad059.svg&#41;]&#40;https://doi.org/10.1093/sysbio/syad059&#41;)
[//]: # ([![GitHub release]&#40;https://img.shields.io/github/v/release/evolbioinfo/treesumstats.svg&#41;]&#40;https://github.com/evolbioinfo/treesumstats/releases&#41;)
[![PyPI version](https://badge.fury.io/py/treesumstats.svg)](https://pypi.org/project/treesumstats/)
[![PyPI downloads](https://shields.io/pypi/dm/treesumstats)](https://pypi.org/project/treesumstats/)
[![Docker pulls](https://img.shields.io/docker/pulls/evolbioinfo/treesumstats)](https://hub.docker.com/r/evolbioinfo/treesumstats/tags)

## Implemented summary statistics

### Basic Tree statistics 
Implemented in [_treesumstats.basic_sumstats.BasicFeatureCalculator_](treesumstats/balance_sumstats.py).

1. **n_trees:** number of trees in the forest.
1. **n_tips:** number of tips in the forest.
1. **n_inodes:** number of internal nodes in the forest.
1. **len_forest:** sum of forest branch lengths.

### Tree resolution statistics
Implemented in [_treesumstats.resolution_sumstats.ResolutionFeatureCalculator_](treesumstats/resolution_sumstats.py).

1. **n_children_mean:** average of the number of children per internal node of forest trees.
1. **n_children_min:** minimum of the number of children per internal node of forest trees.
1. **n_children_max:** maximum of the number of children per internal node of forest trees.
1. **n_children_var:** variance of the number of children per internal node of forest trees.
1. **n_children_median:** median of the number of children per internal node of forest trees.
1. **n_inodes_resolved:** number of resolved (i.e., with exactly 2 children) nodes in the forest.
1. **n_inodes_resolved_non_zero:** number of resolved (i.e., with exactly 2 children) forest nodes that are either root nodes or have non-zero branch length.
1. **frac_inodes_resolved:** fraction of resolved (i.e., with exactly 2 children) nodes in the forest with respect to the number of internal nodes in this forest if all its trees were fully resolved (i.e., binary).
1. **frac_inodes_resolved_non_zero:** fraction of resolved (i.e., with exactly 2 children) forest nodes that are either root nodes or have non-zero branch length with respect to the number of internal nodes in this forest if all its trees were fully resolved (i.e., binary).

### Tree balance statistics
Adapted from [Saulnier et al. 2027](https://doi.org/10.1371/journal.pcbi.1005416), [Colless 1982](https://doi.org/10.2307/2413420), [Sackin 1972](https://doi.org/10.1093/sysbio/21.2.225) 
and [Colijn et al. 2014](https://doi.org/10.1093/emph/eou018).

Implemented in [_treesumstats.balance_sumstats.BalanceFeatureCalculator_](treesumstats/balance_sumstats.py).

A _forest width_ is defined as the number of nodes that are at the same depth, 
and _node depth_ as the number of branches separating a node from its tree root [[Colijn et al. 2014]](https://doi.org/10.1093/emph/eou018).

To normalize balance and depth-related statistics we calculate them on the deepest (and at the same time most unbalanced) forest F_deep with the same numbers of tips (n_tips) and trees (n_trees). 
It contains a ladder tree with (n_tips - n_trees + 1) tips and (n_trees - 1) one-tip trees.

To normalize width-related statistics we calculate them on the widest forest F_wide with the same numbers of tips (n_tips) and trees (n_trees). 
It contains n_trees balanced trees with the total number of n_tips tips (distributed as equally as possible among the trees).

1. **colless:** sum (over internal nodes) of absolute differences of numbers of tips in their left and right subtrees [[Colless 1982]](https://doi.org/10.2307/2413420).
1. **colless_normalized:** colless value (see above), divided it by the colless value for F_deep: (n_tips - n_trees - 1) (n_tips - n_trees) / 2.
1. **sackin:** sum (over tips) of the number of internal nodes separating them from the root [[Sackin 1972]](https://doi.org/10.1093/sysbio/21.2.225).
1. **sackin_normalized:** sackin value (see above), divided it the sackin value for F_deep: (n_tips - n_trees) (n_tips - n_trees + 1) / 2 - 1.
1. **width_max:** maximum width.
1. **width_max_normalized:** maximum width, divided it by the maximum width of F_wide.
1. **depth_max:** maximum node depth.
1. **depth_max_normalized:** maximum node depth, divided it by the maximum node depth in F_deep: (n_tips - n_trees).
1. **width_depth_ratio:** maximum width to maximum depth ratio.
1. **width_depth_ratio_normalized:** maximum width to maximum depth ratio, divided it by this ratio for F_wide.
1. **width_delta:** maximum width difference between neighbouring depths.
1. **width_delta_normalized:** maximum width difference between neighbouring depths, divided it this value for F_wide whose last two layers were reorganised to increase the delta (tips at the last layer were grouped into one ladderized subtree).
1. **frac_inodes_in_ladder:** fraction of forest internal nodes that are resolved and have a tip descendant [[Colijn et al. 2014]](https://doi.org/10.1093/emph/eou018).
1. **n_inodes_in_ladder:** number of forest internal nodes that are resolved and have a tip descendant.
1. **len_ladder_max:** maximum number of connected internal nodes with a single tip descendant.
1. **len_ladder_max_normalized:** maximum number of connected internal nodes with a single tip descendant. We calculate it separately on each forest's tree and divide it by the number of tips in that tree. The maximum of these values is then reported.
1. **frac_inodes_imbalanced:** fraction of internal nodes that have different number of tips in their smallest and their largest child subtrees.
1. **n_inodes_imbalanced:** number of internal nodes that have different number of tips in their smallest and their largest child subtrees.
1. **imbalance_avg:** mean ratio of min-to-max subtree sizes over all internal nodes.

### Event time statistics
Implemented in [_treesumstats.event_time_sumstats.EventTimeFeatureCalculator_](treesumstats/event_time_sumstats.py).

1. **time_tip_mean:** average of the times of forest tips.
1. **time_tip_min:** minimum of the times of forest tips.
1. **time_tip_max:** maximum of the times of forest tips.
1. **time_tip_var:** variance of the times of forest tips.
1. **time_tip_median:** median of the times of forest tips.
1. **time_inode_mean:** average of the times of forest internal nodes.
1. **time_inode_min:** minimum of the times of forest internal nodes.
1. **time_inode_max:** maximum of the times of forest internal nodes.
1. **time_inode_var:** variance of the times of forest internal nodes.
1. **time_inode_median:** median of the times of forest internal nodes.
1. **time_tip_normalized_mean:** average of the times of forest tips, divided by the last tip's time.
1. **time_tip_normalized_min:** minimum of the times of forest tips, divided by the last tip's time.
1. **time_tip_normalized_max:** maximum of the times of forest tips, divided by the last tip's time.
1. **time_tip_normalized_var:** variance of the times of forest tips, divided by the last tip's time.
1. **time_tip_normalized_median:** median of the times of forest tips, divided by the last tip's time.
1. **time_inode_normalized_mean:** average of the times of forest internal nodes, divided by the last tip's time.
1. **time_inode_normalized_min:** minimum of the times of forest internal nodes, divided by the last tip's time.
1. **time_inode_normalized_max:** maximum of the times of forest internal nodes, divided by the last tip's time.
1. **time_inode_normalized_var:** variance of the times of forest internal nodes, divided by the last tip's time.
1. **time_inode_normalized_median:** median of the times of forest internal nodes, divided by the last tip's time.

### Branch length statistics
Adapted from [Saulnier et al. 2027](https://doi.org/10.1371/journal.pcbi.1005416).

Implemented in [_treesumstats.branch_sumstats.BranchFeatureCalculator_](treesumstats/branch_sumstats.py).

The following statistics include ones calculated on the full forest, but also those calculated on its top, middle or bottom parts. 
The total time between the earliest forest tree start (0) and the time of the last sampled tip (T) is split into three equal parts. 
For each part only the branches finishing within the corresponding time period are considered, 
and their start time is cut to the interval start time for the branches that started before.

1. **brlen_inode_mean:** average of branch lengths of the forest internal nodes.
1. **brlen_inode_median:** median of branch lengths of the forest internal nodes.
1. **brlen_inode_var:** variance of branch lengths of the forest internal nodes.
1. **brlen_tip_mean:** average of branch lengths of the forest tips.
1. **brlen_tip_median:** median of branch lengths of the forest tips.
1. **brlen_tip_var:** variance of branch lengths of the forest tips.
1. **brlen_inode_top_mean:** average of branch lengths of the forest's top internal nodes. 
1. **brlen_inode_top_median:** median of branch lengths of the forest's top internal nodes.
1. **brlen_inode_top_var:** variance of branch lengths of the forest's top internal nodes.
1. **brlen_tip_top_mean:** average of branch lengths of the forest's top tips.
1. **brlen_tip_top_median:** median of branch lengths of the forest's top tips. 
1. **brlen_tip_top_var:** variance of branch lengths of the forest's top tips.
1. **brlen_inode_middle_mean:** average of branch lengths of the forest's middle internal nodes.
1. **brlen_inode_middle_median:** median of branch lengths of the forest's middle internal nodes.
1. **brlen_inode_middle_var:** variance of branch lengths of the forest's middle internal nodes.
1. **brlen_tip_middle_mean:** average of branch lengths of the forest's middle tips.
1. **brlen_tip_middle_median:** median of branch lengths of the forest's middle tips.
1. **brlen_tip_middle_var:** variance of branch lengths of the forest's middle tips.
1. **brlen_inode_bottom_mean:** average of branch lengths of the forest's bottom internal nodes.
1. **brlen_inode_bottom_median:** median of branch lengths of the forest's bottom internal nodes.
1. **brlen_inode_bottom_var:** variance of branch lengths of the forest's bottom internal nodes.
1. **brlen_tip_bottom_mean:** average of branch lengths of the forest's bottom tips.
1. **brlen_tip_bottom_median:** median of branch lengths of the forest's bottom tips.
1. **brlen_tip_bottom_var:** variance of branch lengths of the forest's bottom tips.
1. **frac_brlen_inode_mean_by_brlen_tip_mean:** fraction of two values. The dividend is average of branch lengths of the forest internal nodes. The divisor is average of branch lengths of the forest tips.
1. **frac_brlen_inode_median_by_brlen_tip_median:** fraction of two values. The dividend is median of branch lengths of the forest internal nodes. The divisor is median of branch lengths of the forest tips.
1. **frac_brlen_inode_var_by_brlen_tip_var:** fraction of two values. The dividend is variance of branch lengths of the forest internal nodes. The divisor is variance of branch lengths of the forest tips.
1. **frac_brlen_inode_top_mean_by_brlen_tip_top_mean:** fraction of two values. The dividend is average of branch lengths of the forest's top internal nodes. The divisor is average of branch lengths of the forest's top tips.
1. **frac_brlen_inode_top_median_by_brlen_tip_top_median:** fraction of two values. The dividend is median of branch lengths of the forest's top internal nodes. The divisor is median of branch lengths of the forest's top tips.
1. **frac_brlen_inode_top_var_by_brlen_tip_top_var:** fraction of two values. The dividend is variance of branch lengths of the forest's top internal nodes. The divisor is variance of branch lengths of the forest's top tips.
1. **frac_brlen_inode_middle_mean_by_brlen_tip_middle_mean:** fraction of two values. The dividend is average of branch lengths of the forest's middle internal nodes. The divisor is average of branch lengths of the forest's middle tips.
1. **frac_brlen_inode_middle_median_by_brlen_tip_middle_median:** fraction of two values. The dividend is median of branch lengths of the forest's middle internal nodes. The divisor is median of branch lengths of the forest's middle tips.
1. **frac_brlen_inode_middle_var_by_brlen_tip_middle_var:** fraction of two values. The dividend is variance of branch lengths of the forest's middle internal nodes. The divisor is variance of branch lengths of the forest's middle tips.
1. **frac_brlen_inode_bottom_mean_by_brlen_tip_bottom_mean:** fraction of two values. The dividend is average of branch lengths of the forest's bottom internal nodes. The divisor is average of branch lengths of the forest's bottom tips.
1. **frac_brlen_inode_bottom_median_by_brlen_tip_bottom_median:** fraction of two values. The dividend is median of branch lengths of the forest's bottom internal nodes. The divisor is median of branch lengths of the forest's bottom tips.
1. **frac_brlen_inode_bottom_var_by_brlen_tip_bottom_var:** fraction of two values. The dividend is variance of branch lengths of the forest's bottom internal nodes. The divisor is variance of branch lengths of the forest's bottom tips.


### Transmission chain statistics

Adapted from [Voznica et al. 2022](https://doi.org/10.1038/s41467-022-31511-0). 


Implemented in [_treesumstats.transmission_chain_sumstats.TransmissionChainFeatureCalculator_](treesumstats/transmission_chain_sumstats.py).

A _k-node transmission chain_ of node i is the shortest k-branch path descending from i. 
By default k=4, but can be adjusted by setting an argument of _treesumstats.TransmissionChainFeatureCalculator(chain_len=4)_.

4. **n_4-chain:** number of 4-node transmission chains. 
1. **n_4-chain_normalized:** number of 4-node transmission chains, divided by the number of internal nodes.
1. **brlen_sum_4-chain_mean:** average of branch length sums of all 4-node transmission chains.
1. **brlen_sum_4-chain_min:** minimum of branch length sums of all 4-node transmission chains.
1. **brlen_sum_4-chain_max:** maximum of branch length sums of all 4-node transmission chains.
1. **brlen_sum_4-chain_var:** variance of branch length sums of all 4-node transmission chains.
1. **brlen_sum_4-chain_median:** median of branch length sums of all 4-node transmission chains.

11-18. **brlen_sum_4-chain_percN:** Nth percentile (where N can be 10, 20, 30, 40, 60, 70, 80 or 90) of branch length sums of all 4-node transmission chains.


### Lineage-Through-Time (LTT) statistics
Adapted from [Saulnier et al. 2027](https://doi.org/10.1371/journal.pcbi.1005416).


Implemented in [_treesumstats.ltt_sumstats.LTTFeatureCalculator_](treesumstats/ltt_sumstats.py).

In the following metrics times t_i (0 ≤ i ≤ 20) are equally distributed between the time of the start of the first tree (t_0 = 0) in the forest and the time of the forest’s last sampled tip (t_20=T). 
The number of such times (by default 20) can be adjusted by setting the argument of _treesumstats.LTTFeatureCalculator(n_coordinates=20)_.

Some of the following statistics are calculated on the top, middle or bottom part of the forest: 
The total time between the earliest forest tree start (0) and the time of the last sampled tip (T) is split into three equal parts. 
The top part includes times <= T/3, the middle one > T/3 and <= 2T/3, the bottom part > 2T/3.


1-20. **ltt_timeN:** T - t_N, where N can be 0, 1, ..., or 19.

21-40. **ltt_treesN:** number of trees present at t_N, where N can be 0, 1, ..., or 19.

41-60. **ltt_lineagesN:** number of lineages present at t_N, where N can be 0, 1, ..., or 19.

61-80. **ltt_lineagesN_normalized:** number of lineages present at t_N (where N can be 0, 1, ..., or 19), divided by the total number of tips in the forest.

81. **time_trees_max:** T - t_tmax, where t_tmax is the time when the maximum number of trees was first achieved.
1. **time_trees_max_top:** T - t_tmax, where t_tmax is the time when the maximum number of trees was first achieved in the top part of the forest.
1. **time_trees_max_middle:** T - t_tmax, where t_tmax is the time when the maximum number of trees was first achieved in the middle part of the forest.
1. **time_trees_max_bottom:** T - t_tmax, where t_tmax is the time when the maximum number of trees was first achieved in the bottom part of the forest.
1. **trees_max:** maximum number of trees.
1. **trees_max_top:** maximum number of trees in the top part of the forest.
1. **trees_max_middle:** maximum number of trees in the middle part of the forest.
1. **trees_max_bottom:** maximum number of trees in the bottom part of the forest.
1. **time_lineages_max:** T - t_lmax, where t_lmax is the time when the maximum number of lineages was first achieved.
1. **time_lineages_max_top:** T - t_lmax, where t_lmax is the time when the maximum number of lineages was first achieved in the top part of the forest.
1. **time_lineages_max_middle:** T - t_lmax, where t_lmax is the time when the maximum number of lineages was first achieved in the middle part of the forest.
1. **time_lineages_max_bottom:** T - t_lmax, where t_lmax is the time when the maximum number of lineages was first achieved in the bottom part of the forest.
1. **lineages_max:** maximum number of lineages.
1. **lineages_max_top:** maximum number of lineages in the top part of the forest.
1. **lineages_max_middle:** maximum number of lineages in the middle part of the forest.
1. **lineages_max_bottom:** maximum number of lineages in the bottom part of the forest.
1. **lineages_max_normalized:** maximum number of lineages, divided by the total number of tips in the forest.
1. **lineages_max_top_normalized:** maximum number of lineages in the top part of the forest, divided by the total number of tips in the forest.
1. **lineages_max_middle_normalized:** maximum number of lineages in the middle part of the forest, divided by the total number of tips in the forest.
1. **lineages_max_bottom_normalized:** maximum number of lineages in the bottom part of the forest, divided by the total number of tips in the forest.
1. **lineage_start_to_max_slope:** linear slope between the lineages at the first tree start and t_lmax, where t_lmax is the time when the maximum number of lineages was first achieved.
1. **lineage_stop_to_max_slope:** linear slope between the lineages at the t_lmax and T, where t_lmax is the time when the maximum number of lineages was first achieved.
1. **lineage_slope_ratio:** ratio between the linear slope between the lineages at the first tree start and t_lmax, and the linear slope between the lineages at the t_lmax and T, where t_lmax is the time when the maximum number of lineages was first achieved.
1. **lineage_start_to_max_slope_top:** linear slope between the lineages at the first tree start and t_lmax, where t_lmax is the time when the maximum number of lineages was first achieved in the top part of the forest.
1. **lineage_stop_to_max_slope_top:** linear slope between the lineages at the t_lmax and T/3, where t_lmax is the time when the maximum number of lineages was first achieved in the top part of the forest.
1. **lineage_slope_ratio_top:** ratio between the linear slope between the lineages at the first tree start and t_lmax, and the linear slope between the lineages at the t_lmax and T/3, where t_lmax is the time when the maximum number of lineages was first achieved in the top part of the forest.
1. **lineage_start_to_max_slope_middle:** linear slope between the lineages at the T/3 and t_lmax, where t_lmax is the time when the maximum number of lineages was first achieved in the middle part of the forest.
1. **lineage_stop_to_max_slope_middle:** linear slope between the lineages at the t_lmax and 2T/3, where t_lmax is the time when the maximum number of lineages was first achieved in the middle part of the forest.
1. **lineage_slope_ratio_middle:** ratio between the linear slope between the lineages at the T/3 and t_lmax, and the linear slope between the lineages at the t_lmax and 2T/3, where t_lmax is the time when the maximum number of lineages was first achieved in the middle part of the forest.
1. **lineage_start_to_max_slope_bottom:** linear slope between the lineages at the 2T/3 and t_lmax, where t_lmax is the time when the maximum number of lineages was first achieved in the bottom part of the forest.
1. **lineage_stop_to_max_slope_bottom:** linear slope between the lineages at the t_lmax and T, where t_lmax is the time when the maximum number of lineages was first achieved in the bottom part of the forest.
1. **lineage_slope_ratio_bottom:** ratio between the linear slope between the lineages at the 2T/3 and t_lmax, and the linear slope between the lineages at the t_lmax and T, where t_lmax is the time when the maximum number of lineages was first achieved in the bottom part of the forest.
1. **lineage_start_to_max_slope_normalized:** linear slope between the lineages at the first tree start and t_lmax, where t_lmax is the time when the maximum number of lineages was first achieved. This slope is divided by the total number of tips in the forest.
1. **lineage_stop_to_max_slope_normalized:** linear slope between the lineages at the t_lmax and T, where t_lmax is the time when the maximum number of lineages was first achieved. This slope is divided by the total number of tips in the forest.
1. **lineage_start_to_max_slope_top_normalized:** linear slope between the lineages at the first tree start and t_lmax, where t_lmax is the time when the maximum number of lineages was first achieved in the top part of the forest. This slope is divided by the total number of tips in the forest.
1. **lineage_stop_to_max_slope_top_normalized:** linear slope between the lineages at the t_lmax and T/3, where t_lmax is the time when the maximum number of lineages was first achieved in the top part of the forest. This slope is divided by the total number of tips in the forest.
1. **lineage_start_to_max_slope_middle_normalized:** linear slope between the lineages at the T/3 and t_lmax, where t_lmax is the time when the maximum number of lineages was first achieved in the middle part of the forest. This slope is divided by the total number of tips in the forest.
1. **lineage_stop_to_max_slope_middle_normalized:** linear slope between the lineages at the t_lmax and 2T/3, where t_lmax is the time when the maximum number of lineages was first achieved in the middle part of the forest. This slope is divided by the total number of tips in the forest.
1. **lineage_start_to_max_slope_bottom_normalized:** linear slope between the lineages at the 2T/3 and t_lmax, where t_lmax is the time when the maximum number of lineages was first achieved in the bottom part of the forest. This slope is divided by the total number of tips in the forest.
1. **lineage_stop_to_max_slope_bottom_normalized:** linear slope between the lineages at the t_lmax and T, where t_lmax is the time when the maximum number of lineages was first achieved in the bottom part of the forest. This slope is divided by the total number of tips in the forest.

### Tree topology statistics
Implemented in [_treesumstats.subtree_sumstats.SubtreeFeatureCalculator_](treesumstats/subtree_sumstats.py).

In some of the following statistics reshuffled subtrees are mentioned. 
To construct a _reshuffled  subtree_ of a certain kind (cherry, triplet, etc.) from a real one we keep one of its (randomly chosen) locally (with respect to the subtree) external node, 
while for each other locally external node from the real subtree we replace it with a node of globally (with respect to the forest) the same type (external or internal), for which:
    (i) the time at the beginning of its branch is as close as possible to the time at the beginning of the real node's branch, 
    (ii) while all the locally external nodes in the reshuffled  subtree are different and 
    (iii) there are no two locally external nodes in the reshuffled  subtree that used to belong to the same real subtree of this kind 
    (unless there were not enough tips, e.g., 8 tips in total and only 2 ladderized quartets in the forest).

We consider the following 2-tip, 3-tip and 4-tip subtrees to calculate the summary statistics:
* 2: cherry
* 3U: unresolved triplet (3-tip subtree)
* 3L: resolved (ladderized) triplet
* 4U: fully unresolved quartet (4-tip subtree)
* 4U3U1: partially unresolved quartet with an unresolved triplet and a tip as children
* 4U211: partially unresolved quartet with a cherry and two tips as children
* 4L: fully resolved ladderized quartet
* 4B: fully resolved balanced quartet (with two cherries as children)

We also consider fully internal-node subtrees:
* I: fully unresolved subtree (or size 2 or more) whose locally external nodes are globally internal sibling nodes.

In the following statistics (spanning several list positions) XT must be replaced by one of the following values: 2, 3U, 3L, 4U, 4U3U1, 4U211, 4L or 4B, while X must be replaced by either I or one of the XT values.

1-8. **frac_tips_in_XT:** fraction of forest tips that are found in subtrees of type XT.
9. **frac_tips_in_O:** fraction of forest tips that are not part of any subtree of size 2, 3 or 4.

10-17. **n_tips_in_XT:** number of forest tips that are found in subtrees of type XT.
18. **n_tips_in_O:** number of forest tips that are not part of any subtree of size 2, 3 or 4.
19. **frac_inodes_with_sibling_inodes:** fraction of forest non-root internal nodes that have internal siblings.
20. **frac_inodes_without_sibling_inodes:** fraction of forest non-root internal nodes that do not have internal siblings.
19. **n_inodes_with_sibling_inodes:** number of forest non-root internal nodes that have internal siblings.
20. **n_inodes_without_sibling_inodes:** number of forest non-root internal nodes that do not have internal siblings.

21-29. **time_diff_in_X_real_mean:** mean among all subtrees of type X in the forest, of average of all locally external node pair sampling time differences in the subtree.

30-38. **time_diff_in_X_real_min:** minimum among all subtrees of type X in the forest, of average of all locally external node pair sampling time differences in the subtree.

39-47. **time_diff_in_X_real_max:** maximum among all subtrees of type X in the forest, of average of all locally external node pair sampling time differences in the subtree.

48-56. **time_diff_in_X_real_var:** variance among all subtrees of type X in the forest, of average of all locally external node pair sampling time differences in the subtree.

57-65. **time_diff_in_X_real_median:** median among all subtrees of type X in the forest, of average of all locally external node pair sampling time differences in the subtree.

66-74. **time_diff_in_X_random_mean:** mean among all reshuffled subtrees of type X in the forest, of average of all locally external node pair sampling time differences in the subtree.

75-83. **time_diff_in_X_random_min:** minimum among all reshuffled subtrees of type X in the forest, of average of all locally external node pair sampling time differences in the subtree.

84-93. **time_diff_in_X_random_max:** maximum among all reshuffled subtrees of type X in the forest, of average of all locally external node pair sampling time differences in the subtree.

94-103. **time_diff_in_X_random_var:** variance among all reshuffled subtrees of type X in the forest, of average of all locally external node pair sampling time differences in the subtree.

104-112. **time_diff_in_X_random_median:** median among all reshuffled subtrees of type X in the forest, of average of all locally external node pair sampling time differences in the subtree.

113-184. **time_diff_in_X_real_percN:** Nth percentile (where N can be 1, 5, 10, 25, 75, 90, 95 or 99) among all subtrees of type X in the forest, of average of all locally external node pair sampling time differences in the subtree.

184-255. **time_diff_in_X_random_percN:** Nth percentile (where N can be 1, 5, 10, 25, 75, 90, 95 or 99) among all reshuffled subtrees of type X in the forest, of average of all locally external node pair sampling time differences in the subtree.

256-264. **time_diff_in_X_random_vs_real_n_less:** number of subtrees of type X whose average locally external node sampling time differences is smaller in real subtrees than in the corresponding reshuffled  ones. 

265-273. **time_diff_in_X_random_vs_real_n_more:** number of subtrees of type X whose average locally external node sampling time differences is larger in real subtrees than in the corresponding reshuffled  ones. 

274-282. **time_diff_in_X_random_vs_real_frac_less:** fraction of subtrees of type X whose average locally external node sampling time differences is smaller in real subtrees than in the corresponding reshuffled  ones. 

283-291. **time_diff_in_X_random_vs_real_frac_more:** fraction of subtrees of type X whose average locally external node sampling time differences is larger in real subtrees than in the corresponding reshuffled  ones. 

292-301. **time_diff_in_X_random_vs_real_pval_less:** p-value of the sign test checking that for subtrees of type X, their average locally external node sampling time differences are indistinguishable in real subtrees and in the corresponding reshuffled  ones (the alternative hypothesis is that some real ones are smaller). 

302-310. **time_diff_in_X_random_vs_real_pval_more:** p-value of the sign test checking that for subtrees of type X, their average locally external node sampling time differences are indistinguishable in real subtrees and in the corresponding reshuffled  ones (the alternative hypothesis is that some real ones are larger). 


## Input data
One needs to supply a time-scaled phylogenetic tree in newick format. 
If the file contains several trees (one tree per line), it will be considered as a forest.

## Installation and run

There are 4 alternative ways to run __treesumstats__ on your computer: 
with [docker](https://www.docker.com/community-edition), 
[apptainer](https://apptainer.org/),
in Python3, or via command line (requires installation with Python3).



### Install and run in python3 or command-line (for linux systems, recommended Ubuntu 21 or newer versions)

You could either install python (version 3.9 or higher) system-wide and then install treesumstats via pip:
```bash
sudo apt install -y python3 python3-pip python3-setuptools python3-distutils
pip3 install treesumstats
```

or alternatively, you could install python (version 3.9 or higher) and treesumstats via [conda](https://conda.io/docs/) (make sure that conda is installed first). 
Here we will create a conda environment called _phyloenv_:
```bash
conda create --name phyloenv python=3.9
conda activate phyloenv
pip install treesumstats
```


#### Basic usage in a command line
If you installed __treesumstats__ in a conda environment (here named _phyloenv_), do not forget to first activate it, e.g.

```bash
conda activate phyloenv
```

Run the following command to calculate the summary statistics for an input tree _tree.nwk_ and save them to an output tab-delimited file _stats.tab_. 
(The non-mandatory option _--add_descriptions_ would add a column with statistics descriptions to the output table.)

```bash
treesumstats_encode --nwk tree.nwk --tab stats.tab --add_descriptions
```

#### Help

To see detailed options, run:
```bash
treesumstats_encode --help
```


### Run with docker

#### Basic usage
Once [docker](https://www.docker.com/community-edition) is installed, 

run the following command to calculate the summary statistics for an input tree _tree.nwk_ and save them to an output tab-delimited file _stats.tab_. 
(The non-mandatory option _--add_descriptions_ would add a column with statistics descriptions to the output table.)


```bash
docker run -v <path_to_the_folder_containing_the_tree>:/data:rw -t evolbioinfo/treesumstats --nwk /data/tree.nwk --tab /data/stats.tab --add_descriptions
```


This will produce a tab-delimited file _stats.tab_ in the <path_to_the_folder_containing_the_tree> folder,

 containing the summary statistic names in the _statistic_ column, their values in the _value_ column and their descriptions in the _description_ column. 

#### Help

To see advanced options, run
```bash
docker run -t evolbioinfo/treesumstats -h
```



### Run with apptainer

#### Basic usage
Once [apptainer](https://apptainer.org/docs/user/latest/quick_start.html#installation) is installed, 

run the following command to calculate the summary statistics for an input tree _tree.nwk_ and save them to an output tab-delimited file _stats.tab_. 
(The non-mandatory option _--add_descriptions_ would add a column with statistics descriptions to the output table.)


```bash
apptainer run docker://evolbioinfo/treesumstats --nwk tree.nwk --tab stats.tab --add_descriptions
```


This will produce a tab-delimited file _stats.tab_,

 containing the summary statistic names in the _statistic_ column, their values in the _value_ column and their descriptions in the _description_ column. 


#### Help

To see advanced options, run
```bash
apptainer run docker://evolbioinfo/treesumstats -h
```


## How to add your own summary statistics

To add your own summary statistics, your need to first of all 
implement a subclass of an abstract class [summarystatics.FeatureCalculator](treesumstats),
as in the example below, which calculates 2 summary statistics: 'example_feature_1' and 'example_feature_2'.

```python3
from treesumstats import FeatureCalculator


class ExampleFeatureCalculator(FeatureCalculator):
    """Computes summary statistics based on ..."""

    def __init__(self):
        self._forest = None

    def feature_names(self):
        """Returns a list of names of summary statistics that this class can calculate."""
        
        return ['example_feature_1', 'example_feature_2']

    def set_forest(self, forest, **kwargs):
        self._forest = forest

    def calculate(self, feature_name, **kwargs):
        if 'example_feature_1' == feature_name:
            # your code to calculate this summary statistic value on the forest self._forest
            # should go here
            return 1
        if 'example_feature_2' == feature_name:
            # your code to calculate this summary statistic value on the forest self._forest
            # should go here
            return 2
        return None

    def help(self, feature_name, *args, **kwargs):
        """Returns a description of the summary statistic whose name is given as the argument."""
        if 'example_feature_1' == feature_name:
            return 'summary statistic that is equal to 1 for any forest.'
        if 'example_feature_2' == feature_name:
            return 'summary statistic that is equal to 2 for any forest.'
        return None 
```

Then, you need to register it in the [treesumstats.FeatureRegistry](treesumstats), 
potentially with other pertinent statistic calculators:

```python3
from treesumstats import FeatureManager
from treesumstats.tree_manager import read_forest
from treesumstats import FeatureRegistry

FeatureRegistry.register(ExampleFeatureCalculator())

# below we will also register all existing statistic calculators
from treesumstats.basic_sumstats import BasicFeatureCalculator
from treesumstats.branch_sumstats import BranchFeatureCalculator
from treesumstats.event_time_sumstats import EventTimeFeatureCalculator
from treesumstats.ltt_sumstats import LTTFeatureCalculator
from treesumstats.resolution_sumstats import ResolutionFeatureCalculator
from treesumstats.subtree_sumstats import SubtreeFeatureCalculator
from treesumstats.balance_sumstats import BalanceFeatureCalculator
from treesumstats.transmission_chain_sumstats import TransmissionChainFeatureCalculator

FeatureRegistry.register(BasicFeatureCalculator())
FeatureRegistry.register(ResolutionFeatureCalculator())
FeatureRegistry.register(BalanceFeatureCalculator())
FeatureRegistry.register(EventTimeFeatureCalculator())
FeatureRegistry.register(BranchFeatureCalculator())
FeatureRegistry.register(TransmissionChainFeatureCalculator())
FeatureRegistry.register(LTTFeatureCalculator())
FeatureRegistry.register(SubtreeFeatureCalculator())
```

Once registered, you can use it to calculate statistics:

```python3
# make sure the FeatureManager now has our new statistics
assert 'example_feature_1' in FeatureManager.available_features()

forest = read_forest('tree.nwk')

# Compute all possible features on the input forest and print their values and descriptions to the standard output
for feature_name, value in zip(FeatureManager.available_features(), FeatureManager.compute_features(forest, *FeatureManager.available_features())):
    print(f'{feature_name}\t{value}{FeatureManager.help(feature_name)}')
```