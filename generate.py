import os, shutil, sys, json
from git import Repo
from random import random
from github import Github
import github
from github.Repository import Repository
from datetime import datetime

# Configuration
REPO_NAME = os.environ['REPO_NAME'] or None
REPO_TITLE = os.environ['REPO_TITLE'] or None
REPO_WEBSITE = os.environ['REPO_WEBSITE'] or None
REPO_SUPPORT = os.environ['REPO_SUPPORT'] or None
REPO_DONATE = os.environ['REPO_DONATE'] or None
REPO_SUBMIT_MODULE = os.environ['REPO_SUBMIT_MODULE'] or None
REPO_SCOPE = os.environ['REPO_SCOPE'] or None

# Initialize the GitHub objects
g = Github(os.environ['GIT_TOKEN'])
user = g.get_user(REPO_NAME)
repos = user.get_repos()

# Skeleton for the repository
meta = {
    # Fetch the last repository update
    "last_update": int(user.updated_at.timestamp() * 1000),
    "name": REPO_TITLE,
    "website": REPO_WEBSITE,
    "support": REPO_SUPPORT,
    "donate": REPO_DONATE,
    "submitModule": REPO_SUBMIT_MODULE,
    "modules": []
}

def convert_value(value):
    # Convert boolean values
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    # Convert integer values
    try:
        return int(value)
    except ValueError:
        # Convert float values
        try:
            return float(value)
        except ValueError:
            # Keep string values as is
            return value

def does_object_exists(repo: Repository, object_path: str) -> bool:
    try:
        repo.get_contents(object_path)
        return True
    except github.UnknownObjectException:
        return False

# Iterate over all public repositories
for repo in repos:
    # It is possible that module.prop does not exist (meta repo)
    try:
        moduleprop = repo.get_contents("module.prop")
        moduleprop_raw = moduleprop.decoded_content.decode("UTF-8")

        if not does_object_exists(repo, "module.prop"):
            continue

        properties = {}
        for line in moduleprop_raw.splitlines():
            if "=" not in line:
                continue
            lhs, rhs = line.split("=", 1)
            properties.update({
               lhs: convert_value(rhs)
            })

        def getprop(name: str):
            if properties.get(name):
                return properties.get(name)
            else:
                return None

        def getprop_split(name: str, sep: str):
            if properties.get(name):
                return properties.get(name).split(sep)
            else:
                return None

        # Get the last update timestamp of the module.prop file
        last_update_timestamp = moduleprop.last_modified

        # Convert the string to a datetime object
        last_update_datetime = datetime.strptime(last_update_timestamp, '%a, %d %b %Y %H:%M:%S %Z')

        # Get the timestamp of the last update
        last_update_timestamp = datetime.timestamp(last_update_datetime)

        module = {
            "id": getprop("id"),
            "name": getprop("name"),
            "version": getprop("version"),
            "versionCode": getprop("versionCode"),
            "author": getprop("author"),
            "description": getprop("description"),
            # Check if META-INF folder exists, which is required to install modules
            "valid": does_object_exists(repo, "META-INF"),
            "download": f"https://github.com/{repo.full_name}/archive/{repo.default_branch}.zip",
            "last_update": int(last_update_timestamp * 1000),
            "readme": f"https://raw.githubusercontent.com/{repo.full_name}/{repo.default_branch}/README.md",
            "stars": int(repo.stargazers_count),
            "about": {
                "source": repo.clone_url,
                "issues": f"{repo.html_url}/issues" if repo.has_issues else None,
            },
            "mmrl": {
                "cover": getprop("mmrlCover"),
                "logo": getprop("mmrlLogo"),
                "screenshots": getprop_split("mmrlScreenshots", ","),
                "categories": getprop_split("mmrlCategories", ","),
            },
            "fox": {
                "minApi": getprop("minApi"),
                "maxApi": getprop("maxApi"),
                "minMagisk": getprop("minMagisk"),
                "needRamdisk": getprop("needRamdisk"),
                "support": getprop("support"),
                "donate": getprop("donate"),
                "config": getprop("config"),   
                "changeBoot": getprop("changeBoot"),
                "mmtReborn": getprop("mmtReborn"),
            },
        }

        # Handle file to ignore the index process for the current module
        if properties.get("noIndex") or properties.get("gr_ignore"):
            continue
        else:
            # Append to skeleton
            meta.get("modules").append(module)

    except:
        continue

# Return our final skeleton
f = open(f"{REPO_SCOPE}.json", "w")
f.write(json.dumps(meta, indent=4))
f.close()
