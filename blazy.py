#!/usr/bin/env python3.10

from core.arguments import cli_arguments
from core.banner import banner
from core.blazy_core import Blazy

if __name__ == '__main__':
    banner()
    url = cli_arguments.url or input('{BLUE}[?]{END} Enter target URL: ')  # takes input from user
    blazy = Blazy(url=url, username_file=cli_arguments.usernames, passwords_file=cli_arguments.passwords,
                  verbose=cli_arguments.verbose, scan_all=cli_arguments.all)
    blazy.run_scan()
    blazy.save_results(output=cli_arguments.output)
