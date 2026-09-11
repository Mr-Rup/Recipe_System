"""
Measurement structures used to represent ingredient quantities in recipes.
"""

from typing import Optional

from pydantic import BaseModel, Field


class IngredientMeasurement(BaseModel):
    """
    Represents the quantity and measurement information associated with an ingredient.

    The model preserves the original quantity expression while providing normalized numeric values where they can be determined reliably.
    """

    value: Optional[float] = Field(
        default=None,
        description="Normalized numeric quantity when a single numeric value can be determined."
    )

    minimum: Optional[float] = Field(
        default=None,
        description="Lower bound when the ingredient quantity is expressed as a range."
    )

    maximum: Optional[float] = Field(
        default=None,
        description="Upper bound when the ingredient quantity is expressed as a range."
    )

    unit: Optional[str] = Field(
        default=None,
        description="Normalized measurement unit such as gram, milliliter, teaspoon, or piece."
    )

    original_text: Optional[str] = Field(
        default=None,
        description="Original quantity expression extracted from the recipe."
    )

    note: Optional[str] = Field(
        default=None,
        description="Additional quantity information such as 'to taste', 'as needed', or 'a pinch'."
    )