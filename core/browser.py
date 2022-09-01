from http import cookiejar

from mechanize import HTTPRefreshProcessor, Browser, FormNotFoundError


class BlazyBrowser:
    def __init__(self):
        # Stuff related to Mechanize browser module
        self.br = Browser()  # Shortening the call by assigning it to a variable "br"
        # set cookies
        self.cookies = cookiejar.LWPCookieJar()
        self.br.set_cookiejar(self.cookies)
        # Mechanize settings
        self.br.set_handle_equiv(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        self.br.set_debug_http(False)
        self.br.set_debug_responses(False)
        self.br.set_debug_redirects(False)
        self.br.set_handle_refresh(HTTPRefreshProcessor(), max_time=1)
        self.br.addheaders = [('User-agent',
                               'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'),
                              ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                              ('Accept-Encoding', 'br')]

    def open(self, url: str, timeout: float | int = 10.0):
        self.br.open(url, timeout=timeout)

    def get_forms(self, url):
        self.br.open(url)
        return self.br.forms()

    def select_form(self, form_number: int):
        return self.br.select_form(nr=form_number)

    def process_form(self, url: str, username_input: str, passwd_input: str, form_name: str, option: str,
                     username: str, password: str, form_number: int = 0, menu: bool = False):
        try:
            self.br.open(url)
            self.br.select_form(nr=form_number)
        except Exception as e:
            # TODO save error to output, so user can know what passwords was skipped
            print(f'\nRequest is not processed: {e}')
            return ''
        self.br.form[username_input] = username
        self.br.form[passwd_input] = password
        if menu:
            self.br.form[form_name] = [option]
        return self.br.submit().read().decode()

    def get_data(self, url):
        return self.br.open(url).read().decode()
