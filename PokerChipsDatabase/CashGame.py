from CashGamePlayer import CashGamePlayer
import Utils 

class CashGame(object):
    
    players : [CashGamePlayer]
    buy_in : int 
    date : str
    
    
    def __init__(self, buy_in, date = None, players = []):
        self.buy_in = buy_in
        self.players = players
        if date is None:
            self.date = Utils.get_todays_date()
        else:
            self.date = date
    
    # results_string format:
    # (player name) (change in chips)
    @classmethod
    def from_delta(cls, results_string : str) -> 'CashGame':
        results_string = Utils.clean_results_string(results_string)
        players = cls._get_players_from_delta(results_string)
        return cls(0, None, players)
    
    def _get_players_from_delta(results_string : str) -> [CashGamePlayer]:
        players = []
        for line in results_string.split('\n'):
            name, change = line.split(' ')
            players.append(CashGamePlayer(name = name, cashed_out_amount = int(change)))
        return players

    # results_string format:
    # buy-in
    # date
    # many either: 1. player name cashes out or 2. player name rebuys
    @classmethod 
    def from_results_string(cls, results_string : str) -> 'CashGame':
        results_string = Utils.clean_results_string(results_string)
        buy_in, date = cls._get_properties_from_results_string(results_string)
        players = cls._get_players_from_results_string(results_string)
        return cls(buy_in, date, players)
    
    @classmethod
    def _get_players_from_results_string(cls, results_string : str) -> [CashGamePlayer]:
        players = cls._get_cash_outs(results_string)
        cls._set_rebuys(results_string, players)
        return players
    
    def _get_cash_outs(results_string : str) -> [CashGamePlayer]:
        cash_outs = list(filter(lambda line: 'cashes' in line, results_string.split('\n')))
        players = [] 
        for cash_out in cash_outs:
            result = cash_out.split(' cashes out for ')
            name = result[0]
            cashed_out_amount = int(result[1])
            players.append(CashGamePlayer(name = name, cashed_out_amount = cashed_out_amount))
        return players
    
    def _set_rebuys(results_string : str, players : [CashGamePlayer]) -> None:
        rebuys = list(filter(lambda line: 'rebuys' in line, results_string.split('\n')))
        for rebuy in rebuys:
            name = rebuy.split(' rebuys')[0]
            player = next(filter(lambda player: player.name == name, players))
            player.buy_ins += 1
    

    def _get_properties_from_results_string(results_string : str) -> (int, str):
        lines = results_string.split('\n')
        buy_in = int(lines[0])
        date = Utils.get_todays_date() if lines[1] == 'today' else lines[1]
        return buy_in, date

    def calculate_change(self) -> {CashGamePlayer : int}:
        change = {}
        for player in self.players:
            change[player] = player.cashed_out_amount - self.buy_in * player.buy_ins
        return change 
    
    def __str__(self):
        output = "   Name   | Buy-ins | Change in Chips"
        for (player, change) in self.calculate_change().items():
            output += f"\n{player.name.center(9)} | {str(player.buy_ins).center(7)} | {str(change).center(14)}"
        return output
        




