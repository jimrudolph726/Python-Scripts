class Enemy:
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp=hp
        self.damage=damage
    def __str__(self):
        return "{}\nenemy hp: {}\ndamage: {}\n".format(self.name, self.hp, self.damage)

Spider=Enemy('Spider', 25, 3)
GiantSpider=Enemy('Giant Spider', 50, 15)
