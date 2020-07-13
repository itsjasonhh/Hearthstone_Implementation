import sys
import Cards
import random

#you and your_opponent are Player class

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
        self.can_attack = True
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
    def print_board_and_info(self,your_opponent):
        print("Your hand: ")
        print(self.hand)
        print("Your creatures: ")
        print(self.creatures)
        print("Your opponent has " + str(len(your_opponent.hand)) + " cards in hand.")
        print("Your opponent's creatures: ")
        print(your_opponent.creatures)
        return

    
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
        elif type(target) == Player:
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

    def check_if_dead(self):
        if self.life <= 0:
            sys.exit(self.name + " lost the game!")
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
        self.can_attack = True
        self.hero_power_used = False
        self.draw_card()
        return
    
    #this function is used to discard the spell AFTER its effect is used. spell effects are coded elsewhere
    def play_spell(self, card):
        self.graveyard.append(card)
        self.hand.remove(card)
        return
    
    #this function is used to play a creature to the board. Battlecries are coded elsewhere
    def play_creature(self, card):
        self.creatures.append(card)
        self.hand.remove(card)
        return
    
    def main_phase(self,player2):
        while True:
            self.print_board_and_info(player2)
            a = int(input("What would you like to do? \n0. End your turn.\n1. Play a card. \n2. Use your hero power. \n3. Attack with creatures. \n4. Attack with your hero. \n"))
            if a == 0:
                return
            elif a == 1:
                choices = {}
                i = 1
                for j in self.hand:
                    if j.cost <= self.available_mana:
                        choices[i] = j
                        i += 1
                if len(choices) == 0:
                    print("Can't play any cards!")
                else:
                    print(choices)
                    b = int(input('Enter the number of the card to play: '))
                    if type(choices[b]) == Cards.Creature:
                        self.play_creature(choices[b])
                        if choices[b].name == 'Elven Archer' or choices[b].name == 'Ironforge Rifleman':
                            c = int(input("Do you want to target a player or creature? Enter 1 for player, 2 for creature. "))
                            if c == 1:
                                d = int(input("Do you want to target yourself or the opponent? Enter 1 for yourself, 2 for the opponent. "))
                                if d == 1:
                                    if self.armor >= 1:
                                        self.armor -= 1
                                    else:
                                        self.life -= 1
                                        self.check_if_dead()
                                elif d == 2:
                                    if player2.armor >= 1:
                                        player2.armor -= 1
                                    else:
                                        player2.life -= 1 
                                        player2.check_if_dead()
                            elif c == 2:
                                creature_list = {}
                                i_1 = 1
                                for j in self.creatures:
                                    creature_list[i_1] = j
                                    i_1 += 1
                                for k in player2.creatures:
                                    creature_list[i_1] = k
                                    i_1 += 1
                                print(creature_list)
                                e = int(input("Enter the number of the creature to target: "))
                                creature_list[e].current_health -= 1
                                if creature_list[e].check_if_dead():
                                    if creature_list[e] in self.creatures:
                                        self.graveyard.append(creature_list[e])
                                        self.creatures.remove(creature_list[e])
                                    elif creature_list[e] in player2.creatures:
                                        player2.graveyard.append(creature_list[e])
                                        player2.creatures.remove(creature_list[e])
                        elif choices[b].name == 'Darkscale Healer':
                            for creature in self.creatures:
                                creature.available_health += 2
                                if creature.available_health > creature.total_health:
                                    creature.available_health = creature.total_health
                            self.life += 2
                            if self.life > 30:
                                self.life = 30
                        elif choices[b].name == 'Nightblade': 
                            if player2.armor >= 3:
                                player2.armor -= 3
                            elif player2.armor < 3 and player2.armor > 0:
                                player2.life -= (3 - player2.armor)
                                player2.armor = 0
                                player2.check_if_dead()
                            else:
                                player2.life -= 3
                                player2.check_if_dead() 
                            return
                        elif choices[b].name == 'Novice Engineer' or choices[b].name == 'Gnomish Inventor':
                            self.draw_card()
                        elif choices[b].name == 'Dragonling Mechanic':
                            self.creatures.append(Cards.Creature("Mechanical Dragonling",1,2,1,"Mech",False,False))
                        elif choices[b].name == 'Stormpike Commando':
                            c = int(input("Do you want to target a player or creature? Enter 1 for player, 2 for creature. "))
                            if c == 1:
                                d = int(input("Do you want to target yourself or the opponent? Enter 1 for yourself, 2 for the opponent. "))
                                if d == 1:
                                    if self.armor >= 2:
                                        self.armor -= 2
                                    elif self.armor == 1:
                                        self.life -= 1
                                        self.armor = 0
                                        self.check_if_dead()
                                    else:
                                        self.life -= 2
                                        self.check_if_dead()
                                elif d == 2:
                                    if player2.armor >= 2:
                                        player2.armor -= 2
                                    elif player2.armor == 1:
                                        player2.life -= 1
                                        player2.armor = 0
                                        player2.check_if_dead()
                                    else:
                                        player2.life -= 2 
                                        player2.check_if_dead()
                            elif c == 2:
                                creature_list = {}
                                i_2 = 1
                                for j in self.creatures:
                                    creature_list[i_2] = j
                                    i_2 += 1
                                for k in player2.creatures:
                                    creature_list[i_2] = k
                                    i_2 += 1
                                print(creature_list)
                                e = int(input("Enter the number of the creature to target: "))
                                creature_list[e].current_health -= 2
                                if creature_list[e].check_if_dead():
                                    if creature_list[e] in self.creatures:
                                        self.graveyard.append(creature_list[e])
                                        self.creatures.remove(creature_list[e])
                                    elif creature_list[e] in player2.creatures:
                                        player2.graveyard.append(creature_list[e])
                                        player2.creatures.remove(creature_list[e])
                    
                        
                    elif type(choices[b]) == Cards.Spell:
                        self.play_spell(choices[b])
                        if choices[b].name == 'Backstab':
                            targets = {}
                            i_3 = 1
                            for j in self.creatures:
                                if j.current_health == j.total_health:
                                    targets[i_3] = j
                                    i_3 += 1
                            for k in player2.creatures:
                                if k.current_health == k.total_health:
                                    targets[i_3] = k
                                    i_3 += 1
                            print(targets)
                            choice = int(input("Enter the number of the target: "))
                            targets[choice].current_health -= 2
                            if targets[choice].check_if_dead():
                                if targets[choice] in self.creatures:
                                    self.graveyard.append(targets[choice])
                                    self.creatures.remove(targets[choice])
                                elif targets[choice] in player2.creatures:
                                    player2.graveyard.append(targets[choice])
                                    player2.creatures.remove(targets[choice])
                        
                        elif choices[b].name == 'Deadly Poison':
                            if self.weapon_durability == 0:
                                print("Can't play this without a weapon equipped!")
                            else:
                                self.attack += 2
                        
                        elif choices[b].name == 'Sinister Strike':
                            if player2.armor >= 3:
                                player2.armor -= 3
                            elif player2.armor > 0 and player2.armor < 3:
                                player2.life -= (3 - player2.armor)
                                player2.armor = 0
                                player2.check_if_dead()
                            else:
                                player2.life -= 3
                                player2.check_if_dead()
                        
                        elif choices[b].name == 'Sap':
                            if len(player2.creatures) == 0:
                                print("No available targets!")
                            targets = {}
                            i_4 = 1
                            for c in player2.creatures:
                                targets[i_4] = c
                                i_4 += 1
                            print(targets)
                            s = int(input("Enter the number of the target: "))
                            if len(player2.hand) >= 10:
                                player2.graveyard.append(targets[s])
                                player2.creatures.remove(targets[s])
                            else:
                                player2.hand.append(targets[s])
                                player2.creatures.remove(targets[s])
                        
                        elif choices[b].name == 'Assassinate':
                            targets = {}
                            i_5 = 1
                            for c in player2.creatures:
                                targets[i_5] = c
                                i_5 += 1
                            print(targets)
                            s = int(input("Enter the number of the target: "))
                            player2.graveyard.append(targets[s])
                            player2.creatures.remove(targets[s])

                        elif choices[b].name == 'Innervate':
                            self.available_mana += 1

                        elif choices[b].name == 'Claw':
                            self.armor += 2
                            self.attack += 2

                        elif choices[b].name == 'Mark of the Wild':
                            targets = {}
                            i_6 = 1
                            for j in self.creatures:
                                if j.current_health == j.total_health:
                                    targets[i_6] = j
                                    i_6 += 1
                            for k in player2.creatures:
                                if k.current_health == k.total_health:
                                    targets[i_6] = k
                                    i_6 += 1
                            print(targets)
                            choice = int(input("Enter the number of the target: "))
                            targets[choice].taunt = True
                            targets[choice].attack += 2
                            targets[choice].current_health += 2
                        
                        elif choices[b].name == 'Wild Growth':
                            self.mana_crystals += 1
                        
                        elif choices[b].name == 'Healing Touch':
                            r = int(input('Do you want to target a player or creature? Enter 1 for player, 2 for creature: '))
                            if r == 1:
                                s = int(input('Do you want to target yourself or the opponent? Enter 1 for yourself, 2 for the opponent: '))
                                if s == 1:
                                    self.life += 8
                                    if self.life > 30:
                                        self.life = 30
                                elif s == 2:
                                    player2.life += 8
                                    if player2.life > 30:
                                        player2.life = 30

                            elif r == 2:  
                                targets = {}
                                i_7 = 1
                                for j in self.creatures:
                                    targets[i_7] = j
                                    i_7 += 1
                                for k in player2.creatures:
                                    targets[i_7] = k
                                    i_7 += 1
                                print(targets)
                                t = int(input("Enter the number of the target: "))
                                targets[t].current_health += 8
                                if targets[t].current_health > targets[t].total_health:
                                    targets[t].current_health = targets[t].total_health
                          
            elif a == 2:
                if self.hero_power_used:
                    print("Can't use your hero power more than once per turn!")
                else:
                    self.hero_power_used = True
                    self.hero_power()
            
            elif a == 3:
                #Attacking with creatures
                if len(self.creatures) == 0:
                    print("You don't have any creatures!")
                else:
                    attacking_creatures = {}
                    temp = 1
                    for c in self.creatures:
                        if c.can_attack == True:
                            attacking_creatures[temp] = c
                            temp += 1
                    print(attacking_creatures)
                    f = int(input("Enter the number of the attacking creature: "))
                    defenders = {}
                    d = 1
                    taunt_played = False
                    for c in player2.creatures:
                        if c.taunt == True:
                            taunt_played = True
                            defenders[d] = c
                            d += 1
                    if taunt_played == False:
                        defenders[0] = player2
                        for c in player2.creatures:
                            defenders[d] = c
                            d += 1
                    print(defenders)
                    g = int(input("Enter the number of the target of the attack: "))
                    if g == 0:
                            attacking_creatures[f].combat(defenders[g])
                            defnders[g].check_if_dead()        
                    else:
                        attacking_creatures[f].combat(defenders[g])
                        if attacking_creatures[f].check_if_dead():
                            self.graveyard.append(attacking_creatures[f])
                            self.creatures.remove(attacking_creatures[f])
                        if defenders[g].check_if_dead():
                            player2.graveyard.append(defenders[g])
                            player2.creatures.remove(defenders[g])

                
            
            elif a == 4:
                #Attacking with hero
                if self.can_attack == False:
                    print("Already attacked this turn!")
                else:
                    hero_targets = {}
                    i_10 = 1
                    taunt_played = False
                    for d in player2.creatures:
                        if d.taunt == True:
                            taunt_played = True
                            hero_targets[i_10] = d
                            d += 1
                    if taunt_played == False:
                        hero_targets[0] = player2
                        for c in player2.creatures:
                            hero_targets[i_10] = c
                    print(hero_targets)
                    g = int(input("Enter the number of the target of the attack: "))
                    if g == 0:
                        self.hero_attack(hero_targets[g])
                        hero_targets[g].check_if_dead()
                    else:
                        self.hero_attack(hero_targets[g])
                        self.check_if_dead()
                        if hero_targets[g].check_if_dead():
                            player2.graveyard.append(hero_targets[g])
                            player2.creatures.remove(hero_targets[g])
      
    def end_phase(self):
        if self.name == 'Druid':
            self.attack = 0
        return
  
        




    
# a = Player("Rogue")
# b = Player("Druid")
# a.create_deck()
# b.create_deck()
# b.draw_card()
# a.draw_phase()
# a.main_phase(b)



