from random import randint

class Hero():
  def __init__(self, name) -> None:
    self._name = name
    self._lvl = 1
    self._skillpoint = 0
    self._xp = 0
    self._max_xp = 100
    self._hp = 100
    self._max_hp = 100
    self._str = 1
    self._agi = 1
    self._int = 1
    self._gold = 0
    self._status = []
    self._inventory = dict()
    self._weapon = []
    self._armor = []

  @property
  def name(self):
    return self._name
  
  @property
  def lvl(self):
    return self._lvl
  
  @property
  def skillpoint(self):
    return self._skillpoint

  @property
  def xp(self):
    return self._xp
  
  @property
  def max_xp(self):
    return self._max_xp

  @max_xp.setter
  def max_xp(self, value):
    self._max_xp = value

  @xp.setter
  def xp(self, value):
    if value >= self.max_xp:
      self._xp = value - self.max_xp
      self.lvl_up()
    else:
      self._xp = value

  @property
  def hp(self):
    return self._hp

  @hp.setter
  def hp(self, value):
    self._hp = max(0, min(value, self.max_hp))

  @property
  def max_hp(self):
    return self._max_hp
  
  @max_hp.setter
  def max_hp(self, value):
    self._max_hp = value

  @property
  def str(self):
    return self._str
  
  @str.setter
  def str(self, value):
    self._str = value

  @property
  def agi(self):
    return self._agi
  
  @agi.setter
  def agi(self, value):
    self._agi = value

  @property
  def int(self):
    return self._int
  
  @int.setter
  def int(self, value):
    self._int = value

  @property
  def gold(self):
    return self._gold
  
  @gold.setter
  def gold(self, value):
    self._gold = value
  
  @property
  def status(self):
    return self._status if self._status else ["normal"]
  
  def add_status(self, value):
    if value not in self.status:
      self._status.append(value)
      
  def remove_status(self, value):
    if value in self.status:
      self._status.remove(value)

  @property
  def inventory(self):
    return self._inventory
  
  def add_item(self, item, amount=1):
    if item in self.inventory:
      self._inventory[item] += amount
    else:
      self._inventory[item] = amount

  def remove_item(self, item, amount=1):
    if item in self.inventory:
      if self.inventory[item] < amount:
        print("You don't have such amount of items.")
      elif self.inventory[item] == amount:
        self._inventory.pop(item)
      else:
        self._inventory[item] -= amount

  def use_item(self, item):
    match item: 
      case "potion":
        self.heal(self.max_hp/100*25)
        self.remove_item(item)
      case "antidote":
        self.cure()
        self.remove_item(item)
    

  def stats(self):
    print(f"{self.name}, LvL {self.lvl}")
    print(f"{self.gold} gold, {self.xp}/{self.max_xp} exp")
    print(f"Health: {self.hp}/{self.max_hp}")
    print(f"Status: {self.status}")
    print(f"Strength: {self.str}")
    print(f"Agility: {self.agi}")
    print(f"Intelligence: {self.int}\n")


  def update(self):
    if "poisoned" in self.status:
      damage = int(self.max_hp/100*5)
      self.take_damage(cause="poison", value=damage)

  def death(self, cause):
    print(f"deadge cause: {cause}")
    self.add_status("dead")

  def escape(self):
    escape_chance = randint(self.agi * 20, 100)
    if escape_chance > 70:
      return True
    return False

  def attack(self, target):
    roll = randint(0, 100)
    crit_chance = 100 - self.agi*5
    if roll > crit_chance:
      crit = True
    
    damage = randint(10, 20) + self.str*5
    if crit: 
      damage *= 2
      print(f"You deal {damage} crit damage to {target.name}!")
    else:
      print(f"You deal {damage} damage to {target.name}.")
    target.take_damage(damage)

  def defend(self):
    block = randint(self.str*10, self.str*15)
    return block

  def take_damage(self, value, cause):
    if self.hp <= value:
      self.death(cause)
    else:
      self.hp -= value

  def heal(self, value):
    self.hp += value
     
  def lvl_up(self):
    print("Your power grows! You've got a skillpoint.")
    self._lvl += 1
    self._skillpoint += 1
    self._max_xp = self.lvl*100
    self.hp = self.max_hp
  
  def upgrade(self, stat):
    match stat:
      case "str":
        self._str += 1
        self._max_xp += 25
      case "agi":
        self._agi += 1
      case "int":
        self._agi += 1
    self._skillpoint -= 1

  def fullheal(self):
    self.hp = self.max_hp
  
  def cure(self):
    if "poisoned" in self.status:
      self.remove_status("poisoned")

  def poison(self):
    self.add_status("poisoned")