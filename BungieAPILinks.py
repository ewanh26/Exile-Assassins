import math, sqlite3, os, requests, json
from Dicts import nameToId, idToName, modeToNum, numToMode, defToQueryIndex
from functools import lru_cache

API_KEY = 'be8a6658c34947deb6de2c5c6eb75dd7' #HAHA U CANT SEE MY API KEY
API_KEY_HEADER = { 'X-API-Key' : API_KEY }

myId = 15516748
clanId = 3732004
clanDetails = requests.get(
        'https://www.bungie.net/Platform//GroupV2/Name/Exile Assassins/1/',
        headers=API_KEY_HEADER
    ).json()['Response']['detail']

convertToHoursAndMins = lambda i : str(math.floor(i / 60))+ 'h' + ' ' + str(i % 60)+ 'm'

for f in os.listdir(path='.'):
    if f.startswith("world_sql_content_"):
        SQLFile = f
SQLQueries = [qry for qry in open('./SQL/Queries.sql', 'r').read().split(';')]
del SQLQueries[-1] #There was an empty element at the end of the list due to formatting, just deleting it here.

lbStats = ['lbSingleGameKills', 'lbPrecisionKills', 'lbAssists', 'lbDeaths', 'lbKills', 'lbObjectivesCompleted', 'lbSingleGameScore']
def getLeaderboard(mode_i, statid): #Only leaderboard stats can be used: [lbSingleGameKills, lbPrecisionKills, lbAssists, lbDeaths, lbKills, lbObjectivesCompleted, lbSingleGameScore]
    clanLeaderboard_res = requests.get(
            f'https://www.bungie.net/Platform/Destiny2/Stats/Leaderboards/Clans/{clanId}?maxtop=100&statid={statid}&modes={mode_i}',
            headers=API_KEY_HEADER
        ).json()
    try:
        clanLeaderboard_res = clanLeaderboard_res['Response']
        clanLeaderboard_ModeStat = clanLeaderboard_res[numToMode[mode_i]][statid]
    except KeyError:
        return {"NO DATA":"NO DATA"}

    return {
        clanLeaderboard_ModeStat['entries'][i]['player']['destinyUserInfo']['displayName']: 
        clanLeaderboard_ModeStat['entries'][i]['value']['basic']['value']
        for i in range(len(clanLeaderboard_ModeStat['entries']))
    }

userInfoCards = {
    k:requests.get(
        f'https://www.bungie.net/Platform/Destiny2/SearchDestinyPlayer/2/{k}/',
        headers=API_KEY_HEADER
    ).json()['Response'] for k in nameToId.keys()
}
#print(userInfoCards)

def getProfileComponentsForPlayer(componentID, player):
    profile = {}
    try:
        profile[player] = requests.get(
            f'https://www.bungie.net/Platform/Destiny2/{userInfoCards[player][0]["membershipType"]}/Profile/{userInfoCards[player][0]["membershipId"]}/?components={componentID}',
            headers=API_KEY_HEADER
        ).json()['Response']
    except IndexError:
        return profile
    return profile

def getComponentsForCharacter(componentID, characterID):
    player = characterIDToPlayer[str(characterID)]
    return requests.get(
        f'https://www.bungie.net/Platform/Destiny2/{userInfoCards[player][0]["membershipType"]}/Profile/{userInfoCards[player][0]["membershipId"]}/Character/{characterID}/?components={componentID}',
        headers=API_KEY_HEADER
    ).json()['Response']

def getStatsForCharacter(mode_i, group_s, characterID):
    player = characterIDToPlayer[str(characterID)]
    return requests.get(
        f'https://www.bungie.net/Platform/Destiny2/{userInfoCards[player][0]["membershipType"]}/Account/{userInfoCards[player][0]["membershipId"]}/Character/{characterID}/Stats/?modes={mode_i}&groups={group_s}&periodType=AllTime',
        headers=API_KEY_HEADER
    ).json()['Response'][numToMode[mode_i]]['allTime']

@lru_cache(maxsize=None)
def define(definition, hash_, hs=False):
    SQLConnection = sqlite3.connect(SQLFile)
    SQLCursor = SQLConnection.cursor()
    if not hs:
        SQLCursor.execute(
            SQLQueries[defToQueryIndex[definition]]+ str(signedHash(int(hash_)))
        )
        SQLResult = SQLCursor.fetchall()
        return json.loads(SQLResult[0][0])
    else:
        SQLCursor.execute(
            SQLQueries[defToQueryIndex[definition]]+ hash_
        )
        SQLResult = SQLCursor.fetchall()
        return json.loads(SQLResult[0][0])

def getCurrentSQLManifestDatabasePath(filename=False):
    path = 'https://www.bungie.net' + str(
        requests.get(
            'https://www.bungie.net/Platform/Destiny2/Manifest/',
            headers=API_KEY_HEADER
        ).json()['Response']['mobileWorldContentPaths']['en']
    )
    if filename:
        return path.split('/')[7][:-8] + '.sqlite3'
    else:
        return path

playerToCharacterIDs = {
    player : getProfileComponentsForPlayer(100, player)[player]['profile']['data']['characterIds'] for player in nameToId.keys()
}
characterIDToPlayer = {}
for player, characterIDList in playerToCharacterIDs.items():
    for characterID in characterIDList:
        characterIDToPlayer[characterID] = player

@lru_cache(maxsize=None)
def signedHash(hash):
    if hash & (1 << (32 - 1)) != 0:
        return hash - (1 << 32)
    else:
        return hash

def stringFormat(s):
    res = ''
    startCap = False
    for char in s:
        if char == s[0] and not startCap:
            res += char.upper()
            startCap = True
        elif char.isupper() or char.isdigit():
            res += f' {char}'
        elif char == '_':
            s += ' '
        else:
            res += char
    return res

#print(stringFormat("medal5xStreak"))

#print(getCurrentSQLManifestDatabasePath())
#print(getProfileComponentsForPlayer(201, 'Harry221019'))
#print(define('InventoryItem', 4248569242))
#print(characterIDToPlayer)
#print(getComponentsForCharacter(200, 2305843009430784091))
#print(userInfoCards)
#print(getStatsForCharacter(modeToNum['allPvE'], 'Medals', 2305843009430784091))
#print(getLeaderboard('lbKills', modeToNum['allPvE']))

#    for player in nameToId.keys():
#        for characterIDList in playerToCharacterIDs[player]:
#            for character in characterIDList:
#                print({getProfileComponentsForPlayer(1100, player)[player]['characters']['data']['character']['emblemPath']})


