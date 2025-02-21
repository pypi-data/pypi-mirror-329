from treesumstats import FeatureRegistry, FeatureManager
from treesumstats.basic_sumstats import BasicFeatureCalculator
from treesumstats.branch_sumstats import BranchFeatureCalculator
from treesumstats.event_time_sumstats import EventTimeFeatureCalculator
from treesumstats.ltt_sumstats import LTTFeatureCalculator
from treesumstats.resolution_sumstats import ResolutionFeatureCalculator
from treesumstats.subtree_sumstats import SubtreeFeatureCalculator
from treesumstats.balance_sumstats import BalanceFeatureCalculator
from treesumstats.transmission_chain_sumstats import TransmissionChainFeatureCalculator
from treesumstats.tree_manager import read_forest

FeatureRegistry.register(BasicFeatureCalculator())
FeatureRegistry.register(ResolutionFeatureCalculator())
FeatureRegistry.register(BalanceFeatureCalculator())
FeatureRegistry.register(EventTimeFeatureCalculator())
FeatureRegistry.register(BranchFeatureCalculator())
FeatureRegistry.register(TransmissionChainFeatureCalculator())
FeatureRegistry.register(LTTFeatureCalculator())
FeatureRegistry.register(SubtreeFeatureCalculator())


def format_value(value):
    try:
        value = float(value)
        if int(value) == value:
            return f'{value:.0f}'
        if value > 1e-6:
            return f'{value:.6f}'
        return f'{value:.g}'
    except:
        return value


def main():
    """
    Entry point for tree encoding with command-line arguments.
    :return: void
    """
    import argparse

    parser = argparse.ArgumentParser(description="Calculate summary statistics for an input tree/forest.")
    parser.add_argument('--nwk', type=str, required=True, help="input tree/forest files in newick format")
    parser.add_argument('--tab', type=str, required=True,
                        help="output summary statistic table, in tab-delimited format: "
                             "the first column will contain summary statistic name, and the second its value.")
    parser.add_argument('--statistics', type=str, nargs='*',
                        help='an optional list of summary statistics that should be calculated. '
                             'If not given, all the available statistics will be calculated.')
    parser.add_argument('--add_descriptions', action='store_true',
                        help='whether to add a column "description" with the description of each calculated statistic.')
    params = parser.parse_args()

    forest = read_forest(params.nwk)
    features = params.statistics if params.statistics else FeatureManager.available_features()
    with open(params.tab, 'w+') as f:
        f.write(f'statistic\tvalue{'\tdescription' if params.add_descriptions else ''}\n')
        for feature_name, value in zip(features, FeatureManager.compute_features(forest, *features)):
            f.write(f'{feature_name}\t{format_value(value)}{f"\t{FeatureManager.help(feature_name)}" if params.add_descriptions else ""}\n')


if '__main__' == __name__:
    main()