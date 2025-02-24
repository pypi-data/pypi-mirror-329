"""
genaitopic: A package for performing stratified boostrap sampling based methos to theme generation and prediction using LLMs.

Modules:
    - sampling - getstrata: Functions for stratified sampling with bootstraps or without.textstrata: Functions for converting samples to formatted text strings.
    - listthemes: Subpackage for theme extraction and final theme combination.
    - predict: Subpackage to predict or classify text to rag based retrivals 
"""

from . import listthemes
from . import predict
from . import sampling
