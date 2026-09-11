"""
Utilities for optimizing recipe source files before long-term storage.

The optimization layer reduces unnecessary PDF and image file size while preserving sufficient visual quality for later recipe verification and inspection.
"""

from pathlib import Path
from PIL import Image
import fitz

class ImageOptimizer:
    """
    Optimizes image-based recipe sources for local storage.

    Images are resized when they exceed the configured maximum dimension and saved using a quality setting intended to balance file size and readability.
    """

    SUPPORTED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    }

    def __init__(
        self,
        maximum_dimension: int = 3000,
        quality: int = 85,
    ) -> None:
        """
        Initialize the recipe image optimizer.

        Args:
            maximum_dimension: Maximum width or height allowed for the optimized image.
            quality: JPEG/WebP quality level used during optimization.
        """

        self.maximum_dimension = maximum_dimension
        self.quality = quality

    def optimize(self, source_file: str | Path, destination_file: str | Path) -> Path:
        """
        Optimize an image source and save the result to the destination path.

        Args:
            source_file: Path to the source image.
            destination_file: Path where the optimized image should be saved.

        Returns:
            Path to the optimized image.

        Raises:
            FileNotFoundError: If the source image does not exist.
            ValueError: If the image format is not supported.
        """

        source_path = Path(source_file)
        destination_path = Path(destination_file)

        if not source_path.is_file():
            raise FileNotFoundError(f"Source image not found: {source_path}")

        if source_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported image format: {source_path.suffix}"
            )

        destination_path.parent.mkdir(parents=True, exist_ok=True)

        with Image.open(source_path) as image:
            image.thumbnail(
                (self.maximum_dimension, self.maximum_dimension),
                Image.Resampling.LANCZOS,
            )

            if destination_path.suffix.lower() in {".jpg", ".jpeg"}:
                if image.mode in {"RGBA", "LA", "P"}:
                    image = image.convert("RGB")

                image.save(
                    destination_path,
                    format="JPEG",
                    quality=self.quality,
                    optimize=True,
                )

            elif destination_path.suffix.lower() == ".webp":
                image.save(
                    destination_path,
                    format="WEBP",
                    quality=self.quality,
                    method=6,
                )

            else:
                image.save(
                    destination_path,
                    optimize=True,
                )

        return destination_path

class PDFOptimizer:
    """
    Optimizes PDF recipe sources for local storage.

    The optimizer rewrites PDFs using compression and garbage collection options provided by PyMuPDF while preserving the document's pages and visual content.
    """

    SUPPORTED_EXTENSION = ".pdf"

    def optimize(
        self,
        source_file: str | Path,
        destination_file: str | Path,
    ) -> Path:
        """
        Optimize a PDF source and save the result to the destination path.

        Args:
            source_file: Path to the source PDF.
            destination_file: Path where the optimized PDF should be saved.

        Returns:
            Path to the optimized PDF.

        Raises:
            FileNotFoundError: If the source PDF does not exist.
            ValueError: If the source file is not a PDF.
        """

        source_path = Path(source_file)
        destination_path = Path(destination_file)

        if not source_path.is_file():
            raise FileNotFoundError(f"Source PDF not found: {source_path}")

        if source_path.suffix.lower() != self.SUPPORTED_EXTENSION:
            raise ValueError(
                f"Unsupported PDF format: {source_path.suffix}"
            )

        destination_path.parent.mkdir(parents=True, exist_ok=True)

        document = fitz.open(source_path)

        try:
            document.save(
                destination_path,
                garbage=4,
                deflate=True,
                deflate_images=True,
                deflate_fonts=True,
            )
        finally:
            document.close()

        return destination_path