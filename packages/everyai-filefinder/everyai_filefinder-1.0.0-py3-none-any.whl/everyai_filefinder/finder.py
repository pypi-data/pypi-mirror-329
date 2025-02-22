#!python3
"""
File Finder & Manager - A CLI tool for finding, filtering, and managing files.

Copyright (c) 2023-2025, Frank Mashraqi
Copyright (c) 2024-2025, Every AI LLC

Licensed under the MIT License (see LICENSE file for details).

Author: Frank Mashraqi
Email: softwareengineer99@yahoo.com
Version: 1.0.0
"""

import os
import sys
import argparse
import logging
import shutil
import hashlib
from typing import List
from rich.console import Console
from rich.table import Table
from rich.logging import RichHandler

# Setup Rich Console and Logging
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("rich")

import os
import sys
import argparse
import logging
import shutil
import hashlib
from typing import List
from rich.console import Console
from rich.table import Table
from rich.logging import RichHandler

# Setup Rich Console and Logging
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("rich")


def find_files(directory: str, extension: str, recursive: bool = False) -> List[str]:
    """Find files with a specific extension, with optional recursion."""
    if not os.path.isdir(directory):
        logger.error(f"[bold red]Invalid directory:[/bold red] {directory}")
        return []

    try:
        files = []
        if recursive:
            for root, _, filenames in os.walk(directory):
                files.extend(os.path.join(root, f) for f in filenames if f.endswith(extension))
        else:
            files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(extension)]

        logger.info(f"[bold green]Found {len(files)} file(s) with extension '{extension}'[/bold green]")
        return files
    except Exception as e:
        logger.exception(f"[bold red]Error while searching for files: {e}[/bold red]")
        return []


def filter_files_by_size(files: List[str], min_size_kb: int = 0, max_size_kb: int = float('inf')) -> List[str]:
    """Filter files based on size (in KB)."""
    filtered_files = [f for f in files if min_size_kb <= os.path.getsize(f) / 1024 <= max_size_kb]
    logger.info(f"[bold cyan]Filtered {len(filtered_files)} file(s) by size.[/bold cyan]")
    return filtered_files


def get_file_hash(file_path: str) -> str:
    """Compute MD5 hash for a file."""
    try:
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        logger.warning(f"[bold yellow]Error hashing file '{file_path}': {e}[/bold yellow]")
        return None


def remove_duplicate_files(files: List[str]) -> List[str]:
    """Remove duplicate files based on MD5 hash."""
    unique_files = {}
    duplicates = []

    for file in files:
        file_hash = get_file_hash(file)
        if file_hash:
            if file_hash in unique_files:
                duplicates.append(file)
            else:
                unique_files[file_hash] = file

    if duplicates:
        logger.warning(f"[bold yellow]Found {len(duplicates)} duplicate file(s).[/bold yellow]")
    return list(unique_files.values())


def sort_files_by_date(files: List[str], sort_by: str = "modified") -> List[str]:
    """Sort files by modified or created date."""
    try:
        files.sort(key=lambda f: os.path.getctime(f) if sort_by == "created" else os.path.getmtime(f))
        logger.info(f"[bold green]Files sorted by {sort_by} date.[/bold green]")
        return files
    except Exception as e:
        logger.warning(f"[bold yellow]Error sorting files: {e}[/bold yellow]")
        return files


def move_files(files: List[str], target_directory: str):
    """Move files to a target directory."""
    os.makedirs(target_directory, exist_ok=True)
    for file in files:
        try:
            shutil.move(file, target_directory)
            logger.info(f"[bold cyan]Moved {file} to {target_directory}[/bold cyan]")
        except Exception as e:
            logger.warning(f"[bold yellow]Error moving {file}: {e}[/bold yellow]")


def copy_files(files: List[str], target_directory: str):
    """Copy files to a target directory."""
    os.makedirs(target_directory, exist_ok=True)
    for file in files:
        try:
            shutil.copy(file, target_directory)
            logger.info(f"[bold cyan]Copied {file} to {target_directory}[/bold cyan]")
        except Exception as e:
            logger.warning(f"[bold yellow]Error copying {file}: {e}[/bold yellow]")


def display_files(files: List[str], directory: str, extension: str):
    """Display found files in a Rich-styled table."""
    if not files:
        console.print(f"[bold red]No files found with extension '{extension}' in '{directory}'.[/bold red]")
        return

    table = Table(title=f"Files with '{extension}' Extension", show_header=True, header_style="bold cyan")
    table.add_column("No.", justify="center", style="bold magenta")
    table.add_column("Filename", justify="left", style="bold white")

    for i, file in enumerate(files, start=1):
        table.add_row(str(i), os.path.basename(file))

    console.print(table)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Search, filter, and manage files in a directory.")
    parser.add_argument("directory", type=str, help="Directory to search in.")
    parser.add_argument("extension", type=str, help="File extension to filter (e.g., .mp4).")
    
    # Optional Features
    parser.add_argument("-r", "--recursive", action="store_true", help="Search files recursively in subdirectories.")
    parser.add_argument("--min-size", type=int, default=0, help="Minimum file size in KB.")
    parser.add_argument("--max-size", type=int, default=float('inf'), help="Maximum file size in KB.")
    parser.add_argument("--remove-duplicates", action="store_true", help="Remove duplicate files based on MD5 hash.")
    parser.add_argument("--sort", choices=["created", "modified"], default=None, help="Sort files by date.")
    parser.add_argument("--move", type=str, help="Move files to the specified directory.")
    parser.add_argument("--copy", type=str, help="Copy files to the specified directory.")

    args = parser.parse_args()

    console.print(f"[bold cyan]Searching for '{args.extension}' files in directory:[/bold cyan] {args.directory}")

    # Find files
    files = find_files(args.directory, args.extension, args.recursive)

    # Apply filters and operations
    if args.min_size > 0 or args.max_size < float('inf'):
        files = filter_files_by_size(files, args.min_size, args.max_size)

    if args.remove_duplicates:
        files = remove_duplicate_files(files)

    if args.sort:
        files = sort_files_by_date(files, args.sort)

    # Display results
    display_files(files, args.directory, args.extension)

    # Move or Copy files
    if args.move:
        move_files(files, args.move)

    if args.copy:
        copy_files(files, args.copy)
