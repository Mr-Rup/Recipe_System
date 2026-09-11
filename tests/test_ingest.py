"""
Tests for recipe source ingestion.
"""

from pathlib import Path

from recipe_system.ingestion.ingest import SourceIngester
from recipe_system.ingestion.metadata import SourceType
from recipe_system.ingestion.source_storage import SourceStorage

def test_image_source_is_ingested(tmp_path: Path):
    """Verify that an image source is validated, stored, and represented by source metadata."""

    from PIL import Image

    source_file = tmp_path / "recipe.png"

    image = Image.new("RGB", (1000, 800))
    image.save(source_file)

    storage = SourceStorage(tmp_path / "storage" / "raw")
    ingester = SourceIngester(storage=storage)

    source = ingester.ingest(source_file)

    assert source.source_type == SourceType.IMAGE
    assert source.original_file is not None
    assert Path(source.original_file).exists()
    assert source.original_filename == "recipe.png"

def test_pdf_source_is_ingested(tmp_path: Path):
    """Verify that a PDF source is validated, stored, and represented by source metadata."""

    import fitz

    source_file = tmp_path / "recipe.pdf"

    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Chicken Curry Recipe")
    document.save(source_file)
    document.close()

    storage = SourceStorage(tmp_path / "storage" / "raw")
    ingester = SourceIngester(storage=storage)

    source = ingester.ingest(source_file)

    assert source.source_type == SourceType.PDF
    assert source.original_file is not None
    assert Path(source.original_file).exists()
    assert source.original_filename == "recipe.pdf"

def test_text_source_is_ingested(tmp_path: Path):
    """Verify that a text source is validated, stored, and represented by source metadata."""

    source_file = tmp_path / "recipe.txt"
    source_file.write_text(
        "500 g chicken.",
        encoding="utf-8",
    )

    storage = SourceStorage(tmp_path / "storage" / "raw")
    ingester = SourceIngester(storage=storage)

    source = ingester.ingest(source_file)

    assert source.source_type == SourceType.TEXT
    assert source.original_file is not None
    assert Path(source.original_file).exists()
    assert source.original_filename == "recipe.txt"