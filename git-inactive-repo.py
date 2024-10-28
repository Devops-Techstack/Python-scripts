#In this video, we'll walk through a powerful Python script that interacts with the GitHub API to help you manage your
# repositories efficiently. Do you have repositories that are collecting dust? 
# This script identifies all your GitHub repositories that haven't been modified in the last 30 days, 
# allowing you to easily spot stale projects and clean up your account.

#What You'll Learn:

#How to authenticate with the GitHub API using a Personal Access Token.
#The process of fetching your repositories and checking their last modified dates.
#Techniques to filter and display repositories that need attention.

#Code Highlights:
#Utilizing the requests library for API calls.
#Working with Python's datetime module to calculate date differences.
#Easy-to-understand code that you can adapt to your own needs!

#import is a keyword used to bring in external modules or packages into your script.
#requests and datetime are modules used to handle HTTP requests and date-time manipulations.
import requests
from datetime import datetime, timedelta

#To interact with your git repo, you need to generate the Personal Access token for authentication with git under the
#developer settings options and also your github username is required .
# Replace 'your_github_token_here' with your GitHub Personal Access Token
GITHUB_TOKEN = ''
# Replace 'your_github_username_here' with your GitHub username
GITHUB_USERNAME = ''

# GitHub API URL: It is the endpoint used to interact with GitHub’s REST API.
GITHUB_API_URL = f'https://api.github.com/users/{GITHUB_USERNAME}/repos'

#In the context of interacting with the GitHub API (or many other APIs), setting headers 
#with the token for authentication means including a security credential (the token) in the HTTP request headers.
# Set headers with the token for authentication
headers = {
    'Authorization': f'token {GITHUB_TOKEN}'
}

# Calculate the date 30 days ago
thirty_days_ago = datetime.now() - timedelta(days=30)
#print(thirty_days_ago)
# Defining Function to get the repos which are not modified from last 30 days.
def get_repos_not_modified_in_last_30_days():
    #It is using the requests library to send an HTTP GET request to the specified GITHUB_API_URL with the headers provided
    response = requests.get(GITHUB_API_URL, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        #Is converting the API response from JSON format into a Python dictionary or list, 
        # allowing you to easily work with the data.
        repos =  response.json()
        inactive_repos = []
        
        #Iterating through all the repos
        for repo in repos:
            #This allows you to perform date-based operations, such as comparisons and calculations.
            last_modified = datetime.strptime(repo['pushed_at'], '%Y-%m-%dT%H:%M:%SZ') 
            #print("last modified date and time",last_modified)
            #print("before 30 days ago datetime",thirty_days_ago)
            if last_modified < thirty_days_ago:
                inactive_repos.append(repo['name'])
        
        if inactive_repos:
            print("Repositories not modified in the last 30 days:")
            for repo_name in inactive_repos:
                print(f"- {repo_name}")
        else:
            print("All repositories have been modified in the last 30 days.")
    else:
        print(f"Failed to retrieve repositories: {response.status_code}")

# Run the function
get_repos_not_modified_in_last_30_days()
#response.json
