import sys
import Cards
import random

class Player:
    #name must be "Rogue or Druid"
    def __init__(self, name):
        if not (name == 'Rogue' or name == 'Druid'):
            sys.exit('Not a valid name!') 
        self.name = name
        self.life = 30
        self.armor = 0
        self.weapon_durability = 0
        self.attack = 0
        self.creatures = []
        self.deck = []
        self.hand = []
        self.mana_crystals = 0
        self.available_mana = 0
        self.graveyard = []
        self.fatigue = 0
        self.hero_power_used = False
    def __str__(self):
        return self.name + ': Life = ' + str(self.life)
    
    def create_deck(self):
        if self.name == 'Rogue':
            for _ in range(2):
                self.deck.append(Cards.Spell('Backstab',0))
                self.deck.append(Cards.Spell('Deadly Poison',1))
                self.deck.append(Cards.Creature('Elven Archer',1,1,1,None,False,False))
                self.deck.append(Cards.Creature('Goldshire Footman',1,1,2,None, True,False))
                self.deck.append(Cards.Spell('Sinister Strike',1))
                self.deck.append(Cards.Creature('Bloodfen Raptor',2,3,2,'Beast',False,False))
                self.deck.append(Cards.Creature('Novice Engineer',2,1,1,None,False,False))
                self.deck.append(Cards.Spell('Sap',2))
                self.deck.append(Cards.Creature('Ironforge Rifleman',3,2,2,None,False,False))
                self.deck.append(Cards.Creature('Dragonling Mechanic',4,2,4,None,False,False))
                self.deck.append(Cards.Creature('Gnomish Inventor',4,2,4,None,False,False))
                self.deck.append(Cards.Creature('Stormwind Knight',4,2,5,None,False,True))
                self.deck.append(Cards.Spell('Assassinate',5))
                self.deck.append(Cards.Creature('Nightblade',5,4,4,None,False,False))
                self.deck.append(Cards.Creature('Stormpike Commando',5,4,2,None,False,False))  
        
        if self.name == 'Druid':
            for _ in range(2):
                self.deck.append(Cards.Spell('Innervate',0))
                self.deck.append(Cards.Spell('Claw',1))
                self.deck.append(Cards.Creature('Elven Archer',1,1,1,None,False,False))
                self.deck.append(Cards.Creature('River Crocolisk',2,2,3,'Beast',False,False))
                self.deck.append(Cards.Spell('Mark of the Wild',2))
                self.deck.append(Cards.Spell('Wild Growth',3))
                self.deck.append(Cards.Spell('Healing Touch',3))
                self.deck.append(Cards.Creature('Silverback Patriarch',3,1,4,'Beast',True,False))
                self.deck.append(Cards.Creature('Chillwind Yeti',4,4,5,None,False,False))
                self.deck.append(Cards.Creature('Oasis Snapjaw',4,2,7,'Beast',False,False))
                self.deck.append(Cards.Creature('Darkscale Healer',5,4,5,None,False,False))
                self.deck.append(Cards.Creature('Nightblade',5,4,4,None,False,False))
                self.deck.append(Cards.Creature('Boulderfist Ogre',6,6,7,None,False,False))
                self.deck.append(Cards.Creature('Lord of the Arena',6,6,5,None,True,False))
                self.deck.append(Cards.Creature('Core Hound',7,9,5,'Beast',False,False))

        
        random.shuffle(self.deck)  

    
    def hero_power(self):
        if self.available_mana < 2:
            print("Not enough mana!")
            return
        if self.name == 'Rogue':
            self.weapon_durability = 2
            self.attack = 1
        elif self.name == 'Druid':
            self.attack += 1
            self.armor += 1
        return

    def hero_attack(self,target):
        if self.attack < 1:
            print("I can't attack!")
            return
        if type(target) == Cards.Creature:
            target.available_health -= self.attack
            if self.armor >= target.attack:
                self.armor -= target.attack
            elif (self.armor > 0 and self.armor < target.attack):
                self.life -= (target.attack - self.armor)
                self.armor = 0
            else:
                self.life -= target.attack
        else:
            if target.armor >= self.attack:
                target.armor -= self.attack
            elif (target.armor > 0 and target.armor < self.attack):
                target.life -= (self.attack - target.armor)
                target.armor = 0
            else:
                target.life -= self.attack
        if self.weapon_durability > 0:
            self.weapon_durability -= 1
            if self.weapon_durability == 0:
                self.attack = 0
        return


    #mulligan? initial draw?
    def draw_card(self):
        if len(self.deck) > 0:
            self.hand.append(self.deck.pop(0))
            if len(self.hand) > 10:
                self.graveyard.append(self.hand.pop())
        else:
            self.fatigue += 1
            if self.armor == 0:
                self.life -= self.fatigue
            elif self.armor > 0 and self.armor < self.fatigue:
                self.armor = 0
                self.life -= (self.fatigue - self.armor)
            elif self.armor >= self.fatigue:
                self.armor -= self.fatigue
        return
    def draw_phase(self):
        self.mana_crystals += 1
        self.available_mana = self.mana_crystals
        for i in self.creatures:
            i.can_attack = True
        self.draw_card()
        return
    
    def main_phase(self):
        while True:
            a = int(input("What would you like to do? \n1. Play a card. \n2. Use your hero power. \n3. Attack with creatures. \n4. Attack with your hero. \n0. End your turn.\n"))
            if a == 0:
                return
            elif a == 1:
                choices = {}
                i = 1
                for j in self.hand:
                    if j.cost <= self.available_mana:
                        choices[i] = j
                        i += 1
                print(choices)
                b = int(input('Enter the number of the card to play: '))
                #Need to add card effects here.
            elif a == 2:
                if self.hero_power_used:
                    print("Can't use your hero power more than once per turn!")
                else:
                    self.hero_power_used = True
                    self.hero_power()
            
    
    def end_phase(self):
        if self.name == 'Druid':
            self.attack = 0
        if self.weapon_durability == 0:
            self.attack = 0
        self.hero_power_used = False
        return
    
        
    
a = Player("Rogue")
a.main_phase()



        



