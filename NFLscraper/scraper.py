import pandas as pd
import requests
from io import StringIO

try:
    import requests_cache
    requests_cache.install_cache("scraper_cache", expire_after=2*86400) # cache any requests for 2 days
except ImportError:
    print("Warning: requests-cache not installed, NOT using cache") 

def get_text(url: str) -> str:
    '''
    use of explicit requests library, so that it automatically uses `requests_cache` if set up
    https://github.com/pandas-dev/pandas/issues/6456#issuecomment-1127777910
    
    '''
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def team_schedule(teamcode:str, year:int) -> pd.DataFrame:
    """
    Gets the schedule for the requested team and year

    Args:
        teamcode (str): e.g. "nwe" for New England Patriots
        year (int): The season to get a schedule for
    """    
    url = f'https://www.pro-football-reference.com/teams/{teamcode}/{year}.htm'  # To get the schedule of one team
    resp = get_text(url)
    df = pd.read_html(StringIO(resp))
    df = df[1]
    
    return df

def year_schedule(year:int) -> pd.DataFrame:
    """Fetch a schedule for a given year from www.pro-football-reference.com/years/

    Args:
        year (int): Year of season-start

    Returns:
        pd.DataFrame: A row for every game
    """    
    url = f'https://www.pro-football-reference.com/years/{year}/games.htm'
    resp = get_text(url)
    df = pd.read_html(StringIO(resp))
    assert len(df) == 1, "Unexpected iterable length"
    df = df[0]
    
    # Drop the rows that repeat column indices
    df = df[df['Week'] != 'Week']
    
    # Drop all rows where team names are NaN
    df = df.dropna(subset=['Winner/tie', 'Loser/tie'], inplace=False)
    
    # Edge case: neutral site for SuperBowl games - I'll just put the winner as Home Team for now...
    df['Neutral Site'] = df['Unnamed: 5'] == 'N'
    
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Add columns for Home Team and Away Team
    winnerIsAway = df['Unnamed: 5'] == "@"
    awayteam = df['Winner/tie'] * winnerIsAway + df['Loser/tie'] * df['Unnamed: 5'].isna() + df['Winner/tie'] * df['Neutral Site']
    hometeam = df['Winner/tie'] * df['Unnamed: 5'].isna() + df['Loser/tie'] * winnerIsAway + df['Loser/tie'] * df['Neutral Site']
    df['Home Team'] = hometeam   
    df['Away Team'] = awayteam
    
    # Replace week numbers 
    df['Week'] = df['Week'].replace(
        {"WildCard": '19', "Division" : '20', "ConfChamp" :'21', 'SuperBowl':'22'},
        inplace=False)
    
    return df

def week_schedule(year:int, week:int) -> pd.DataFrame:
    # Note: this is inefficient
    year_sched = year_schedule(year)
    week_schedule = year_sched[year_sched['Week'] == str(week)]
    return week_schedule