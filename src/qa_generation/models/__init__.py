"""Data models for QA generation."""

from qa_generation.models.qa_pair import GeneratorConfig, QAPair, QASourceDocument
from qa_generation.models.report_ingestion import (
    ChangeSnippet,
    DiffResult,
    SemanticDiffReport,
)

__all__ = [
    "ChangeSnippet",
    "DiffResult",
    "SemanticDiffReport",
    "QAPair",
    "QASourceDocument",
    "GeneratorConfig",
]
