"""
Data structures representing raw recipe sources submitted to the recipe system.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class SourceType(str, Enum):
    """
    Defines the type of source from which a recipe was obtained.
    """

    IMAGE = "image"
    PDF = "pdf"
    TEXT = "text"


class RecipeSource(BaseModel):
    """
    Represents the original material from which a recipe is extracted.

    The source is preserved independently from the structured recipe so that extracted information can always be reviewed against the original material.
    """

    source_type: SourceType = Field(
        ...,
        description="Type of source provided for recipe extraction."
    )

    original_file: Optional[str] = Field(
        default=None,
        description="Path to the original source file stored by the system."
    )

    extracted_text: Optional[str] = Field(
        default=None,
        description="Raw text extracted from the original source before AI structuring."
    )