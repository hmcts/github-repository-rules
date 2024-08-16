import os
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# File paths
script_dir = os.path.dirname(__file__)
JSON_FILE_PATH = os.path.join(script_dir, '../production-repos.json')
README_FILE_PATH = os.path.join(script_dir, '../ReadMe.md')

def load_repos(file_path):
    """
    Load repositories from the given JSON file.

    1. Opens and reads the JSON file from the path above.
    2. Parses the JSON content and ensures it is a list.
    3. Returns the list of repositories.

    Error Handling:

    1. Logs an error if the file is not found at the path specified above.

    Args:
        file_path: The path to the JSON file containing the repositories.

    Returns:
        list: A list of repositories parsed from the JSON file.

    Raises:
        FileNotFoundError: If the JSON file path is not found.
        ValueError: If the JSON content is not a list.
        json.JSONDecodeError: If the JSON file contains invalid JSON.

    """
    try:
        with open(file_path, 'r') as f:
            repos = json.load(f)
            if not isinstance(repos, list):
                raise ValueError("JSON content is not a list")
            return repos
    except FileNotFoundError:
        logging.error(f"Error: '{file_path}' not found.")
        raise

def update_readme(prod_count, dev_count, prod_link):
    """
    Update the README file with a count displayed of the number of production repositories as custom properties can't be searched by in GitHub.

    1. Reads the existing README file content.
    2. Updates the section between markers with new repository counts.
    3. Writes the updated content back to the README file.

    Error Handling:

    1. Prints "Failed to update README file" if the README file cannot be found at the path we defined above.

    Args:
        1. prod_count: This integer is the number of production repositories.
        2. dev_count: The number of development repositories.
        3. prod_link: The file path to the production repositories JSON file.
    
    """
    try:
        with open(README_FILE_PATH, 'r') as file:
            readme_content = file.readlines()

        table_content = f"""
| **Repository Type**       | **Count** |
|---------------------------|-----------|
| Production Repositories   | [{prod_count}]({prod_link})        |
| Development Repositories  | {dev_count}        |
"""
        start_marker = "<!--START_PRODUCTION_COUNT-->"
        end_marker = "<!--END_PRODUCTION_COUNT-->"
        start_index = None
        end_index = None

        for i, line in enumerate(readme_content):
            if start_marker in line:
                start_index = i
            if end_marker in line:
                end_index = i

        if start_index is not None and end_index is not None:
            readme_content = (
                readme_content[:start_index + 1]
                + [table_content]
                + readme_content[end_index:]
            )
        else:
            readme_content.append(f"\n{start_marker}\n{table_content}\n{end_marker}\n")

        with open(README_FILE_PATH, 'w') as file:
            file.writelines(readme_content)
    except Exception as e:
        logging.error(f"Failed to update README file: {str(e)}")
        raise

# Load production repositories
try:
    production_repos = load_repos(JSON_FILE_PATH)
    production_count = len(production_repos)
    logging.info(f"Number of production repositories: {production_count}")
    
    # Placeholder value for dev repo count, can be updated similarly
    development_count = 0  # Update this to load actual data if available
    
    # Local link to the production-repos.json file
    prod_link = "../production-repos.json"
    
    update_readme(production_count, development_count, prod_link)
except Exception as e:
    logging.error(f"Failed to load or update repositories: {str(e)}")