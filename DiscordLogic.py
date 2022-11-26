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

"TO IMPLEMENT: HANDLE ALL ACTIVITY TYPES FOR CONCISE WORDING IN SENT EMBEDS"

from discord_webhook import DiscordWebhook, DiscordEmbed
from PlayerLogic import Type


class DiscordLogic:
    url = None

    def __init__(self, url):
        self.url = url

    def get_player_thumbnail(self, player_obj):
        with open(player_obj.thumbnail, 'rb') as file:
            return file.read()

    def push_level_up(self, player_obj, buffer_obj, skill_name):
        message = DiscordWebhook(self.url, rate_limit_retry=True)
        player_skill = getattr(player_obj, skill_name)
        buffer_skill = getattr(buffer_obj, skill_name)

        if skill_name == 'Overall':  # we do not want to update this with every level
            if not int(buffer_skill.level) % 50 == 0:
                return  # return if overall level not modulo of 50 with remainder of 0

        embed = DiscordEmbed(title=f"{player_obj.name} Advanced {skill_name} Level   :   "
                                   f"{player_skill.level} --> {buffer_skill.level}",
                             color=buffer_skill.colour)
        embed.add_embed_field(name=f"Total {skill_name} XP    ",
                              value=f"{int(buffer_skill.xp):,}")
        embed.add_embed_field(name=f"Overall Player XP",
                              value=f"{int(buffer_obj.Overall.xp):,}")

        #message.add_file(file=self.get_player_thumbnail(player_obj), filename='thumbnail.png')
        #embed.set_author(name=f"{player_obj.name}⠀", icon_url=f"attachment://thumbnail.png")

        embed.set_thumbnail(url=player_skill.icon_url)
        message.add_embed(embed)
        message.execute()
        print("\nINFO : PUSHING LEVEL TO DISCORD")

    def push_activity_up(self, player_obj, buffer_obj, activity_name):  # this function is long to add custom embeds
        message = DiscordWebhook(self.url)
        player_activity = getattr(player_obj, activity_name)
        buffer_activity = getattr(buffer_obj, activity_name)

        # this if statement is because the api sends -1 as the value for an unkilled boss or activity
        # we dont want the bot to print out KC "-1 --> new value", so we change the value to 0 so it shows e.g "0 --> 5"
        if player_activity.count == "-1":
            player_activity.count = 0

        if player_activity.type == Type.boss:
            embed = DiscordEmbed(title=f"{player_obj.name} Killed {player_activity.name}",
                                 color=player_activity.colour)
            embed.add_embed_field(name=f"{player_activity.name} KC    ",
                                  value=f"{int(player_activity.count):,} --> {int(buffer_activity.count):,}")
            embed.add_embed_field(name=f"{player_activity.name} Rank",
                                  value=f"{int(buffer_activity.rank):,}")

        elif player_activity.type == Type.clue:
            embed = DiscordEmbed(title=f"{player_obj.name} Completed A {player_activity.name}",
                                 color=player_activity.colour)
            embed.add_embed_field(name=f"{player_activity.name}s Completed    ",
                                  value=f"{int(buffer_activity.count):,}")
            embed.add_embed_field(name=f"{player_activity.name} Rank",
                                  value=f"{int(buffer_activity.rank):,}")

        elif player_activity.type == Type.clue_all:
            if not int(player_activity.count) % 50 == 0:  # if not multiple of 50 then return
                return
            embed = DiscordEmbed(title=f"{player_obj.name} Reached A Clue Scroll Milestone",
                                 color=player_activity.colour)
            embed.add_embed_field(name=f"{player_activity.name}s Completed    ",
                                  value=f"{int(buffer_activity.count):,}")
            embed.add_embed_field(name=f"{player_activity.name} Rank",
                                  value=f"{int(buffer_activity.rank):,}")

        elif player_activity.type == Type.minigame or player_activity.type == Type.league:
            embed = DiscordEmbed(title=f"{player_obj.name} Gained Points For : {player_activity.name}",
                                 color=player_activity.colour)
            embed.add_embed_field(name=f"{player_activity.name} Points    ",
                                  value=f"{int(player_activity.count):,} --> {int(buffer_activity.count):,}")
            embed.add_embed_field(name=f"{player_activity.name} Rank",
                                  value=f"{int(buffer_activity.rank):,}")

        elif player_activity.type == Type.raid:
            embed = DiscordEmbed(title=f"{player_obj.name} Completed {player_activity.name}",
                                 color=player_activity.colour)
            embed.add_embed_field(name=f"{player_activity.name} Completions    ",
                                  value=f"{int(player_activity.count):,} --> {int(buffer_activity.count):,}")
            embed.add_embed_field(name=f"{player_activity.name} Rank",
                                  value=f"{int(buffer_activity.rank):,}")

        # This should not be needed as embed content is identical to that of Type.minigame so the two are combined.
        elif player_activity.type == Type.chest:
            embed = DiscordEmbed(title=f"{player_obj.name} Opened : Barrows Chest",
                                 color=player_activity.colour)
            embed.add_embed_field(name=f"Barrows Chests Opened    ",
                                  value=f"{int(player_activity.count):,} --> {int(buffer_activity.count):,}")
            embed.add_embed_field(name=f"Barrows Rank", value=f"{int(buffer_activity.rank):,}")

        elif player_activity.type == Type.rifts:
            embed = DiscordEmbed(title=f"{player_obj.name} Closed A Rift",
                                 color=player_activity.colour)
            embed.add_embed_field(name=f"{player_activity.name}",
                                  value=f"{int(player_activity.count):,} --> {int(buffer_activity.count):,}")
            embed.add_embed_field(name=f"Guardians Of The Rift Rank", value=f"{int(buffer_activity.rank):,}")

        else:
            print("\nERROR: Unaccounted for activity")
            return  # This should never execute as all activity types are covered.

        embed.set_thumbnail(url=player_activity.icon_url)
        message.add_embed(embed)
        message.execute()
        print("\nINFO : PUSHING ACTIVITY TO DISCORD")
