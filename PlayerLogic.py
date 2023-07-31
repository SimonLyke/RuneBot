""" Runebot is a discord webhook bot which tracks player achievements such as levels and boss/activity counts
This was developed by runescape player "Jelapeeno" as a side project to develop skills, this bot is in no way the
most efficient version of itself as using json rather than an SQLite database in order to store data is not ideal.
However this bot was created to gain experience and for private use solely developed by the author listed below.

@author : Simon Lyke
@Version : 2.2
@date : 01/08/2023
@github : https://github.com/SimonLyke

PLEASE LOOK AT README FOR INFORMATION ON HOW TO SETUP THE BOT FOR PRIVATE USE WITHIN A DISCORD
"""

import jsonpickle
import os
import sys
from enum import Enum

skills_list = ['Overall', 'Attack', 'Defence', 'Strength', 'Hitpoints', 'Ranged', 'Prayer', 'Magic', 'Cooking',
               'Woodcutting', 'Fletching', 'Fishing', 'Firemaking', 'Crafting', 'Smithing', 'Mining', 'Herblore',
               'Agility', 'Thieving', 'Slayer', 'Farming', 'Runecrafting', 'Hunter', 'Construction']

activity_list = ['leaguePoints', 'bountyHunter', 'bountyRogue', 'legacyBountyHunter', 'legacyBountyRogue', 'clueAll', 'clueBeginner', 'clueEasy', 'clueMedium',
                 'clueHard', 'clueElite', 'clueMaster', 'LMS', 'pvpArenaRank', 'soulWarsZeal', 'riftsClosed',
                 'abyssalSire',
                 'alchemicalHydra', 'artio' ,'barrowsChests', 'bryophyta', 'callisto', 'calvarion', 'cerberus', 'chambersOfXeric',
                 'chambersOfXericChallenge', 'chaosElemental', 'chaosFanatic', 'commanderZilyana', 'corporealBeast',
                 'crazyArchaeologist', 'dagannothPrime', 'dagganothRex', 'dagganothSupreme', 'derangedArchaeologist',
                 'dukeSucellus', 'generalGraardor', 'giantMole', 'grotesqueGuardians', 'hespori', 'kalphiteQueen', 'kingBlackDragon',
                 'kraken', 'kreearra', 'kriltsutsaroth', 'mimic', 'nex', 'nightmare', 'phosanisNightmare', 'obor',
                 "phantomMuspah", 'sarachnis', 'scorpia', 'skotizo', 'spindel', 'tempoross', 'theGauntlet', 'theCorruptedGauntlet',
                 'theLeviathon', 'theWhisperer', 'theatreOfBlood', 'theatreOfBloodHardMode', 'ThermonuclearSmokeDevil', 'tombsOfAmascut',
                 'tombsOfAmascutExpertMode', 'tzKalZuk', 'tzTokJad', 'vardorvis', 'venenatis', 'vetion', 'vorkath', 'wintertodt',
                 'zalcano', 'zulrah']


class Type(Enum):
    boss = 1
    clue = 2
    clue_all = 3
    minigame = 4
    raid = 5
    league = 6
    chest = 7
    rifts = 8


class Player:

    def __init__(self, name, thumbnail): # redo all skill icons with correct aspect ratio and max width or height as 100px
        self.name = name
        self.thumbnail = thumbnail
        self.Overall = Skill(1098762, "https://i.imgur.com/bX8yAwW.png", "Overall")
        self.Attack = Skill(7368816, "https://i.imgur.com/ieVoUt8.png", "Attack")
        self.Defence = Skill(4342338, "https://i.imgur.com/fu7roAC.png", "Defence")
        self.Strength = Skill(13415993, "https://i.imgur.com/fgWiDC4.png", "Strength")
        self.Hitpoints = Skill(12191238, "https://i.imgur.com/tDG1vpS.png", "Hitpoints")
        self.Ranged = Skill(8170752, "https://i.imgur.com/c5tivGa.png", "Ranged")
        self.Prayer = Skill(16448250, "https://i.imgur.com/b6HHA0U.png", "Prayer")
        self.Magic = Skill(21196, "https://i.imgur.com/9hAooHz.png", "Magic")
        self.Cooking = Skill(13417984, "https://i.imgur.com/Le5Uh5S.png", "Cooking")
        self.Woodcutting = Skill(761344, "https://i.imgur.com/zx8YTKx.png", "Woodcutting")
        self.Fletching = Skill(5743441, "https://i.imgur.com/W9bcv5c.png", "Fletching")
        self.Fishing = Skill(4288883, "https://i.imgur.com/t2xHAjp.png", "Fishing")
        self.Firemaking = Skill(15760142, "https://i.imgur.com/dK1SQ7b.png", "Firemaking")
        self.Crafting = Skill(6375214, "https://i.imgur.com/HBkf6AA.png", "Crafting")
        self.Smithing = Skill(6052182, "https://i.imgur.com/lSVT1Wj.png", "Smithing")
        self.Mining = Skill(2897541, "https://i.imgur.com/RX24N9A.png", "Mining")
        self.Herblore = Skill(1534737, "https://i.imgur.com/7m19V7r.png", "Herblore")
        self.Agility = Skill(197379, "https://i.imgur.com/QLCisV9.png", "Agility")
        self.Thieving = Skill(197379, "https://i.imgur.com/qm0oJnd.png", "Thieving")
        self.Slayer = Skill(12762114, "https://i.imgur.com/uDHeiNw.png", "Slayer")
        self.Farming = Skill(697233, "https://i.imgur.com/9yJvyxc.png", "Farming")
        self.Runecrafting = Skill(7211207, "https://i.imgur.com/aJ9MrnP.png", "Runecrafting")
        self.Hunter = Skill(6372356, "https://i.imgur.com/gvTsaxl.png", "Hunter")
        self.Construction = Skill(12885512, "https://i.imgur.com/lLrIp2H.png", "Construction")
        # creating 'Activity' objects
        self.leaguePoints = Activity(Type.league, "Twisted League", "https://i.imgur.com/m62Xpnw.png")
        self.bountyHunter = Activity(Type.minigame, "Bounty Hunter", "https://i.imgur.com/uiTkQUx.png")
        self.bountyRogue = Activity(Type.minigame, "Bounty Hunter Rogue", "https://i.imgur.com/uiTkQUx.png")
        self.legacyBountyHunter = Activity(Type.minigame, "Bounty Hunter (Legacy)", "https://i.imgur.com/uiTkQUx.png")
        self.legacyBountyRogue = Activity(Type.minigame, "Bounty Hunter Rogue (Legacy)", "https://i.imgur.com/uiTkQUx.png")
        self.clueAll = Activity(Type.clue_all, "Total Clue Scroll", "https://i.imgur.com/AdwEjjr.png")
        self.clueBeginner = Activity(Type.clue, "Beginner Clue Scroll", "https://i.imgur.com/pSmD4j9.png")
        self.clueEasy = Activity(Type.clue, "Easy Clue Scroll", "https://i.imgur.com/vvjnl3b.png")
        self.clueMedium = Activity(Type.clue, "Medium Clue Scroll", "https://i.imgur.com/Q41t77c.png")
        self.clueHard = Activity(Type.clue, "Hard Clue Scroll", "https://i.imgur.com/Me3AlhA.png")
        self.clueElite = Activity(Type.clue, "Elite Clue Scroll", "https://i.imgur.com/sq3aBrr.png")
        self.clueMaster = Activity(Type.clue, "Master Clue Scroll", "https://i.imgur.com/l5uT4ED.png")
        self.LMS = Activity(Type.minigame, "Last Man Standing", "https://i.imgur.com/0Dww0kI.png")
        self.pvpArenaRank = Activity(Type.minigame, "PvP Arena Ranking", "https://i.imgur.com/BSFfZ73.png")
        self.soulWarsZeal = Activity(Type.minigame, "Soul Wars Zeals", "https://i.imgur.com/jvU7ccs.png")
        self.riftsClosed = Activity(Type.rifts, "Rifts Closed", "https://i.imgur.com/mTbKhlI.png")
        self.abyssalSire = Activity(Type.boss, "Abyssal Sire", "https://i.imgur.com/Ezlrc2h.png")
        self.alchemicalHydra = Activity(Type.boss, "Alchemical Hydra", "https://i.imgur.com/tIGR7du.png")
        self.artio = Activity(Type.boss, "Artio", "https://i.imgur.com/0ugbKUC.png")
        self.barrowsChests = Activity(Type.chest, "Barrows Chests", "https://i.imgur.com/s7NK1Qp.png")
        self.bryophyta = Activity(Type.boss, "Bryophyta", "https://i.imgur.com/arnWNjt.png")
        self.callisto = Activity(Type.boss, "Callisto", "https://i.imgur.com/kJM9PAP.png")
        self.calvarion = Activity(Type.boss, "Cal'varion", "https://i.imgur.com/YcKry3h.png")
        self.cerberus = Activity(Type.boss, "Cerberus", "https://i.imgur.com/fWoVz8s.png")
        self.chambersOfXeric = Activity(Type.raid, "Chambers Of Xeric", "https://i.imgur.com/WTPVASA.png")
        self.chambersOfXericChallenge = Activity(Type.raid, "Chambers Of Xeric Challenge Mode", "https://i.imgur.com/9PGp3p1.png")
        self.chaosElemental = Activity(Type.boss, "Chaos Elemental", "https://i.imgur.com/fV939GA.png")
        self.chaosFanatic = Activity(Type.boss, "Chaos Fanatic", "https://i.imgur.com/AHPcI1o.png")
        self.commanderZilyana = Activity(Type.boss, "Commander Zilyana", "https://i.imgur.com/rf7vIIV.png")
        self.corporealBeast = Activity(Type.boss, "Corporeal Beast", "https://i.imgur.com/NpsdWii.png")
        self.crazyArchaeologist = Activity(Type.boss, "Crazy Archaeologist", "https://i.imgur.com/W1ja7BF.png")
        self.dagannothPrime = Activity(Type.boss, "Dagganoth Prime", "https://i.imgur.com/oEXx6Gu.png")
        self.dagganothRex = Activity(Type.boss, "Dagganoth Rex", "https://i.imgur.com/rV5ude7.png")
        self.dagganothSupreme = Activity(Type.boss, "Dagganoth Supreme", "https://i.imgur.com/oOgNkmR.png")
        self.derangedArchaeologist = Activity(Type.boss, "Deranged Archaeologist", "https://i.imgur.com/1VX25of.png")
        self.dukeSucellus = Activity(Type.boss, "Duke Sucellus", "https://i.imgur.com/g1p7QFs.png")
        self.generalGraardor = Activity(Type.boss, "General Graardor", "https://i.imgur.com/dsC3rT5.png")
        self.giantMole = Activity(Type.boss, "Giant Mole", "https://i.imgur.com/CSjGiQP.png")
        self.grotesqueGuardians = Activity(Type.boss, "Grotesque Guardians", "https://i.imgur.com/sSkzo7L.png")
        self.hespori = Activity(Type.boss, "Hespori", "https://i.imgur.com/LDhWY60.png")
        self.kalphiteQueen = Activity(Type.boss, "Kalphite Queen", "https://i.imgur.com/fcYB8Pq.png")
        self.kingBlackDragon = Activity(Type.boss, "King Black Dragon", "https://i.imgur.com/GMAp5JJ.png")
        self.kraken = Activity(Type.boss, "Kraken", "https://i.imgur.com/aMCS6pp.png")
        self.kreearra = Activity(Type.boss, "Kreearra", "https://i.imgur.com/iUUKMBC.png")
        self.kriltsutsaroth = Activity(Type.boss, "Kriltsutsaroth", "https://i.imgur.com/A6OW8p4.png")
        self.mimic = Activity(Type.boss, "Mimic", "https://i.imgur.com/ZHn6yPk.png")
        self.nex = Activity(Type.boss, "Nex", "https://i.imgur.com/piOFR8p.png")
        self.nightmare = Activity(Type.boss, "Nightmare", "https://i.imgur.com/PUJVzK6.png")
        self.phosanisNightmare = Activity(Type.minigame, "Phosani's Nightmare", "https://i.imgur.com/PUJVzK6.png")
        self.obor = Activity(Type.boss, "Obor", "https://i.imgur.com/DCGG89D.png")
        self.phantomMuspah = Activity(Type.boss, "Phantom Muspah", "https://i.imgur.com/ch29CKd.png")
        self.sarachnis = Activity(Type.boss, "Sarachnis", "https://i.imgur.com/axpYan0.png")
        self.scorpia = Activity(Type.boss, "Scorpia", "https://i.imgur.com/NPFDZCH.png")
        self.skotizo = Activity(Type.boss, "Skotizo", "https://i.imgur.com/rhX85uf.png")
        self.spindel = Activity(Type.boss, "Spindel", "https://i.imgur.com/hZqn7Yt.png")
        self.tempoross = Activity(Type.boss, "Tempoross", "https://i.imgur.com/gnys3sU.png")
        self.theGauntlet = Activity(Type.boss, "The Gauntlet", "https://i.imgur.com/kvIQwVL.png")
        self.theCorruptedGauntlet = Activity(Type.boss, "The Corrupted Gauntlet", "https://i.imgur.com/C1VDOWw.png")
        self.theLeviathon = Activity(Type.boss, 'The Leviathon', "https://i.imgur.com/KRoIZJM.png")
        self.theWhisperer = Activity(Type.boss, 'The Whisperer', "https://i.imgur.com/Xi9j7tn.png")
        self.theatreOfBlood = Activity(Type.raid, "Theatre Of Blood", "https://i.imgur.com/tYgPpZn.png")
        self.theatreOfBloodHardMode = Activity(Type.raid, "Theatre Of Blood Hard Mode", "https://i.imgur.com/tYgPpZn.png")
        self.ThermonuclearSmokeDevil = Activity(Type.boss, "Thermonuclear Smoke Devil", "https://i.imgur.com/7WN5AKv.png")
        self.tombsOfAmascut = Activity(Type.raid, "Tombs Of Amascut", "https://i.imgur.com/76EzlBt.png")
        self.tombsOfAmascutExpertMode = Activity(Type.raid, "Tombs Of Amascut Expert Mode", "https://i.imgur.com/76EzlBt.png")
        self.tzKalZuk = Activity(Type.boss, "TzKal-Zuk", "https://i.imgur.com/Y835Sv6.png")
        self.tzTokJad = Activity(Type.boss, "TzTok-Jad", "https://i.imgur.com/ihr1yHm.png")
        self.vardorvis = Activity(Type.boss, 'Vardorvis', "https://i.imgur.com/eGAjnMj.png")
        self.venenatis = Activity(Type.boss, "Venenatis", "https://i.imgur.com/RqgdOgJ.png")
        self.vetion = Activity(Type.boss, "Vetion", "https://i.imgur.com/aVt30z5.png")
        self.vorkath = Activity(Type.boss, "Vorkath", "https://i.imgur.com/Kg3xR1G.png")
        self.wintertodt = Activity(Type.minigame, "Wintertodt", "https://i.imgur.com/1Hyp6xJ.png")
        self.zalcano = Activity(Type.boss, "Zalcano", "https://i.imgur.com/5yDcjtk.png")
        self.zulrah = Activity(Type.boss, "Zulrah", "https://i.imgur.com/cAEgR9f.png")


class Skill:
    name = None
    rank = None
    level = None
    xp = None
    colour = None
    icon_url = None

    def __init__(self, colour, icon_url, name):
        self.colour = colour
        self.icon_url = icon_url
        self.name = name


class Activity:
    name = None
    rank = None
    count = None
    colour = 1098762
    icon_url = None
    type = None

    def __init__(self, type, name, icon_url):
        self.type = type
        self.name = name
        self.icon_url = icon_url

# ----------------------------------------------------------------------Init Player Names from file Into Object


class PlayerLogic:  # The use of a class is to limit the scope in which the Players dictionary can be accessed from.
    # Without the use of a class 'Players' would have to be a global variable which is bad practice.
    username = {}  # Init empty dictionary that will hold player name as key and player object as value
    buffer = None

    def __init__(self): # run on object creation
        self.init_players()

    @staticmethod
    def player_names_exists():
        if not os.path.exists("PlayerNames.txt"):  # Check if file exists
            with open("PlayerNames.txt", 'w') as file:  # if not, create an empty file of that name
                pass  # immediately pass in order to close the file
            return False
        return True

    @staticmethod
    def player_names_empty():
        return os.path.getsize("PlayerNames.txt") == 0

    def create_player_buffer(self):  # Creates Buffer Object for use with comparing API Data Between New & Previous
        self.buffer = Player(name='buffer', thumbnail=None)

    def player_into_object(self):
        with open("PlayerNames.txt", 'r') as file:
            for line in file:
                name = line.strip()
                # line is always players name, no need to cleanse string as spelling mistakes cannot be solved either.
                # player usernames cannot contain special characters so if it does the program will run into errors
                if not os.path.exists(f"thumbnails/{name}.png"):  # set thumbnail to default if custom one doesnt exist
                    thumbnail = "thumbnails/default.png"
                else:
                    thumbnail = f"thumbnails/{name}.png"
                self.username[name] = Player(name=name, thumbnail=thumbnail)

    def export_json(self):
        for player in self.username:
            with open(f"players/{player}.json", 'w') as file:
                file.write(jsonpickle.dumps(self.username[player]))

    def import_json(self):
        for player in self.username:
            if os.path.exists(f"players/{player}.json"):
                if not os.path.getsize(f"players/{player}.json") == 0:
                    with open(f"players/{player}.json") as file:
                        file.seek(0)
                        self.username[player] = jsonpickle.loads(file.read())
                        print(f"IMPORTED PLAYER: {self.username[player].name}")

    def init_players(self):
        if not self.player_names_exists():  # Check if file exists, if not create file, return False, exit with error.
            print("Error: No Player File Found - File Created - Populate With Usernames Separated One On Each Line")
            raise SystemExit
        if not self.player_names_empty():  # Check if file is empty, if empty ignore guard clause and raise systemexit
            self.create_player_buffer()
            self.player_into_object()
            self.import_json()
            return
        print("Error: PlayerNames.txt Is Empty. Please Populate With Usernames Separated One On Each Line")
        raise SystemExit
