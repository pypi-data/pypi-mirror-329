import re
from collections import namedtuple

import numpy as np

from treesumstats import FeatureCalculator, NORMALIZED, EPSILON
from treesumstats.tree_manager import annotate_forest_with_time, TIME

TREE_PARTS = ['top', 'middle', 'bottom']

N_LTT_COORDINATES = 20

LTT = namedtuple('LTT', ['times', 'lineages', 'trees'])

def get_ltt_plot(forest):
    """
    Returns a mapping of forest event times to
        the numbers of started-but-unfinished lineages,
        the numbers of started-but-unfinished trees,
    where the times correspond to events (internal or external nodes on the tree)
    and the tree start times (time at the beginning of the root branch).

    :param forest: list(ete3.Tree), forest of trees on which these metrics are computed.
        Its nodes must be annotated with their times (feature treesumstats.tree_manager.TIME)
    :return: named tuple LTT containing three numpy arrays: times, lineages, and trees
    """
    time_dlineages_dtrees = []

    for tree in forest:
        time_dlineages_dtrees.append((getattr(tree, TIME) - tree.dist, 1, 1))
        max_time = -np.inf
        for node in tree.traverse():
            # if is a tip it will give -1, if a binary internal node +1, etc.
            node_time = getattr(node, TIME)
            max_time = max(max_time, node_time)
            time_dlineages_dtrees.append((node_time, len(node.children) - 1, 0))
        time_dlineages_dtrees.append((max_time, 0, -1))


    times, lineages, trees = [], [], []

    cur_lineages, cur_trees = 0, 0
    for time, delta_lineages, delta_trees in sorted(time_dlineages_dtrees, key=lambda _: _[0]):
        cur_lineages += delta_lineages
        cur_trees += delta_trees
        # if there is no collision in times of two events, increase the array
        if not times or np.abs(time - times[-1]) > EPSILON:
            times.append(time)
            lineages.append(cur_lineages)
            trees.append(cur_trees)
        # else just update the last lineage count
        else:
            lineages[-1] = cur_lineages
            trees[-1] = cur_trees

    return LTT(times=np.array(times), lineages=np.array(lineages), trees=np.array(trees))


def normalize_lineages_by_total_tip_count(lineages, total_tip_counts):
    """Normalize lineages by total number of tips in the trees that correspond to each time point"""
    lineages = np.array(lineages, dtype=float)
    mask = total_tip_counts > 0
    lineages[mask] /= total_tip_counts[mask]
    return lineages


def get_ltt_coordinates(ltt, n_coordinates=N_LTT_COORDINATES):
    """
    Returns representation of LTT plot over 'n_coordinates' time intervals,
    distributed equally between the time of the first tree start and the time of the last sampled tip.
    We report the numbers of lineages/trees at the start of each interval,
    and do not end the last interval as it corresponds to the end of the sampling period and zero lineages/trees.

    :param ltt: input LTT plot (named tuple LTT)
    :param n_coordinates: number of coordinates to consider
    :return: output LTT plot (named tuple LTT) over 'n_coordinates' time intervals
    """
    start_time = ltt.times[0]
    end_time = ltt.times[-1]
    dt = (end_time - start_time) / n_coordinates

    # to make absolutely sure its size is n_coordinates + 1 and not (n_coordinates + 2) due to rounding we do [: _]
    xs = np.arange(start_time, end_time + dt, dt)[: (n_coordinates + 1)]
    ys = np.zeros(n_coordinates + 1, dtype=float)
    zs = np.zeros(n_coordinates + 1, dtype=float)
    prev_idx = 0
    for i in range(n_coordinates + 1):
        while prev_idx < len(ltt.times) - 1 and ltt.times[prev_idx + 1] <= xs[i]:
            prev_idx += 1
        ys[i] = ltt.lineages[prev_idx]
        zs[i] = ltt.trees[prev_idx]
    return LTT(times=xs[:-1], lineages=ys[:-1], trees=zs[:-1])


def filter_LTT_by_time(ltt, start_time=-np.inf, stop_time=np.inf):
    mask = (ltt.times >= start_time) & (ltt.times <= stop_time)
    filtered_times = ltt.times[mask]
    filtered_lineages = ltt.lineages[mask]
    filtered_trees = ltt.trees[mask]
    if not len(filtered_times) \
            or (filtered_times[0] > ltt.times[0] and start_time > ltt.times[0] and start_time not in ltt.times):
        prev_i = next(i for i in range(len(ltt.times)) if ltt.times[i + 1] > start_time)
        filtered_times = np.concat([[start_time], filtered_times])
        filtered_trees = np.concat([[ltt.trees[prev_i]], filtered_trees])
        filtered_lineages = np.concat([[ltt.lineages[prev_i]], filtered_lineages])
    if not len(filtered_times) \
            or (filtered_times[-1] < ltt.times[-1] and stop_time < ltt.times[-1] and stop_time not in ltt.times):
        filtered_times = np.concat([filtered_times, [stop_time]])
        filtered_trees = np.concat([filtered_trees, [filtered_trees[-1]]])
        filtered_lineages = np.concat([filtered_lineages, [filtered_lineages[-1]]])
    return LTT(times=filtered_times, lineages=filtered_lineages, trees=filtered_trees)


class LTTFeatureCalculator(FeatureCalculator):
    """Computes tree LTT-related summary statistics."""

    def __init__(self, n_coordinates=N_LTT_COORDINATES):
        self._n_coordinates = n_coordinates
        self._n_tips = None
        self._i_ml_top = None
        self._i_ml_middle = None
        self._i_ml_bottom = None
        self._max_time = None
        self._i_ml = None
        self._ltt = None
        self._forest = None
        self._ltt_bottom = None
        self._ltt_top = None
        self._ltt_middle = None
        self._ltt_coord = None

    def feature_names(self):
        return [f'ltt_time{i}' for i in range(self._n_coordinates)] \
            + [f'ltt_trees{i}' for i in range(self._n_coordinates)] \
            + [f'ltt_lineages{i}' for i in range(self._n_coordinates)] \
            + [f'ltt_lineages{i}_{NORMALIZED}' for i in range(self._n_coordinates)] \
            + ['time_trees_max'] + [f'time_trees_max_{part}' for part in TREE_PARTS] \
            + ['trees_max'] + [f'trees_max_{part}' for part in TREE_PARTS] \
            + ['time_lineages_max'] + [f'time_lineages_max_{part}' for part in TREE_PARTS] \
            + ['lineages_max'] + [f'lineages_max_{part}' for part in TREE_PARTS] \
            + [f'lineages_max_{NORMALIZED}'] + [f'lineages_max_{part}_{NORMALIZED}' for part in TREE_PARTS] \
            + ['lineage_start_to_max_slope', 'lineage_stop_to_max_slope', 'lineage_slope_ratio'] \
            + [f'{f}_{part}' for part in TREE_PARTS for f in ['lineage_start_to_max_slope', 'lineage_stop_to_max_slope', 'lineage_slope_ratio']] \
            + [f'lineage_start_to_max_slope_{NORMALIZED}', f'lineage_stop_to_max_slope_{NORMALIZED}'] \
            + [f'{f}_{part}_{NORMALIZED}' for part in TREE_PARTS for f in ['lineage_start_to_max_slope', 'lineage_stop_to_max_slope']]

    def set_forest(self, forest, **kwargs):
        self._forest = forest
        annotate_forest_with_time(self._forest)
        self._i_ml = None
        self._max_time = None
        self._ltt = None
        self._ltt_bottom = None
        self._ltt_top = None
        self._ltt_middle = None
        self._i_ml_top = None
        self._i_ml_middle = None
        self._i_ml_bottom = None
        self._n_tips = None
        self._ltt_coord = None

    @property
    def ltt(self):
        if self._ltt is None:
            self._ltt = get_ltt_plot(self._forest)
        return self._ltt

    @property
    def ltt_coord(self):
        if self._ltt_coord is None:
            self._ltt_coord = get_ltt_coordinates(self.ltt, n_coordinates=self._n_coordinates)
        return self._ltt_coord

    @property
    def ltt_top(self):
        if self._ltt_top is None:
            self._ltt_top = filter_LTT_by_time(self.ltt, stop_time=self.max_time / 3)
        return self._ltt_top

    @property
    def ltt_middle(self):
        if self._ltt_middle is None:
            self._ltt_middle = filter_LTT_by_time(self.ltt, start_time=self.max_time / 3, stop_time=2 * self.max_time / 3)
        return self._ltt_middle

    @property
    def ltt_bottom(self):
        if self._ltt_bottom is None:
            self._ltt_bottom = filter_LTT_by_time(self.ltt, start_time=2 * self.max_time / 3)
        return self._ltt_bottom

    @property
    def i_ml(self):
        if self._i_ml is None:
            self._i_ml = self.ltt.lineages.argmax()
        return self._i_ml

    @property
    def i_ml_top(self):
        if self._i_ml_top is None:
            self._i_ml_top = self.ltt_top.lineages.argmax()
        return self._i_ml_top

    @property
    def i_ml_middle(self):
        if self._i_ml_middle is None:
            self._i_ml_middle = self.ltt_middle.lineages.argmax()
        return self._i_ml_middle

    @property
    def i_ml_bottom(self):
        if self._i_ml_bottom is None:
            self._i_ml_bottom = self.ltt_bottom.lineages.argmax()
        return self._i_ml_bottom

    @property
    def max_time(self):
        if self._max_time is None:
            self._max_time = max(getattr(_, TIME) for tree in self._forest for _ in tree)
        return self._max_time


    @property
    def n_tips(self):
        if self._n_tips is None:
            self._n_tips = sum(len(tree) for tree in self._forest)
        return self._n_tips


    def calculate(self, feature_name, **kwargs):

        if feature_name.startswith('ltt'):
            coordinate = int(re.findall(r'\d+', feature_name)[0])
            if 'time' in feature_name:
                # Invert the time so that the end of the sampling period is at time 0
                return self.max_time - self.ltt_coord.times[coordinate]
            if 'trees' in feature_name:
                return self.ltt_coord.trees[coordinate]
            if 'lineages' in feature_name:
                denominator = self.n_tips if feature_name.endswith(NORMALIZED) else 1
                return self.ltt_coord.lineages[coordinate] / denominator
            return None

        part = 'top' if '_top' in feature_name \
            else ('middle' if '_middle' in feature_name else ('bottom' if '_bottom' in feature_name else ''))
        if part:
            feature_name = feature_name.replace(f'_{part}', '')
        ltt = self.ltt_top if 'top' == part \
                    else (self.ltt_middle if 'middle' == part \
                              else (self.ltt_bottom if 'bottom' == part else self.ltt))

        if 'time_trees_max' == feature_name:
            # Invert the time so that the end of the sampling period is at time 0
            return self.max_time - ltt.times[ltt.trees.argmax()]
        if 'trees_max' == feature_name:
            return ltt.trees.max()

        i_ml = self.i_ml_top if 'top' == part \
                    else (self.i_ml_middle if 'middle' == part \
                              else (self.i_ml_bottom if 'bottom' == part else self.i_ml))
        if 'time_lineages_max' == feature_name:
            # Invert the time so that the end of the sampling period is at time 0
            return self.max_time - ltt.times[i_ml]

        if 'lineage_slope_ratio' == feature_name:
            time_lin_max, lin_max = ltt.times[i_ml], ltt.lineages[i_ml]
            time_start, lin_start = ltt.times[0], ltt.lineages[0]
            time_stop, lin_stop = ltt.times[-1], ltt.lineages[-1]
            if time_lin_max == time_start == time_stop:
                return 1
            return (lin_max - lin_start) * (time_stop - time_lin_max) \
                / max((time_lin_max - time_start) * (lin_max - lin_stop), EPSILON)

        denominator = self.n_tips if feature_name.endswith(NORMALIZED) else 1
        if feature_name.startswith('lineages_max'):
            return ltt.lineages[i_ml] / denominator

        time_lin_max, lin_max = ltt.times[i_ml], ltt.lineages[i_ml]
        if feature_name.startswith('lineage_start_to_max_slope'):
            time_start, lin_start = ltt.times[0], ltt.lineages[0]
            return (lin_max - lin_start) / max(time_lin_max - time_start, EPSILON) / denominator
        if feature_name.startswith('lineage_stop_to_max_slope'):
            time_stop, lin_stop = ltt.times[-1], ltt.lineages[-1]
            return (lin_max - lin_stop) / max(time_stop - time_lin_max, EPSILON) / denominator

        return None




    def help(self, feature_name, *args, **kwargs):
        if feature_name.startswith('ltt'):
            coordinate = int(re.findall(r'\d+', feature_name)[0])
            explanation = f", where times t_i (0 ≤ i ≤ {self._n_coordinates}) are equally distributed between " \
                          f"the time of the start of the first tree (t_0 = 0) in the forest and " \
                          f"the time of the forest’s last sampled tip (t_{self._n_coordinates}=T)."
            if 'time' in feature_name:
                # Invert the time so that the end of the sampling period is at time 0
                return f"T - t_{coordinate}{explanation}"
            if 'trees' in feature_name:
                return f"number of trees present at t_{coordinate}{explanation}"
            if 'lineages' in feature_name:
                return f'number of lineages present at t_{coordinate}' \
                       f'{' divided by the total number of tips in the forest' if feature_name.endswith(NORMALIZED) else ''}' \
                       f'{explanation}'
            return None

        part = 'top' if '_top' in feature_name \
            else ('middle' if '_middle' in feature_name else ('bottom' if '_bottom' in feature_name else ''))
        explanation = ''
        if part:
            feature_name = feature_name.replace(f'_{part}', '')
            start_time = "the first tree start" if "top" == part else f"{'2' if 'bottom' == part else ''}T/3"
            end_time = "T" if "bottom" == part else f"{'2' if 'middle' == part else ''}T/3"
            explanation = f" in the {part} part of the forest: between {start_time} and {end_time}"
        else:
            start_time = "first tree start"
            end_time = "T"

        if 'time_trees_max' == feature_name:
            return f"T - t_tmax, where T is the sampling time of the last forest's tip " \
                   f"and t_tmax is the time when the maximum number of trees was first achieved{explanation}."
        if 'trees_max' == feature_name:
            return f"maximum number of trees{explanation}."

        if 'time_lineages_max' == feature_name:
            return f"T - t_lmax, where T is the sampling time of the last forest's tip " \
                   f"and t_lmax is the time when the maximum number of lineages was first achieved{explanation}."
        if feature_name.startswith('lineages_max'):
            return f"maximum number of lineages" \
                   f"{explanation}" \
                   f"{', divided by the total number of tips in the forest' if feature_name.endswith(NORMALIZED) else ''}."
        long_exp = f", where t_lmax is the time when the maximum number of lineages was first achieved{explanation}, " \
                   "where T is the sampling time of the last forest's tip."
        if feature_name.startswith('lineage_start_to_max_slope'):
            res = f"linear slope between the lineages at the {start_time} and t_lmax{long_exp}"
            if feature_name.endswith(NORMALIZED):
                res += " This slope is divided by the total number of tips in the forest."
            return res
        if feature_name.startswith('lineage_stop_to_max_slope'):
            res = f"linear slope between the lineages at the t_lmax and {end_time}{long_exp}"
            if feature_name.endswith(NORMALIZED):
                res += " This slope is divided by the total number of tips in the forest."
            return res
        if 'lineage_slope_ratio' == feature_name:
            return f"ratio between the linear slope between the lineages at the {start_time} and t_lmax, " \
                   f"and the linear slope between the lineages at the t_lmax and {end_time}{long_exp}"
        return None