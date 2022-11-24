Runebot is a discord webhook bot which tracks player achievements such as levels and boss/activity counts
This was developed by runescape player "Jelapeeno" as a side project to develop skills, this bot is in no way the
most efficient version of itself as using json rather than an SQLite database in order to store data is not ideal.
However this bot was created to gain experience and for private use solely developed by the author listed below.

**@author** : Simon Lyke

**@Version** : 2.1.1

**@date** : 20/11/2022

**@github** : https://github.com/SimonLyke

.
.

The embeds look like this : 

![image](https://user-images.githubusercontent.com/94386835/203864429-1a84cf62-6921-4b29-a6fe-f271e460b565.png)

![image](https://user-images.githubusercontent.com/94386835/203864532-c700ef2d-ab71-40ac-9fa3-4611c4008aac.png)


In this example, this player has killed skotizo and completed a hard clue scroll since he last logged off the game.

.
.

The folder structure should be as follows:

players/
thumbnails/
APILogic.py
DiscordLogic.py
PlayerLogic.py
PlayerNames.txt
RuneBotMain.py
WebhookURL.txt

Files with .py extension are the source files and should not be edited unless you know what you are doing.

**players/** is a folder that contains player data stored as json so the bot can still update discord with new achievements even when it goes offline. 
whilst this solution works, if the bot has been offline for a long time since it was last used i recommend deleting all player json files within this folder
so the bot does not spam discord with updates of everything they have done since it was last turned on, this is useful when hosted on a personal computer
where the bot is running almost all the time.

**thumbnails/** is a folder that contains thumbnails of skills and activities, this is technically obselete as i use imgur links of these images 
in order to clean up the code instead of using discord-webhook's file opening function. 

**PlayerNames.txt** should be populated with player names one for each line, and no other characters inside so that when python's readline() function executes it retrieves
a string of a players name only, such as "TheLegend27" (obviously dont add " " in the file).

**WebhookURL.txt** should be populated with the webhook integration url for the chosen discord server. You will need to have permission on the server to do this
and im not going to explain how as there are plenty of up to date tutorials available on the internet. The URL should be placed on the first line.

If neither of the text files exist you can either create them by yourself with the correct names as listed above, or run the program twice and it will generate both
for you to populate

.
.

Any issues with the bot please let me know. Thanks.
