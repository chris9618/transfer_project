import gitlab

# Initialize the connection to GitLab
GITLAB_URL = 'https://gitlab.com'  # Change this to your GitLab instance URL if different
PRIVATE_TOKEN = 'your_private_token'  # Replace with your private token

gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN)

def migrate_repository(repo_name, target_group):
    # Get the project
    try:
        project = gl.projects.get(repo_name)
    except gitlab.exceptions.GitlabGetError:
        print(f"Project {repo_name} not found.")
        return
    
    # Check if the develop branch exists
    branches = project.branches.list()
    develop_branch_exists = any(branch.name == 'develop' for branch in branches)
    
    if not develop_branch_exists:
        # Create the develop branch from the default branch
        default_branch = project.default_branch
        project.branches.create({'branch': 'develop', 'ref': default_branch})
        print(f"Develop branch created for {repo_name}.")
    else:
        print(f"Develop branch already exists for {repo_name}.")
    
    # Transfer project to the target group
    try:
        project.transfer(target_group)
        print(f"Project {repo_name} migrated to group {target_group}.")
    except gitlab.exceptions.GitlabTransferError as e:
        print(f"Failed to migrate project: {e}")

if __name__ == "__main__":
    repo_names = [
        'namespace/project1',
        'namespace/project2',
        'namespace/project3'
    ]
    target_group = 'exploratory-group-id-or-path'  # Replace with the actual group ID or full path
    
    for repo_name in repo_names:
        migrate_repository(repo_name, target_group)
