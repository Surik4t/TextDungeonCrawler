import os, random
from Hero import Hero
from Events import chest, fountain
from Enenmies import Enemy
from time import sleep

def cls():
  os.system('cls' if os.name=='nt' else 'clear')

depth = 0

def main():
  cls()
  print("Demo v0.1.0")
  cmd = input("type 'new' or 'load' to start the game\n").strip().lower()
  if cmd == "new":
    new_game()
  elif cmd == "load":
    load_game()
  elif cmd == "quit":
    os._exit(0)
  elif cmd == "dev":
    dev()
  else:
    main()
  cls()
  wait_for_action(Env)


def dev():
  cls()
  print("dev mode")
  global Env
  global hero
  hero = Hero("Dev")
  hero.str = 5
  hero.xp = 90
  Env = "Dungeon"
  wait_for_action()


def new_game():
  cls()
  global Env
  global hero
  Env = "Town"
  hero_name = input("Name your hero: ").strip().title()

  cmd = input(f"Your name is {hero_name}, is that correct? y/n: ").strip().lower()
  if cmd == "y":
    cls()
    hero = Hero(name=hero_name)
    print(f"Welcome, adventurer, I wish you good luck.\n")
    wait_for_action()
  elif cmd == "n":
    new_game()
  elif cmd == "quit":
    os._exit(0)
  

def load_game():
  cls()
  print("Not available in Demo")
  main()

def game_over():
  answer = input("Start a new game?  y/n: ").strip().lower()
  if answer == "y":
    new_game()
  elif answer == "n":
    os._exit(0)
  game_over()


### main loop
def wait_for_action():
  match Env:
    case "Town":
      actions = ["stats", "tavern", "market", "dungeon", "inv", "save", "quit"]
    case "Dungeon":
      actions = ["stats", "town", "forward", "inv", "save", "quit"]
    case "Tavern":
      actions = ["stats", "inv", "room", "quest", "town", "save", "quit"]

  if hero.skillpoint: actions.append("lvlup")

  print(actions)
  action = input(f"You are in {Env}. What will you do?\n").strip().lower()

  if action in actions:
    cls()
    action = globals()[action]
    action()
  else:
    cls()
    wait_for_action()


def guild():
  print("Guild is closed for repair.")
  wait_for_action()


def market():
  print("Not available in Demo.")
  wait_for_action()


### Dungeon
def forward():
  wait("Going deeper", 2)
  global depth
  depth += 10
  hero.update()
  if "dead" in hero.status:
    game_over()

  evt = generate_event()
  if evt == "event":
    cls()
    event()
  if evt == "enemy_encounter":
    cls()
    combat()
  else:
    cls()
    print("nothing happens")
  wait_for_action()


def generate_event():
  events = ["enemy_encounter", "event"]
  random.shuffle(events)
  return events.pop()


def event():
  events = (chest, fountain)
  chosen_event = random.choice(events)

  event = chosen_event()
  evt_end = False
  actions = event.actions
  
  while not evt_end:
    if "dead" in hero.status:
      game_over()
    print(f"Depth: ", depth)
    print(f"HP: {hero.hp} / {hero.max_hp}, Inventory: {hero.inventory}\n")
    print(f"You see a {event.name} before you...")
    action_input = input(f"You can {actions}\n")
    cls()
    if action_input in actions:
      if action_input == "leave":
        evt_end = True
        break
      else:
        action = getattr(event, action_input)
        evt_end = action(hero)
        if evt_end:
          input("press 'Enter' to continue.")
  wait_for_action()


def combat():
  global Env
  Env = "Combat"
  enemy = Enemy(max(1, int(depth/20)))
  combat_end = False
  actions = ["attack", "item", "escape"]
  while not combat_end:
    print(f"Depth: ", depth)
    print(f"HP: {hero.hp} / {hero.max_hp}\n")
    print(f"{enemy.name} (LvL {enemy.lvl}) is standing before you...")
    print(f"enemy hp: {enemy.hp}")
    action_input = input(f"You can {actions}\n")
    match action_input:
      case "attack":
        cls()
        hero.attack(enemy)
        if enemy.is_dead:
          print(f"{enemy.name} has fallen.")
          enemy.drop_loot(hero)
          combat_end = True
        else:
          enemy.attack(hero)
      case "item":
        cls()
        inv()
      case "escape":
        cls()
        escaped = hero.escape()
        wait("Trying to escape")
        if escaped:
          print("You escaped.")
          combat_end = True
        else:
          enemy.attack(hero)
      case _:
        cls()
        continue
    if "dead" in hero.status:
      game_over()
    input("Press 'Enter' to continue.")
    cls()
  Env = "Dungeon"
  wait_for_action()


def inv():
  cls()
  invent = hero.inventory
  print(invent)
  item = input("Type name of an item that you want to use.\nType 'close' to close the inventory.\n").strip().lower()

  if item == "close":
    cls()
    if Env != "Combat":
      wait_for_action()
    else:
      return
  elif item in invent:
    hero.use_item(item)
    input("Press 'Enter' to continue.")
    inv()
  else:
    inv()


def lvlup():
  cls()
  hero.stats()
  stats = ["str", "agi", "int"]
  stat = input(f"\nChoose a stat to increase: {stats}\n").strip().lower()
  if stat in stats:
    hero.upgrade(stat)
    print("Stat increased.")
  wait_for_action()
  

###
def wait(msg, delay=3):
  print(msg, end="", flush=True)
  for _ in range(delay):
    sleep(0.5)
    print(".", end="", flush=True)
  sleep(0.5)
  cls()


### Tavern 
def tavern():
  cls()
  print("Tavern Keeper greets you with a big smile.")
  global Env
  Env = "Tavern"
  wait_for_action()


def quest():
  cls()
  print("Sorry, traveler, I don't have quests for you yet.")


def room():
  cls()
  cure_cost = 50
  room_cost = 100

  if "poisoned" in hero.status:
    answer = input(f"What a pale face you got. Aren't you feeling well? I can fix that for some gold coins.\nSpend {cure_cost}g? y/n: ").strip().lower()
    match answer:
      case "y":
        if hero.gold >= cure_cost:
          cls()
          hero.gold -= cure_cost
          hero.remove_status("poisoned")
          print("The Keeper hands you a shot glass of gooye liquid.")
          wait("You drink the potion with disgust")
          input("You feel better.\nPress 'Enter' to continue.")
          room()
        else:
          print("You dont have enough gold.")
          input("Press 'Enter' to continue.")
      case _:
        room()
        
  answer = input(f"Room costs {room_cost}g per night. Do you want to spend night in the tavern? y/n: ").strip().lower()
  match answer:
    case "y":
      if hero.gold >= room_cost:
        cls()
        hero.gold -= room_cost
        hero.hp = hero.max_hp
        wait(f"You spent {room_cost}g to get some rest")
        wait_for_action()
      else:
        cls()
        print("You dont have enough gold.")
        input("Press 'Enter' to continue.")
        wait_for_action()
    case "n":
      cls()
      wait_for_action()
    case _:
      room()
####


def dungeon():
  wait("Descending to the Dungeon")
  global Env, depth
  depth = 0
  Env = "Dungeon"
  wait_for_action()


def town():
  wait("Returning back to Town")
  global Env
  Env = "Town"
  wait_for_action()


def stats():
  hero.stats()
  wait_for_action()


def save():
  cls()
  print("Not available in Demo")
  wait_for_action()


def quit():
  answer = input("Do you really want to quit? y/n: ").strip().lower()
  if answer.strip() == "y":
    os._exit(0)
  elif answer == "n":
    cls()
    wait_for_action()
  else:
    print("unknown command")
    quit()


if __name__ == "__main__":
  main()