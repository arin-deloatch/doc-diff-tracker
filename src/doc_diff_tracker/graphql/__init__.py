"""
GraphQL Polling Service for Doc-Diff-Tracker.

This module provides continuous monitoring of GraphQL APIs for documentation changes
and automatically triggers the diff + QA generation pipeline when changes are detected.

Main components:
    - client: GraphQL client with authentication and retry logic
    - fetcher: HTTP client for fetching HTML content from URLs
    - models: Pydantic models for GraphQL responses and configuration
    - state: State persistence with file locking and atomic writes
    - scheduler: Async polling loop orchestrator
    - pipeline: Pipeline runner that invokes diff/QA generation
    - config: Configuration loading from YAML and environment variables
"""

__version__ = "1.0.0"
