from Player import Player

class TournamentPlayer(Player):
    def __init__(self, name, chips = -1, placement = -1, buy_ins = 1, busted_by = Player("No One")):
        super().__init__(name, chips)
        self.placement = placement
        self.buy_ins = buy_ins
        self.busted_by = busted_by
     
    def __str__(self):
        return f"{super().__str__()} - placement: {str(self.placement).ljust(2)} - buy-ins: {self.buy_ins} - busted by: {self.busted_by.name.ljust(9)}"

    def __repr__(self):
        return self.__str__()
    
