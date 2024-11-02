                                                            # Description
# This Python script automates the management of repository access within a GitHub organization. It performs the following tasks:

# Retrieve All Repositories: The script connects to the GitHub API to fetch a comprehensive list of all repositories under a specified organization, ensuring that you have an up-to-date overview of your projects.

# List Collaborators: For each repository, the script retrieves the list of collaborators, providing insights into who has access to each project. This is crucial for maintaining security and access control within the organization.

# Remove Access for Specific User: The script checks if a user named "Sandy" is listed as a collaborator on any repository. If found, it automatically removes her access, streamlining the process of managing user permissions and ensuring compliance with organizational policies.

# This script is particularly useful for organizations undergoing personnel changes, ensuring that access rights are promptly updated to reflect current team members.
#The requests library provides various methods like get(), post(), put(), and delete() to interact with APIs.
import requests

# Constants
GITHUB_API_URL = "https://api.github.com"
GITHUB_USERNAME = "Devops-Techstack"  # Replace with your GitHub organization name
TOKEN = ""  # Replace with your GitHub token
USER_TO_REMOVE = "yaswant24"  # User to be removed

#Get all the repository list in your organization
def get_repositories():
    """Get all repositories in the organization."""
    url = f'https://api.github.com/users/{GITHUB_USERNAME}/repos'
    #Call the REST API 
    response = requests.get(url, auth=('username', TOKEN))  # Replace 'username' with your GitHub username
    #If response code is 200 , your call is success
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve repositories: {response.status_code} - {response.text}")
        return []

#Now for each repo you got from above function , you need to get the colloborator .
def get_collaborators(repo_name):
    """Get all collaborators for a specific repository."""
    url = f"{GITHUB_API_URL}/repos/{GITHUB_USERNAME}/{repo_name}/collaborators"
    #Again calling the REST API endpoint for collaborators
    response = requests.get(url, auth=('username', TOKEN))  # Replace 'username' with your GitHub username
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve collaborators for {repo_name}: {response.status_code} - {response.text}")
        return []

#Defining the function to remove access for the user who have resigned from organization
def remove_user_from_repo(repo_name, username):
    """Remove a user from a specific repository."""
    url = f"{GITHUB_API_URL}/repos/{GITHUB_USERNAME}/{repo_name}/collaborators/{username}"
    response = requests.delete(url, auth=('username', TOKEN))  # Replace 'username' with your GitHub username
    
    if response.status_code == 204:
        print(f"Successfully removed {username} from {repo_name}.")
    elif response.status_code == 404:
        print(f"{username} not found in {repo_name}.")
    else:
        print(f"Failed to remove {username} from {repo_name}: {response.status_code} - {response.text}")

def main():
    #Calling to get all the repo in your organization
    repos = get_repositories()
    
    if not repos:
        print("No repositories found or failed to retrieve.")
        return
 #Iterating through each repo.
    for repo in repos:
        #Getting each repo name
        repo_name = repo['name']
        print(f"\nRepository: {repo_name}")
        #Getting collaborator output in form of dictionary for each repo
        collaborators = get_collaborators(repo_name)
        #if collaborator is there 
        if collaborators:
            found = False
            #For each collaborator in your repo
            for collaborator in collaborators:
                print(f"- {collaborator['login']}")
                #collaborator['login'] : This accesses the login key from the collaborator dictionary, which represents the username of the collaborator.
                #If collaborator username matches the user you want to remove , we will set found boolean to True
                if collaborator['login'] == USER_TO_REMOVE:
                    found = True
            #if found is True , call  the remove_user_from_repo function with the repo_name and user_to_remove parameters
            if found:
                print(f"Removing access for {USER_TO_REMOVE} from {repo_name}...")
                remove_user_from_repo(repo_name, USER_TO_REMOVE)
        else:
            print("No collaborators found or failed to retrieve.")

if __name__ == "__main__":
    main()
