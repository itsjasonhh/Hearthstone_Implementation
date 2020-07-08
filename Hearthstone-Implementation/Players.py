import sys

class Player:
    #name must be "Rogue or Priest"
    def __init__(self, name):
        if not (name == 'Rogue' or name == 'Priest'):
            sys.exit('Not a valid name!') 
        self.name = name
        self.life = 30
        self.weapon_equipped = False
        self.attack = 0
        self.creatures = []
        self.mana = 0
        self.deck = []
    def __str__(self):
        return self.name + ': Life = ' + str(self.life)


