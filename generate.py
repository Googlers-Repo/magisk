import os, shutil, sys, json
from git import Repo
from random import random
from github import Github
import github
from github.Repository import Repository
from datetime import datetime
import ini

# Configuration
REPO_NAME = os.environ['REPO_NAME']
REPO_TITLE = os.environ['REPO_TITLE']
REPO_WEBSITE = os.environ['REPO_WEBSITE']
REPO_SUPPORT = os.environ['REPO_SUPPORT']
REPO_DONATE = os.environ['REPO_DONATE']
REPO_SUBMIT_MODULE = os.environ['REPO_SUBMIT_MODULE']
REPO_SCOPE = os.environ['REPO_SCOPE']
REPO_EXTRA_TRACKS = os.environ['REPO_EXTRA_TRACKS']

# Initialize the GitHub objects
GIT_TOKEN = os.environ['GIT_TOKEN']
g = Github(GIT_TOKEN)
user = g.get_user(REPO_NAME)
repos = user.get_repos()

fverified = open('verified.json')
verified = json.load(fverified)

f_user_verified = open('user_verified.json')
user_verified = json.load(f_user_verified)

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

def does_object_exists(repo: Repository, object_path: str) -> bool:
    try:
        repo.get_contents(object_path)
        return True
    except github.UnknownObjectException:
        return False

def get_mmrl_json(repo: Repository, key: str, default: str | None) -> str | None:
    try:
        jsonfile = repo.get_contents("mmrl.json")
        jsonfile_raw = jsonfile.decoded_content.decode("UTF-8")
        return json.loads(jsonfile_raw)[key]
    except:
        return default

def get_user(username: str | None):
    if not (username is None):
        _user = g.get_user(username)
        return {
            "name": _user.login,
            "avatar": _user.avatar_url,
            "bio": _user.bio,
            "followers": _user.followers,
            "verified": _user.login in user_verified,
        }
    else:
        return None

def get_contri(usernames: any):
    if not (usernames is None):
        contributors = []
        for username in usernames:
            try:
                contributors.append(get_user(username))
            except:
                continue
        return contributors
    else:
        return None


def make_module_json(repo: Repository):
    if does_object_exists(repo, "module.prop"):
        moduleprop = repo.get_contents("module.prop")
        moduleprop_raw = moduleprop.decoded_content.decode("UTF-8")

        properties = ini.parse(moduleprop_raw)

        # Get the last update timestamp of the module.prop file
        last_update_timestamp = moduleprop.last_modified

        # Convert the string to a datetime object
        last_update_datetime = datetime.strptime(last_update_timestamp, '%a, %d %b %Y %H:%M:%S %Z')

        # Get the timestamp of the last update
        last_update_timestamp = datetime.timestamp(last_update_datetime)

        mod_id = properties.get("id")

        module = {
            "id": mod_id,
            "name": properties.get("name"),
            "author": properties.get("author"),
            "description": get_mmrl_json(repo, "description", properties.get("description")),
            "version": properties.get("version"),
            "versionCode": properties.get("versionCode"),
            "download": f"https://github.com/{repo.full_name}/archive/{repo.default_branch}.zip",
            # Check if META-INF folder exists, which is required to install modules
            "valid": does_object_exists(repo, "META-INF"),
            "verified": mod_id in verified,
            "updateJson": properties.get("updateJson"),
            "last_update": int(last_update_timestamp * 1000),
            "readme": f"https://raw.githubusercontent.com/{repo.full_name}/{repo.default_branch}/README.md",
            "stars": int(repo.stargazers_count),
            "about": {
                "repo_source": REPO_TITLE,
                # "license": repo.license.spdx_id if not repo.license == None else None,
                "language": repo.language,
                "source": repo.clone_url,
                "issues": f"{repo.html_url}/issues" if repo.has_issues else None,
            },
            "mmrl": {
                "author": get_user(get_mmrl_json(repo, "author", None)),
                "contributors": get_contri(get_mmrl_json(repo, "contributors", None)),
                "cover": get_mmrl_json(repo, "cover", None),
                "logo": get_mmrl_json(repo, "logo", None),
                "screenshots": get_mmrl_json(repo, "screenshots", None),
                "categories": get_mmrl_json(repo, "categories", None),
                "require": get_mmrl_json(repo, "require", None)
            },
            "fox": {
                "minApi": properties.get("minApi"),
                "maxApi": properties.get("maxApi"),
                "minMagisk": properties.get("minMagisk"),
                "needRamdisk": properties.get("needRamdisk"),
                "support": properties.get("support"),
                "donate": properties.get("donate"),
                "config": properties.get("config"),   
                "changeBoot": properties.get("changeBoot"),
                "mmtReborn": properties.get("mmtReborn"),
            },
        }

        # Handle file to ignore the index process for the current module
        if not (properties.get("noIndex") or properties.get("gr_ignore")):
            # Append to skeleton
            meta.get("modules").append(module)

if not REPO_NAME == "":
    # Iterate over all public repositories
    for repo in repos:
        try:
            make_module_json(repo)
        except:
            continue

if not REPO_EXTRA_TRACKS  == "":
    input_file = open(f"{REPO_EXTRA_TRACKS}.json")
    json_array = json.load(input_file)

    for item in json_array:
        try:
            user = g.get_user(item["user"])
            repo = user.get_repo(item["repo"])
            make_module_json(repo)
        except:
            continue

# Return our final skeleton
f = open(f"{REPO_SCOPE}.json", "w")
f.write(json.dumps(meta, indent=4))
f.close()
fverified.close()
f_user_verified.close()
