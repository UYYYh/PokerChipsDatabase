class Player(object):
    def __init__(self, name, chips = 20000):
        self.name = name
        self.chips = chips

    def __str__(self):
        return f"{self.name.rjust(9)} (chips: {str(self.chips)}):"

    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)

    
