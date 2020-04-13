import requests, json
'''
[
  {
    "teamname": "Name",
    "wins": 1,
    "losses": 1,
    "ties": 1,
    "players": [
      {
        "player": {
          "playerno": " 1",
          "playername": "Name"
        }
      },
      {
        "player": {
          "playerno": " 2",
          "playername": "Name"
        }
      },
      .
      .
      .
      {
        "player": {
          "playerno": " n",
          "playername": "Name"
        }
      }
    ]
  },
  .
  .
  .
  {
    "teamname": "Name2",
    "wins": 1,
    "losses": 1,
    "ties": 1,
    "players": [
      {
        "player": {
          "playerno": " 1",
          "playername": "Name"
        }
      },
      {
        "player": {
          "playerno": " 2",
          "playername": "Name"
        }
      },
      .
      .
      .
      {
        "player": {
          "playerno": " n",
          "playername": "Name"
        }
      }
    ]
  }
]
'''

#function to get team data
def get_team_data(link):
    teamdata = requests.get(link)
    f = open('teamdata.html', 'w')
    f.write(teamdata.text)
    f.close()
    f = open('teamdata.html', 'r')
    team_data_lines = f.read().split('\n')
    f.close()
    
    team = {}
    teamname_parse = True
    tc = 0
    cc = 0
    cc2 = 0
    rc = 0
    rc2 = 0
    
    player_no_list = []
    player_name_list = []
    for teamline in team_data_lines:

        #get team-name
        if '&nbsp;' in teamline and '<BR>' in teamline and teamname_parse:
            teamname = teamline.split('&nbsp;')[1]
            teamname = teamname.split('<BR>')[0]
            teamname_parse = False
            team['team-name'] = teamname

        #counting table
        if '<table width="856" border=1 cellpadding=1 cellspacing=1 class="chssmallreg">' in teamline:
            tc+=1

        #counting rows
        if '<tr valign=top align=right>' in teamline:
            rc+=1
            cc = 0

        #counting columns
        if '<td ' in teamline:
            cc+=1

        #get player-no   
        if tc == 1 and cc == 0 and ' </td>' in teamline:
            player_no = teamline.split('<td>')[1]
            player_no = player_no.split(' </td>')[0]
            player_no_list.append(player_no)

        #get player-name
        if tc == 1 and cc == 1 and '<strong>' in teamline:
            player_name = teamline.split('<strong>')[1]
            player_name = player_name.split('</strong>')[0]
            player_name_list.append(player_name)
        
        #counting row and columns for table 6
        if tc == 6 and '<tr' in teamline:
          rc2+=1
          cc2 = 0
        
        #columns for table 6
        if tc == 6 and '<td' in teamline:
          cc2+=1

        #getting team wins, losses and ties
        if tc == 6 and rc2 == 2 and cc2 == 4:
            score = teamline.split('>')[1]
            score = score.split('</')[0]
            team['wins'] = int(score.split('-')[0])
            team['losses'] = int(score.split('-')[1])
            team['ties'] = int(score.split('-')[2])

    #appending player data
    players = []
    team['players'] = []
    for i,j in zip(player_no_list, player_name_list):
        player = {}
        player['player'] = {}
        player['player']['playerno'] = i
        player['player']['playername'] = j
        players.append(player)
    
    team['players'] = players

    #return team dictionary
    return team  

#for getting links of team data
data = requests.get('http://www.collegehockeystats.net/1920/teamstats/ecachm')
f = open('teamname_link.html', 'w')
f.write(data.text)
f.close()
f = open('teamname_link.html', 'r')
lines = f.read().split('\n')
f.close()

teams = []
#setting 
mainlink = 'http://www.collegehockeystats.net'

#extracting link and getting team data and appending it
for line in lines:
    if '<A HREF="/1920' in line: 
            link = line.split('"')[1]
            url = mainlink+link
            teamdata = get_team_data(url)
            teams.append(teamdata)

#printing json structured team data.
print(json.dumps(teams))