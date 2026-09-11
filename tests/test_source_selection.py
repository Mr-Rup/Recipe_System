"""
Tests for recipe source selection and validation.
"""

from pathlib import Path
import pytest
from recipe_system.ingestion.source_selection import SourceSelector

def test_valid_source_file_is_accepted(tmp_path: Path):
    """Verify that a supported local recipe source is accepted."""

    source_file = tmp_path / "chicken_curry.pdf"
    source_file.write_text(
        "Recipe source",
        encoding="utf-8",
    )

    selector = SourceSelector()

    result = selector.validate(source_file)

    assert result == source_file.resolve()

def test_missing_source_file_is_rejected(tmp_path: Path):
    """Verify that a missing recipe source raises an error."""

    selector = SourceSelector()

    with pytest.raises(FileNotFoundError):
        selector.validate(tmp_path / "missing.pdf")

def test_directory_is_rejected(tmp_path: Path):
    """Verify that a directory cannot be selected as a recipe source."""

    selector = SourceSelector()

    with pytest.raises(IsADirectoryError):
        selector.validate(tmp_path)

def test_unsupported_source_format_is_rejected(tmp_path: Path):
    """Verify that unsupported source formats raise an error."""

    source_file = tmp_path / "recipe.docx"
    source_file.write_text(
        "Recipe",
        encoding="utf-8",
    )

    selector = SourceSelector()

    with pytest.raises(ValueError):
        selector.validate(source_file)