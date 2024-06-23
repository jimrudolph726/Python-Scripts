import Items

Jim=''
location=0
class Fighter():
    def __init__(self):
        self.inventory=[Items.rusty_dagger, Items.feather_cap, Items.playergold]
        self.inventoryprint=[Items.rusty_dagger.name, Items.feather_cap.name, Items.playergold.name]
        self.hp=100
        self.damage=5
        self.magic=3
        self.defense=5
        self.location=location
    def __str__(self):
        return "player hp: {}".format(self.hp)

class Mage():
    def __init__(self):
        self.inventory=[Items.leafy_sprig, Items.feather_cap, Items.playergold]
        self.inventoryprint=[Items.leafy_sprig.name, Items.feather_cap.name, Items.playergold.name]
        self.hp=90
        self.damage=3
        self.magic=10
        self.defense=3
        self.location=location

class Blacksmith():
    def __init__(self):
        self.inventory=[Items.short_sword, Items.small_axe, Items.cloak]
        self.inventoryprint=[Items.short_sword.name]
        self.hp=70
        self.damage=3
        self.magic=8
        self.location=location

class InnKeeper():
    def __init__(self):
        self.inventory=[]
        self.inventoryprint=[]
        self.hp=50
        self.damage=3
        self.magic=2
        self.location=location

class ShopKeeper():
    def __init__(self):
        self.inventory=[Items.parchment, Items.apple]
        self.inventoryprint=[]
        self.hp=50
        self.damage=3
        self.magic=2
        self.location=location