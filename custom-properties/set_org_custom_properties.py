import os
import requests
import json

# GitHub API base URL
API_BASE = "https://api.github.com"

# Get OAuth token from environment variable
TOKEN = os.environ.get('OAUTH_TOKEN')
if not TOKEN:
    raise ValueError("OAUTH_TOKEN environment variable is not set")

# Your organization name
ORG_NAME = "hmcts-test"

# Headers for API requests
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def define_custom_property(org_name):
    """
    Define a custom property for the organization.
    """
    url = f"{API_BASE}/orgs/{org_name}/properties/schema/is_production"
    data = {
        "value_type": "true_false",
        "required": False,
        "default_value": "",
        "description": "Indicates if the repository is in production",
        "allowed_values": None,
        "values_editable_by": "org_and_repo_actors"
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"Failed to define custom property for {org_name}: {response.json().get('message', 'Unknown error')}")
    response.raise_for_status()
    return response.status_code

def get_org_repos(org_name):
    """
    Get all repositories in the organization.
    """
    url = f"{API_BASE}/orgs/{org_name}/repos"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def set_custom_properties(repo_full_name, properties):
    """
    Set custom properties for a repository.
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
        print(f"Failed to set properties for {repo_full_name}: {response.json().get('message', 'Unknown error')}")
    response.raise_for_status()
    return response.status_code

def get_custom_properties(repo_full_name):
    """
    Get custom properties for a repository.
    """
    owner, repo = repo_full_name.split('/')
    url = f"{API_BASE}/repos/{owner}/{repo}/properties/values"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def load_production_repos():
    """
    Load production repositories from production-repos.json file.
    """
    # The file is in the same directory as the script, so we don't need to change directories
    json_file_path = '../production-repos.json'
    
    try:
        with open(json_file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: 'production-repos.json' not found at {os.path.abspath(json_file_path)}")
        print("Current working directory:", os.getcwd())
        print("Contents of the current directory:")
        print(os.listdir('.'))
        raise
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {json_file_path}: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error reading {json_file_path}: {e}")
        raise

# Define the custom property at the organization level
try:
    status = define_custom_property(ORG_NAME)
    print(f"Defined custom property for {ORG_NAME}: Status {status}")
except requests.RequestException as e:
    print(f"Failed to define custom property for {ORG_NAME}: {str(e)}")

# Get all repositories in the organization
try:
    repos = get_org_repos(ORG_NAME)
except requests.RequestException as e:
    print(f"Failed to get repositories for {ORG_NAME}: {str(e)}")
    repos = []

# Load production repositories
production_repos = load_production_repos()

print(f"Repositories found in production-repos.json:")
for repo in production_repos:
    print(f"- {repo}")

# Apply custom properties to each repository and verify
repo_ids = []
for repo_name in production_repos:
    repo_full_name = f"{ORG_NAME}/{repo_name}"
    custom_properties = {
        "is_production": "true"
    }

    print(f"\nSetting custom property for: {repo_name}")
    try:
        status = set_custom_properties(repo_full_name, custom_properties)
        print(f"Set properties for {repo_full_name}: Status {status}")

        # Verify the properties were set correctly
        retrieved_properties = get_custom_properties(repo_full_name)
        print(f"Custom properties for {repo_full_name}: {retrieved_properties}")

        # Get repository ID
        for repo in repos:
            if repo["name"] == repo_name:
                repo_ids.append(repo["id"])

    except requests.RequestException as e:
        print(f"Failed to set properties for {repo_full_name}: {str(e)}")

print("\nScript execution completed.")