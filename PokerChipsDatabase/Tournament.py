from tkinter import Place
from Player import Player
from TournamentPlayer import TournamentPlayer
import Utils

class Tournament(object):
    
    players : [TournamentPlayer]
        
    # buy_in : number of chips per buy in
    buy_in : int
    
    # placement : percentage of prize pool
    prize_distribution : {int : float}
    
    # date : date of tournament
    date : str
    
    _default_payout = {1 : 0.5, 2 : 0.3, 3 : 0.2}
  
    
    def __init__(self, players, buy_in, prize_distribution, date = None):
        self.players = players
        self.buy_in = buy_in
        self.prize_distribution = prize_distribution 
        if date is None:
            self.date = Utils.get_todays_date()
        else:
            self.date = date

    # results_string format:
    # buy-in 
    # date
    # { placement : payout_proportion }
    # followed by many either: 1. player name busted by player name or 2. player name rebuys
    # placement is determined by the order of the players in the results_string (ignore the rebuys lines)

    @classmethod
    def from_results_string(cls, results_string : str) -> 'Tournament':
        results_string = Utils.clean_results_string(results_string)
        buy_in, date, prize_distribution = cls._get_properties_from_results_string(results_string)
        players = cls._get_players_from_results_string(results_string)
        return cls(players, buy_in, prize_distribution, date)

    def _get_properties_from_results_string(results_string : str) -> (int, str, {int : float}):
        lines = results_string.split('\n')
        buy_in = int(lines[0])
        date = Utils.get_todays_date() if lines[1] == 'today' else lines[1]
        prize_distribution = Tournament._default_payout if lines[2] == 'default payouts' else eval(lines[2]) 
        return buy_in, date, prize_distribution

    # returns a list of TournamentPlayers with name and placement, and other attributes set to default values.
    def _get_placements(results_string : str) -> [TournamentPlayer]:
        busts = list(filter(lambda line: 'busted by' in line, results_string.split('\n')))
        busts.reverse()
        placements = []
        for placement in range(1, len(busts) + 1):
            line = busts[placement - 1].split(' busted by ')
            name = line[0]
            busted_by = TournamentPlayer(name = line[1])
            placements.append(TournamentPlayer(name = name, placement = placement, busted_by = busted_by))
        return placements
    
    def _set_rebuys(results_string : str, players : [TournamentPlayer]) -> [TournamentPlayer]:
        rebuys = list(filter(lambda line: 'rebuy' in line, results_string.split('\n')))
        for rebuy in rebuys:
            name = rebuy.split(' ')[0]
            player = next(filter(lambda player: player.name == name, players))
            player.buy_ins += 1
        return players

    @classmethod
    def _get_players_from_results_string(cls, results_string : str):
        return cls._set_rebuys(results_string, cls._get_placements(results_string))
        
    def calculate_prize_pool(self) -> int:
        return sum(map(lambda player: player.buy_ins, self.players)) * self.buy_in
    
    def calculate_prize(self) -> {Player : int}:
        prize_pool = self.calculate_prize_pool()
        prize = {}
        for player in self.players:
            prize[player] = prize_pool * self.prize_distribution.get(player.placement, 0)
        return prize
    
    def calculate_change(self) -> {TournamentPlayer : int}:
        prize_pool = self.calculate_prize_pool()
        change = {}
        for player in self.players:
            change[player] = prize_pool * self.prize_distribution.get(player.placement, 0) - player.buy_ins * self.buy_in
        return change

    def __str__(self):
        output = "Placement |   Name    | Buy-ins | Busted by | Change in Chips"
        for (player, change) in self.calculate_change().items():
            output += f"\n{str(player.placement).center(9)} | {player.name.center(9)} | {str(player.buy_ins).center(7)} | {player.busted_by.name.center(9)} | {str(change).center(14)}"
           
        return output
    
    
    
