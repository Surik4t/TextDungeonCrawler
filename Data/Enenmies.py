from random import choice, randint

class Enemy():
  def __init__(self, lvl) -> None:
    self._name = self.generate_name()
    self._lvl = lvl
    self._hp = self.generate_hp()
    self.gold = 0
    self.loot = {}
    self.is_dead = False
    self.generate_gold()
    self.generate_loot()

  @property
  def name(self):
    return self._name
  
  def generate_name(self):
    adjective = ["Spooky", "Sussy", "Crazy", "Angry", "Tricky", "Chunky", "Chill", "Mad", "Silly", "Insane", "Freaky", "Sigma", "Alpha", "Beta", "Omega", "Kinky", "Stinky", "Giant", "Small", "Tiny", "Wild"]
    name = ["Skeleton", "Goblin", "Werewolf", "Orc", "Slime", "Beast", "Crab", "Ghost", "Imp", "Troll", "Golem", "Frog", "Hydra", "Vampire", "Madman"]
    generated_name = choice(adjective) + " " + choice(name)
    return generated_name

  @property
  def lvl(self):
    return self._lvl

  @property
  def hp(self):
    return self._hp
  
  @hp.setter
  def hp(self, value):
    self._hp = max(0, value)

  def generate_hp(self):
    min_hp = 25 + self.lvl*10
    max_hp = 40 + self.lvl*10
    hp = randint(min_hp, max_hp)
    return hp
  
  def generate_gold(self):
    self.gold = randint(1, 20 + self.lvl*20)

  def generate_loot(self):
    chance = randint(0, 100)
    items = ["key", "potion", "lockpick", "antidote"]
    drop = choice(items)
    if 50 <= chance < 75:
      self.loot[drop] = 1
    if 75 <= chance <= 99:
      self.loot[drop] = 2
    if chance == 100:
      self.loot[drop] = 3

  def drop_loot(self, target):
    target.gold += self.gold
    print(f"You got {self.gold} gold", end="")
    if self.loot:
      for item, amount in self.loot.items():
        target.add_item(item, amount)
      print(f" and {item} x{amount}", end="")
    print(".")
    multiplier = (self.lvl - target.lvl) * 10 
    xp = max(0, self.lvl*25 + multiplier)
    print(f"You also gain {xp} exp")
    target.xp += xp


  def take_damage(self, value):
    self.hp -= value
    if self.hp == 0:
      self.is_dead = True

  def attack(self, target):
    damage = 10 + randint(0, self.lvl*10)
    print(f"{self.name} attacks you for {damage} damage.")
    target.take_damage(cause=self.name, value=damage)