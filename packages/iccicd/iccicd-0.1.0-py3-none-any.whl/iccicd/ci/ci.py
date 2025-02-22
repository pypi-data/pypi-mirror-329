import logging
from pathlib import Path

from iccore.version_control import (
    git,
    GitlabClient,
    GitlabInstance,
    GitRemote,
    GitUser,
    GitlabToken,
)

logger = logging.getLogger(__name__)


def gitlab_ci_push(
    user_name: str, user_email: str, repo_url: str, token: str, message: str
):

    gitlab = GitlabClient(
        instance=GitlabInstance(),  # FIXME in iccore url=repo_url
        token=GitlabToken(value=token),
        user=GitUser(name=user_name, email=user_email),
    )
    gitlab.push_change(message)


def sync_external_archive(
    repo_dir: Path,
    user_name: str = "",
    user_email: str = "",
    url: str = "",
    token: str = "",
):

    if user_name and user_email:
        git.set_user(repo_dir, GitUser(name=user_name, email=user_email))
    if url and token:
        url_prefix = f"https://oauth2:{token}"
        git.add_remote(
            repo_dir, GitRemote(name="oauth_remote", url=f"{url_prefix}@{url}")
        )

    # Download package

    # Run sync script

    # Commit and push change

    logger.info("Finished external package sync")
