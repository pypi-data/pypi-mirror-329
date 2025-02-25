import os
import sys

from cmpal.models.config import CommitStyleConfigs
from cmpal.scripts.config import load_config
from cmpal.scripts.onboard import setup
from cmpal.scripts.verify import verify_commit_message
from cmpal.utils.git import main as generate_commit_message
from cmpal.utils.terminal import print_available_commands, print_error_message


def main():
    if len(sys.argv) > 2:
        print_error_message("Too many arguments provided.")
        return 1
    elif len(sys.argv) == 1:
        if saved_config := load_config():
            configs: CommitStyleConfigs = CommitStyleConfigs.model_validate(saved_config)
            commit_message: str = generate_commit_message(configs=configs)
            if not commit_message:
                return

            print("\n")
            is_approved: bool = verify_commit_message()
            if is_approved:
                os.system(f'git commit -m "{commit_message}"')
            else:
                print("Commit message rejected :(")
            return

        return setup()

    match sys.argv[1]:
        case "--setup" | "--init":
            return setup()
        case "--help":
            print_available_commands()
            return 0
        case _:
            print_error_message("Invalid argument provided.")
            print_available_commands()
            return 1
