from datetime import timedelta, datetime
from os import getenv

import requests

access_token = getenv('GITHUB_ACCESS_TOKEN')
headers = {'Authorization': "Bearer " + access_token, 'Accept': 'application/vnd.github+json',
           'X-GitHub-Api-Version': '2022-11-28'}
company_repo = getenv('REPOSITORY_OWNER_NAME')
default_branch_name = 'main'


def main():
    all_repos = fetch_all_repos()

    # TODO: getting any repo to test
    example_repo_name = all_repos[3]['name']

    default_branch_sha = get_default_branch_sha(example_repo_name)
    if not default_branch_sha:
        print("Default branch not found.")
        return

    commits = fetch_commits_from_branch(example_repo_name, default_branch_sha)
    calculate_deployment_frequency(commits)


def fetch_all_repos() -> list[dict]:
    """Fetch all repositories for the company."""
    url = f'https://api.github.com/orgs/{company_repo}/repos'
    response = requests.get(url, headers=headers).json()
    return response


def get_default_branch_sha(repo_name: str) -> str | None:
    """Get the SHA of the default branch for the given repository."""
    branches_url = f'https://api.github.com/repos/{company_repo}/{repo_name}/branches'
    branches_response = requests.get(branches_url, headers=headers).json()

    for branch in branches_response:
        if branch['name'] == default_branch_name:
            return branch['commit']['sha']
    return None


def fetch_commits_from_branch(repo_name: str, branch_sha: str) -> list[str]:
    """Fetch commits from the given branch."""
    commits = []
    current_sha = branch_sha

    while current_sha:
        commit_data = get_commit(repo_name, current_sha)
        if not commit_data or 'parents' not in commit_data or not commit_data['parents']:
            break

        commits.append(commit_data['author']['date'])
        current_sha = commit_data['parents'][0]['sha']

    return commits


def get_commit(repo_name: str, sha: str) -> dict:
    """Get commit details for a specific SHA."""
    commit_url = f'https://api.github.com/repos/{company_repo}/{repo_name}/git/commits/{sha}'
    return requests.get(commit_url, headers=headers).json()


def calculate_deployment_frequency(deployment_dates_raw: list[str]):
    """Calculate and print the deployment frequency based on commit dates."""
    if not deployment_dates_raw:
        print("No deployment dates provided.")
        return

    # Convert string dates to datetime objects
    deployment_dates: list[datetime] = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ") for date in deployment_dates_raw]
    deployment_dates.sort()

    # Filter deployment dates by time range
    now = datetime.utcnow()
    time_ranges = {
        'last_30_days': now - timedelta(days=30),
        'last_60_days': now - timedelta(days=60),
        'last_90_days': now - timedelta(days=90),
        'last_360_days': now - timedelta(days=360)
    }

    for label, start_date in time_ranges.items():
        filtered_dates = [date for date in deployment_dates if date >= start_date]
        print(f'filtered dates:{filtered_dates}')
        calculate_and_print_frequency(filtered_dates, label)


def calculate_and_print_frequency(deployment_dates: list[datetime], label: str):
    """Calculate and print the deployment frequency for a given list of deployment dates."""
    if not deployment_dates:
        print(f"No deployments in {label}.")
        return

    # Calculate the time spans between commits
    time_spans = [deployment_dates[i] - deployment_dates[i - 1] for i in range(1, len(deployment_dates))]

    if not time_spans:
        print(f"Not enough commits to determine frequency in {label}.")
        return

    # Calculate the average time span between commits
    average_time_span = sum(time_spans, timedelta()) / len(time_spans)

    # Determine deployment frequency
    if average_time_span <= timedelta(days=1):
        print(f"High deployment frequency in {label}: On-demand - multiple deployments per day")
    elif timedelta(days=1) < average_time_span <= timedelta(days=7):
        print(f"Medium deployment frequency in {label}: One deployment per week to one per month")
    else:
        print(f"Low deployment frequency in {label}: One deployment per month to one every six months")


if __name__ == '__main__':
    print('Getting repos...')
    main()
