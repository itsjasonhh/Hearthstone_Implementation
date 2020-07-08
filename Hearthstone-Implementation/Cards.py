class Creature:
    def __init__(self, name, cost, attack, health, tag, battlecry, effect):
        self.name = name
        self.cost = cost
        self.attack = attack
        self.current_health = health
        self.total_health = health
        self.tag = tag
        self.battlecry = battlecry
        self.effect = effect


class Spell:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost


