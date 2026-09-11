"""
Enumerations used by the ingredient domain.

This module contains controlled vocabularies that define how ingredients are categorized and how they function within a recipe.
"""

from enum import Enum

class IngredientCategory(str, Enum):
    """
    Defines the broad culinary category to which an ingredient belongs.

    Categories describe WHAT an ingredient is, rather than its importance or purpose within a particular recipe.
    """

    MAIN = "main"
    SPICE = "spice"
    AROMATIC = "aromatic"
    OIL_AND_FAT = "oil_and_fat"
    LIQUID = "liquid"
    OTHER = "other"


class IngredientRole(str, Enum):
    """
    Defines the functional importance of an ingredient within a recipe.

    Roles describe HOW IMPORTANT an ingredient is to preparing the recipe, independently of its culinary category.
    """

    ESSENTIAL = "essential"
    SUPPORTING = "supporting"
    PANTRY_BASIC = "pantry_basic"
    OPTIONAL = "optional"
    GARNISH = "garnish"
    ADDITIONAL = "additional"