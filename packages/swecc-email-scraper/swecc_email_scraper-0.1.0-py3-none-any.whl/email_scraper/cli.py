"""Command line interface for email-scraper."""

import click
from rich.console import Console
from rich.progress import Progress
from pathlib import Path

from . import __version__
from .analyzer import EmailAnalyzer

console = Console()

@click.group()
@click.version_option(version=__version__)
def main():
    """Email Scraper - Analyze email data in mbox format."""
    pass

@main.command()
@click.argument('mbox_path', type=click.Path(exists=True, path_type=Path))
@click.option('--output', '-o', type=click.Path(path_type=Path),
              help='Path to save the analysis report.')
def analyze(mbox_path: Path, output: Path | None):
    """Analyze an mbox file and generate a report.

    MBOX_PATH: Path to the mbox file to analyze
    """
    try:
        with Progress() as progress:
            task = progress.add_task("Analyzing emails...", total=100)
            analyzer = EmailAnalyzer(mbox_path)
            results = analyzer.analyze()
            progress.update(task, completed=100)

        console.print("[green]Analysis complete![/green]")
        console.print(results)

        if output:
            analyzer.save_report(results, output)
            console.print(f"[green]Report saved to {output}[/green]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise click.Abort()

if __name__ == '__main__':
    main()