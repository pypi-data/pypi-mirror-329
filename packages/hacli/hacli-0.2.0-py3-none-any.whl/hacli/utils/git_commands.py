import os

import git


class LocalGitCommand:
    def __init__(self, is_global: bool):
        self.is_local = is_global
        self.working_dir = os.environ["PROJECT_GLOBAL_GIT_LOCAL_WORKING_DIR"] if is_global else os.environ[
            "PROJECT_LOCAL_GIT_LOCAL_WORKING_DIR"]
        self.repo = git.Repo(self.working_dir)

    def create_branch(self, branch: str, base_branch):
        if self.repo.active_branch.name != base_branch:
            self.repo.git.checkout(base_branch)
            print(f"Switched to base branch '{base_branch}'!")
        self.repo.git.pull('origin', base_branch)
        self.repo.git.checkout("-b", branch)
