import argparse

from core.constants import BASE_DIR, BASE_OUTPUT_PATH


def arguments():
    p = argparse.ArgumentParser(description='Tool for bruteforce log-in forms')
    p.add_argument("-v", "--verbose", action='store_true', required=False, default=False,
                   help="Show debug information")
    p.add_argument("-a", "--all", action='store_true', required=False, default=False,
                   help="Run everything scans without choices and don't quit after finding results")
    p.add_argument("-u", "--usernames", required=False, default=BASE_DIR.joinpath('usernames.txt'), type=str,
                   help="File with usernames")
    p.add_argument("-p", "--passwords", required=False, default=BASE_DIR.joinpath('passwords.txt'), type=str,
                   help="File with passwords")
    p.add_argument("-o", "--output", default=BASE_OUTPUT_PATH,
                   help="Output file. Data will be saved as json")
    p.add_argument('url', type=str, help='Target url or domain')
    return p


cli_arguments = arguments().parse_args()
