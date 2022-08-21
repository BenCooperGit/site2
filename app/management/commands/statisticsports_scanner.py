import requests
import time

NOTIFICATION_DETAILS = {"notification generator": {"market": "Asian Handicap", "betOn": "Away"},  # Temporary for testing
                         "Underdog Home 1x2": {"market": "1x2", "betOn": "Home"},
                         "Home Minus": {"market": "Asian Handicap", "betOn": "Home"},
                         "Late Late +0.5": {"market": "Asian Handicap", "betOn": "Underdog"},
                         "Switchup Away": {"market": "Asian Handicap", "betOn": "Away"},
                         "Underdog Away 1x2": {"market": "1x2", "betOn": "Away"},
                         "Underdog Home AH": {"market": "Asian Handicap", "betOn": "Home"},
                         "Underdog AH": {"market": "Asian Handicap", "betOn": "Underdog"},
                         "Switchup Plus": {"market": "Asian Handicap", "betOn": "Underdog"},
                         "Switchup Home": {"market": "Asian Handicap", "betOn": "Home"},
                         "Plus 2+": {"market": "Asian Handicap", "betOn": "Underdog"},
                         "Plus 1.25+": {"market": "Asian Handicap", "betOn": "Underdog"},
                         "Plus": {"market": "Asian Handicap", "betOn": "Underdog"},
                         "Late Great +0.5": {"market": "Asian Handicap", "betOn": "Underdog"},
                         "Switchup Minus": {"market": "Asian Handicap", "betOn": "Favourite"},
                         "Home Press": {"market": "Asian Handicap", "betOn": "Home"},
                         "Away Press": {"market": "Asian Handicap", "betOn": "Away"},
                         "2nd Half +1": {"market": "Asian Handicap", "betOn": "Underdog"}
                        }

def return_selection(notification_name, odds):
    market = NOTIFICATION_DETAILS[notification_name]["market"]
    bet_on = NOTIFICATION_DETAILS[notification_name]["betOn"]
    if market=="1x2":
        odds = odds["ftr"]
        odds_home = float(odds["home"])
        odds_away = float(odds["away"])
        if (bet_on!="Underdog") and (bet_on!="Favourite"):
            return bet_on.lower()
        elif bet_on=="Underdog":
            if odds_home <= odds_away:
                return "away"
            else:
                return "home"
        else:  # bet_on=="Favourite":
            if odds_home <= odds_away:
                return "home"
            else:
                return "away"
            
    else: # bet_on=="Asian Handicap"
        odds = odds["ah"]
        odds_home = float(odds["home"])
        odds_away = float(odds["away"])
        odds_line = float(odds["line"])
        if (bet_on!="Underdog") and (bet_on!="Favourite"):
            return bet_on.lower()
        elif bet_on=="Underdog":
            if odds_line>0.0:
                return "home"
            elif odds_line<0.0:
                return "away"
            elif odds_line==0.0 and odds_home>=odds_away:
                return "home"
            elif odds_line==0.0 and odds_home<odds_away:
                return "away"
        else:  # bet_on=="Favourite":
            if odds_line>0.0:
                return "away"
            elif odds_line<0.0:
                return "home"
            elif odds_line==0.0 and odds_home>=odds_away:
                return "away"
            elif odds_line==0.0 and odds_home<odds_away:
                return "home"

def handle_notification(notification):
    match_time = notification["time"]
    league = notification["league"]
    notification_name = notification["name"]
    home_team = notification["home_team"]
    away_team = notification["away_team"]
    _market = NOTIFICATION_DETAILS[notification_name]["market"]
    _bet_on = return_selection(notification_name, notification["odds"])
    if _bet_on=="home":
        selection = home_team
    elif _bet_on=="away":
        selection = away_team
    _dict_odds_string = {"1x2": "ftr", "Asian Handicap": "ah"}
    _odds_string = _dict_odds_string[_market]
    odds = notification["odds"][_odds_string][_bet_on]
    if _market=="Asian Handicap":
        market = _market + " " + notification["odds"][_odds_string]["line"]
        
    return match_time, league, notification_name, home_team, away_team, selection, odds, market