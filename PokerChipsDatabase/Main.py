from email import utils
from string import printable
from Player import Player
from Tournament import Tournament
from TournamentPlayer import TournamentPlayer
from CashGame import CashGame
from DatabaseService import get_leaderboard, record_cash_game, record_tournament, reset_all_to_20000, revert_cash_game, revert_tournament, test_connection, get_stats_string
from Utils import get_todays_date
        

def test_parse_tournament():
    results_string = """200
today
default payouts
Nyron rebuy
Kevin rebuy
Rory busted by Henry
Kevin rebuy
Noe rebuy
Yuquan busted by Henry 
Nyron busted by Noe
Henry busted by Andrew
Dima busted by Andrew
Kevin busted by Raj
Murad busted by Raj
Raj busted by Andrew
Noe busted by Henry
Andrew busted by Nobody"""
    tourney = Tournament.from_results_string(results_string)
    print(tourney)
    record_cash_game(tourney)

def test_parse_cash_game():
    results_string = """200
today
Kevin rebuys
Henry rebuys
Dima cashes out for 400
Kevin cashes out for 300
Henry cashes out for 300"""
    cash_game = CashGame.from_results_string(results_string)
    print(cash_game)
    record_cash_game(cash_game)

def main():
    results = """200
today
default payouts
Ryann rebuys 
Sienna busted by Kevin
Joy busted by Henry
Elsa busted by Zachary
Ryann busted by Andrew
Dima busted by Henry
Kevin busted by Henry
Raj busted by Henry
Zachary busted by Henry
Andrew busted by Henry
Henry busted by Nobody"""
    tourney = Tournament.from_results_string(results)
    print(tourney)
    prompt = input("Would you like to proceed? (y/n): ")
    if prompt == 'y':
        record_tournament(tourney)

def main2():
    results = """4000
today
Leo rebuys
Leo rebuys
Zachary rebuys
Kaka rebuys 
Zachary cashes out for 0
Murad cashes out for 0
Leo cashes out for 0
Kevin cashes out for 4710
Kaka cashes out for 5820
Joy cashes out for 17760
Sayuri cashes out for 3420
Lily cashes out for 1920
Andrew cashes out for 15430
Issac cashes out for 6940"""
    cash_game = CashGame.from_results_string(results)
    print(cash_game)
    
    prompt = input("Would you like to proceed? (y/n): ")

    if prompt == 'y':
        record_cash_game(cash_game)


print(get_stats_string("2025-04-30", True))


