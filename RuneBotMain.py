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


from APILogic import filtered_api_data
from PlayerLogic import skills_list, activity_list, PlayerLogic
from DiscordLogic import DiscordLogic
import time
import copy
import os
import sys

def update_buffer(player_name):
    api_data_list = filtered_api_data(player_name=player_name)
    for count, skill in enumerate(api_data_list):
        if count < len(skills_list):
            rank, level, xp = skill.split(',')
            buffer_skill = players.buffer.__getattribute__(skills_list[count])
            buffer_skill.rank = rank
            buffer_skill.level = level
            buffer_skill.xp = xp
        else:
            rank, kc = skill.split(',')
            buffer_activity = players.buffer.__getattribute__(activity_list[(count - len(skills_list))])
            buffer_activity.rank = rank
            buffer_activity.count = kc


def check_updated_stats(player_name):
    #skills
    for skill in skills_list:  # if new level is higher than previous level then push level update to discord
        if not players.username[player_name].__getattribute__(skill).level is None:
            if (players.buffer.__getattribute__(skill).level
                    > players.username[player_name].__getattribute__(skill).level):
                discord.push_level_up(player_obj=players.username[player_name],
                                      buffer_obj=players.buffer, skill_name=skill)
    #activities
    for activity in activity_list:  # if new count is higher than previous count then push activity update to discord
        if not players.username[player_name].__getattribute__(activity).count is None:
            if (players.buffer.__getattribute__(activity).count
                    > players.username[player_name].__getattribute__(activity).count):
                discord.push_activity_up(player_obj=players.username[player_name],
                                         buffer_obj=players.buffer, activity_name=activity)


def update_player(player_name):
    # replace player object with buffer object instead of updating each value individually - both objects of same class
    # this method requires replacing 2 unique values in the buffer before replacing the player object with the buffer
    players.buffer.name = players.username[player_name].name
    players.buffer.thumbnail = players.username[player_name].thumbnail
    players.username[player_name] = copy.deepcopy(players.buffer)
    # deepcopy is the only method that works, surprisingly it is not significantly slow to use this method

def get_webhook_url():
    if not os.path.exists("WebhookURL.txt"):  # Check if file exists
        with open("WebhookURL.txt", 'w') as file:  # if not, create an empty file of that name
            pass  # immediately pass in order to close the file
        print("Error: WebhookURL.txt Does Not Exist. File Created, Please Populate With Webhook URL")
        raise SystemExit
    if not os.path.getsize("WebhookURL.txt") == 0:
        with open("WebhookURL.txt", "r") as file:  # this is so webhook url is not on git
            webhook_url = file.readline()
        return webhook_url
    print("Error: WebhookURL.txt Empty. Please Populate With Webhook URL")
    raise SystemExit
# ------------------------------------------------------------------------------------------------------- main function

def main():
    while True:
        print("\rUPDATING", end='')
        for player in players.username:
            update_buffer(player)
            check_updated_stats(player)
            update_player(player)
            players.export_json()
        time.sleep(60)  # interval of 60 seconds where python will not use cpu cycles



if __name__ == "__main__":
    players = PlayerLogic()  # has to be global, could use class but not required
    discord = DiscordLogic(url=get_webhook_url())  # this is the webhook URL for discord integration
    main()
