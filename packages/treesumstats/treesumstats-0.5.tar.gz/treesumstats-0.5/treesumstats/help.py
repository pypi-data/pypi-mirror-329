from treesumstats import FeatureRegistry, FeatureManager
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



def main():
    """
    Entry point for summary statistic description.
    :return: void
    """
    import argparse

    parser = argparse.ArgumentParser(description="Prints available summary statistics and their descriptions.")
    params = parser.parse_args()

    for feature_name in FeatureManager.available_features():
        # print(f'1. **{feature_name}:** {FeatureManager.help(feature_name)}')
        print(feature_name)


if '__main__' == __name__:
    main()