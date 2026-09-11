"""
Core recipe structures used by the recipe system.
"""

from typing import Optional
from pydantic import BaseModel, Field
from recipe_system.ingredients.items import Ingredient

class RecipeSource(BaseModel):
    """
    Represents the original source from which a recipe was obtained.

    The source information is preserved so that extracted and normalized recipe data can always be traced back to the original material.
    """

    source_type: str = Field(
        ...,
        description="Type of source from which the recipe was obtained."
    )

    original_file: Optional[str] = Field(
        default=None,
        description="Path or identifier of the original recipe file."
    )

    extracted_text: Optional[str] = Field(
        default=None,
        description="Raw text extracted from the original recipe source."
    )


class CookingStep(BaseModel):
    """
    Represents one ordered instruction in a recipe's cooking process.

    Both the structured instruction and its original wording are preserved to support review and correction of AI-generated extraction.
    """

    step_number: int = Field(
        ...,
        description="Sequential position of the cooking step."
    )

    instruction: str = Field(
        ...,
        description="Structured cooking instruction."
    )

    original_text: Optional[str] = Field(
        default=None,
        description="Original wording of the cooking instruction."
    )

    duration_minutes: Optional[float] = Field(
        default=None,
        description="Cooking duration associated with the step, when available."
    )

    temperature: Optional[str] = Field(
        default=None,
        description="Cooking temperature associated with the step, when available."
    )


class RecipeIngredients(BaseModel):
    """
    Organizes the ingredients used by a recipe into culinary categories.

    The additional collection stores ingredients discovered during extraction that were not explicitly present in the supplied ingredient list.
    """

    main: list[Ingredient] = Field(
        default_factory=list,
        description="Primary ingredients that form the main component of the recipe."
    )

    spices: list[Ingredient] = Field(
        default_factory=list,
        description="Spices used in the recipe."
    )

    aromatics: list[Ingredient] = Field(
        default_factory=list,
        description="Aromatic ingredients such as onions, garlic, ginger, or herbs."
    )

    oils_and_fats: list[Ingredient] = Field(
        default_factory=list,
        description="Oils, butter, ghee, and other cooking fats."
    )

    liquids: list[Ingredient] = Field(
        default_factory=list,
        description="Liquid ingredients used in the recipe."
    )

    other: list[Ingredient] = Field(
        default_factory=list,
        description="Ingredients that do not fit the other ingredient categories."
    )

    additional: list[Ingredient] = Field(
        default_factory=list,
        description="Ingredients discovered during extraction that were not explicitly listed in the source ingredient list."
    )


class Recipe(BaseModel):
    """
    Represents a complete structured recipe stored by the recipe system.

    A recipe combines source information, structured ingredients, cooking instructions, and basic preparation metadata.
    """

    recipe_name: str = Field(
        ...,
        description="Name of the recipe."
    )

    source: RecipeSource = Field(
        ...,
        description="Original source information for the recipe."
    )

    ingredients: RecipeIngredients = Field(
        ...,
        description="Ingredients required or associated with the recipe."
    )

    cooking_steps: list[CookingStep] = Field(
        default_factory=list,
        description="Ordered cooking instructions for the recipe."
    )

    servings: Optional[int] = Field(
        default=None,
        description="Number of servings produced by the recipe."
    )

    preparation_time_minutes: Optional[float] = Field(
        default=None,
        description="Estimated preparation time in minutes."
    )

    cooking_time_minutes: Optional[float] = Field(
        default=None,
        description="Estimated cooking time in minutes."
    )

    total_time_minutes: Optional[float] = Field(
        default=None,
        description="Total recipe time in minutes."
    )

class RecipeDraft(BaseModel):
    """
    Represents a recipe extracted from a raw source before user verification.

    A recipe draft contains AI-generated structured information that may require correction before it becomes part of the permanent recipe collection.
    """

    recipe: Recipe = Field(
        ...,
        description="Structured recipe produced during the extraction process."
    )

    extraction_notes: list[str] = Field(
        default_factory=list,
        description="Notes describing uncertainties, ambiguities, or issues identified during extraction."
    )