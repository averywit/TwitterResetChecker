import json
import requests
import time
import threading
from colorama import Fore

print("1 <- All 5 letter words")
print("2 <- All 5+6 letter repeaters")
choice = int(input("Please enter what you want to check: "))

lines = []
random = 0
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
            "V", "W", "X", "Y", "Z"]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
index = 0
stupidparse = ""

# Retrieving the list of all 5 letter words from Github scrape
if choice == 1:
    url = "https://raw.githubusercontent.com/averywit/LicensePlateChecker/main/5letterwords.txt"
    r = requests.get(url)
    for line in r.iter_lines():
        if line:
            stupidparse = str(line)
            lines.insert(index, stupidparse[2:7])
            index += 1

# Creating an array of all 3 letter combinations
elif choice == 2:
    for i in alphabet:
        lines.insert(index, i + i + i + i)
        index += 1
    for j in alphabet:
        lines.insert(index, j + j + j + j + j + j)
        index += 1


def check(username):
    session = requests.Session()
    proxy = {
        # 'http': "INSERT PROXIES HERE",
        # 'https': "INSERT PROXIES HERE"
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,bn;q=0.8",
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        "content-type": "application/json",
        "dnt": "1",
        'origin': 'https://twitter.com',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36',
        'x-twitter-active-user': 'yes',
        'x-twitter-client-language': 'en'
    }
    try:
        response = session.get(url=f"https://api.twitter.com/graphql/P8ph10GzBbdMqWZxulqCfA/UserByScreenName?variables=%7B%22screen_name%22%3A%22{username}%22%2C%22withHighlightedLabel%22%3Atrue%7D", headers=headers, proxies=proxy)
        print(response.text)
        if "Rate limit" in response.text:
            t = threading.Thread(target=check(username))
            t.Daemon = True
            threads.append(t)
            print(Fore.BLUE + "RATE LIMIT EXCEEDED")
        else:
            if '"errors":[{"message":"Authorization: User has been suspended. (63)"' in response.text:
                print(Fore.GREEN + username + ": RESET (BANNED)")
            elif '"media_count":0' in response.text and '"default_profile_image":true' in response.text:
                json_response = json.loads(response.text)
                print(json_response['legacy'])
                print(Fore.GREEN + username + ": RESET (SQUATTER)")
            else:
                print(Fore.RED + username + ": NO RESET")
    except:
        t = threading.Thread(target=check(username))
        t.Daemon = True
        threads.append(t)
        print(Fore.BLUE + "PROXY ERROR")


threads = []

for i in range(len(lines)):
    t = threading.Thread(target=check(lines[i]))
    t.Daemon = True
    threads.append(t)

for i in range(len(lines)):
    threads[i].start()
    time.sleep(0.2)

for i in range(1):
    threads[i].join()
