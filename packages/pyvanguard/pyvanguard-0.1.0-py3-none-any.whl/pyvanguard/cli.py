# MIT License
#
# Copyright (c) 2025 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import click

from pyvanguard import __version__
from pyvanguard.command import LoadCommand, AlertCommand, AssistantCommand, QueryCommand


@click.group(help="🐺 Oncall AI Assistant.")
@click.version_option(version=__version__, help="Show the current version")
def main():
    """Main command group for PyVanguard CLI."""
    pass


@main.command(help="Load documentation into the RAG")
@click.option(
    "--dir_path",
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Path to the directory containing documentation.",
)
@click.option(
    "--team_name",
    required=True,
    type=str,
    help="Name of the team responsible for the documentation.",
)
def load(dir_path: str, team_name: str):
    LoadCommand().run(dir_path, team_name)


@main.command(help="Send a PagerDuty Alert")
@click.option("--summary", required=True, type=str, help="Summary of the alert.")
@click.option(
    "--severity",
    required=True,
    type=click.Choice(["info", "warning", "error", "critical"]),
    help="Severity of the alert.",
)
@click.option(
    "--team", required=True, type=str, help="Team to which the alert should be routed."
)
def alert(summary: str, severity: str, team: str):
    AlertCommand().run(summary, severity, team)


@main.command(help="Query the RAG system")
@click.option(
    "--text",
    required=True,
    type=str,
    help="The query text to search in the RAG system.",
)
@click.option(
    "--kind",
    required=True,
    type=str,
    help="The kind of query.",
)
@click.option(
    "--team",
    required=True,
    type=str,
    help="Name of the team whose documentation/pages to search.",
)
@click.option(
    "--limit",
    required=True,
    type=int,
    help="The maximum number of results to return.",
)
def query(text: str, kind: str, team: str, limit: int):
    QueryCommand().run(text, kind, team, limit)


@main.command(help="Run the AI Assistant")
def assistant():
    AssistantCommand().run()


if __name__ == "__main__":
    main()
