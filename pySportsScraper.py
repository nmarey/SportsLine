import pandas as pd
import urllib.request as request
import json

from tzlocal import get_localzone



class pySportsScraper:
    
    url = 'https://www.sportsline.com/sportsline-web/service/v1/odds?league=mlb&auth=3'
    
    book_dict = {'game_id':[], 'game_date':[], 'gametime':[],
                 'Team':[], 'team_status':[], 'book':[], 
                 'cur_total':[], 'cur_over': [], 'cur_under':[], 'ml':[],
                 'open_total':[], 'open_over':[], 'open_under':[], 'open_ml':[]}
    
    def __init__(self):
        pass
        
    def get_raw_data(self, url = url):
        with request.urlopen(url) as response:
            source = response.read()
            data = json.loads(source)
            
        return(data)
    
    def get_book_data(self, game_data, home_team, away_team,
                      game_date, gametime,
                      game_id, book_dict):
    
        for i in game_data['sportsbookOdds']:
            try:
                # Home from raw_data
                book_dict['cur_total'].append(i['currentTotal'])                
                book_dict['cur_over'].append(i['currentOverUnderOverOdd'])
                book_dict['cur_under'].append(i['currentOverUnderUnderOdd'])
                book_dict['ml'].append(i['currentMoneyLineHomeOdds'])
                book_dict['open_total'].append(i['openingTotal'])
                book_dict['open_over'].append(i['openingOverUnderOverOdd'])
                book_dict['open_under'].append(i['openingOverUnderUnderOdd'])
                book_dict['open_ml'].append(i['openingMoneyLineHomeOdds'])
                book_dict['book'].append(i['sportsbookName'])
                # Home constants
                book_dict['game_id'].append(game_id)
                book_dict['game_date'].append(game_date)
                book_dict['gametime'].append(gametime)
                book_dict['Team'].append(home_team)
                book_dict['team_status'].append('Home')

                # Away from raw_data
                book_dict['cur_total'].append(i['currentTotal'])
                book_dict['cur_over'].append(i['currentOverUnderOverOdd'])
                book_dict['cur_under'].append(i['currentOverUnderUnderOdd'])
                book_dict['ml'].append(i['currentMoneyLineAwayOdds'])
                book_dict['open_total'].append(i['openingTotal'])
                book_dict['open_over'].append(i['openingOverUnderOverOdd'])
                book_dict['open_under'].append(i['openingOverUnderUnderOdd'])
                book_dict['open_ml'].append(i['openingMoneyLineAwayOdds'])
                book_dict['book'].append(i['sportsbookName'])
                # Away constants
                book_dict['game_id'].append(game_id)
                book_dict['game_date'].append(game_date)
                book_dict['gametime'].append(gametime)
                book_dict['Team'].append(away_team)
                book_dict['team_status'].append('Away')
                                
            except:
                pass

        return(book_dict)
    
    def game_data_simplified(self, raw_data):
        mytz = get_localzone()
        book_dict = self.book_dict

        for data in raw_data['competitions']:
            game_id = data['competId']

            gt_raw = data['gameStartFullDate']
            game_timestamp = pd.to_datetime(gt_raw, unit='ms').tz_localize('UTC').tz_convert(mytz)
            game_date = game_timestamp.date()
            gametime = game_timestamp.time()

            home_team = data['homeTeamAbbreviation']
            away_team = data['awayTeamAbbreviation']

            self.get_book_data(game_data = data, home_team = home_team, away_team = away_team,
                              game_date = game_date, gametime = gametime,
                              game_id = game_id, book_dict = book_dict)
        
        return(book_dict)
    

