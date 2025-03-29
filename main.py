print("Welcome to the Pokémon-like CLI Game!")

# Import necessary classes
from game.classes.pokemon import Pokemon
from game.classes.move import Move
from game.classes.player import Player
from game.battle import Battle


def main():
    """Main function to run the game."""
    print("Initializing game...")

    # --- Create Player --- 
    player = Player(name="Hero")
    print(f"Created Player: {player.name}")
    
    # --- Create Sample Pokémon --- 
    # TODO: Replace with loading player data / generating wild encounters
    player_pokemon = Pokemon(
        species_name="Pikachu", 
        types=["Electric"], 
        level=50, 
        max_hp=145, 
        attack=55, 
        defense=40, 
        speed=90
    )
    player_pokemon.nickname = "Pika"
    player_pokemon.moves = [
        Move(name="Thunder Shock", type="Electric", category="Special", power=40, accuracy=100, pp=30),
        Move(name="Quick Attack", type="Normal", category="Physical", power=40, accuracy=100, pp=30),
        Move(name="Growl", type="Normal", category="Status", power=0, accuracy=100, pp=40)
    ]
    player.add_pokemon(player_pokemon)
    
    opponent_pokemon = Pokemon(
        species_name="Meowth", 
        types=["Normal"], 
        level=48, 
        max_hp=130, 
        attack=45, 
        defense=35, 
        speed=90
    )
    opponent_pokemon.moves = [
        Move(name="Scratch", type="Normal", category="Physical", power=40, accuracy=100, pp=35),
        Move(name="Tail Whip", type="Normal", category="Status", power=0, accuracy=100, pp=30)
    ]

    print(f"Player starts with: {player.get_active_pokemon()}")
    print(f"Opponent starts with: {opponent_pokemon}")

    # --- Start Battle --- 
    battle = Battle(player, opponent_pokemon)
    winner = battle.run_battle()

    # --- Post-Battle --- 
    if winner:
        print(f"\nGame Over: {winner.nickname or winner.species_name} is the final winner!")
        active_player_pokemon = player.get_active_pokemon()
        if active_player_pokemon and winner == active_player_pokemon:
            xp_amount = 50 * opponent_pokemon.level // 7
            print(f"\n{active_player_pokemon.nickname or active_player_pokemon.species_name} gains {xp_amount} XP!")
            active_player_pokemon.gain_xp(xp_amount)
    else:
        print("\nGame Over: The battle ended in a draw or unexpectedly.")


if __name__ == "__main__":
    main() 