import os
import random
import discord
from keep_alive import keep_alive

# AGENTS
AGENT = {
    "AGENT_MALE": [
        "BRIMSTONE", "OMEN", "CYPHER", "SOVA", "PHOENIX", "BREACH", "YORU",
        "KAY/O", "CHAMBER"
    ],
    "AGENT_FEMALE": [
        "VIPER", "KILLJOY", "SAGE", "JETT", "REYNA", "RAZE", "SKYE", "ASTRA",
        "NEON", "FADE"
    ],
    "AGENT_CONTROLLER": ["BRIMSTONE", "VIPER", "OMEN", "ASTRA"],
    "AGENT_DUELIST": ["PHONENIX", "JETT", "REYNA", "RAZE", "YORU", "NEON"],
    "AGENT_INITIATOR": ["SOVA", "BREACH", "SKYE", "KAY/O", "FADE"],
    "AGENT_SENTINEL": ["KILLJOY", "CYPHER", "SAGE", "CHAMBER"]
}

# GUNS
GUN = {
    "GUN_NOPISTOL": [
        "BULLDOG", "PHANTOM", "VANDAL", "ARES", "ODIN", "STINGER", "SPECTRE",
        "JUDGE", "SHORTY", "GUARDIAN", "MARSHAL", "OPERATOR"
    ],
    "GUN_PISTOL": ["CLASSIC", "SHORTY", "FRENZY", "GHOST", "SHERIFF"],
    "GUN_RIFLES": ["BULLDOG", "PHANTOM", "VANDAL"],
    "GUN_MACHINEGUNS": ["ARES", "ODIN"],
    "GUN_SMG": ["STINGER", "SPECTRE"],
    "GUN_SHORT": ["BUCKY", "JUDGE", "SHORTY"],
    "GUN_ONESHOT": ["GUARDIAN", "MARSHAL", "OPERATOR"]
}

# MAPS
MAPS = ["BIND", "HAVEN", "SPLIT", "ASCENT", "ICEBOX", "BREEZE", "FRACTURE"]

# Bot
TOKEN = os.environ['TOKEN']
client = discord.Client()

# Base
playerBaselist = []
agentBaselist = []
gunBaselist = []
mapBaselist = []
playerData = {}


def Printing(output, list):
    for object in list:
        output += object + "\t|\t"
    return (output)


def RollPrinting(selectedMap, inputData):
    try:
        if selectedMap != None:
            output = f"Map Selected {selectedMap}\n\n"
        else:
            output = ""
    except IndexError:
        return "Use V!roll.all first!"
    for player in inputData:
        try:
            output += f'{player}\t:\t{inputData[player][0]}\t|\t{inputData[player][1]}\n'
        except IndexError:
            return "Use V!roll.all first!"
    return output


def Listing(objList):
    if objList.startswith("V!list.player"):
        if len(playerBaselist) > 0:
            return Printing("Current Player List:\n|\t", playerBaselist)
        else:
            return "Player List is Empty!"
    if objList.startswith("V!list.agent"):
        if len(agentBaselist) > 0:
            return Printing("Current Agent List:\n|\t", agentBaselist)
        else:
            return "Agent List is Empty!"
    if objList.startswith("V!list.gun"):
        if len(gunBaselist) > 0:
            return Printing("Current Gun List:\n|\t", gunBaselist)
        else:
            return "Gun List is Empty!"
    if objList.startswith("V!list.map"):
        if len(mapBaselist) > 0:
            return Printing("Current Map List:\n|\t", mapBaselist)
        else:
            return "Map List is Empty!"
    if objList.startswith("V!list.all"):
        return Listing("V!list.player") + "\n\n\n" + Listing(
            "V!list.agent") + "\n\n\n" + Listing(
                "V!list.gun") + "\n\n\n" + Listing("V!list.map")
    return 'Name of the category to list is not found'


def Adding(objList):
    title = objList.pop(0)
    if title == "V!add.player":
        for player in objList:
            if player.upper() not in playerBaselist:
                playerBaselist.append(player.upper())
        return Printing("Current Player list:\n|\t", playerBaselist)
    if title == "V!add.agent":
        for agent in objList:
            if agent.upper() in AGENT.keys():
                for fixedAgent in AGENT[agent.upper()]:
                    if fixedAgent not in agentBaselist:
                        agentBaselist.append(fixedAgent.upper())
            elif agent.upper() in AGENT["AGENT_MALE"] or agent.upper(
            ) in AGENT["AGENT_FEMALE"]:
                if agent.upper() not in agentBaselist:
                    agentBaselist.append(agent.upper())
            else:
                return f"{agent} is not a valid agent in the list"
        return Printing("Current Agent list:\n|\t", agentBaselist)
    if title == "V!add.gun":
        for gun in objList:
            if gun.upper() in GUN.keys():
                for fixedgun in GUN[gun.upper()]:
                    if fixedgun not in gunBaselist:
                        gunBaselist.append(fixedgun.upper())
            elif gun.upper() in GUN["GUN_PISTOL"] or gun.upper(
            ) in GUN["GUN_NOPISTOL"]:
                if gun.upper() not in gunBaselist:
                    gunBaselist.append(gun.upper())
            else:
                return f"{gun} is not a valid gun in the list"
        return Printing("Current Gun list:\n|\t", gunBaselist)
    if title == "V!add.map":
        for map in objList:
            if map.upper() in MAPS:
                if map.upper() not in mapBaselist:
                    mapBaselist.append(map.upper())
            else:
                return f"{map} is not a valid map in the list"
        return Printing("Current Map list:\n|\t", mapBaselist)
    return 'Name of the category to add is not found'


def Removing(objList):
    title = objList.pop(0)
    if title == "V!remove.player":
        for player in objList:
            playerBaselist.remove(player.upper())
        return Printing("Current Player List:\n|\t", playerBaselist)
    if title == "V!remove.agent":
        for agent in objList:
            if agent.upper() in AGENT.keys():
                for fixedAgent in AGENT[agent.upper()]:
                    if fixedAgent in agentBaselist:
                        agentBaselist.remove(fixedAgent.upper())
            elif agent.upper() in AGENT["AGENT_MALE"] or agent.upper(
            ) in AGENT["AGENT_FEMALE"]:
                if agent.upper() in agentBaselist:
                    agentBaselist.remove(agent.upper())
            else:
                return f"{agent} is not a valid agent in the list"
        return Printing("Current Agent List:\n|\t", agentBaselist)
    if title == "V!remove.gun":
        for gun in objList:
            if gun.upper() in GUN.keys():
                for fixedgun in GUN[gun.upper()]:
                    if fixedgun in gunBaselist:
                        gunBaselist.remove(fixedgun.upper())
            elif gun.upper() in GUN["GUN_NOPISTOL"] or gun.upper(
            ) in GUN["GUN_PISTOL"]:
                if gun.upper() in gunBaselist:
                    gunBaselist.remove(gun.upper())
            else:
                return f"{gun} is not a valid gun in the list"
        return Printing("Current Gun List:\n|\t", gunBaselist)
    if title == "V!remove.map":
        for map in objList:
            if map.upper() in MAPS:
                if map.upper() in mapBaselist:
                    mapBaselist.remove(map.upper())
            else:
                return f"{map} is not a valid map in the list"
        return Printing("Current Map list:\n|\t", mapBaselist)
    return 'Name of the category to remove is not found'


def Clearing(objList):
    title = objList.pop(0)
    if title == "V!clear.player":
        playerBaselist.clear()
        return 'Player List Cleared! Use "V!add.player <playername>" to add players!'
    if title == "V!clear.agent":
        agentBaselist.clear()
        return 'Agent List Cleared! Use "V!add.agent <agentname>" to add agent!'
    if title == "V!clear.gun":
        gunBaselist.clear()
        return 'Gun List Cleared! Use "V!add.gun <gunname>" to add gun!'
    if title == "V!clear.map":
        mapBaselist.clear()
        return 'Map List Cleared! Use "V!add.map <mapname>" to add map!'
    if title == "V!clear.all":
        playerBaselist.clear()
        agentBaselist.clear()
        gunBaselist.clear()
        mapBaselist.clear()
        return 'All Lists have been cleared! Use "V!add" to add stuffs!'
    return 'Name of the list to clear is not found'


def Defaulting(objList):
    title = objList.pop(0)
    if title == "V!default.agent":
        agentBaselist.clear()
        for agent in AGENT["AGENT_MALE"]:
            agentBaselist.append(agent.upper())
        for agent in AGENT["AGENT_FEMALE"]:
            agentBaselist.append(agent.upper())
        return Printing("Current Agent list:\n|\t", agentBaselist)
    if title == "V!default.gun":
        gunBaselist.clear()
        for gun in GUN["GUN_NOPISTOL"]:
            gunBaselist.append(gun.upper())
        for gun in GUN["GUN_PISTOL"]:
            gunBaselist.append(gun.upper())
        return Printing("Current Gun list:\n|\t", gunBaselist)
    if title == "V!default.map":
        mapBaselist.clear()
        for map in MAPS:
            mapBaselist.append(map.upper())
        return Printing("Current Map list:\n|\t", mapBaselist)
    if title == "V!default.all":
        return Defaulting(objList=["V!default.agent"]) + "\n\n\n" + Defaulting(
            objList=["V!default.gun"]) + "\n\n\n" + Defaulting(
                objList=["V!default.map"])
    return 'Name of the category to default is not found'


def Rolling(objList):
    title = objList.pop(0)
    if title == "V!roll.all":
        if len(playerBaselist) == 0:
            return 'Player list is empty! Use "V!add.player <playername>" to add players!'
        if len(agentBaselist) == 0:
            return 'Agent list is empty! Use "V!add.agent <agentname>" to add agents!'
        if len(gunBaselist) == 0:
            return 'Gun list is empty! Use "V!add.gun <gunname>" to add guns!'
        if len(mapBaselist) == 0:
            return 'Map list is empty! Use "V!add.map <mapname>" to add maps!'
        tempAgentlist = agentBaselist.copy()
        tempGunlist = gunBaselist.copy()
        for player in playerBaselist:
            if len(tempAgentlist) == 0:
                tempAgentlist = agentBaselist.copy()
            if len(tempGunlist) == 0:
                tempGunlist = gunBaselist.copy()
            randomAgent = random.choice(tempAgentlist)
            randomGun = random.choice(tempGunlist)
            playerData[player] = [randomAgent, randomGun]
            tempGunlist.remove(randomGun)
            tempAgentlist.remove(randomAgent)
        selectedMap = random.choice(mapBaselist)
        return RollPrinting(selectedMap, playerData)
    if title == "V!roll.agent.all":
        for player in playerBaselist:
            Rolling(["V!roll.agent", player.upper()])
        return RollPrinting(None, playerData)
    if title == "V!roll.agent":
        if len(playerBaselist) == 0:
            return 'Player list is empty! Use "V!add.player <playername>" to add players!'
        if len(agentBaselist) == 0:
            return 'Agent list is empty! Use "V!add.agent <agentname>" to add agents!'
        if len(objList) == 0:
            return "Enter a player's name following the command to reroll his/her agent"
        tempAgentlist = agentBaselist.copy()
        for player in playerData:
            if len(tempAgentlist) == 0:
                tempAgentlist = agentBaselist.copy()
            if playerData[player][0] in tempAgentlist:
                tempAgentlist.remove(playerData[player][0])
        for player in objList:
            if player.upper() not in playerBaselist:
                return f"Player name {player} not found!"
            if len(tempAgentlist) == 0:
                tempAgentlist = agentBaselist.copy()
            randomAgent = random.choice(tempAgentlist)
            if playerData.get(player.upper()) == None:
                playerData[player.upper()] = [randomAgent]
            else:
                playerData[player.upper()][0] = randomAgent
        return RollPrinting(None, playerData)
    if title == "V!roll.gun":
        if len(playerBaselist) == 0:
            return 'Player list is empty! Use "V!add.player <playername>" to add players!'
        if len(gunBaselist) == 0:
            return 'Gun list is empty! Use "V!add.gun <gunname>" to add guns!'
        if len(objList) == 0:
            return "Enter a player's name following the command to reroll his/her agent"
        tempGunlist = gunBaselist.copy()
        for player in playerData:
            if len(tempGunlist) == 0:
                tempGunlist = gunBaselist.copy()
            if playerData[player][1] in tempGunlist:
                tempGunlist.remove(playerData[player][1])
        for player in objList:
            if player.upper() not in playerBaselist:
                return f"Player name {player} not found!"
            if len(tempGunlist) == 0:
                tempGunlist = agentBaselist.copy()
            randomGun = random.choice(tempGunlist)
            if playerData.get(player.upper()) == None:
                playerData[player.upper()] = [randomGun]
            else:
                playerData[player.upper()][1] = randomGun
        return RollPrinting(None, playerData)
    if title == "V!roll.gun.all":
        for player in playerBaselist:
            Rolling(["V!roll.gun", player.upper()])
        return RollPrinting(None, playerData)
    if title == "V!roll.map":
        if len(mapBaselist) == 0:
            return 'Map list is empty! Use "V!add.map <mapname>" to add maps!'
        selectedMap = random.choice(mapBaselist)
        return RollPrinting(selectedMap, playerData)
    return 'Name of the category to roll is not found'


def Helping():
  return "https://docs.google.com/document/d/1K7YmGcIEe_mnknwR_ETUcsD4iAMxicpTokYsrypA2IY/edit?usp=sharing"


@client.event
async def on_ready():
    print(f'We have logged in as {client}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content
    if msg.startswith("V!list"):
        await message.channel.send(f'```{Listing(msg)}```')
    elif msg.startswith("V!add"):
        await message.channel.send(f'```{Adding(msg.split(" "))}```')
    elif msg.startswith("V!remove"):
        await message.channel.send(f'```{Removing(msg.split(" "))}```')
    elif msg.startswith("V!clear"):
        await message.channel.send(f'```{Clearing(msg.split(" "))}```')
    elif msg.startswith("V!default"):
        await message.channel.send(f'```{Defaulting(msg.split(" "))}```')
    elif msg.startswith("V!roll"):
        await message.channel.send(f'```{Rolling(msg.split(" "))}```')
    elif msg.startswith("V!help"):
        await message.channel.send(f'```{Helping()}```')
    elif msg.startswith("V!"):
        await message.channel.send(
            "Command not recognized, use V!help for list of commands")


keep_alive()
client.run(TOKEN)
