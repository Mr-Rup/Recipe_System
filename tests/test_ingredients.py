"""
Tests for ingredient domain models.
"""

from recipe_system.ingredients.enums import (
    IngredientCategory,
    IngredientRole,
)
from recipe_system.ingredients.items import *


def test_ingredient():
    """Verify that a recipe ingredient can be created before normalization."""

    ingredient = Ingredient(
        name="dhania",
        quantity=2,
        unit="tbsp",
        original_text="2 tbsp dhania",
        category=IngredientCategory.AROMATIC,
        role=IngredientRole.ESSENTIAL,
    )

    assert ingredient.name == "dhania"
    assert ingredient.quantity == 2
    assert ingredient.unit == "tbsp"
    assert ingredient.master_ingredient_id is None

def test_master_ingredient():
    """Verify that a recipe ingredient can reference its canonical master ingredient."""

    coriander = MasterIngredient(
        canonical_name="coriander",
        aliases=[
            "dhania",
            "cilantro",
            "coriander leaves",
        ],
        default_category=IngredientCategory.AROMATIC,
    )

    ingredient = Ingredient(
        name="dhania",
        master_ingredient_id=coriander.id,
        quantity=2,
        unit="tbsp",
        original_text="2 tbsp dhania",
        category=IngredientCategory.AROMATIC,
        role=IngredientRole.ESSENTIAL,
    )

    assert ingredient.master_ingredient_id == coriander.id
    assert coriander.canonical_name == "coriander"