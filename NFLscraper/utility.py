import pandas as pd

def team_schedule(teamcode:str, year:int) -> pd.DataFrame:
    """
    Gets the schedule for the requested team and year

    Args:
        teamcode (_type_): e.g. "nwe" for New England Patriots
    """    
    url = f'https://www.pro-football-reference.com/teams/{teamcode}/2024.htm'  # To get the schedule of one team
    resp = pd.read_html(url)
    df = resp[1]

def year_schedule(year:int):
    url = f'https://www.pro-football-reference.com/years/{year}/games.htm'
    resp = pd.read_html(url)
    assert len(resp) == 1, "Unexpected iterable length"
    df = resp[0]
    
    # Add a column to determine the home team
    winnerIsAway = df['Unnamed: 5'] == "@"
    hometeam = df['Winner/tie'] * winnerIsAway + df['Loser/tie'] * df['Unnamed: 5'].isna()
    df['Home Team'] = hometeam   # Add the column to dataframe

    return df

def week_schedule(year:int, week:int) -> pd.DataFrame:
    year_sched = year_schedule(year)
    week_schedule = year_sched[year_sched['Week'] == str(week)]
    return week_schedule