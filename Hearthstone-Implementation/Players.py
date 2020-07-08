class Player:
    def __init__(self, name, archetype):
        self.name = name
        self.archetype = archetype
        self.life = 30
        self.weapon_equipped = False
        self.attack = 0
        self.creatures = []
        self.mana = 0

