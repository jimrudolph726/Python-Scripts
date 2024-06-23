class Item:
    def __init__(self, name, value, description):
        self.name = name
        self.value=value
        self.description=description
    def __str__(self):
        return "{}\n=====\nValue: {}\n{}\n".format(self.name, self.value, self.description)

class Weapon(Item):
    def __init__(self, name, value, description, damage):
        self.name = name
        self.value=value
        self.description=description
        self.damage=damage
    def __str__(self):
        return "{}\n=====\nValue: {}\n{}\ndamage: {}\n".format(self.name, self.value, self.description, self.damage)
    

rusty_dagger=Weapon('rusty dagger', 5, 'a small dull dagger with a loose hilt',3)
leafy_sprig=Weapon('leafy sprig', 5, 'a curly hard wooden stick with a slight glow',5)
short_sword=Weapon('short sword', 5, 'a small sword with a worn inscription',6)
small_axe=Weapon('small axe', 8, 'an old little axe worn at the hip',7)

class Armor(Item):
    def __init__(self, name, value, description, armor):
        self.name = name
        self.value=value
        self.description=description
        self.armor=armor
    
    def __str__(self):
        return "{}\n=====\nValue: {}\n{}\narmor: {}\n".format(self.name, self.value, self.description, self.armor)

cloak=Armor('cloak', 5, 'a weatherworn brown cloak',2)
feather_cap=Armor('feather cap', 3, 'a thin leather cap with a feather',1)

class HeadArmor(Armor):
    def __init__(self, name, value, description, armor):
        self.name = name
        self.value=value
        self.description=description
        self.armor=armor
    
    def __str__(self):
        return "{}\n=====\nValue: {}\n{}\narmor: {}\n".format(self.name, self.value, self.description, self.armor)

class Gold(Item):
    def __init__(self,name,value,description):
        self.name=name
        self.value=value
        self.description=description
    
    def __str__(self):
        return "{}\n=====\nValue: {}\n{}\n".format(self.name, self.value, self.description)

playergold=Gold('gold', 50, 'gold coins with a weatherworn profile of a long forgotten king')

class Object(Item):
    def __init__(self,name,value,description):
        self.name=name
        self.value=value
        self.description=description

wooden_spoon=Object('wooden spoon', 1, 'a small carved wooden spoon')
silver_tankard=Object('silver tankard', 3, 'a large silver tankard commonly used for drinking ale')
silver_plate=Object('silver plate', 3, 'a large dinner plate made of silver')
parchment=Object('parchment', 2, "a partially burnt parchment with a cryptic message...the text is hard to make out.....pider wi...fac..of woman")

class Food(Item):
    def __init__(self,name,value,description):
        self.name=name
        self.value=value
        self.description=description

potato=Food('po-ta-to', 1, 'a small knobby yellow tuber')
apple=Food('apple', 1, 'a tart round green treat')
bread=Food('loaf of bread', 2, 'a loaf of fresh baked bread')
pig=Food('stuffed pigs head', 5, 'a glistening cooked pigs head stuffed with tart fruits')
