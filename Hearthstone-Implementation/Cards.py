#effects, battlecries, deathrattles will be handled by functions in player class instead of in the card class
class Creature:
    def __init__(self, name, cost, attack, health, tag, taunt, can_attack):
        self.name = name
        self.cost = cost
        self.attack = attack
        self.current_health = health
        self.total_health = health
        self.can_attack = can_attack
        self.tag = tag
        self.taunt = taunt
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name


class Spell:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost
    def __repr__(self):
        return self.name

