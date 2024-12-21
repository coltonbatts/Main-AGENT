import git
from pathlib import Path
from typing import List, Optional

class GitManager:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self._init_repo()
        
    def _init_repo(self):
        """Initialize a git repository if it doesn't exist."""
        if not (self.repo_path / '.git').exists():
            self.repo = git.Repo.init(self.repo_path)
        else:
            self.repo = git.Repo(self.repo_path)
    
    def create_branch(self, branch_name: str) -> bool:
        """Create a new branch and switch to it."""
        try:
            current = self.repo.create_head(branch_name)
            current.checkout()
            return True
        except git.GitCommandError as e:
            print(f"Error creating branch: {e}")
            return False
    
    def commit_changes(self, files: List[str], message: str) -> bool:
        """Stage and commit specified files."""
        try:
            self.repo.index.add(files)
            self.repo.index.commit(message)
            return True
        except git.GitCommandError as e:
            print(f"Error committing changes: {e}")
            return False
    
    def merge_branch(self, source_branch: str, target_branch: str = "main") -> bool:
        """Merge source branch into target branch."""
        try:
            # Switch to target branch
            self.repo.heads[target_branch].checkout()
            # Merge source branch
            self.repo.git.merge(source_branch)
            return True
        except git.GitCommandError as e:
            print(f"Error merging branches: {e}")
            return False
    
    def get_current_branch(self) -> str:
        """Get the name of the current branch."""
        return self.repo.active_branch.name
