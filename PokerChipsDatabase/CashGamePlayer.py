from Player import Player 
class CashGamePlayer(Player):
    def __init__(self, name, chips = 20000, buy_ins = 1, cashed_out_amount = -1):
        super().__init__(name, chips)
        self.buy_ins = buy_ins
        self.cashed_out_amount = cashed_out_amount

    




