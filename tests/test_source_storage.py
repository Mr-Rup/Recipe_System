"""
Tests for recipe source storage.
"""

from pathlib import Path
import pytest
from recipe_system.ingestion.source_storage import RecipeSourceStorage

def test_source_file_is_stored(tmp_path: Path):
    """Verify that a valid recipe source file is copied into source storage."""

    source_file = tmp_path / "chicken_curry.txt"
    source_file.write_text("500 g chicken.", encoding="utf-8")

    storage_directory = tmp_path / "storage" / "raw"
    storage = RecipeSourceStorage(storage_directory)

    stored_file = storage.store(source_file)

    assert stored_file.exists()
    assert stored_file.parent == storage_directory
    assert stored_file.name.endswith("_chicken_curry.txt")
    assert stored_file.read_text(encoding="utf-8") == "500 g chicken."


def test_missing_source_file_raises_error(tmp_path: Path):
    """Verify that attempting to store a missing source file raises an error."""

    storage = RecipeSourceStorage(tmp_path / "storage" / "raw")

    with pytest.raises(FileNotFoundError):
        storage.store(tmp_path / "missing_recipe.pdf")


def test_unsupported_source_format_raises_error(tmp_path: Path):
    """Verify that unsupported source formats are rejected."""

    source_file = tmp_path / "recipe.docx"
    source_file.write_text("Recipe", encoding="utf-8")

    storage = RecipeSourceStorage(tmp_path / "storage" / "raw")

    with pytest.raises(ValueError):
        storage.store(source_file)