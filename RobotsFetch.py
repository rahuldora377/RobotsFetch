import requests
import re
import threading
from termcolor import colored
import sys
import argparse

parser=argparse.ArgumentParser(
    description="Fetch robots.txt from a list of url and get status of each Disallowed individual path"
)
parser.add_argument("--list",help="path to file containing a list of target URLs")

args=parser.parse_args()


ascii_text=f"""
 _                 __            
|_) _ |_  _ _|_ _ |_  _ _|_ _ |_ 
| \(_)|_)(_) |__> |  (/_ |_(_ | |
            Developed By: {colored("rahuldora377","green")}
"""

print(colored(ascii_text,"red"))

path='robots.txt'
pattern=r'Disallow:\s(.*)'
status_codes_to_check=(200,403,500)

def fetchUrl(url):
    try:
        full_url=url+path
        response=requests.get(full_url)

        if response.status_code==200:
            # print(response.text)
            matches=re.findall(pattern,response.text)
            for match in matches:
                disallowd_path=match.strip()
                full_url=url[:-1]+disallowd_path
                # print(full_url)
                thread=threading.Thread(target=requestRobots,args=(full_url,))
                thread.start()
    except:
        print("Exception occoured at: "+full_url)

def requestRobots(url):
    try:
        response=requests.get(url)
        if response.status_code in status_codes_to_check:
            print(f'{url} [{colored(response.status_code,"green")}]',end='\n')
    except:
        # print(f'Problem in fetching{url}')
        pass

    
if args.list:
    with open(args.list,'r') as urls:
        for url in urls:
            url=url.strip()
            if not url.endswith('/'):
                url+='/'

            thread=threading.Thread(target=fetchUrl,args=(url,))
            thread.start()
        

# Handle stdin

if sys.stdin.isatty() and args.list==None:
    print(colored("~~ No input is provided ~~","red"))
else:
    for url in sys.stdin:
        url=url.strip()
        if not url.startswith('/'):
            url+='/'
        thread=threading.Thread(target=fetchUrl,args=(url,))
        thread.start()







