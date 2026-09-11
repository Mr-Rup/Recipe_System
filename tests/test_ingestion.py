"""
Tests for recipe source ingestion and local storage.
"""

from pathlib import Path

from recipe_system.ingestion.storage import RecipeSourceStorage
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

def test_recipe_source_storage(tmp_path: Path):
    """Verify that a local recipe source can be copied into recipe storage."""

    source_file = tmp_path / "chicken_curry.txt"
    source_file.write_text(
        "500 g chicken\n2 onions\n1 tsp turmeric",
        encoding="utf-8",
    )

    storage = RecipeSourceStorage(
        storage_directory=tmp_path / "storage" / "raw"
    )

    stored_file = storage.store(source_file)

    assert stored_file.exists()
    assert stored_file.name.endswith("_chicken_curry.txt")
    assert stored_file.read_text(encoding="utf-8") == source_file.read_text(
        encoding="utf-8"
    )