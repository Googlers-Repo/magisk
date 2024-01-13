import os, shutil, sys, json
import functools
import time 
import ini
from git import Repo, InvalidGitRepositoryError, GitCommandError
from random import random
from github import Github
from github.Repository import Repository
from datetime import datetime
from pathlib import Path
from typing import Optional

# Configuration
REPO_NAME = os.environ.get('NAME')
REPO_TITLE = os.environ.get('TITLE')
REPO_WEBSITE = os.environ.get('WEBSITE')
REPO_SUPPORT = os.environ.get('SUPPORT')
REPO_DONATE = os.environ.get('DONATE')
REPO_SUBMIT_MODULE = os.environ.get('SUBMIT_MODULE')
REPO_SCOPE = os.environ.get('SCOPE')
REPO_EXTRA_TRACKS = os.environ.get('EXTRA_TRACKS')

# Initialize the GitHub objects
GIT_TOKEN = os.environ.get('GITHUB_TOKEN')
g = Github(GIT_TOKEN)
user = g.get_user(REPO_NAME)
repos = user.get_repos()

REPO_VERIFIED_MODULES = os.environ.get('VERIFIED_MODULES', "metadata/verified_modules.json")
REPO_VERIFIED_USERS = os.environ.get('VERIFIED_USERS', "metadata/verified_users.json")

# Check if verified modules and users exists
if REPO_VERIFIED_MODULES and os.path.isfile(REPO_VERIFIED_MODULES):
    f_verified_modules = open(REPO_VERIFIED_MODULES)
    verified_modules = json.load(f_verified_modules)
    f_verified_modules.close()
else:
    verified_modules = []

if REPO_VERIFIED_USERS and os.path.isfile(REPO_VERIFIED_USERS):
    f_verified_users = open(REPO_VERIFIED_USERS)
    verified_users = json.load(f_verified_users)
    f_verified_users.close()
else:
    verified_users = []

# Skeleton for the repository
meta = {
    # Fetch the last repository update
    "last_update": int(time.time() * 1000),
    "name": REPO_TITLE,
    "website": REPO_WEBSITE,
    "support": REPO_SUPPORT,
    "donate": REPO_DONATE,
    "submitModule": REPO_SUBMIT_MODULE,
    "modules": []
}

def clone_and_zip(url: str, out: Path):
    repo_dir = out.with_suffix("")
    #if repo_dir.exists():
        #shutil.rmtree(repo_dir)

    try:
        repo = Repo.clone_from(url, repo_dir)
    except GitCommandError:
       # shutil.rmtree(repo_dir, ignore_errors=True)
        raise GitCommandError(f"clone failed: {url}")

  #  for path in repo_dir.iterdir():
#        if path.name.startswith(".git"):
#            if path.is_dir():
#                shutil.rmtree(path, ignore_errors=True)
#            if path.is_file():
#                path.unlink(missing_ok=True)

#            continue

    try:
        shutil.make_archive(repo_dir.as_posix(), format="zip", root_dir=repo_dir)
        #shutil.rmtree(repo_dir)
    except FileNotFoundError:
        raise FileNotFoundError(f"archive failed: {repo_dir.as_posix()}")

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
            "verified": _user.login in verified_users,
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
            "verified": mod_id in verified_modules,
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
                "require": get_mmrl_json(repo, "require", None),
                "developerNote": get_mmrl_json(repo, "developerNote", None),
                "supportedRoots": properties.get("supportedRoots"),
                "minKernelSU": properties.get("minKernelSU"),
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

        # clone_and_zip(f"{repo.html_url}.git", Path(f"modules/{REPO_SCOPE}/{mod_id}.zip"))
        
        # Handle file to ignore the index process for the current module
        if not (properties.get("noIndex") or properties.get("gr_ignore")):
            # Append to skeleton
            meta.get("modules").append(module)

if REPO_NAME:
    # Iterate over all public repositories
    for repo in repos:
        try:
            make_module_json(repo)
        except:
            continue

if REPO_EXTRA_TRACKS and os.path.isfile(f"{REPO_EXTRA_TRACKS}.json"):
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
