# ogboost/__init__.py

# Re-export key components from submodules
from .data import load_wine_quality
from .main import GradientBoostingOrdinal, concordance_index, LinkFunctions
from .utils import generate_heterogeneous_learners

# Define the public API
__all__ = ["load_wine_quality", "GradientBoostingOrdinal", "concordance_index", "LinkFunctions", "generate_heterogeneous_learners"]
