import re

import numpy as np

from treesumstats import BASIC_METRIC2HELP, BASIC_ARRAY_METRICS, BASIC_METRIC2FUN, FeatureCalculator, NORMALIZED

CHAIN_LEN = 4

CHAIN = 'chain'

CHAIN_PERCENTILES = [p for p in range(10, 91, 10) if 50 != p]


class TransmissionChainFeatureCalculator(FeatureCalculator):
    """Computes tree transmission chain-related summary statistics."""

    def __init__(self, chain_len=CHAIN_LEN, percentiles=CHAIN_PERCENTILES):
        self._n_inodes = None
        self._chains = None
        self._chain_len = chain_len
        self._percentiles = percentiles
        self._forest = None

    def feature_names(self):
        return [f'n_{self._chain_len}-{CHAIN}', f'n_{self._chain_len}-{CHAIN}_{NORMALIZED}'] \
            + [f'brlen_sum_{self._chain_len}-{CHAIN}_{flavour}' for flavour in BASIC_ARRAY_METRICS]\
            + [f'brlen_sum_{self._chain_len}-{CHAIN}_perc{p}' for p in self._percentiles]

    def set_forest(self, forest, **kwargs):
        self._forest = forest
        self._chains = None
        self._n_inodes = None

    @property
    def chains(self):
        if self._chains is None:
            self._chains = []

            for tree in self._forest:
                for n in tree.traverse('postorder'):
                    for i in range(1, self._chain_len + 1):
                        feature = f'chain{i}'
                        if i == 1:
                            cur_chain = min([c.dist for c in n.children], default=np.inf)
                        else:
                            prev_feature = f'chain{i - 1}'
                            cur_chain = min([c.dist + getattr(c, prev_feature) for c in n.children], default=np.inf)
                            for c in n.children:
                                delattr(c, prev_feature)

                        if i == self._chain_len:
                            if cur_chain < np.inf:
                                self._chains.append(cur_chain)
                        elif not n.is_root():
                            n.add_feature(feature, cur_chain)

            self._chains = np.array(self._chains)
        return self._chains

    @property
    def n_inodes(self):
        if self._n_inodes is None:
            self._n_inodes = sum(1 for tree in self._forest for n in tree.traverse() if not n.is_leaf())
        return self._n_inodes

    def calculate(self, feature_name, **kwargs):
        if feature_name.startswith(f'n_{self._chain_len}-{CHAIN}'):
            denominator = self.n_inodes if feature_name.endswith(NORMALIZED) else 1
            return len(self.chains) / denominator
        if feature_name.startswith(f'brlen_sum_{self._chain_len}-{CHAIN}'):
            if 0 == len(self.chains):
                return 0
            flavour = feature_name.split('_')[-1]
            if flavour in BASIC_METRIC2FUN:
                return BASIC_METRIC2FUN[flavour](self.chains)
            elif 'perc' in flavour:
                perc = int(re.findall(r'\d+', flavour)[0])
                return np.percentile(self.chains, perc)
        return None

    def help(self, feature_name, *args, **kwargs):
        if feature_name.startswith(f'n_{self._chain_len}-{CHAIN}'):
            return f'number of {self._chain_len}-node transmission chains'\
                   f'{', divided by the number of internal nodes' if NORMALIZED in feature_name else ''}. ' \
                   f'(A {self._chain_len}-node transmission chain of node i is the shortest {self._chain_len}-branch path descending from i [Voznica et al. 2022].)'
        if feature_name.startswith(f'brlen_sum_{self._chain_len}-{CHAIN}'):
            flavour = feature_name.split('_')[-1]
            if flavour in BASIC_METRIC2FUN:
                return f'{BASIC_METRIC2HELP[flavour]} of branch length sums of all {self._chain_len}-node transmission chains. ' \
                   f'(A {self._chain_len}-node transmission chain of node i is the shortest {self._chain_len}-branch path descending from i [Voznica et al. 2022].)'
            elif 'perc' in flavour:
                perc = re.findall(r'\d+', flavour)[0]
                return f'{perc}th percentile of branch length sums of all {self._chain_len}-node transmission chains. ' \
                       f'(A {self._chain_len}-node transmission chain of node i is the shortest {self._chain_len}-branch path descending from i [Voznica et al. 2022].)'
        return None