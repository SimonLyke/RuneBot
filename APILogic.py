""" Runebot is a discord webhook bot which tracks player achievements such as levels and boss/activity counts
This was developed by runescape player "Jelapeeno" as a side project to develop skills, this bot is in no way the
most efficient version of itself as using json rather than an SQLite database in order to store data is not ideal.
However this bot was created to gain experience and for private use solely developed by the author listed below.

@author : Simon Lyke
@Version : 2.1.2
@date : 15/12/2022
@github : https://github.com/SimonLyke

PLEASE LOOK AT README FOR INFORMATION ON HOW TO SETUP THE BOT FOR PRIVATE USE WITHIN A DISCORD
"""

"TO IMPLEMENT : CATCH ALL EXCEPTIONS AND HANDLE THEM ACCORDINGLY"


import requests
import time


def api_call(player_name):
    """
    Assigning the base API url to a variable each time this function executes would waste memory and GC processing.
    for loop is used as we need to keep the bot retrying the request so that it won't crash if internet goes
    down or if request failed. This is so if hosted on external server or device, it should retry 3 times before
    skipping the player, this should account for mispelled usernames and other issues without hanging endlessly.
    An interval of 60 seconds on failed requests as to not take up unnecessary cpu cycles
    as time.sleep delays execution of current thread and the cpu will process other things during this time.
    """
    for retry in range(3):
        try:
            request = requests.get("https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=" + player_name)
            request.raise_for_status()
            if request.status_code == 200:
                return request.text  # no guard clause needed as it will check and return

        except requests.exceptions.RequestException as err:  # log requestexception
            print(f"Error : Requests : Exception, \nError : {err}\nSleeping : 60 Seconds")

        else:
            print(f"Error : Unhandled Exception, \nError : {err}\nSleeping : 60 Seconds")
        time.sleep(60)  # only executes if response != 200
    return None  # only return None if retries are exhausted and still failed


# this function returns list of values filtered due to the api returning data such as
# 0,0,0,12,12353,145,89,12334,51,21,1243235,123,14,-1,-1,-1,-1...    for example
def filtered_api_data(player_name):
    api_data = api_call(player_name).replace(' ', '')
    if not api_data:
        return None
    return list(filter(None, api_data.splitlines()))