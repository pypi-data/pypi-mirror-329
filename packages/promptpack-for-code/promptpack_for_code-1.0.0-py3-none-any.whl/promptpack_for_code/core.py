import os
from pathlib import Path
from typing import List, Optional
import fnmatch
import logging
from concurrent.futures import ThreadPoolExecutor
import mimetypes
from tqdm import tqdm

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_tree(
    path: Path,
    prefix: str = "",
    ignore_patterns: Optional[List[str]] = None
) -> str:
    """
    Generate a tree-like structure of the directory.
    
    Args:
        path: Path object to generate tree from
        prefix: Prefix for tree formatting
        ignore_patterns: List of patterns to ignore (supports fnmatch wildcards)
    
    Returns:
        A string representing the directory tree structure
    """
    if ignore_patterns is None:
        ignore_patterns = [
            ".git", "__pycache__", "*.pyc", "*.pyo", "*.pyd", "*.swp",
            ".DS_Store", "*.log", ".venv", "venv",
            "node_modules", "vendor"
        ]

    # Check if this directory matches ignore patterns
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(path.name, pattern):
            return prefix + path.name + " [...]"

    output = []
    try:
        contents = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        for i, item in enumerate(contents):
            is_last = i == len(contents) - 1
            connector = "└── " if is_last else "├── "
            new_prefix = prefix + ("    " if is_last else "│   ")

            if any(fnmatch.fnmatch(item.name, pattern) for pattern in ignore_patterns):
                if item.is_dir():
                    output.append(prefix + connector + item.name + " [...]")
                continue

            output.append(prefix + connector + item.name)
            if item.is_dir():
                subtree = generate_tree(item, new_prefix, ignore_patterns)
                if subtree:
                    output.append(subtree)

    except PermissionError:
        logger.warning(f"Permission denied accessing directory: {path}")
        return prefix + f"[Error: Permission denied for {path}]"

    return "\n".join(output)

def _process_file(file_path: Path, root_path: Path, ignore_patterns: List[str]) -> Optional[str]:
    """
    Helper function to process a single file's content with path relative to root.
    
    Args:
        file_path: Path to the file
        root_path: Root directory for relative paths
        ignore_patterns: Patterns to ignore
    
    Returns:
        Formatted file content string or None if skipped
    """
    rel_path = file_path.relative_to(root_path)  # 使用 root_path 而非 base_path

    if any(fnmatch.fnmatch(file_path.name, pattern) for pattern in ignore_patterns):
        return None

    try:
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type and "text" not in mime_type:
            return None

        with open(file_path, 'rb') as test_file:
            chunk = test_file.read(8192)
            if b'\0' in chunk:
                return None

        with open(file_path, 'r', encoding='utf-8') as infile:
            content = infile.read()
        
        return f"\n====\nFile: {rel_path}\n----\n\n{content}\n"
                
    except UnicodeDecodeError:
        logger.warning(f"Skipped non-UTF-8 file: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error processing {file_path}: {str(e)}")
        return None

def process_directories(
    directories: List[str],
    root_directory: str,
    output_file: str = "output.txt",
    ignore_patterns: Optional[List[str]] = None,
    force_overwrite: bool = False,
    show_progress: bool = False
) -> None:
    """
    Process all files in multiple directories and their subdirectories.
    
    Args:
        directories: List of directories to process files from
        root_directory: The root directory for generating tree structure and relative paths
        output_file: The output file path
        ignore_patterns: List of patterns to ignore (supports fnmatch wildcards)
        force_overwrite: Whether to overwrite existing output file
        show_progress: Whether to show a progress bar
    """
    if ignore_patterns is None:
        ignore_patterns = [
            ".git", "__pycache__", "*.pyc", "*.pyo", "*.pyd",
            ".DS_Store", "*.log", ".venv", "venv",
            "node_modules", "vendor"
        ]

    output_path = Path(output_file)
    if output_path.exists() and not force_overwrite:
        raise FileExistsError(
            f"Output file '{output_file}' already exists. "
            "Use -f/--force to overwrite existing file."
        )

    root_path = Path(root_directory).resolve()
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Write directory tree structure
        outfile.write("Project Directory Structure:\n")
        outfile.write("==========================\n\n")
        outfile.write(root_path.name + "\n")
        tree_structure = generate_tree(root_path, ignore_patterns=ignore_patterns)
        outfile.write(tree_structure)
        outfile.write("\n\n")
        
        # Write file contents section header
        outfile.write("File Contents from Selected Directories:\n")
        outfile.write("===================================\n\n")
        
        # Collect all files from specified directories
        all_files = []
        for directory in directories:
            base_path = Path(directory).resolve()
            if not base_path.exists() or not base_path.is_dir():
                logger.warning(f"Skipping invalid directory: {directory}")
                continue
            for root, dirs, files in os.walk(base_path):
                dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, p) for p in ignore_patterns)]
                for file in files:
                    file_path = Path(root) / file
                    if not any(fnmatch.fnmatch(file, p) for p in ignore_patterns):
                        all_files.append(file_path)

        # Process files in parallel
        with ThreadPoolExecutor() as executor:
            file_contents = list(executor.map(
                lambda f: _process_file(f, root_path, ignore_patterns),
                all_files
            ))

        # Write contents with optional progress bar
        if show_progress:
            for content in tqdm(file_contents, desc="Writing files", unit="file"):
                if content:
                    outfile.write(content)
        else:
            for content in file_contents:
                if content:
                    outfile.write(content)

if __name__ == "__main__":
    process_directories(
        directories=["tests"],
        root_directory=".",
        output_file="output_test.txt",
        force_overwrite=True,
        show_progress=True
    )
