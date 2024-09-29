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
    
    return df

def year_schedule(year:int):
    
    url = f'https://www.pro-football-reference.com/years/{year}/games.htm'
    resp = pd.read_html(url)
    assert len(resp) == 1, "Unexpected iterable length"
    df = resp[0]
    
    # Drop the rows that repeat column indices
    df = df[df['Week'] != 'Week']
    
    # Drop all rows where team names are NaN
    df.dropna(subset=['Winner/tie', 'Loser/tie'], inplace=True)
    
    # Edge case: neutral site for SuperBowl games - I'll just put the winner as Home Team for now...
    df['Neutral Site'] = df['Unnamed: 5'] == 'N'
    
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Add columns for Home Team and Away Team
    winnerIsAway = df['Unnamed: 5'] == "@"
    hometeam = df['Winner/tie'] * winnerIsAway + df['Loser/tie'] * df['Unnamed: 5'].isna() + df['Winner/tie'] * df['Neutral Site']
    awayteam = df['Winner/tie'] * df['Unnamed: 5'].isna() + df['Loser/tie'] * winnerIsAway + df['Loser/tie'] * df['Neutral Site']
    df['Home Team'] = hometeam   
    df['Away Team'] = awayteam
    
    # Replace week numbers 
    df['Week'].replace(
        {"WildCard": '19', "Division" : '20', "ConfChamp" :'21', 'SuperBowl':'22'},
        inplace=True)
    
    return df

def week_schedule(year:int, week:int) -> pd.DataFrame:
    # Note: this is inefficient
    year_sched = year_schedule(year)
    week_schedule = year_sched[year_sched['Week'] == str(week)]
    return week_schedule