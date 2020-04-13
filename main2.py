import requests, json

def isint(value):
  try:
    int(value)
    return True
  except ValueError:
    return False

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
    player_gameplayed_list = []
    player_goal_list = []
    player_assisted_list = []
    count = 0
    for teamline in team_data_lines:
        if '&nbsp;' in teamline and '<BR>' in teamline and teamname_parse:
            teamname = teamline.split('&nbsp;')[1]
            teamname = teamname.split('<BR>')[0]
            #print(teamname)
            teamname_parse = False
            team['teamname'] = teamname

        if '<table width="856" border=1 cellpadding=1 cellspacing=1 class="chssmallreg">' in teamline:
            tc+=1

        if '<tr valign=top align=right>' in teamline:
            rc+=1
            cc = 0

        if '<td ' in teamline:
            cc+=1
            
        if tc == 1 and cc == 0 and ' </td>' in teamline:
            player_no = teamline.split('<td>')[1]
            player_no = player_no.split(' </td>')[0]
            #print(int(player_no))
            player_no_list.append(player_no)
            count+=1

        if tc == 1 and cc == 1 and '<strong>' in teamline:
            player_name = teamline.split('<strong>')[1]
            player_name = player_name.split('</strong>')[0]
            #print(player_name)
            player_name_list.append(player_name)

        if tc == 1 and cc == 4:
            if '<td bgcolor="#FFFFFF"' in teamline and '&nbsp;' not in teamline:
              #print(tc, rc, cc, teamline)
              gameplayed = teamline.split('>')[1]
              gameplayed = gameplayed.split('<')[0]
              player_gameplayed_list.append(gameplayed)

        if tc == 1 and cc == 5:
            if '<td bgcolor="#FFFFFF"' in teamline and '&nbsp;' not in teamline:
              #print(tc, rc, cc, teamline)
              goal = teamline.split('>')[1]
              goal = goal.split('<')[0]
              player_goal_list.append(goal)
        
        if tc == 1 and cc == 6:
            if '<td bgcolor="#FFFFFF"' in teamline and '&nbsp;' not in teamline:
              print(tc, rc, cc, teamline)
              assisted = teamline.split('>')[1]
              assisted = assisted.split('<')[0]
              if isint(assisted):
                print(assisted, 'True')
                player_assisted_list.append(assisted)
              else:
                print(assisted, "False")
              '''
              print(assisted)
              if count == len(player_assisted_list):
                print('Okay')
              else:
                player_assisted_list.pop()
                print("False")
              '''
        if tc == 6 and '<tr' in teamline:
          rc2+=1
          cc2 = 0
        
        if tc == 6 and '<td' in teamline:
          cc2+=1

        if tc == 6 and rc2 == 2 and cc2 == 4:
            #print(tc, rc2, cc2, teamline)
            score = teamline.split('>')[1]
            score = score.split('</')[0]
            team['wins'] = int(score.split('-')[0])
            team['losses'] = int(score.split('-')[1])
            team['ties'] = int(score.split('-')[2])

    players = []
    team['players'] = []
    for i,j,k,l,m in zip(player_no_list, player_name_list,player_gameplayed_list, player_goal_list, player_assisted_list):
        player = {}
        player['player'] = {}
        player['player']['playerno'] = i
        player['player']['playername'] = j
        player['player']['gameplayed'] = k
        player['player']['goal'] = l
        player['player']['assisted'] = m
        players.append(player)
        #print(i, j)
    #print(json.dumps(players))
    team['players'] = players
    
    return team  

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
data = requests.get('http://www.collegehockeystats.net/1920/teamstats/ecachm')
f = open('teamname_link.html', 'w')
f.write(data.text)
f.close()

f = open('teamname_link.html', 'r')
lines = f.read().split('\n')
f.close()

teams = []
mainlink = 'http://www.collegehockeystats.net'
parse = False

for line in lines:
    if '<A' in line:
        parse = True
    
    if parse and '1920' in line: 
            link = line.split('"')[1]
            url = mainlink+link
            teamdata = get_team_data(url)
            teams.append(teamdata)

#print(json.dumps(teams))   

    
