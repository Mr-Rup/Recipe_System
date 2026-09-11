"""
Tests for recipe domain objects.
"""

from recipe_system.ingredients.enums import *
from recipe_system.ingredients.items import Ingredient
from recipe_system.ingredients.measurements import IngredientMeasurement
from recipe_system.recipes.items import *
from recipe_system.ingestion.metadata import RecipeSource, SourceType

def test_recipe_source():
    """Verify that a raw recipe source preserves its type and extracted content."""

    source = RecipeSource(
        source_type=SourceType.PDF,
        original_file="storage/raw/chicken_curry.pdf",
        extracted_text="500 g chicken.",
    )

    assert source.source_type == SourceType.PDF
    assert source.original_file == "storage/raw/chicken_curry.pdf"
    assert source.extracted_text == "500 g chicken."

def test_recipe_creation():
    """Verify that a complete structured recipe can be created."""

    chicken = Ingredient(
        name="chicken",
        measurement=IngredientMeasurement(
            value=500,
            unit="g",
            original_text="500 g",
        ),
        original_text="500 g chicken",
        category=IngredientCategory.MAIN,
        role=IngredientRole.ESSENTIAL,
    )

    recipe = Recipe(
        recipe_name="Chicken Curry",
        source=RecipeSource(
            source_type=SourceType.TEXT,
            extracted_text="500 g chicken. Cook until tender.",
        ),
        ingredients=RecipeIngredients(
            main=[chicken],
        ),
        cooking_steps=[
            CookingStep(
                step_number=1,
                instruction="Cook the chicken until tender.",
                original_text="Cook chicken until tender.",
            )
        ],
        servings=4,
        preparation_time_minutes=10,
        cooking_time_minutes=30,
        total_time_minutes=40,
    )

    assert recipe.recipe_name == "Chicken Curry"
    assert recipe.ingredients.main[0].name == "chicken"
    assert recipe.cooking_steps[0].step_number == 1
    assert recipe.servings == 4
    assert recipe.total_time_minutes == 40

def test_recipe_draft():
    """Verify that a structured recipe can be represented as an unverified draft."""

    recipe = Recipe(
        recipe_name="Chicken Curry",
        source=RecipeSource(
            source_type=SourceType.TEXT,
            extracted_text="500 g chicken. Cook until tender.",
        ),
        ingredients=RecipeIngredients(),
    )

    draft = RecipeDraft(
        recipe=recipe,
        extraction_notes=[
            "Cooking time was not explicitly provided in the source."
        ],
    )

    assert draft.recipe.recipe_name == "Chicken Curry"
    assert len(draft.extraction_notes) == 1