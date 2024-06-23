import Items, characters, enemies, os, platform, pygame

pygame.mixer.init(44100, -16, 2, 1024)
pygame.init()

######## define sound effects
s='C:/Users/jimru/Desktop/scripts/games/Wyndmere/sounds'
sword = pygame.mixer.Sound(os.path.join(s, 'sword.flac'))
armorequipsound=pygame.mixer.Sound(os.path.join(s, 'armorequip.wav'))
purchase=pygame.mixer.Sound(os.path.join(s, 'purchase.wav'))
chestsound=pygame.mixer.Sound(os.path.join(s, 'chest.wav'))
townsquaresound=pygame.mixer.Sound(os.path.join(s, 'townsquaresound.mp3'))
Wyndmeretheme=pygame.mixer.Sound(os.path.join(s, 'Wyndmeretheme.mp3'))
innwelcomesound=pygame.mixer.Sound(os.path.join(s, 'innwelcome.mp3'))
######## define sound effects

######## Block 1: define lists and variables
currentinv=[]
equippedweapon=[]
equippedarmor=[]
viewweaponinv=[]
viewarmorinv=[]
chest=[Items.wooden_spoon,Items.silver_plate,Items.potato]
blacksmith=characters.Blacksmith()
shopkeeperchar=characters.ShopKeeper()
enemy1=enemies.Spider
userselect=''
CLEAR="cls" if platform.system()=="Windows" else "clear"
######## Block 1: define lists

######## Block 2: define attacking
def attack():
    if equippedweapon:
        totaldamage=5+equippedweapon[0].damage
        player.hp=player.hp-enemy1.damage
        enemy1.hp=enemy1.hp-totaldamage
        os.system(CLEAR)
        encounter()
    else:
        player.hp=player.hp-enemy1.damage
        enemy1.hp=enemy1.hp-player.damage
        os.system(CLEAR)
        encounter()

def magic():
    player.hp=player.hp-enemy1.damage
    enemy1.hp=enemy1.hp-player.magic
    os.system(CLEAR)
    encounter()
######## Block 2: define attacking

######## define inventory item inspection
def inventoryinspection():
    while True:
        n=1
        print('The contents of your inventory:\n')
        for item in player.inventory:
            print("[{}] {}".format(n,item.name))
            n+=1
        inventory=input('\nWhat would you like to do? \n Equip [W]eapons\n Equip [A]rmor\n View W[e]apons\n View Ar[m]or\n Inspect individual item with number\n [R]eturn\n')
        if inventory=='W' or inventory=='w':
            os.system(CLEAR)
            weaponequip()
        elif inventory=='A' or inventory=='a':
            os.system(CLEAR)
            armorequip()
        elif inventory=='E' or inventory=='e':
            os.system(CLEAR)
            print('your weapons:\n')
            for item in player.inventory:
                if item.__class__.__name__ == 'Weapon':
                    print(item.name)
            townsquare()
        elif inventory=='M' or inventory=='m':
            print('\nyour armor:')
            for item in player.inventory:
                if item.__class__.__name__ == 'Armor':
                    print(item.name)
            print('\n')
        elif inventory.isnumeric():
                os.system(CLEAR)
                inventory1=int(inventory)-1
                print(player.inventory[inventory1])
                inventoryinspection()
        elif inventory=='R' or inventory=='r':
            os.system(CLEAR)
            townsquare()
        else:
            os.system(CLEAR)
            print('please choose again')
######## define inventory item inspection

######## define personal chest
def cheststash():
    while True:
        n=1
        print('contents of your chest:\n')
        for item in chest:
            print("[{}] {}".format(n,item.name))
            n+=1
        chestchoice=input('\nWould you like to [s]tore or [t]ake an item?\n [R]eturn to townsquare\n')
        
        if chestchoice=='R' or chestchoice=='r':
            os.system(CLEAR)
            townsquare()
        elif chestchoice=='T' or chestchoice=='t':
            os.system(CLEAR)
            while True:
                n=1
                for item in chest:
                    print("[{}] {}".format(n,item.name))
                    n+=1
                print('\npress [R] to return to townsquare')
                chesttake=input('\nWhich item would you like to take?') 
                if chesttake == 'R' or chesttake == 'r':
                    os.system(CLEAR)
                    townsquare()
                if chesttake != 'R' and chesttake != 'r' and chesttake.isalpha():
                    os.system(CLEAR)
                    print('please choose again')
                if chesttake.isnumeric():
                    chesttake1=int(chesttake)-1
                    player.inventory.append(chest[int(chesttake1)])
                    chest.pop(int(chesttake1))
                    os.system(CLEAR)

        elif chestchoice=='S' or chestchoice=='s':
            os.system(CLEAR)
            while True:
                n=1
                for item in player.inventory:
                    print("[{}] {}".format(n,item.name))
                    n+=1
                print('\npress [R] to return to townsquare\n')
                itemstore=input('what item would you like to store?')
                if itemstore == 'R' or itemstore == 'r':
                    os.system(CLEAR)
                    townsquare()
                if itemstore != 'R' and itemstore != 'r' and itemstore.isalpha():
                    os.system(CLEAR)
                    print('please choose again')
                if itemstore.isnumeric():
                    itemstore1=int(itemstore)-1
                    chest.append(player.inventory[int(itemstore1)])
                    player.inventory.pop(int(itemstore1))
                    os.system(CLEAR)
        else:
            os.system(CLEAR)
            print('please choose again')
######## define personal chest

######## Block 3: define weapon and armor equipping
def weaponequip():
    chooseweaponinv=[]
    print('\nyour weapons:')
    for item in player.inventory:
        if item.__class__.__name__ == 'Weapon':
            print(item.name)
            chooseweaponinv.append(item)
    weaponchoice=input('Which weapon would you like to equip?')
    weaponchoice1=int(weaponchoice)-1
    if equippedweapon and equippedweapon[0]==chooseweaponinv[weaponchoice1]:
        print('Weapon is already equipped')
        os.system(CLEAR)
        townsquare()
    else:
        pygame.mixer.Sound.play(sword)
        equippedweapon.insert(0,chooseweaponinv[weaponchoice1])
        os.system(CLEAR)
        townsquare()

def armorequip():
    choosearmorinv=[]
    print('\nyour armor:')
    for item in player.inventory:
        if item.__class__.__name__ == 'Armor':
            print(item.name)
            choosearmorinv.append(item)
    armorchoice=input('Which armor would you like to equip?')
    armorchoice1=int(armorchoice)-1
    equippedarmor.insert(0,choosearmorinv[armorchoice1])
    pygame.mixer.Sound.play(armorequipsound)
    os.system(CLEAR)
    townsquare()
######## Block 3: define weapon and armor equipping

######## Block 4: define enemy encounters
def encounter():
    print('you find yourself in a dingy, small musty cave, and a small spider attacks you!')
    print('player hp: {}\nenemy hp: {}\n'.format(player.hp,enemy1.hp))
    while True:
        attack1=input('[a]ttack\n[m]agic\n[i]nventory\n[d]etailed inventory\n')
        if attack1=='a' or attack1=='A':
            os.system(CLEAR)
            attack()
        elif attack1=='m' or attack1=='M':
            os.system(CLEAR)
            magic()
        elif attack1=='i' or attack1=='I':
            for item in player.inventory:
               print(item.name)
        elif attack1=='d' or attack1=='D':
            for item in player.inventory:
               print(item.name)
        else:
            print("Please choose again")
######## Block 4: define enemy encounters

######## Block 5: define blacksmith
def blacksmithwelcome():
    while True:
        n=1
        os.system(CLEAR)
        print('Welcome to the blacksmith')
        buyorsell=input('Would you like to [b]uy, [s]ell, [r]eturn to townsquare?') 

        if buyorsell=='S'or buyorsell=='s':
            os.system(CLEAR)
            while True:
                n=1
                for item in player.inventory:
                    print('[{}] {}'.format(n, item.name))
                    n+=1
                print('\npress [R] to return to townsquare\n')
                sell=input('What would you like to sell?')
                if sell == 'R' or sell == 'r':
                    os.system(CLEAR)
                    townsquare()
                if sell.isnumeric():
                    os.system(CLEAR)
                    sell1=int(sell)-1
                    Items.playergold.value=Items.playergold.value+player.inventory[sell1].value
                    blacksmith.inventory.append(player.inventory[sell1])
                    player.inventory.pop(int(sell1))
                if sell.isalpha() and sell != 'R' and sell != 'r':
                    os.system(CLEAR)
                    print('please choose again')

        elif buyorsell=='B'or buyorsell=='b':
            weaponorarmor=input('Would you like to buy [w]eapons or [a]rmor?')
            if weaponorarmor=='W' or weaponorarmor=='w':
                os.system(CLEAR)
                blacksmithweapons()
            if weaponorarmor=='A' or weaponorarmor=='a':
                os.system(CLEAR)
                blacksmitharmor()
        elif buyorsell=='R'or buyorsell=='r':
            townsquare()

        else: print('Please choose again')

def blacksmithweapons():
    while True:
        n=1
        os.system(CLEAR)
        print("Blacksmith's inventory:\n")
        for item in blacksmith.inventory:
            if item.__class__.__name__ == 'Weapon':
                print('[{}] {}'.format(n,item.name))
                n+=1
        print('\nWhat weapon would you like to buy?:\n')
        print('[R]eturn to townsquare')
        while True:
            weaponbuy=input('Choose a weapon: ')
            if weaponbuy == '1':
                pygame.mixer.Sound.play(purchase)
                player.inventory.append(Items.short_sword)
                Items.playergold.value=Items.playergold.value-Items.short_sword.value
                blacksmith.inventory.remove(Items.short_sword)
                os.system(CLEAR)
                townsquare()
            elif weaponbuy == '2':
                pygame.mixer.Sound.play(purchase)
                player.inventory.append(Items.small_axe)
                Items.playergold.value=Items.playergold.value-Items.small_axe.value
                blacksmith.inventory.remove(Items.small_axe)
                os.system(CLEAR)
                townsquare()
            elif weaponbuy=='R'or weaponbuy=='r':
                os.system(CLEAR)
                townsquare()
            else:
                print('Please choose again')
    
def blacksmitharmor():
    print('What armor would you like to buy?:')
    print('[1] cloak')
    print('[R]eturn to townsquare')
    while True:
        armorbuy=input('Choose a piece of armor: ')
        if armorbuy == '1':
            pygame.mixer.Sound.play(purchase)
            player.inventory.append(Items.cloak)
            Items.playergold.value=Items.playergold.value-Items.cloak.value
            blacksmith.inventory.remove(Items.cloak)
            os.system(CLEAR)
            townsquare()
        elif armorbuy=='R'or armorbuy=='r':
            townsquare()
        else:
            print('Please choose again')
######## Block 5: define blacksmith

######## define inn
def innwelcome():
    print('Welcome to the inn')
    while True:
        innchoice=input('Would you like to [r]est or [b]uy items?')
        print('[R]eturn to townsquare')
        if innchoice=='R'or innchoice=='r':
            innrest()
        elif innchoice=='R'or innchoice=='r':
            townsquare()
        else:
            print('Please choose again')
######## define inn

######## define shopkeeper
def shopkeeperwelcome():
    pygame.mixer.Sound.play(innwelcomesound)
    print('Welcome to the item shop')
    while True:
        shopkeep=input('Would you like to [b]uy items or [r]eturn to the townsquare?')
        if shopkeep=='R'or shopkeep=='r':
            os.system(CLEAR)
            townsquare()
        elif shopkeep=='B'or shopkeep=='b':
            os.system(CLEAR)
            shopkeeper()

def shopkeeper():
    while True:
        n=1
        print('Shopkeepers inventory:\n')
        for item in shopkeeperchar.inventory:
            print("[{}] {}".format(n,item.name))
            n+=1
        print('\n[R]eturn to the townsquare')
        shopkeep=input('What would you like to buy?')
        if shopkeep == 'R' or shopkeep == 'r':
            os.system(CLEAR)
            townsquare()
        if shopkeep.isnumeric():
            shopkeepitem=int(shopkeep)-1
            skitem=shopkeeperchar.inventory[shopkeepitem]
            player.inventory.append(shopkeeperchar.inventory[shopkeepitem])
            shopkeeperchar.inventory.remove(shopkeeperchar.inventory[shopkeepitem])
            Items.playergold.value-=skitem.value
            os.system(CLEAR)
        else:
            os.system(CLEAR)
            shopkeeper()
######## define shopkeeper

######## Block 5: define townsquare
def townsquare():
    pygame.mixer.Sound.play(townsquaresound)
    
    print("\nYou find yourself in the middle of a bustling townsquare and see a blacksmith to your left, an inn to your right and a path straight ahead of you.\n\n")
    while True:
        tschoice=input('[i]nventory\n[d]etailed inventory\n[s]tats\n[b]lacksmith\n[c]hest\n[p]ath\ni[n]n\ns[h]opkeeper\n\n')
        if tschoice=='C' or tschoice=='c':
            pygame.mixer.Sound.play(chestsound)
            os.system(CLEAR)
            cheststash()
        elif tschoice=='B' or tschoice=='b':
            os.system(CLEAR)
            blacksmithwelcome()
        elif tschoice=='P' or tschoice=='p':
            os.system(CLEAR)
            encounter()
        elif tschoice=='S' or tschoice=='s':
            os.system(CLEAR)
            if equippedarmor:
                equippedarmor1=equippedarmor[0]
                if player.__class__.__name__ == 'Fighter':
                    player.defense=5+int(equippedarmor1.armor)
                    print('Defense: {}'.format(player.defense))
                if player.__class__.__name__ == 'Mage':
                    player.defense=3+int(equippedarmor1.armor)
                    print('Defense: {}'.format(player.defense))
            else:
                print('Defense: {}'.format(player.defense))
            if equippedweapon:
                equippedweapon1=equippedweapon[0]
                if player.__class__.__name__ == 'Fighter':
                    player.damage=5+int(equippedweapon1.damage)
                    print('Damage: {}\n\n'.format(player.damage))
                if player.__class__.__name__ == 'Mage':
                    player.damage=3+int(equippedweapon1.damage)
                    print('Damage: {}\n'.format(player.damage))
            else:
                print('Damage: {}\n'.format(player.damage))
        elif tschoice=='i' or tschoice=='I':
            os.system(CLEAR)
            inventoryinspection()
        elif tschoice=='d' or tschoice=='D':
            os.system(CLEAR)
            for item in player.inventory:
               print(item)
        elif tschoice=='N' or tschoice=='n':
            os.system(CLEAR)
            innwelcome()
        elif tschoice=='H' or tschoice=='h':
            os.system(CLEAR)
            shopkeeperwelcome()
        else:
            print("Please choose again")
######## Block 5: define townsquare

        

######## Block 6: define game start
pygame.mixer.Sound.play(Wyndmeretheme)
os.system(CLEAR)
print('')
print("|  /|  / \ / |\  | |\   |\    /| |‾‾‾ |‾‾) |‾‾‾")
print("| / | /   |  | \ | | \  | \  / | |‾‾‾ |_/  |‾‾‾")
print("|/  |/    |  |  \| |__) |  \/  | |___ | \  |___")
print('')

while True:
    chooseclass=input('Choose your class: (F) for Fighter, (M) for Mage: ')
    if chooseclass=='F' or chooseclass=='f':
        player=characters.Fighter()
        charclass='Fighter'
        os.system(CLEAR)
        townsquare()
    elif chooseclass=='M' or chooseclass=='m':
        player=characters.Mage()
        charclass='Mage'
        os.system(CLEAR)
        townsquare()
        break
    else:
        print("Please choose again: ")

townsquare()
######## Block 6: define game start
