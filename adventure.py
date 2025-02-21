import random

def display_player_status(player_stats):
    """Displays the player's current health and attack."""
    print(f"Your health: {player_stats['health']}, Attack: {player_stats['attack']}")

def handle_path_choice(player_stats):
    """Handles the player's path choice, modifying health accordingly."""
    path = random.choice(["left", "right"])
    if path == "left":
        print("You encounter a friendly gnome who heals you for 10 health points.")
        player_stats['health'] = min(player_stats['health'] + 10, 100)
    else:
        print("You fall into a pit and lose 15 health points.")
        player_stats['health'] = max(player_stats['health'] - 15, 0)
    return player_stats

def player_attack(monster_health, player_stats):
    """Player attacks the monster."""
    print(f"You strike the monster for {player_stats['attack']} damage!")
    monster_health = max(monster_health - player_stats['attack'], 0)
    return monster_health

def monster_attack(player_stats):
    """Monster attacks the player."""
    damage = 20 if random.random() < 0.5 else 10
    print(f"The monster hits you for {damage} damage!")
    player_stats['health'] = max(player_stats['health'] - damage, 0)
    return player_stats

def combat_encounter(player_stats, monster_health, has_treasure):
    """Manages combat with a monster."""
    while player_stats['health'] > 0 and monster_health > 0:
        monster_health = player_attack(monster_health, player_stats)
        if monster_health > 0:
            player_stats = monster_attack(player_stats)
            display_player_status(player_stats)

    if player_stats['health'] == 0:
        print("Game Over!")
    else:
        print("You defeated the monster!")
    return has_treasure if player_stats['health'] > 0 else None

def discover_artifact(player_stats, artifacts, artifact_name):
    """Handles discovering artifacts and updating player stats."""
    if artifact_name in artifacts:
        artifact = artifacts.pop(artifact_name)  # Remove from dictionary so it can't be found again
        print(f"You found {artifact_name}: {artifact['description']}")
        if artifact['effect'] == "increases health":
            player_stats['health'] += artifact['power']
        elif artifact['effect'] == "enhances attack":
            player_stats['attack'] += artifact['power']
        print(f"Effect: {artifact['effect']}, Power: {artifact['power']}")
    else:
        print("You found nothing of interest.")
    return player_stats, artifacts

def find_clue(clues, new_clue):
    """Handles discovering unique clues in the library."""
    if new_clue not in clues:
        clues.add(new_clue)
        print(f"You discovered a new clue: {new_clue}")
    else:
        print("You already know this clue.")
    return clues

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues):
    """Handles dungeon exploration, including the Cryptic Library."""
    for room in dungeon_rooms:
        print(f"Entering: {room['room_description']}")
        if room['item'] and room['item'] not in inventory:
            inventory.append(room['item'])
            print(f"You found a {room['item']}!")

        if room['challenge_type'] == "library":
            print("This is the Cryptic Library, full of mysterious books.")
            clues_list = ["The treasure is hidden where the dragon sleeps.",
                          "The key lies with the gnome.", "Beware the shadows.",
                          "The amulet unlocks the final door."]
            selected_clues = random.sample(clues_list, 2)
            for clue in selected_clues:
                clues = find_clue(clues, clue)
            if "staff_of_wisdom" in inventory:
                print("The staff of wisdom helps you understand the clues. You may bypass a puzzle!")
        
    return player_stats, inventory, clues

def main():
    """Main game loop."""
    player_stats = {'health': 100, 'attack': 5}
    monster_health = 70
    inventory = []
    clues = set()
    artifacts = {
        "amulet_of_vitality": {"description": "A glowing amulet that enhances your life force.", "power": 15, "effect": "increases health"},
        "ring_of_strength": {"description": "A powerful ring that boosts your attack damage.", "power": 10, "effect": "enhances attack"},
        "staff_of_wisdom": {"description": "A staff imbued with ancient wisdom.", "power": 5, "effect": "solves puzzles"}
    }
    dungeon_rooms = [
        {"room_description": "A dusty library", "item": "key", "challenge_type": "puzzle", "challenge_outcome": -5},
        {"room_description": "A narrow passage, creaky floor", "item": "torch", "challenge_type": "trap", "challenge_outcome": -10},
        {"room_description": "A grand hall, shimmering pool", "item": "healing potion", "challenge_type": "none", "challenge_outcome": None},
        {"room_description": "A small room, locked chest", "item": "treasure", "challenge_type": "puzzle", "challenge_outcome": -5},
        {"room_description": "The Cryptic Library", "item": None, "challenge_type": "library", "challenge_outcome": None}
    ]

    has_treasure = random.choice([True, False])
    display_player_status(player_stats)
    player_stats = handle_path_choice(player_stats)

    if player_stats['health'] > 0:
        treasure_obtained_in_combat = combat_encounter(player_stats, monster_health, has_treasure)
        if treasure_obtained_in_combat:
            print("You found the treasure!")
        
        if random.random() < 0.3:
            artifact_keys = list(artifacts.keys())
            if artifact_keys:
                artifact_name = random.choice(artifact_keys)
                player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)
                display_player_status(player_stats)
        
        if player_stats['health'] > 0:
            player_stats, inventory, clues = enter_dungeon(player_stats, inventory, dungeon_rooms, clues)
            print("\n--- Game End ---")
            display_player_status(player_stats)
            print("Final Inventory:", inventory)
            print("Clues:", clues if clues else "No clues.")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
