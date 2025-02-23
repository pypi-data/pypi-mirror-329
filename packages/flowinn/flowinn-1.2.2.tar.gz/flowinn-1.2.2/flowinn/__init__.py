"""
flowinn: Multi-Scale Turbulent Flow Investigation using Neural Networks
====================================================================

A Python package for investigating multi-scale turbulent flows using physics-informed neural networks.
"""

__version__ = "1.2.2"
__author__ = "Jon Errasti Odriozola"
__email__ = "errasti13@gmail.com"

from . import mesh
from . import models
from . import physics
from . import plot
from . import training
from . import tests
from .version import __version__

__all__ = ["mesh", "models", "physics", "plot", "training", "tests", "__version__"]
