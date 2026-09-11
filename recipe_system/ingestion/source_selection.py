"""
Utilities for validating recipe source files selected by the user.

The source selection layer validates a selected local file before it is passed to the recipe source storage layer.
"""

from pathlib import Path

class SourceSelector:
    """
    Validates local files selected as recipe sources.

    The selector is responsible only for identifying whether a selected file can be processed by the recipe ingestion system.
    """

    SUPPORTED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".pdf",
        ".txt",
    }

    def validate(self, source_file: str | Path) -> Path:
        """
        Validate a selected local recipe source file.

        Args:
            source_file: Path to the local file selected by the user.

        Returns:
            Resolved path to the validated source file.

        Raises:
            FileNotFoundError: If the selected file does not exist.
            IsADirectoryError: If the selected path is a directory.
            ValueError: If the selected file format is not supported.
        """

        source_path = Path(source_file)

        if not source_path.exists():
            raise FileNotFoundError(
                f"Selected source file not found: {source_path}"
            )

        if source_path.is_dir():
            raise IsADirectoryError(
                f"Selected source path is a directory: {source_path}"
            )

        if source_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported source format: {source_path.suffix}"
            )

        return source_path.resolve()