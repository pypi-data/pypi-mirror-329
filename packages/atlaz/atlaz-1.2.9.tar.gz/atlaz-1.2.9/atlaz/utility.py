import json
import os
from pathlib import Path
import tiktoken

from atlaz.old_overview.main_overview import gather_repository

def count_tokens(string_inp):
    encc = tiktoken.encoding_for_model("gpt-4")
    encoded_str = encc.encode(string_inp)
    return len(encoded_str)

def build_code_prompt(file_contents: list[dict]):
    output_text = '\n'
    for file in file_contents:
        output_text += f'```{file["name"]}\n{file["content"]}\n```\n\n\n'
    return output_text[:-2]

def manual_overview(focus_directories: list[str] = None, manual_ignore_files: list[str] = None):
    from pathlib import Path
    # __file__ is something like MyPackage/atlaz/utility.py
    current_script = Path(__file__).resolve()
    # Define the project root as the parent of the current package folder.
    # For example, if current_script is in MyPackage/atlaz, then project_root becomes MyPackage.
    project_root = current_script.parent.parent

    # If no focus directories are provided, we want to scan the entire project root.
    if not focus_directories:
        # Use the relative path "." (i.e. the project root itself)
        focus_directories = ["."]
        # Set the script_path to project_root so that gather_repository works relative to it.
        script_path = project_root
    else:
        # Otherwise, use the default behavior (relative to the current file's directory)
        script_path = current_script.parent

    # Set default ignore list if none is provided.
    if manual_ignore_files is None:
        manual_ignore_files = ['env', 'dist', 'build', '.eggs']

    # Gather the repository data and directory tree.
    directory_data, directory_structure = gather_repository(
        script_path=script_path,
        focus_directories=focus_directories,
        manual_ignore_files=manual_ignore_files
    )

    # Remove the absolute project root prefix from the directory tree,
    # so that the tree is displayed relative to the project root.
    project_root_str = str(project_root.resolve())
    directory_structure = directory_structure.replace(project_root_str + "/", "")

    prompt = directory_structure + "\n\n" + build_code_prompt(directory_data)
    return prompt

def analyse_codebase(focus_directories: list[str], manual_ignore_files: list[str]) -> str:
    """
    Scans the repository using the given focus directories and ignore files.
    
    Returns a string report containing:
      1. A list of scripts (files) that are longer than 150 lines with their line counts.
      2. A list of folders that contain more than 6 items (files or subdirectories),
         excluding standard ignored items (e.g. '__init__.py' and '__pycache__').
    """
    # Part 1: Gather file data as before.
    directory_data, _ = gather_repository(
        script_path=Path(__file__).resolve().parent,
        focus_directories=focus_directories,
        manual_ignore_files=manual_ignore_files
    )
    
    # Analyze files longer than 150 lines.
    long_files = []
    for file in directory_data:
        line_count = len(file["content"].splitlines())
        if line_count > 150:
            long_files.append(f"{file['name']}: {line_count} lines")
    
    # Part 2: Analyze folders with more than 6 items.
    # Define the set of ignored names.
    ignore_set = {"__init__.py", "__pycache__"}
    folders_info = []
    
    for focus_dir in focus_directories:
        focus_path = Path(focus_dir)
        # Skip if the focus item is a file.
        if focus_path.is_file():
            continue
        
        # Walk through the directory tree.
        for root, dirs, files in os.walk(focus_path):
            # Remove ignored directories from further traversal.
            dirs[:] = [d for d in dirs if d not in ignore_set]
            # If the current folder itself should be ignored, skip it.
            if Path(root).name in ignore_set:
                continue

            # Combine subdirectories and files, then filter out ignored items.
            items = dirs + files
            filtered_items = [item for item in items if item not in ignore_set]
            if len(filtered_items) > 6:
                # Get folder path relative to the focus directory for clarity.
                try:
                    rel_path = Path(root).relative_to(focus_path)
                except ValueError:
                    rel_path = Path(root)
                folder_name = str(rel_path) if str(rel_path) != "." else focus_dir
                folders_info.append(f"Folder '{folder_name}': {len(filtered_items)} items")
    
    # Build the final report.
    report_lines = []
    if long_files:
        report_lines.append("Files longer than 150 lines:")
        report_lines.extend(long_files)
    else:
        report_lines.append("No files longer than 150 lines found.")
    
    if folders_info:
        report_lines.append("\nFolders with more than 6 items:")
        report_lines.extend(folders_info)
    else:
        report_lines.append("\nNo folders with more than 6 items found.")
    
    return "\n".join(report_lines)