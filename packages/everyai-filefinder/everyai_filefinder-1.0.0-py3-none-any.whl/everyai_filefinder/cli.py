# filefinder/cli.py
import argparse
from rich.console import Console
from .finder import find_files

console = Console()

def main():
    """Entry point for CLI."""
    parser = argparse.ArgumentParser(description="Search, filter, and manage files.")
    parser.add_argument("directory", type=str, help="Directory to search in.")
    parser.add_argument("extension", type=str, help="File extension to filter (e.g., .mp4).")
    parser.add_argument("-r", "--recursive", action="store_true", help="Enable recursive search.")
    
    args = parser.parse_args()
    files = find_files(args.directory, args.extension, args.recursive)

    if files:
        console.print(f"[bold green]Found {len(files)} files[/bold green]")
        for file in files:
            console.print(f"[cyan]{file}[/cyan]")
    else:
        console.print("[bold red]No files found.[/bold red]")
