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
        return self.name + ": " + str(self.attack) + "/" + str(self.current_health)
    def __repr__(self):
        return self.name + ": " + str(self.attack) + "/" + str(self.current_health)
    def check_if_dead(self):
        if self.current_health <= 0:
            return True
        else:
            return False
        
    def combat(self,target):
        if type(target) == Creature:
            target.current_health -= self.attack
            self.current_health -= target.attack
        else:
            if target.armor >= self.attack:
                target.armor -= self.attack
            elif (target.armor > 0 and target.armor < self.attack):
                target.life -= (self.attack - target.armor)
                target.armor = 0
            else:
                target.life -= self.attack
                


class Spell:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost
    def __repr__(self):
        return self.name

