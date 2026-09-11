"""
Streamlit interface for selecting and ingesting recipe source files.

This module provides the user-facing source upload workflow while keeping source validation, storage, and optimization inside the ingestion layer.
"""

from pathlib import Path
from tempfile import NamedTemporaryFile

import fitz
import streamlit as st

from recipe_system.ingestion.ingest import SourceIngester

SUPPORTED_EXTENSIONS = [
    "jpg",
    "jpeg",
    "png",
    "webp",
    "pdf",
    "txt",
]

def render_source_upload() -> None:
    """
    Render the recipe source selection, preview, and ingestion interface.

    The interface allows the user to select a supported recipe source, inspect the source before ingestion, and then pass it to the ingestion pipeline.
    """

    st.title("Recipe Source")

    st.write(
        "Select a recipe image, PDF, or text file to add it to the recipe system."
    )

    uploaded_file = st.file_uploader(
        "Choose a recipe source",
        type=SUPPORTED_EXTENSIONS,
    )

    if uploaded_file is None:
        return

    source_path = Path(uploaded_file.name)
    source_type = source_path.suffix.lower()

    st.write(f"Selected file: {uploaded_file.name}")

    with st.expander("Preview source", expanded=True):
        _render_preview(uploaded_file, source_type)

    st.divider()

    if st.button("Ingest Recipe Source", type="primary"):
        temporary_file = _save_uploaded_file(uploaded_file)

        try:
            with st.spinner("Ingesting recipe source..."):
                ingester = SourceIngester()
                source = ingester.ingest(temporary_file)

            st.success("Recipe source ingested successfully.")

            st.write(f"Original filename: {source.original_filename}")
            st.write(f"Stored source: {source.original_file}")
            st.write(f"Source type: {source.source_type.value}")

        finally:
            temporary_file.unlink(missing_ok=True)

def _render_preview(uploaded_file, source_type: str) -> None:
    """
    Render a preview appropriate for the selected source type.

    Args:
        uploaded_file: File object returned by Streamlit's file uploader.
        source_type: Lowercase file extension of the selected source.
    """

    if source_type in {".jpg", ".jpeg", ".png", ".webp"}:
        st.image(
            uploaded_file,
            caption=uploaded_file.name,
            use_container_width=True,
        )

    elif source_type == ".pdf":
        _render_pdf_preview(uploaded_file)

    elif source_type == ".txt":
        text = uploaded_file.getvalue().decode(
            "utf-8",
            errors="replace",
        )
        st.code(text, language="text")

def _render_pdf_preview(uploaded_file) -> None:
    """
    Render the first page of a PDF as a visual preview.

    Args:
        uploaded_file: File object returned by Streamlit's file uploader.
    """

    document = fitz.open(
        stream=uploaded_file.getvalue(),
        filetype="pdf",
    )

    try:
        if not document.page_count:
            st.info("The selected PDF does not contain any pages.")
            return

        page = document.load_page(0)
        pixmap = page.get_pixmap()
        preview = pixmap.tobytes("png")

        st.image(
            preview,
            caption=f"Preview: {uploaded_file.name} (first page)",
            use_container_width=True,
        )

        if document.page_count > 1:
            st.caption(
                f"Showing the first page of {document.page_count} pages."
            )

    finally:
        document.close()

def _save_uploaded_file(uploaded_file) -> Path:
    """
    Save a Streamlit uploaded file temporarily for the ingestion pipeline.

    Args:
        uploaded_file: File object returned by Streamlit's file uploader.

    Returns:
        Path to the temporary local file.
    """

    suffix = Path(uploaded_file.name).suffix

    with NamedTemporaryFile(
        delete=False,
        suffix=suffix,
    ) as temporary_file:
        temporary_file.write(uploaded_file.getbuffer())
        return Path(temporary_file.name)