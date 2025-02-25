import logging
import os
import sys
import tempfile

import git
from git import Repo, Tree


def get_name_from_url(url: str):
    path = url.split("/")[-1]
    if path.endswith(".git"):
        return path[0:-4]
    else:
        return path


def _repo_from_url(url):
    return {
        'owner': None,
        'repository': get_name_from_url(url),
        'url': url
    }


class GitClient(object):

    def __init__(self, directory: str = ".", logger: logging.Logger = None):
        super().__init__()
        if logger is None:
            logger = logging.getLogger("menschmachine.gitclient")
        try:
            root = self._find_git_root(directory)
            self.root_dir = root
            os.chdir(root)
            self.repo = Repo(root)
            self.repo_url = self._get_repo()["url"]
        except git.exc.InvalidGitRepositoryError:
            logger.error("Current directory is not a valid git repository")
            sys.exit(1)

    def _find_git_root(self, directory):
        """
        Recursively search for the git root directory.
        """
        if os.path.isdir(os.path.join(directory, ".git")):
            return directory
        parent_dir = os.path.abspath(os.path.join(directory, ".."))
        if parent_dir == directory:
            return None
        return self._find_git_root(parent_dir)

    def _get_repo(self):
        for remote in self.repo.remotes:
            for url in remote.urls:
                return _repo_from_url(url)
        return _repo_from_url(f"file:///{self.repo.common_dir}")

    def get_diff(self):
        t = self.repo.head.commit.tree
        return self.repo.git.diff(t)

    def get_untracked_files(self):
        return self.repo.untracked_files

    def get_git_files(self):
        files = list()
        tree = self.repo.tree()
        self._read_tree(files, tree)
        return files

    def _read_tree(self, files: list[str], tree: Tree):
        for f in tree:
            if f.type == "blob":
                files.append(f.path)
            elif f.type == "tree":
                self._read_tree(files, f)

    def commit(self, message, add_all: bool = False):
        if add_all:
            self.repo.git.add(A=True)
            self.repo.git.refresh()
        index = self.repo.index
        index.commit(message)

    def diff_file(self, filename: str, content: str) -> str:
        with tempfile.NamedTemporaryFile(mode='w+', delete=True) as tmp:
            tmp.write(content)
            tmp.flush()
            return self.repo.git.diff("--no-index", filename, tmp.name, with_exceptions=False)

    def get_root_dir(self) -> str:
        return self.root_dir
