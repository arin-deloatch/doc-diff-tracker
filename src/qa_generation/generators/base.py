"""Base protocol for QA pair generators."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from qa_generation.models import GeneratorConfig, QAPair, QASourceDocument


@runtime_checkable
class QAGenerator(Protocol):
    """Protocol for QA pair generators.

    Implementations must provide a generate() method that takes
    source documents and configuration, returning generated QA pairs.

    This protocol allows swapping between different QA generation
    frameworks (RAGAS, custom generators, etc.) without changing
    the calling code.
    """

    def generate(
        self,
        documents: list[QASourceDocument],
        config: GeneratorConfig,
    ) -> list[QAPair]:
        """Generate QA pairs from source documents.

        Args:
            documents: List of QASourceDocument to generate from
            config: GeneratorConfig with generation parameters

        Returns:
            List of generated QAPair objects with traceability

        Raises:
            ValueError: If documents list is empty or invalid
            RuntimeError: If generation fails due to LLM/API errors
        """
        ...


class QAGenerationError(RuntimeError):
    """Base exception for QA generation errors.

    Inherits from RuntimeError to comply with QAGenerator protocol contract.
    """

    pass


class LLMError(QAGenerationError):
    """Raised when LLM API calls fail.

    Inherits from QAGenerationError (RuntimeError) for protocol compliance.
    """

    pass


class ConfigurationError(QAGenerationError):
    """Raised when configuration is invalid or incomplete.

    Inherits from QAGenerationError (RuntimeError) for protocol compliance.
    """

    pass
