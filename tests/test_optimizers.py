"""
Tests for recipe source image and PDF optimization.
"""

import fitz
from pathlib import Path
from PIL import Image
from recipe_system.ingestion.source_optimizer import ImageOptimizer, PDFOptimizer

def test_image_is_optimized(tmp_path: Path):
    """Verify that a recipe image can be resized and stored as an optimized image."""

    source_file = tmp_path / "recipe.png"
    destination_file = tmp_path / "optimized" / "recipe.png"

    image = Image.new("RGB", (5000, 4000))
    image.save(source_file)

    optimizer = ImageOptimizer(maximum_dimension=3000)

    result = optimizer.optimize(source_file, destination_file)

    assert result == destination_file
    assert result.exists()

    with Image.open(result) as optimized_image:
        assert max(optimized_image.size) <= 3000

def test_image_optimizer_preserves_small_images(tmp_path: Path):
    """Verify that images already within the maximum dimension are not enlarged."""

    source_file = tmp_path / "recipe.png"
    destination_file = tmp_path / "optimized" / "recipe.png"

    image = Image.new("RGB", (1000, 800))
    image.save(source_file)

    optimizer = ImageOptimizer(maximum_dimension=3000)

    optimizer.optimize(source_file, destination_file)

    with Image.open(destination_file) as optimized_image:
        assert optimized_image.size == (1000, 800)

def create_test_pdf(path: Path) -> None:
    """Create a minimal PDF used for testing PDF optimization."""

    document = fitz.open()

    page = document.new_page()
    page.insert_text(
        (72, 72),
        "Chicken Curry Recipe",
    )

    document.save(path)
    document.close()

def test_pdf_is_optimized(tmp_path: Path):
    """Verify that a valid recipe PDF can be optimized and saved."""

    source_file = tmp_path / "recipe.pdf"
    destination_file = tmp_path / "optimized" / "recipe.pdf"

    create_test_pdf(source_file)

    optimizer = PDFOptimizer()

    result = optimizer.optimize(
        source_file,
        destination_file,
    )

    assert result == destination_file
    assert result.exists()

    document = fitz.open(result)

    try:
        assert len(document) == 1
        assert "Chicken Curry Recipe" in document[0].get_text()
    finally:
        document.close()

def test_missing_pdf_raises_error(tmp_path: Path):
    """Verify that a missing PDF source raises an error."""

    optimizer = PDFOptimizer()

    missing_file = tmp_path / "missing.pdf"
    destination_file = tmp_path / "optimized.pdf"

    try:
        optimizer.optimize(missing_file, destination_file)
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("Expected FileNotFoundError")

def test_non_pdf_file_raises_error(tmp_path: Path):
    """Verify that non-PDF sources are rejected by the PDF optimizer."""

    source_file = tmp_path / "recipe.txt"
    source_file.write_text("Chicken curry recipe.", encoding="utf-8")

    destination_file = tmp_path / "optimized.pdf"

    optimizer = PDFOptimizer()

    try:
        optimizer.optimize(source_file, destination_file)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")