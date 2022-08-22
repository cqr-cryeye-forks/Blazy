# Blazy
Blazy is a modern login page bruteforcer.
<p><img src='https://i.imgur.com/Jhwa58j.png' /></p>

### Features
- [x] Easy target selections
- [x] Smart form and error detection
- [x] CSRF and Clickjacking Scanner
- [x] Cloudflare and WAF Detector
- [x] 90% accurate results
- [x] Checks for login bypass via SQL injection
- [x] large database of credentials
- [ ] Multi-threading
- [ ] 100% accurate results
- [ ] Better form detection and compatibility

#### Requirements
- Beautiful Soup
- Mechanize

### Installation
Open your terminal and enter
```
git clone https://github.com/cqr-cryeye-forks/Blazy
```
Now enter the following command
```
cd Blazy
```
Lets install the required modules before running Blazy
```
pip install -r requirements.txt
```
### Usage
```
usage: blazy.py [-h] [-v] [-a] [-u USERNAMES] [-p PASSWORDS] [-o OUTPUT] url

Tool for bruteforce log-in forms

positional arguments:
  url                   Target url or domain

options:
  -h, --help            show this help message and exit
  -v, --verbose         Show debug information
  -a, --all             Run everything scans without choices and don't quit
                        after finding results
  -u USERNAMES, --usernames USERNAMES
                        File with usernames
  -p PASSWORDS, --passwords PASSWORDS
                        File with passwords
  -o OUTPUT, --output OUTPUT
                        Output file. Data will be saved as json

```

If `--all` flag is selected, then, after finding first match script will not stop and will brute all given usernames and passwords

## Output examples

Findings and extra data are saving in `output.json`

### Json structure

```json
{
  "url": "http://testphp.vulnweb.com/login.php",
  "findings": [
    {
      "username": "test",
      "related_username_form": "uname",
      "password": "test",
      "related_password_form": "pass"
    }
  ],
  "extra": [
    "Heuristic found a Clickjacking Vulnerability",
    "Heuristic found a CSRF Vulnerability"
  ]
}
```


CLI output (clear):
```
    ____   _                    
       |  _ \ | |              
       | |_) || |  __ _  ____ _   _ 
       |  _ < | | / _` ||_  /| | | |
       | |_) || || (_| | / / | |_| |
       |____/ |_| \__,_|/___| \__, |
                               __/ |
        Made with <3 By D3V   |___/ 
        
[+] Heuristic found a Clickjacking Vulnerability
[+] Heuristic found a CSRF Vulnerability
[+] Found 2 forms

[+] Valid credentials found:
Username: test
Password: test
```


CLI output (verbose):
```
    ____   _                    
       |  _ \ | |              
       | |_) || |  __ _  ____ _   _ 
       |  _ < | | / _` ||_  /| | | |
       | |_) || || (_| | / / | |_| |
       |____/ |_| \__,_|/___| \__, |
                               __/ |
        Made with <3 By D3V   |___/ 
        
[>] Usernames loaded: 81483
[>] Passwords loaded: 100006
Target url: http://testphp.vulnweb.com/login.php
[+] Heuristic found a Clickjacking Vulnerability
[+] Heuristic found a CSRF Vulnerability
[+] Found 2 forms
[!] Username field: uname
[!] Password field: pass
[-] Bruteforce started: 2022-08-22 23:19:27.901756
[>] Brute forcing username: test
[>] Passwords tried: 1 / 100006
[+] Valid credentials found:
Username: test
Password: test
[-] Bruteforce finished: 2022-08-22 23:19:28.776774. Total: 0:00:00.875018
[!] Username field: searchFor
Saving data into /home/nick/PycharmProjects/tools/blazy/output.json
```
