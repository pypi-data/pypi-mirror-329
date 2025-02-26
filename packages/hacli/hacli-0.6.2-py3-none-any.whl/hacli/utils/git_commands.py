import os
from pathlib import Path
from typing import List, Optional

import git
from git import Repo, Remote, Head


class GitBranchManager:
    """Git 分支管理器"""

    def __init__(self, repo: Repo):
        self.repo = repo

    def create_branch(self, branch: str, base_branch: str) -> Head:
        """
        创建新分支

        Args:
            branch: 新分支名称
            base_branch: 基础分支名称
        """
        if self.repo.active_branch.name != base_branch:
            self.repo.git.checkout(base_branch)
        self.repo.git.pull('origin', base_branch)
        return self.repo.create_head(branch)

    def delete_branch(self, branch: str, force: bool = False) -> None:
        """
        删除分支

        Args:
            branch: 分支名称
            force: 是否强制删除
        """
        self.repo.delete_head(branch, force=force)

    def list_branches(self) -> List[str]:
        """列出所有本地分支"""
        return [head.name for head in self.repo.heads]

    def checkout_branch(self, branch: str) -> None:
        """切换到指定分支"""
        self.repo.git.checkout(branch)


class GitRemoteManager:
    """Git 远程仓库管理器"""

    def __init__(self, repo: Repo):
        self.repo = repo

    def add_remote(self, name: str, url: str) -> Remote:
        """添加远程仓库"""
        return self.repo.create_remote(name, url)

    def remove_remote(self, name: str) -> None:
        """删除远程仓库"""
        self.repo.delete_remote(name)

    def list_remotes(self) -> List[str]:
        """列出所有远程仓库"""
        return [remote.name for remote in self.repo.remotes]

    def fetch_all(self) -> None:
        """获取所有远程更新"""
        self.repo.git.fetch('--all')


class GitCommitManager:
    """Git 提交管理器"""

    def __init__(self, repo: Repo):
        self.repo = repo

    def commit(self, message: str, files: Optional[List[str]] = None) -> None:
        """
        提交更改

        Args:
            message: 提交信息
            files: 要提交的文件列表，None 表示提交所有更改
        """
        if files:
            self.repo.index.add(files)
        else:
            self.repo.git.add('.')
        self.repo.index.commit(message)

    def get_commit_logs(self, from_rev: str, to_rev: str) -> List[str]:
        """获取指定版本范围的提交日志"""
        logs = self.repo.git.log(f"{from_rev}..{to_rev}", "--oneline")
        return logs.splitlines()

    def execute_git_command(self, command: str, shell: bool = False) -> str:
        """
        执行自定义 Git 命令

        Args:
            command: Git 命令
            shell: 是否使用 shell 执行
        """
        return self.repo.git.execute(command=command, shell=shell)


class LocalGitCommand:
    """Git 本地命令管理器"""

    def __init__(self, is_global: bool):
        """
        初始化 Git 命令管理器

        Args:
            is_global: 是否使用全局仓库
        """
        self.is_global = is_global
        self.working_dir = Path(
            os.environ["PROJECT_GLOBAL_GIT_LOCAL_WORKING_DIR"] if is_global
            else os.environ["PROJECT_LOCAL_GIT_LOCAL_WORKING_DIR"]
        )
        self.repo = git.Repo(self.working_dir)

        # 初始化子管理器
        self.branch = GitBranchManager(self.repo)
        self.remote = GitRemoteManager(self.repo)
        self.commit = GitCommitManager(self.repo)

    def get_current_branch(self) -> str:
        """获取当前分支名称"""
        return self.repo.active_branch.name

    def is_clean(self) -> bool:
        """检查工作区是否干净"""
        return not self.repo.is_dirty()

    def reset_hard(self, reference: str = 'HEAD') -> None:
        """硬重置到指定引用"""
        self.repo.git.reset('--hard', reference)

    def stash_changes(self, include_untracked: bool = False) -> None:
        """
        暂存更改

        Args:
            include_untracked: 是否包含未跟踪的文件
        """
        if include_untracked:
            self.repo.git.stash('--include-untracked')
        else:
            self.repo.git.stash()

    def pop_stash(self) -> None:
        """恢复暂存的更改"""
        self.repo.git.stash('pop')
