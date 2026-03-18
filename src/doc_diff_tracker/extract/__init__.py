"""Content extraction and semantic diffing."""

from doc_diff_tracker.extract.block_differ import BlockChange, compare_documents
from doc_diff_tracker.extract.content_extractor import extract_document_content

__all__ = ["extract_document_content", "compare_documents", "BlockChange"]
