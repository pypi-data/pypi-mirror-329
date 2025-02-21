import warnings
from abc import ABC, abstractmethod

import numpy as np

MED = 'median'

VAR = 'var'

MEAN = 'mean'

MAX = 'max'

MIN = 'min'

EPSILON = 1e-6


BASIC_ARRAY_METRICS = [MEAN, MIN, MAX, VAR, MED]

BASIC_METRIC2HELP = {VAR: 'variance',
                     MIN: 'minimum',
                     MEAN: 'average',
                     MED: 'median',
                     MAX: 'maximum'}

BASIC_METRIC2FUN = {VAR: np.var,
                    MIN: np.min,
                    MEAN: np.mean,
                    MED: np.median,
                    MAX: np.max}


NORMALIZED = 'normalized'


class FeatureCalculator(ABC):
    """Abstract base class for feature calculators."""

    @abstractmethod
    def feature_names(self):
        """Return a list of feature names this class can compute."""
        pass

    @abstractmethod
    def set_forest(self, forest, **kwargs):
        """Sets the forest on which the features are to be calculated"""
        pass

    @abstractmethod
    def calculate(self, forest, feature_name, **kwargs):
        """Compute a specific feature or features."""
        pass

    @abstractmethod
    def help(self, feature_name, *args, **kwargs):
        """Shows the definition of the specific feature."""
        pass


class FeatureRegistry:
    """Registry for mapping feature names to their respective calculator classes."""

    _registry = {}
    _calculators = []

    @classmethod
    def register(cls, calculator):
        """Register a feature calculator class and map its features."""
        cls._calculators.append(calculator)
        for feature in calculator.feature_names():
            cls._registry[feature] = calculator

    @classmethod
    def get_calculator(cls, feature_name):
        """Retrieve the appropriate calculator class for a given feature."""
        return cls._registry.get(feature_name)

    @classmethod
    def list_features(cls):
        return list(cls._registry.keys())

    @classmethod
    def list_calculators(cls):
        return list(cls._calculators)


class FeatureManager:
    """Manages feature computation dynamically based on user input."""

    @classmethod
    def compute_features(cls, forest, *feature_list, **kwargs):
        """Compute and return requested features."""

        for calc in FeatureRegistry.list_calculators():
            calc.set_forest(forest, **kwargs)

        if not feature_list:
            feature_list = FeatureManager.available_features()

        for feature in feature_list:
            calculator = FeatureRegistry.get_calculator(feature)
            if calculator:
                yield calculator.calculate(feature, **kwargs)
            else:
                warnings.warn(f'Did not find a Feature Calculator for feature {feature}')
                yield None

    @classmethod
    def available_features(cls):
        return FeatureRegistry.list_features()

    @classmethod
    def help(cls, feature_name, *args, **kwargs):
        """Returns feature description"""

        calculator = FeatureRegistry.get_calculator(feature_name)
        if calculator:
            return calculator.help(feature_name, **kwargs)
        else:
            warnings.warn(f'Did not find a Feature Calculator for feature {feature_name}')
            return None



