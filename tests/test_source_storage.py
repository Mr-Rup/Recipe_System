"""
Tests for recipe source storage.
"""

from pathlib import Path

from PIL import Image
import pytest, fitz

from recipe_system.ingestion.source_storage import SourceStorage


def test_image_source_is_optimized_and_stored(tmp_path: Path):
    """Verify that an image source is automatically optimized before storage."""

    source_file = tmp_path / "recipe.png"
    image = Image.new("RGB", (5000, 4000))
    image.save(source_file)

    storage_directory = tmp_path / "storage" / "raw"
    storage = SourceStorage(storage_directory)

    stored_file = storage.store(source_file)

    assert stored_file.exists()
    assert stored_file.parent == storage_directory

    with Image.open(stored_file) as stored_image:
        assert max(stored_image.size) <= 3000


def test_pdf_source_is_optimized_and_stored(tmp_path: Path):
    """Verify that a PDF source is automatically optimized before storage."""

    source_file = tmp_path / "recipe.pdf"

    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Chicken Curry Recipe")
    document.save(source_file)
    document.close()

    storage_directory = tmp_path / "storage" / "raw"
    storage = SourceStorage(storage_directory)

    stored_file = storage.store(source_file)

    assert stored_file.exists()

    document = fitz.open(stored_file)

    try:
        assert len(document) == 1
        assert "Chicken Curry Recipe" in document[0].get_text()
    finally:
        document.close()


def test_text_source_is_copied_without_optimization(tmp_path: Path):
    """Verify that a text source is copied directly into source storage."""

    source_file = tmp_path / "recipe.txt"
    source_file.write_text(
        "500 g chicken.",
        encoding="utf-8",
    )

    storage_directory = tmp_path / "storage" / "raw"
    storage = SourceStorage(storage_directory)

    stored_file = storage.store(source_file)

    assert stored_file.exists()
    assert stored_file.read_text(encoding="utf-8") == "500 g chicken."


def test_unsupported_source_format_raises_error(tmp_path: Path):
    """Verify that unsupported source formats are rejected."""

    source_file = tmp_path / "recipe.docx"
    source_file.write_text(
        "Recipe",
        encoding="utf-8",
    )

    storage = SourceStorage(tmp_path / "storage" / "raw")

    with pytest.raises(ValueError):
        storage.store(source_file)