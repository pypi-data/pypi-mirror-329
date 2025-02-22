def create_file_paths_rules_prompt() -> str:
    return _FILE_PATHS_RULES_PROMPT

_FILE_PATHS_RULES_PROMPT = """
## File paths usage

When working with files in your tasks, it is crucial to always use the absolute file path provided to you. This ensures consistency and prevents errors that may arise from using relative paths or incomplete file locations.

1. Always use the entire file_path when referring to the file location.
2. Do not attempt to shorten or modify the path, even if it seems redundant.
3. If you need to perform operations on files in the same directory, still use the full absolute path for each file.

"""