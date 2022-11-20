""" Runebot is a discord webhook bot which tracks player achievements such as levels and boss/activity counts
This was developed by runescape player "Jelapeeno" as a side project to develop skills, this bot is in no way the
most efficient version of itself as using json rather than an SQLite database in order to store data is not ideal.
However this bot was created to gain experience and for private use solely developed by the author listed below.

@author : Simon Lyke
@Version : 2.1.1
@date : 20/11/2022
@github : https://github.com/SimonLyke

PLEASE LOOK AT README FOR INFORMATION ON HOW TO SETUP THE BOT FOR PRIVATE USE WITHIN A DISCORD
"""

"TO IMPLEMENT : CATCH ALL EXCEPTIONS AND HANDLE THEM ACCORDINGLY"
import requests


def api_call(player_name):
    # Assigning the base API url to a variable each time this function executes would waste memory and GC processing
    try:
        request = requests.get("https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=" + player_name)
        request.raise_for_status()
    except requests.exceptions.RequestException as err:
        # log requestexception
        # return status code
        print("api call error")
        pass
    except requests.exceptions.Timeout as errtimeout:
        # log timeout
        # return status code
        print("api call error")
        pass
    except requests.exceptions.HTTPError as errhttp:
        # log httperror
        # return status code
        print("api call error")
        pass
    except requests.exceptions.ConnectionError as errconnection:
        # log connectionerror
        # return status code
        print("api call error")
        pass
    else:
        # also return status code
        return request.text


def filtered_api_data(player_name):
    api_data = api_call(player_name).replace(' ', '')
    return list(filter(None, api_data.splitlines()))