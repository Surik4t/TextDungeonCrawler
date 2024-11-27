import random
from random import randint

def check_stats(stat):
  if stat < 3:
    return "failed"
  elif 3 <= stat < 5:
    return "partial success"
  else:
    return "success"
  

### Chest  
class chest():
  def __init__(self) -> None:
    self.name = "Treasure chest"
    self.trapped = random.choice([True, False])
    self.locked = random.choice([True, False])
    self.actions = ["observe", "open", "leave"]
    self.loot = {}
    self.generate_loot()


  def generate_loot(self):
    coinflip = randint(0, 100)
    if coinflip <= 75:
      gold = randint(30, 200)
      self.loot["gold"] = gold
    if coinflip <= 50:
      possible_drop = ("potion", "antidote", "key", "lockpick")
      items = random.choice(possible_drop)
      self.loot["items"] = items


  def check_stats(stat):
    if stat < 3:
      return "failed"
    elif 3 <= stat < 5:
      return "partial success"
    else:
      return "success"
    

  def observe(self, hero):
    statcheck = check_stats(hero.int)
    locked = "unlocked"
    if statcheck == "success":
      if self.locked:
        locked = "locked"
        self.actions.append("pick")
        self.actions.append("unlock")
      if self.trapped:
        self.actions.append("disarm")
        print(f"You see an old, {locked} treasure chest.\nUpon further inspection you notice that it is trapped.")
        return False
      else:
        print(f"You see an old, {locked} treasure chest.\nIt looks safe to open.")
        return False
    elif statcheck == "partial success":
      if self.locked:
        locked = "locked"
        self.actions.append("pick")
        self.actions.append("unlock")
        print(f"You see an old treasure chest before you.\nIt seems to be {locked}...")
        return False
      else:
        print("You see an old treasure chest before you.\nYou can't quite figure out whether it's safe to open...")
        return False


  def unlock(self, hero):
    if "old key" in hero.inventory:
      hero.remove_item("old key", 1)
      self.actions.remove("pick")
      self.actions.remove("unlock")
      self.locked == False
      print("You used an old key, the chest is now unlocked.")
      return False
    else:
      print("You don't have a key.")
      return False


  def open(self, hero):
    if self.locked:
      if "pick" not in self.actions:
        self.actions.append("pick")
        self.actions.append("unlock")
        print("You attempt to open the chest, but it won't budge. It appears to be locked.")
      return False
    if self.trapped:
      damage = int(hero.max_hp/100*randint(10, 30))
      hero.take_damage(cause="trap", value=damage)
      print("Oppening the chest you hear strange clicking sound...\nBefore you know it, mechanism inside the chest detonates.")
      self.trapped = False
      if "disarm" in self.actions:
        self.actions.remove("disarm")
      print(f"You take {damage} damage. Treasure chest is now disarmed...")
    return self.get_loot(hero)


  def get_loot(self, hero):
    if not self.loot:
      outcome = "The chest is empty."
    if "gold" in self.loot:
      gold = self.loot["gold"]
      hero.gold += gold
      outcome = f"You found:\n{gold} gold.\n"
    if "items" in self.loot:
      item = self.loot["items"]
      outcome += f"{item}\n"
      hero.add_item(item, 1)
    print(outcome)
    return True


  def pick(self, hero):
    if not "lockpick" in hero.inventory:
      print("You can't pick a lock without a lockpick.")
      return False
    statcheck = check_stats(hero.agi)
    if statcheck == "failed":
      pick_chance = 50
    elif statcheck == "partial success":
      pick_chance = 75
    else:
      pick_chance = 100
    hero.remove_item("lockpick", 1)
    lock_difficulty = randint(0, 100)
    if pick_chance >= lock_difficulty:
      self.actions.remove("pick")
      self.actions.remove("unlock")
      self.locked = False
      print("You used a lockpick. The chest is now open.")
      return False
    else:
      print("The lockpick snaps as you attempt to open the chest.")
      return False


  def disarm(self, hero):
    statcheck = check_stats(hero.agi)
    if statcheck == "partial success" or statcheck == "success":
      self.trapped == False
      self.actions.remove("disarm")
      print("With careful precision, you disarm the trap.\nThe chest is now safe to open.")
      return False
    else:
      damage = int(hero.max_hp/100*randint(10, 30))
      hero.take_damage(cause="trap", value=damage)
      print("You attempt to disarm the trap, but your hand slips...\nBefore you know it, mechanism inside the chest detonates.")
      self.trapped = False
      self.actions.remove("disarm")
      print(f"You take {damage} damage. Treasure chest is now disarmed...")
      return False
  
### Fountain
class fountain():
  def __init__(self) -> None:
    self.name = "Fountain"
    self.poisoned = random.choice([True, False])
    self.actions = ["observe", "drink", "leave"]


  def observe(self, hero):
    statcheck = check_stats(hero.int)
    if statcheck == "failed":
      print("It looks like water, it smells like water, maybe it is water?")
      return False
    if statcheck == "partial success" or statcheck == "success":
      if self.poisoned:
        print("You take a sip from the fountain, but within seconds you start to feel sick...\nIt's clear that this water is unsafe to drink.")
        return False
      else:
        print("You take a sip from the fountain...\nIt seems safe to drink.")
        return False
  

  def drink(self, hero):
    if not "poisoned" in hero.status:
      if self.poisoned:
        hero.poison()
        print("After couple of gulps you feel sick...\nYou've been poisoned.")
      else:
        hero.fullheal() 
        print("You drink from the fountain...\nYou feel refreshed.")
    else:
      hero.cure()
      print("You drink from the fountain, feeling your body rejuvenate. You are now fully cured.")
    return True