"""
Utilities for storing recipe source files in the local recipe system.

The source storage layer manages physical recipe files independently from recipe metadata and structured recipe information.
"""

from pathlib import Path
from shutil import copy2
from uuid import uuid4

class RecipeSourceStorage:
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

    def __init__(self, storage_directory: str | Path = "storage/raw") -> None:
        """
        Initialize the recipe source storage manager.

        Args:
            storage_directory: Directory in which source files should be stored.
        """

        self.storage_directory = Path(storage_directory)
        self.storage_directory.mkdir(parents=True, exist_ok=True)

    def store(self, source_file: str | Path) -> Path:
        """
        Copy a local recipe source file into the recipe system's source storage.

        A unique identifier is added to the stored filename to prevent collisions between files with identical names.

        Args:
            source_file: Path to the local source file selected by the user.

        Returns:
            Path to the stored source file.

        Raises:
            FileNotFoundError: If the supplied source file does not exist.
            ValueError: If the source file format is not supported.
        """

        source_path = Path(source_file)

        if not source_path.is_file():
            raise FileNotFoundError(f"Source file not found: {source_path}")

        if source_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported source format: {source_path.suffix}"
            )

        stored_filename = f"{uuid4()}_{source_path.name}"
        destination = self.storage_directory / stored_filename

        copy2(source_path, destination)

        return destination