"""
Entry points for ingesting recipe source files into the recipe system.

The ingestion layer coordinates source validation, storage, and source metadata creation without performing recipe extraction or AI processing.
"""

from pathlib import Path

from recipe_system.ingestion.metadata import RecipeSource, SourceType
from recipe_system.ingestion.source_selection import SourceSelector
from recipe_system.ingestion.source_storage import SourceStorage


class SourceIngester:
    """
    Coordinates the initial ingestion of a local recipe source.

    The ingester validates the selected source, stores it using the source storage layer, and creates metadata describing the stored source.
    """

    def __init__(
        self,
        storage: SourceStorage | None = None,
        selector: SourceSelector | None = None,
    ) -> None:
        """
        Initialize the recipe source ingester.

        Args:
            storage: Source storage manager used to persist the selected file.
            selector: Source selector used to validate the selected file.
        """

        self.storage = storage or SourceStorage()
        self.selector = selector or SourceSelector()

    def ingest(self, source_file: str | Path) -> RecipeSource:
        """
        Validate and store a local recipe source.

        Args:
            source_file: Path to the local recipe source selected by the user.

        Returns:
            Metadata describing the stored recipe source.

        Raises:
            FileNotFoundError: If the selected source does not exist.
            IsADirectoryError: If the selected path is a directory.
            ValueError: If the source format is unsupported.
        """

        source_path = self.selector.validate(source_file)
        stored_file = self.storage.store(source_path)

        return RecipeSource(
            source_type=self._get_source_type(source_path),
            original_file=str(stored_file),
            original_filename=source_path.name,
        )

    @staticmethod
    def _get_source_type(source_file: Path) -> SourceType:
        """
        Determine the source type from the selected file extension.

        Args:
            source_file: Validated source file path.

        Returns:
            Source type represented by the file extension.
        """

        extension = source_file.suffix.lower()

        if extension in {".jpg", ".jpeg", ".png", ".webp"}:
            return SourceType.IMAGE

        if extension == ".pdf":
            return SourceType.PDF

        if extension == ".txt":
            return SourceType.TEXT

        raise ValueError(
            f"Unsupported source format: {source_file.suffix}"
        )