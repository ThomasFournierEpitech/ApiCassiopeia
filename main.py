import cassiopeia as cass
from cassiopeia import Summoner, Match
from cassiopeia.data import Season, Queue
from collections import Counter

def takeLeaguePoints(elem):
    return elem.league_points
api_key = "RGAPI-b9446d2c-aa53-40f6-9d85-2ab9c884f5d9"
cass.set_riot_api_key(api_key)
region= "EUW"
challLeague = cass.get_challenger_league(queue=Queue.ranked_solo_fives, region=region)
challLeague.entries.sort(key=takeLeaguePoints, reverse=True)
for position, entry in enumerate(challLeague.entries):
    if (position == 0):

        bestEntry = entry
    print(entry.league_points, entry.summoner.name)
print("Best player:",bestEntry.summoner.name, " with ", bestEntry.league_points, " lp")
summoner = bestEntry.summoner
match_history = summoner.match_history
match_history(seasons={Season.season_9}, queues={Queue.ranked_solo_fives})
print("Length of match history:", len(match_history))
champion_id_to_name_mapping = {champion.id: champion.name for champion in cass.get_champions(region=region)}
played_champions = Counter()
for match in match_history:
    champion_id = match.participants[summoner.name].champion.id
    champion_name = champion_id_to_name_mapping[champion_id]
    played_champions[champion_name] += 1

print("Top 10 champions {} played:".format(summoner.name))
for champion_name, count in played_champions.most_common(10):
    print(champion_name, count)
print()
match = match_history[0]
print("\n", "Blue team won" if match.blue_team.win else "Red team won")
print("Participants on blue team:")
for p in match.blue_team.participants:
    print(p.summoner.name, " playing ", p.champion.name)
# Print keystone and the stat runes for each player/champion
for p in match.participants:
    print(p.champion.name, "'s keystones: ", p.runes.keystone.name, *[r.name for r in p.stat_runes])
