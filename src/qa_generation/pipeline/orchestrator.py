"""Main orchestrator for QA generation pipeline.

Coordinates the full pipeline:
1. Load semantic diff report
2. Extract and filter snippets
3. Convert to QA source documents
4. Generate QA pairs via RAGAS
5. Write output files
"""

from __future__ import annotations

from pathlib import Path

import structlog

from qa_generation.config.settings import QAGenerationSettings
from qa_generation.generators import RAGASQAGenerator
from qa_generation.ingest.diff_report_reader import read_diff_report
from qa_generation.ingest.snippet_extractor import extract_snippets
from qa_generation.models import QAPair, QASourceDocument
from qa_generation.output import write_qa_pairs

logger = structlog.get_logger(__name__)


def generate_qa_from_report(
    report_path: str | Path,
    output_path: str | Path,
    settings: QAGenerationSettings,
    output_format: str = "json",
    allow_overwrite: bool = False,
    num_documents: int | None = None,
) -> list[QAPair]:
    """Generate QA pairs from a semantic diff report.

    This is the main entry point for the QA generation pipeline.

    Args:
        report_path: Path to semantic diff report JSON file
        output_path: Path to write QA pairs (JSON or YAML)
        settings: QA generation settings
        output_format: Output format ("json" or "yaml")
        allow_overwrite: Allow overwriting existing output file
        num_documents: Limit number of documents to process (None = all)

    Returns:
        List of generated QAPair objects

    Raises:
        FileNotFoundError: If report file not found
        ValueError: If report is invalid or no snippets extracted
        QAGenerationError: If generation fails
        QAWriteError: If writing output fails
    """
    report_path = Path(report_path)
    output_path = Path(output_path)

    logger.info(
        "starting_qa_generation_pipeline",
        report_path=str(report_path),
        output_path=str(output_path),
        testset_size=settings.testset_size,
    )

    # Step 0: Set up environment variables for LLM/embeddings
    logger.info("setting_up_environment")
    settings.setup_environment()

    # Step 1: Load semantic diff report
    logger.info("loading_diff_report", path=str(report_path))
    report = read_diff_report(report_path)
    logger.info(
        "diff_report_loaded",
        num_results=len(report.results),
        old_version=report.old_version,
        new_version=report.new_version,
    )

    # Step 2: Extract snippets
    logger.info("extracting_snippets")
    generator_config = settings.to_generator_config()
    snippets, stats = extract_snippets(report, generator_config.filtering)

    logger.info(
        "snippets_extracted",
        extracted=stats.extracted_snippets,
        total_filtered=stats.total_filtered,
        extraction_rate=f"{stats.extraction_rate:.1f}%",
    )

    if not snippets:
        raise ValueError(
            f"No snippets extracted from report. "
            f"Total changes: {stats.total_changes}, "
            f"Filtered: {stats.total_filtered}. "
            f"Try adjusting filter settings."
        )

    # Step 3: Snippets are already QASourceDocument objects
    source_documents = snippets

    # Limit documents if requested
    if num_documents is not None:
        if num_documents <= 0:
            raise ValueError(f"num_documents must be positive, got {num_documents}")
        original_count = len(source_documents)
        source_documents = source_documents[:num_documents]
        logger.info(
            "documents_limited",
            original_count=original_count,
            limited_count=len(source_documents),
        )

    logger.info(
        "source_documents_ready",
        num_documents=len(source_documents),
        total_chars=sum(doc.char_count for doc in source_documents),
    )

    # Step 4: Generate QA pairs
    logger.info("initializing_ragas_generator")
    generator = RAGASQAGenerator(settings)

    logger.info("generating_qa_pairs", testset_size=generator_config.testset_size)
    qa_pairs = generator.generate(source_documents, generator_config)


    logger.info(
        "qa_pairs_generated",
        num_pairs=len(qa_pairs),
        avg_question_length=sum(p.question_length for p in qa_pairs) / len(qa_pairs)
        if qa_pairs
        else 0,
    )

    # Step 5: Write output
    logger.info("writing_qa_pairs", format=output_format, path=str(output_path))
    write_qa_pairs(
        qa_pairs,
        output_path,
        format=output_format,
        allow_overwrite=allow_overwrite,
    )

    logger.info(
        "qa_generation_pipeline_complete",
        num_pairs=len(qa_pairs),
        output_path=str(output_path),
    )

    return qa_pairs
