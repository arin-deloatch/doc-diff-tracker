"""Unified CLI for docta - documentation delta tracking tool.

This module organizes all CLI commands into logical subcommand groups:
- diff: Document comparison and semantic analysis
- daemon: GraphQL polling daemon management
- qa: QA generation from documentation changes
"""

from __future__ import annotations

import typer

from docta.cli.daemon import app as daemon_app
from docta.cli.diff import app as diff_app
from docta.cli.qa import app as qa_app

# Create main application
app = typer.Typer(
    help="Documentation delta tracking and analysis tool",
    no_args_is_help=True,
)

# Register subcommand groups
app.add_typer(
    diff_app,
    name="diff",
    help="Compare and analyze documentation differences",
)

app.add_typer(
    daemon_app,
    name="daemon",
    help="Manage GraphQL polling daemon service",
)

app.add_typer(
    qa_app,
    name="qa",
    help="Generate QA pairs from documentation changes",
)


if __name__ == "__main__":
    app()
