import requests

data = requests.get('http://www.collegehockeystats.net/1920/teamstats/ecachm')

f = open('teamname-link.html', 'w')
f.write(data.text)
f.close()

f = open('teamname-link.html', 'r')
lines = f.read().split('\n')
f.close()

parse = False
teamnames = {}
for line in lines:
    if '<A' in line:
        parse = True
    if parse and '1920' in line:
        teamname = line.split('>')[1]
        teamname = teamname.split('<')[0]
        if teamname in teamnames:
            teamnames[teamname] = {}
        else:
            teamnames[teamname] = {}

print(teamnames)

