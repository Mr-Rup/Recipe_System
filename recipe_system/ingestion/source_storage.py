"""
Utilities for storing and optimizing recipe source files in the local recipe system.

The source storage layer manages physical recipe files independently from recipe metadata and structured recipe information.
"""

from pathlib import Path
from shutil import copy2
from uuid import uuid4

from recipe_system.ingestion.source_optimizer import ImageOptimizer, PDFOptimizer

class SourceStorage:
    """
    Manages persistent storage of recipe source files.

    Source files are stored inside the dedicated recipe-system storage directory rather than inside the Python package.
    """

    SUPPORTED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".pdf",
        ".txt",
    }

    IMAGE_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    }

    def __init__(
        self,
        storage_directory: str | Path = "storage/raw",
    ) -> None:
        """
        Initialize the recipe source storage manager.

        Args:
            storage_directory: Directory in which source files should be stored.
        """

        self.storage_directory = Path(storage_directory)
        self.storage_directory.mkdir(parents=True, exist_ok=True)

        self.image_optimizer = ImageOptimizer()
        self.pdf_optimizer = PDFOptimizer()

    def store(self, source_file: str | Path) -> Path:
        """
        Store a recipe source file using the appropriate optimization process.

        Image and PDF sources are optimized before being stored, while text sources are copied directly without modification.

        Args:
            source_file: Path to the local source file selected by the user.

        Returns:
            Path to the final stored source file.

        Raises:
            FileNotFoundError: If the supplied source file does not exist.
            ValueError: If the source file format is not supported.
        """

        source_path = Path(source_file)

        if not source_path.is_file():
            raise FileNotFoundError(f"Source file not found: {source_path}")

        extension = source_path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported source format: {source_path.suffix}"
            )

        stored_filename = f"{uuid4()}_{source_path.name}"
        destination = self.storage_directory / stored_filename

        if extension in self.IMAGE_EXTENSIONS:
            self.image_optimizer.optimize(
                source_path,
                destination,
            )

        elif extension == ".pdf":
            self.pdf_optimizer.optimize(
                source_path,
                destination,
            )

        else:
            copy2(source_path, destination)

        return destination