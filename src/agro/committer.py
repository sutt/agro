import logging
import os
import subprocess
import sys
import time


def setup_logging(worktree_path):
    """Set up logging to a file in the worktree's .git directory."""
    log_file = os.path.join(worktree_path, ".agswap", "agro-committer.log")
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(process)d - %(levelname)s - %(message)s",
        filename=log_file,
        filemode="w",
    )


def wait_for_pid(pid):
    """Wait for a process with a given PID to exit."""
    logging.info(f"Monitoring PID {pid}. Waiting for it to exit.")
    # On Unix, we can use a simple poll with os.kill(pid, 0)
    # This will raise an OSError if the process does not exist.
    while True:
        try:
            os.kill(pid, 0)
            time.sleep(5)
        except OSError:
            logging.info(f"Process {pid} has exited.")
            break


def git_commit_changes(worktree_path, task_file, agent_type):
    """Check for changes in the git repo and commit them if any are found."""
    logging.info(f"Checking for git changes in {worktree_path}")
    try:
        # Check if there are any changes
        res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=worktree_path,
            text=True,
            capture_output=True,
        )
        if res.returncode != 0:
            logging.error(f"'git status' failed: {res.stderr}")
            return
        if not res.stdout.strip():
            logging.info("No changes detected. Nothing to commit.")
            return

        logging.info("Changes detected. Staging all changes.")
        subprocess.run(
            ["git", "add", "."],
            cwd=worktree_path,
            check=True,
            capture_output=True,
            text=True,
        )

        task_file_stem = os.path.splitext(task_file)[0]
        commit_message = (
            f"feat: impl {task_file_stem} with {agent_type} (agro auto-commit)"
        )
        logging.info(f"Committing with message: '{commit_message}'")
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=worktree_path,
            check=True,
            capture_output=True,
            text=True,
        )
        logging.info("Successfully committed changes.")

    except subprocess.CalledProcessError as e:
        logging.error(f"A git command failed in {worktree_path}: {e}")
        logging.error(f"Stderr: {e.stderr.strip()}")
        logging.error(f"Stdout: {e.stdout.strip()}")
    except Exception as e:
        logging.error(f"An unexpected error occurred in git_commit_changes: {e}")


def main():
    """Main entry point for the committer script."""
    if len(sys.argv) != 5:
        print(
            "Usage: python -m agro.committer <pid> <worktree_path> <task_file> <agent_type>",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        pid = int(sys.argv[1])
        worktree_path = sys.argv[2]
        task_file = sys.argv[3]
        agent_type = sys.argv[4]
    except (ValueError, IndexError):
        print("Invalid arguments.", file=sys.stderr)
        print(
            "Usage: python -m agro.committer <pid> <worktree_path> <task_file> <agent_type>",
            file=sys.stderr,
        )
        sys.exit(1)

    setup_logging(worktree_path)
    logging.info("Committer script started.")
    wait_for_pid(pid)
    git_commit_changes(worktree_path, task_file, agent_type)
    logging.info("Committer script finished.")


if __name__ == "__main__":
    main()
