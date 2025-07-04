import sys
import urllib.request
import urllib.error
import json

RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

def fetch_github_events(username):
    url = f"https://api.github.com/users/{username}/events"
    request = urllib.request.Request(url, headers={"User-Agent": "python-cli"})

    try:
        with urllib.request.urlopen(request) as response:
            if response.status != 200:
                print(f"Failed to fetch data. Status code: {response.status}")
                return

            data = response.read().decode('utf-8')
            events = json.loads(data)
            if not events:
                print("No recent public activity found.")
            else:
                print("API call was successful")
                display_events(events)

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("GitHub user not found")
        else:
            print(f"HTTP error: {e}")
    except urllib.error.URLError as e:
        print(f"Network error: {e}")

def display_events(events):
    for event in events[:10]:
        event_type = event["type"]
        repo_name = event["repo"]["name"]

        if event_type == "PushEvent":
            commit_count = len(event["payload"]["commits"])
            print(f"{GREEN}- Pushed {commit_count} commit(s) to {repo_name}{RESET}")
        elif event_type == "WatchEvent":
            print(f"{YELLOW}- Starred {repo_name}{RESET}")
        elif event_type == "IssuesEvent":
            action = event["payload"]["action"]
            print(f"{YELLOW}- {action.capitalize()} an issue in {repo_name}{RESET}")
        elif event_type == "PullRequestEvent":
            action = event["payload"]["action"]
            print(f"{CYAN}- {action.capitalize()} a pull request in {repo_name}{RESET}")
        else:
            print(f"- {event_type} in {repo_name}")

def main():
    if len(sys.argv) != 2:
        print("Usage: github-activity <github username>")
        sys.exit(1)

    username = sys.argv[1]
    fetch_github_events(username)

if __name__ == "__main__":
    main()
