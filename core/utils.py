import json
from pathlib import Path

from core.colors import RED, BOLD, END


def print_data(message: str, verbose: bool = True):
    if verbose:
        print(message)


def can_not_use_brute_force(username, error: Exception):
    print(f'\r{RED}[!]{END} Cannot use brute force with user: {username}')
    print(f'\r\t[Error: {error}]')


def wordlist_u(file_path) -> list[str]:  # Loads usernames from usernames.txt
    try:
        with open(file_path, 'r') as f:
            return f.read().splitlines()
    except IOError:
        print(f"{RED}[-]{BOLD} Wordlist not found!")
        quit()


def wordlist_p(file_path) -> list[str]:  # Loads passwords from passwords.txt
    try:
        with open(file_path, 'r') as f:
            return f.read().splitlines()
    except IOError:
        print(f"{RED}[-]{BOLD} Wordlist not found!")
        quit()


def save_data(data: dict | list, file_path: str | Path):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
    except OSError as e:  # handle all times of possible file issues
        print(f"{RED}[-]{BOLD} Error on saving data: {e}!")
        quit()
