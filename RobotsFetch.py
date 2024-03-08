import requests
import re
import threading
from termcolor import colored
import sys

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

    

with open(f'{sys.argv[1]}','r') as urls:
    for url in urls:
        url=url.strip()
        if not url.endswith('/'):
            url+='/'

        thread=threading.Thread(target=fetchUrl,args=(url,))
        thread.start()

print(sys.argv)
        








