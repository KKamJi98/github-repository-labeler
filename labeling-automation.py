import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# GitHub Personal Access Token
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
# Organization name
ORG_NAME = os.getenv('ORG_NAME')
# Headers for the GitHub API requests
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# Common labels to be added to each repository
COMMON_LABELS = [
    {"name": "🚨 bug", "color": "f29513"},
    {"name": "🎉 enhancement", "color": "a2eeef"},
    {"name": "🔥 feature", "color": "008672"},
    {"name": "💬 question", "color": "d876e3"},
    {"name": "📝 documentation", "color": "008672"},
]

def get_repos(org_name):
    url = f'https://api.github.com/orgs/{org_name}/repos'
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_labels(repo_name):
    url = f'https://api.github.com/repos/{ORG_NAME}/{repo_name}/labels'
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def create_label(repo_name, label):
    url = f'https://api.github.com/repos/{ORG_NAME}/{repo_name}/labels'
    response = requests.post(url, headers=HEADERS, data=json.dumps(label))
    if response.status_code == 201:
        print(f'Successfully created label {label["name"]} in {repo_name}')
    elif response.status_code == 422:
        print(f'Label {label["name"]} already exists in {repo_name}')
    else:
        print(f'Failed to create label {label["name"]} in {repo_name}: {response.content}')

def delete_label(repo_name, label_name):
    url = f'https://api.github.com/repos/{ORG_NAME}/{repo_name}/labels/{label_name}'
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        print(f'Successfully deleted label {label_name} in {repo_name}')
    else:
        print(f'Failed to delete label {label_name} in {repo_name}: {response.content}')
        
def main():
    repos = get_repos(ORG_NAME)
    common_label_names = {label['name'] for label in COMMON_LABELS}
    for repo in repos:
        repo_name = repo['name']
        
        # Get existing labels
        existing_labels = get_labels(repo_name)
        existing_label_names = {label['name'] for label in existing_labels}
        
        # Create common labels if they do not exist
        for label in COMMON_LABELS:
            if label['name'] not in existing_label_names:
                create_label(repo_name, label)
        
        # Delete labels that are not in the common labels list
        for label_name in existing_label_names:
            if label_name not in common_label_names:
                delete_label(repo_name, label_name)

if __name__ == '__main__':
    main()
