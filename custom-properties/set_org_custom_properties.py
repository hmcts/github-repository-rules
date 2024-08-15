import os
import requests
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# GitHub API base URL
API_BASE = "https://api.github.com"

# Get OAuth token from environment variable
TOKEN = os.environ.get('OAUTH_TOKEN')
if not TOKEN:
    raise ValueError("OAUTH_TOKEN environment variable is not set")

# Your organisation name
ORG_NAME = "hmcts"

# Headers for API requests
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def define_custom_property(org_name):
    """
    Define a custom property for the organisation.

    1. Creates a custom "is_production" property at the organisation level, which is then passed down to the individual repository level.
    2. Sends a PUT request to GitHub's API to create the property.
    3. Defines the property as a boolean (true/false) value.
    4. The JSON file is where all the production repositories are stored, these will then be used to assign custom properties to.

    Error Handling:

    1. Checks if the API response status code is not 200.
    2. Logs an error message with the specific reason from the API, or a generic HTTP status code error if no specific message is provided.
    3. Raises an HTTP error if the request was unsuccessful.

    Args:
        org_name (str): The name of the GitHub organisation.

    Returns:
        int: The status code of the API response (200 if successful).

    Raises:
        requests.RequestException: If the API request to GitHub fails.
        
    """

    url = f"{API_BASE}/orgs/{org_name}/properties/schema/is_production"
    data = {
        "value_type": "true_false",
        "required": False,
        "default_value": "",
        "description": "Indicates if the repository is in production",
        "allowed_values": None,  # Set to None as required by API
        "values_editable_by": "org_and_repo_actors"
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code != 200:
        error_message = response.json().get('message', f"HTTP {response.status_code} error")
        logging.error(f"Failed to define custom property for {org_name}: {error_message}")
    response.raise_for_status()
    return response.status_code


def set_custom_properties(repo_full_name, properties):
    """
    1. Sets custom properties for the repositories listed from the JSON file.
    2. Sends a PATCH request to GitHub's API to update the repository's properties.

    Sets the custom properties for a repository.

    Error Handling:
    1. Checks if the API response status code is not 204.
    2. Logs an error message with the specific reason from the API, or a generic HTTP status code error if no specific message can be provided.
    3. Raises an HTTP error if the request was unsuccessful.

    Sets the custom properties for a repository.

    Args:
        repo_full_name (str): The full name of the repository (org/repo).
        properties (dict): The custom properties to set.

    Returns:
        int: The status code of the API response.

    Raises:
        requests.RequestException: If the API request fails.

    """

    owner, repo = repo_full_name.split('/')
    url = f"{API_BASE}/repos/{owner}/{repo}/properties/values"
    data = {
        "properties": [
            {"property_name": key, "value": value}
            for key, value in properties.items()
        ]
    }
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code != 204:
        error_message = response.json().get('message', f"HTTP {response.status_code} error")
        logging.error(f"Failed to set properties for {repo_full_name}: {error_message}")
    response.raise_for_status()
    return response.status_code

def get_custom_properties(repo_full_name):
    """
    Get custom properties for a repository.

    1. Retrieves the current custom properties of the repositories.
    2. Sends a GET request to GitHub's API for the specific repository.
    3. Returns the custom properties as a JSON object.

    Args:
        repo_full_name (str): The full name of the repository (org/repo).

    Returns:
        dict: The custom properties of the repository.

    Raises:
        requests.RequestException: If the API request fails.

    """

    owner, repo = repo_full_name.split('/')
    url = f"{API_BASE}/repos/{owner}/{repo}/properties/values"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def load_production_repos():
    """
    1. Loads a list of production repositories from a JSON file.
    2. Reads from the production-repos.json.
    3. Parses the JSON content and returns it as a list.


    Error Handling:
    1. Handles FileNotFoundError by logging an error if the JSON file is not found, including the expected file path and current directory contents.
    2. Handles JSONDecodeError by logging an error if the JSON file cannot be parsed correctly, including the specific error encountered.
    
    """

    script_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(script_dir, '../production-repos.json')
    
    try:
        with open(json_file_path, 'r') as f:
            repos = json.load(f)
            return repos
    except FileNotFoundError:
        logging.error(f"Error: 'production-repos.json' not found at {os.path.abspath(json_file_path)}")
        logging.error("Contents of the current directory: %s", os.listdir('.'))
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {json_file_path}: {e}")
        raise


# Define the custom property at the organisation level
try:
    status = define_custom_property(ORG_NAME)
    logging.info(f"Defined custom property for {ORG_NAME}: Status {status}")
except requests.RequestException as e:
    logging.error(f"Failed to define custom property for {ORG_NAME}: {str(e)}")

# Load production repositories
production_repos = load_production_repos()

logging.info(f"Repositories found in production-repos.json:")
for repo in production_repos:
    logging.info(f"- {repo}")

# Apply custom properties to each repository and verify
for repo_name in production_repos:
    repo_full_name = f"{ORG_NAME}/{repo_name}"
    custom_properties = {
        "is_production": "true"
    }

    logging.info(f"\nSetting custom property for: {repo_name}")
    try:
        status = set_custom_properties(repo_full_name, custom_properties)
        logging.info(f"Set properties for {repo_full_name}: Status {status}")

        # Verify the properties were set correctly
        retrieved_properties = get_custom_properties(repo_full_name)
        logging.info(f"Custom properties for {repo_full_name}: {retrieved_properties}")

    except requests.RequestException as e:
        logging.error(f"Failed to set properties for {repo_full_name}: {str(e)}")

logging.info("\nScript execution completed.")