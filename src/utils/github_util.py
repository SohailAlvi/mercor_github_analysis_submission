import os
import re
import shutil
import logging
from git import Repo
from requests import get


"""
example: https://api.github.com/users/sohailalvi/repos
"""


class GithubUtil:

    def __init__(self):
        self.regex_username = re.compile("(?:http?:\/\/|https?:\/\/)?(?:www\.)?github\.com\/(?:\/*)([\w\-\.\/]*)")

    def fetch_repositories(self, git_user_url: str) -> list:
        repository_list = list()
        logging.info(f"Extracting git username from {git_user_url}.")
        git_username = self.regex_username.findall(git_user_url)[0]
        git_url = f"https://api.github.com/users/{git_username}/repos"
        try:
            response = get(git_url)
            for _, repository in enumerate(response.json()):
                if os.path.exists(f"cloned/{repository['full_name']}"):
                    shutil.rmtree(f"cloned/{repository['full_name']}", ignore_errors=False)
                Repo.clone_from(repository['html_url'], f"cloned/{repository['full_name']}")
                repository_list.append(repository['html_url'])
        except Exception as e:
            logging.error(f"Exception occurred while fetching list of repositories from url: {git_url}\n"
                          f"Cause: {str(e)}")




#print(GithubUtil().fetch_repositories("https://github.com/SohailAlvi"))