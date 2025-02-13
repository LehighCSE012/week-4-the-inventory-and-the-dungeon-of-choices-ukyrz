"""Week 3"""
import random

def display_player_status(player_health):
    """Displays the player's current health."""
    print(f"Your current health: {player_health}")

def acquire_item(inventory, item):
    """Adds an item to the player's inventory and prints a message."""
    inventory.append(item)
    print(f"You acquired a {item}!")

def display_inventory(inventory):
    """Displays the player's inventory."""
    if not inventory:
        print("Your inventory is empty.")
    else:
        print("Your inventory:")
        for i, item in enumerate(inventory, start=1):
            print(f"{i}. {item}")

def handle_path_choice(player_health):
    """Handles the player's path choice, randomly selecting 'left' or 'right'."""
    path = random.choice(["left", "right"])
    if path == "left":
        print("You encounter a friendly gnome who heals you for 10 health points.")
        player_health = min(player_health + 10, 100)
        return player_health
        
    print("You fall into a pit and lose 15 health points.")
    player_health = max(player_health - 15, 0)
    if player_health == 0:
        print("You are barely alive!")
    return player_health

def player_attack(monster_health):
    """Simulates the player's attack, dealing 15 damage."""
    print("You strike the monster for 15 damage!")
    monster_health = max(monster_health - 15, 0)
    return monster_health

def monster_attack(player_health):
    """Simulates the monster's attack with a 50% chance of a critical hit."""
    if random.random() < 0.5:
        print("The monster lands a critical hit for 20 damage!")
        player_health = max(player_health - 20, 0)
        return player_health

    print("The monster hits you for 10 damage!")
    player_health = max(player_health - 10, 0)
    return player_health

def combat_encounter(player_health, monster_health, has_treasure):
    """Manages the combat sequence between the player and the monster."""
    while player_health > 0 and monster_health > 0:
        monster_health = player_attack(monster_health)
        if monster_health > 0:
            player_health = monster_attack(player_health)
            display_player_status(player_health)

    if player_health == 0:
        print("Game Over!")
        return False, player_health
    else:
        print("You defeated the monster!")
        return True, player_health

def enter_dungeon(player_health, inventory, dungeon_rooms):
    """Handles dungeon exploration and challenges."""
    for room in dungeon_rooms:
        print(f"\n{room[0]}")
        
        if room[1]:
            acquire_item(inventory, room[1])
        
        if room[2] == "none":
            print("There doesn't seem to be a challenge in this room. You move on.")
        else:
            if room[2] == "puzzle":
                print("You encounter a puzzle!")
                choice = input("Do you want to 'solve' or 'skip' the puzzle? ").strip().lower()
            elif room[2] == "trap":
                print("You see a potential trap!")
                choice = input("Do you want to 'disarm' or 'bypass' the trap? ").strip().lower()
            
            if choice in ["solve", "disarm"]:
                success = random.choice([True, False])
                if success:
                    print(room[3][0])
                else:
                    print(room[3][1])
                    player_health = max(player_health + room[3][2], 0)
                    if player_health == 0:
                        print("You are barely alive!")
        
        display_inventory(inventory)
    
    print(f"\nYou exit the dungeon with {player_health} health remaining.")
    return player_health, inventory

def main():
    """Orchestrates the game logic by managing health, encounters, and dungeon exploration."""
    player_health = 100
    monster_health = 70
    inventory = []

    player_health = handle_path_choice(player_health)
    survived, player_health = combat_encounter(player_health, monster_health)

    if survived:
        dungeon_rooms = [
            ("A dusty old library", "key", "puzzle", ("You solved the puzzle!", "The puzzle remains unsolved.", -5)),
            ("A narrow passage with a creaky floor", None, "trap", ("You skillfully avoid the trap!", "You triggered a trap!", -10)),
            ("A grand hall with a shimmering pool", "healing potion", "none", None),
            ("A small room with a locked chest", "treasure", "puzzle", ("You cracked the code!", "The chest remains stubbornly locked.", -5))
        ]
        player_health, inventory = enter_dungeon(player_health, inventory, dungeon_rooms)
    
    print("Game Over. Thanks for playing!")

if __name__ == "__main__":
    main()
