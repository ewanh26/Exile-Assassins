from flask import *
from flask_caching import Cache
from BungieAPILinks import *

app = Flask(__name__)

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 1000
}
app.config.from_mapping(config)
cache = Cache(app)

@app.route('/')
def root():
    return redirect(url_for("home"))

@app.route("/home")
def home():
    return render_template('index.html')

@app.route('/members')
def membersNULL():
    return redirect(url_for("members", member="all", character="NA"))

@app.route('/members/<member>/<character>')
@cache.cached(timeout=3600) #1 hour
def members(member, character):
    if member == "all" and character == "NA":
        return render_template(
            'members.html',
            nameToId=nameToId,
            playerToCharacterIDs=playerToCharacterIDs,
            getProfileComponentsForPlayer=lambda c, p : getProfileComponentsForPlayer(c, p),
            define=lambda d, h : define(d, h)
        )
    else:
        res = getComponentsForCharacter(200, character)['character']['data']
        equips = getComponentsForCharacter(205, character)['equipment']['data']['items']
        generalHS_PVP = getStatsForCharacter(modeToNum['allPvP'], 'General', character)
        generalHS_PVE = getStatsForCharacter(modeToNum['allPvE'], 'General', character)
        medalHS_PVP = getStatsForCharacter(modeToNum['allPvP'], 'Medals', character)
        return render_template(
            "member.html",
            player=member,
            profileComponentsForCharacter=res,
            equipment=equips,
            define=lambda d, h : define(d, h),
            generalPvP=generalHS_PVP,
            generalPvE=generalHS_PVE,
            medalPvP=medalHS_PVP,
            format=lambda s : stringFormat(s),
            time=convertToHoursAndMins(int(res['minutesPlayedTotal'])),
            lastPlayed=res['dateLastPlayed'][:10]+' '+res['dateLastPlayed'][11:19]
        )

@app.route("/leaderboards")
def leaderboardsNULL():
    return redirect(url_for("leaderboards", mode="none", stat="none"))

@app.route('/leaderboards/<mode>/<stat>')
def leaderboards(mode, stat):
    lb = getLeaderboard(modeToNum[mode], str(stat))
    return render_template(
        "leaderboard.html",
        modeToNum=modeToNum,
        lbStats=lbStats,
        format=lambda s : stringFormat(s),
        lb=lb
    )

@app.route('/lore')
def lore():
    return render_template("lore.html")

if __name__ == "__main__":
    app.run(debug=True)