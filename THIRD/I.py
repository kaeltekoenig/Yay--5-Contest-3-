def divide_mquery(strn):
    div1 = strn.find('-')
    div2 = strn.rfind('"')
    div3 = strn.rfind(':')

    at = strn[1:div1- 2]
    bt = strn[div1 + 3:div2]
    ascr = int(strn[div2 + 2:div3])
    bscr = int(strn[div3 + 1:])

    return at, bt, ascr, bscr


def provide_goalinfo(strn):
    strn = strn.split()
    kckr = ' '.join(strn[:-1])
    mnt = int(strn[-1].strip('\''))

    return kckr, mnt


def add_team_info(tms_dict, tm, tmgls):
    if tm not in tms_dict:
        tms_dict[tm] = {
            'games': 1,
            'goals': tmgls,
            'opener': 0
                        }
    else:
        tms_dict[tm]['games'] += 1
        tms_dict[tm]['goals'] += tmgls


def collect_current_match_info(crnt, kckr, gmnt):
    if kckr not in crnt:
        crnt[kckr] = [gmnt]
    else:
        crnt[kckr].append(gmnt)


def define_opener(crnt=dict):
    minmnt = 91
    opnr = ''
    for k, v in crnt.items():
        for mv in v:
            if mv < minmnt:
                minmnt = mv
                opnr = k

    return opnr


def add_player_info(pldict, plr, tm, glsmnt):
    if plr not in pldict:
        pldict[plr] = {
            'team': tm,
            'games': 0,
            'goals': [glsmnt],
            'opener': 0
            }
    else:
        pldict[plr]['goals'].append(glsmnt)


def add_adjacent_info(opnr, plrdict, tmdict):
    plrdict[opnr]['opener'] += 1
    opnr_tm = plrdict[opnr]['team']
    tmdict[opnr_tm]['opener'] += 1


def process_query_total_goals(strn, plrdct, tmdict):
    if 'Total goals by ' in strn:
        plr = strn[15:].strip()
        if plr in plrdct:
            return len(plrdct[plr]['goals'])
    elif 'Total goals for "' in strn:
        tm = strn[17:strn.rfind('"')]
        if tm in tmdict:
            return tmdict[tm]['goals']

    return 0


def process_query_mean_goals(strn, plrdct, tmdict):
    if 'Mean goals per game by ' in strn:
        plr = strn[22:].strip()
        if plr in plrdct:
            return len(plrdct[plr]['goals']) / plrdct[plr]['games']
    elif 'Mean goals per game for "' in strn:
        tm = strn[25:strn.rfind('"')]
        if tm in tmdict:
            return tmdict[tm]['goals'] / tmdict[tm]['games']

    return 0


def process_query_goalson(strn, plrdct):
    plr = strn[strn.find('y') + 2:].strip()
    mnt = int(''.join([sym for sym in strn if sym.isdigit()]))
    if 'Goals on minute ' in strn:
        if plr in plrdct:
            return sum(g == mnt for g in plrdct[plr]['goals'])
    elif 'Goals on first ' in strn:
        if plr in plrdct:
            return sum(g <= mnt for g in plrdct[plr]['goals'])
    elif 'Goals on last ' in strn:
        if plr in plrdct:
            return sum(g >= 91 - mnt for g in plrdct[plr]['goals'])

    return 0


def process_query_openers(strn, plrdct, tmdct):
    if '"' in strn:
        tm = strn[strn.find('y') + 3:strn.rfind('"')]
        if tm in tmdct:
            return tmdct[tm]['opener']
    else:
        plr = strn[strn.find('y') + 2:].strip()
        if plr in plrdct:
            return plrdct[plr]['opener']

    return 0

####################################
teams = {}
players = {}

with open('output.txt', 'w') as z:
    with open('input.txt', 'r') as f:
        while True:
            query = f.readline()
            if query == '':
                break

            if '-' in query:    # МАТЧ
                a, b, agoals, bgoals = divide_mquery(query)
                add_team_info(teams, a, agoals)
                add_team_info(teams, b, bgoals)

                current_match = {}
                for _ in range(agoals):
                    goal = f.readline()
                    kicker, goalminute = provide_goalinfo(goal)
                    add_player_info(players, kicker, a, goalminute)
                    collect_current_match_info(current_match, kicker, goalminute)
                    
                for _ in range(bgoals):
                    goal = f.readline()
                    kicker, goalminute = provide_goalinfo(goal)
                    add_player_info(players, kicker, b, goalminute)
                    collect_current_match_info(current_match, kicker, goalminute)
                
                if current_match:
                    add_adjacent_info(define_opener(current_match), players, teams)

                for player in players.keys():
                    if players[player]['team'] == a:
                        players[player]['games'] = teams[a]['games']
                    elif players[player]['team'] == b:
                        players[player]['games'] = teams[b]['games']

            elif query.startswith('Total goals'):
                print(process_query_total_goals(query, players, teams), file=z)
            elif query.startswith('Mean goals'):
                print(process_query_mean_goals(query, players, teams), file=z)
            elif query.startswith('Goals on'):
                print(process_query_goalson(query, players), file=z)
            elif query.startswith('Score opens'):
                print(process_query_openers(query, players, teams), file=z)

