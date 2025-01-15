from Player import Player
from Tournament import Tournament
from TournamentPlayer import TournamentPlayer
from CashGame import CashGame
from DatabaseService import get_leaderboard, record_cash_game, record_tournament, revert_tournament, test_connection
        

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


test_parse_cash_game()



