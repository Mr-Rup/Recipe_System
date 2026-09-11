"""
Core data models for individual recipe ingredients.
"""

from typing import Optional
from pydantic import BaseModel, Field
from recipe_system.ingredients.enums import (
    IngredientCategory,
    IngredientRole,
)
from recipe_system.ingredients.measurements import IngredientMeasurement
from uuid import UUID, uuid4

class Ingredient(BaseModel):
    """
    Represents an ingredient as it appears within a specific recipe.

    The model preserves both the normalized representation used by the application and the original wording extracted from the source recipe.

    Attributes:
        name: Normalized ingredient name used for recipe processing.
        quantity: Numeric quantity when one can be reliably determined.
        unit: Unit associated with the quantity, such as 'g', 'ml', or 'tablespoon'.
        original_text: Exact ingredient wording extracted from the source.
        preparation: Preparation instructions associated with the ingredient, such as 'finely chopped' or 'boneless'.
        quantity_note: Non-numeric quantity information such as 'to taste' or 'as needed'.
        category: Broad culinary category of the ingredient.
        role: Functional importance of the ingredient within the recipe.
    """

    name: str = Field(
        ...,
        description="Normalized name of the ingredient."
    )

    master_ingredient_id: Optional[UUID] = Field(
        default=None,
        description="Identifier of the canonical master ingredient associated with this recipe ingredient."
    )

    measurement: Optional[IngredientMeasurement] = Field(
        default=None,
        description="Quantity and measurement information associated with the ingredient."
    )

    original_text: Optional[str] = Field(
        default=None,
        description="Original ingredient wording extracted from the source."
    )

    preparation: Optional[str] = Field(
        default=None,
        description="Preparation or processing instruction for the ingredient."
    )

    category: IngredientCategory = Field(
        ...,
        description="Broad culinary category of the ingredient."
    )

    role: IngredientRole = Field(
        ...,
        description="Functional importance of the ingredient in the recipe."
    )

class MasterIngredient(BaseModel):
    """
    Represents the canonical identity of an ingredient used across the recipe system.

    A master ingredient provides a stable identity for different names or
    expressions that may refer to the same ingredient.
    """

    id: UUID = Field(
        default_factory=uuid4,
        description="Unique identifier for the master ingredient."
    )

    canonical_name: str = Field(
        ...,
        description="Canonical name used to identify the ingredient."
    )

    aliases: list[str] = Field(
        default_factory=list,
        description="Alternative names or expressions used for the ingredient."
    )

    default_category: IngredientCategory = Field(
        ...,
        description="Default culinary category assigned to the ingredient."
    )

    pantry_basic: bool = Field(
        default=False,
        description="Indicates whether the ingredient is treated as a basic pantry item during recipe matching."
    )