"""
Tests for ingredient domain objects.
"""

from recipe_system.ingredients.enums import (
    IngredientCategory,
    IngredientRole,
)
from recipe_system.ingredients.items import (
    Ingredient,
    MasterIngredient,
)
from recipe_system.ingredients.measurements import IngredientMeasurement


def test_ingredient():
    """Verify that a recipe ingredient can be created before normalization."""

    ingredient = Ingredient(
        name="dhania",
        measurement=IngredientMeasurement(
            value=500,
            unit="g",
            original_text="500 g",
        ),
        original_text="500 g dhania",
        category=IngredientCategory.AROMATIC,
        role=IngredientRole.ESSENTIAL,
    )

    assert ingredient.name == "dhania"
    assert ingredient.measurement.value == 500
    assert ingredient.measurement.unit == "g"
    assert ingredient.measurement.original_text == "500 g"
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
        measurement=IngredientMeasurement(
            value=500,
            unit="g",
            original_text="500 g",
        ),
        original_text="500 g dhania",
        category=IngredientCategory.AROMATIC,
        role=IngredientRole.ESSENTIAL,
    )

    assert ingredient.master_ingredient_id == coriander.id
    assert coriander.canonical_name == "coriander"
    assert ingredient.measurement.value == 500
    assert ingredient.measurement.unit == "g"
    assert ingredient.measurement.original_text == "500 g"