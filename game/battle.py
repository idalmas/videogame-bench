# game/battle.py

"""Contains the logic for handling Pokémon battles."""

# Need to import the relevant classes
import random
import time
# Assuming Pokemon and Move classes are in game.classes
# We'll need to adjust imports if structure changes
try:
    from game.classes.pokemon import Pokemon
    from game.classes.move import Move
    from game.classes.player import Player # Import Player
except ImportError:
    # Allow running/testing this file directly if imports fail
    print("Could not import Pokemon/Move classes. Ensure they exist and PYTHONPATH is set.")
    # Define dummy classes if needed for basic execution without full context
    class Pokemon: pass
    class Move: pass
    class Player: pass # Dummy classes

class Battle:
    """Manages a single 1v1 Pokémon battle."""

    def __init__(self, player: Player, opponent_pokemon: Pokemon):
        """Initialize the battle with a Player object and an opponent Pokemon."""
        if not isinstance(player, Player):
            raise TypeError("First participant must be a Player object.")
        if not isinstance(opponent_pokemon, Pokemon):
            raise TypeError("Second participant must be a Pokemon object.")
            
        self.player: Player = player
        self.opponent: Pokemon = opponent_pokemon
        
        # Get the player's active Pokemon
        self.player_active_pokemon: Pokemon | None = self.player.get_active_pokemon()
        if not self.player_active_pokemon:
            raise ValueError("Player has no active Pokemon to start the battle.")
            
        self.turn_count: int = 0
        print(f"\n--- Battle Start: {self.player.name}'s {self.player_active_pokemon.nickname or self.player_active_pokemon.species_name} vs Wild {self.opponent.species_name} ---")

    def _get_turn_order(self) -> tuple[Pokemon, Pokemon]:
        """Determine which Pokémon attacks first based on speed."""
        player_poke = self.player_active_pokemon
        opponent_poke = self.opponent
        
        if player_poke.speed > opponent_poke.speed:
            return player_poke, opponent_poke
        elif opponent_poke.speed > player_poke.speed:
            return opponent_poke, player_poke
        else:
            return (player_poke, opponent_poke) if random.choice([True, False]) else (opponent_poke, player_poke)

    def _calculate_damage(self, attacker: Pokemon, defender: Pokemon, move: Move) -> int:
        """Calculate damage for a move (simplified version)."""
        if move.category == "Status":
            return 0 # Status moves don't do direct damage
        
        # Basic factors
        # TODO: Add Special Attack/Defense distinction based on move.category
        # TODO: Implement type effectiveness
        # TODO: Add critical hits
        # TODO: Add STAB (Same-type attack bonus)
        # TODO: Add random damage variance (e.g., 85% to 100%)
        
        # Simplified Formula (based loosely on Gen 1-4 formula parts)
        level_factor = (2 * attacker.level / 5) + 2
        # Use Attack/Defense for now regardless of category
        atk_def_ratio = attacker.attack / defender.defense 
        damage = ((level_factor * move.power * atk_def_ratio) / 50) + 2
        
        # Apply random variance (85% - 100%)
        variance = random.uniform(0.85, 1.00)
        final_damage = int(damage * variance)
        
        return max(1, final_damage) # Ensure at least 1 damage is dealt

    def _get_player_move_choice(self) -> Move | None:
        """Prompt the player to choose a move."""
        active_poke = self.player_active_pokemon
        if not active_poke or not active_poke.moves:
            return None

        print(f"\nWhat should {active_poke.nickname or active_poke.species_name} do?")
        for i, move in enumerate(active_poke.moves):
            # TODO: Add current PP / max PP display
            print(f"  {i + 1}: {move.name}")
        # TODO: Add options for switching Pokemon, using items, running

        while True:
            try:
                choice = input("Enter move number: ")
                move_index = int(choice) - 1
                if 0 <= move_index < len(active_poke.moves):
                    # TODO: Check if move has PP left
                    return active_poke.moves[move_index]
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(active_poke.moves)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except EOFError: # Handle Ctrl+D or similar EOF
                 print("\nBattle input cancelled.")
                 return None # Indicate cancellation or inability to choose

    def _get_opponent_move_choice(self) -> Move | None:
        """Select a move for the opponent (simple AI)."""
        if not self.opponent or not self.opponent.moves:
            return None
        # Simple AI: Choose the first available move
        # TODO: Implement smarter AI (consider type, power, PP etc.)
        # TODO: Check PP
        return self.opponent.moves[0]
        
    def _execute_turn(self, attacker: Pokemon, defender: Pokemon, move: Move):
        """Executes a single Pokémon's move against another."""
        print(f"\n{attacker.nickname or attacker.species_name} uses {move.name}!", end="")
        time.sleep(0.5) # Small pause for readability
        
        # --- Accuracy Check --- 
        accuracy_threshold = move.accuracy
        # TODO: Add modifiers for accuracy/evasion stats if implemented
        if accuracy_threshold > 100 or random.randint(1, 100) <= accuracy_threshold:
            print(f" - It hits!", end="")
            # --- Damage Calculation --- 
            damage = self._calculate_damage(attacker, defender, move)
            if damage > 0:
                print(f" - Dealt {damage} damage.")
                defender.current_hp -= damage
                defender.current_hp = max(0, defender.current_hp) # Prevent negative HP
                print(f"{defender.nickname or defender.species_name} HP: {defender.current_hp}/{defender.max_hp}")
            else:
                print(" - But it had no direct effect.") # Status move or 0 power
                # TODO: Implement status effects (e.g., Growl lowering Attack)

            # TODO: Implement move side effects (status conditions, stat changes)
        else:
            print(f" - But it missed!")
            
        # TODO: Deduct PP for the move

    def run_battle(self):
        """Run the main battle loop until one Pokémon faints."""
        
        # Ensure player has an active Pokemon (checked in init, but double check)
        if not self.player_active_pokemon:
            print("ERROR: Player has no active Pokemon to battle with.")
            return None
            
        # --- TEMP: Assign default moves if opponent has none --- 
        if not self.opponent.moves:
             try:
                 self.opponent.moves = [Move(name="Tackle", type="Normal", category="Physical", power=40, accuracy=100, pp=35)]
             except NameError:
                 print("WARN: Could not create default Move for Opponent")
        # --- END TEMP HACK --- 
        
        while not self.player_active_pokemon.is_fainted() and not self.opponent.is_fainted():
            self.turn_count += 1
            print(f"\n--- Turn {self.turn_count} ---")
            # Make sure we use the potentially updated active pokemon
            # TODO: Handle switching - for now, always use the initial one
            current_player_poke = self.player_active_pokemon 
            print(f"{current_player_poke.nickname or current_player_poke.species_name}: {current_player_poke.current_hp}/{current_player_poke.max_hp} HP")
            print(f"{self.opponent.species_name}: {self.opponent.current_hp}/{self.opponent.max_hp} HP")
            time.sleep(1)

            # Determine turn order
            # Note: _get_turn_order compares self.player_active_pokemon and self.opponent
            first, second = self._get_turn_order()
            print(f"{first.nickname or first.species_name} goes first this turn.")
            time.sleep(0.5)
            
            # --- Select Moves --- 
            move1 = None
            if first == current_player_poke:
                move1 = self._get_player_move_choice()
            else:
                move1 = self._get_opponent_move_choice()
            
            move2 = None
            if second == current_player_poke:
                move2 = self._get_player_move_choice()
            else:
                move2 = self._get_opponent_move_choice()
                
            # Handle potential cancellation from player input
            if move1 is None or move2 is None:
                print("Move selection failed or was cancelled. Ending battle.")
                return None

            # --- Execute Turns --- 
            print("-"*20) # Separator
            # Execute first Pokémon's turn
            if not first.is_fainted(): # Check faint status before turn
                self._execute_turn(first, second, move1)
                if second.is_fainted():
                    print(f"\n{second.nickname or second.species_name} fainted!")
                    break 
            
            print("-"*20) # Separator
            time.sleep(0.5)
            
            # Execute second Pokémon's turn
            if not second.is_fainted(): # Check faint status before turn
                self._execute_turn(second, first, move2)
                if first.is_fainted(): 
                    print(f"\n{first.nickname or first.species_name} fainted!")
                    break 
                 
            time.sleep(1)

        # --- Battle End --- 
        print(f"\n--- Battle End --- Turn {self.turn_count}")
        if self.player_active_pokemon.is_fainted():
            print(f"{self.opponent.species_name} wins!")
            return self.opponent # Return the winner
        elif self.opponent.is_fainted():
            print(f"{self.player.name}'s {self.player_active_pokemon.nickname or self.player_active_pokemon.species_name} wins!")
            return self.player_active_pokemon # Return the winner
        else:
            print("Battle ended unexpectedly (maybe a draw?).")
            return None

# Example Usage (if running this file directly)
if __name__ == "__main__":
    print("Setting up example battle...")
    # Need dummy Pokemon and Moves if classes weren't imported
    # This will likely fail if Pokemon/Move are not properly defined/imported
    try:
        # Create player
        player = Player("Tester")
        # Create pokemon and add to team
        pika = Pokemon(species_name="Pikachu", types=["Electric"], level=50, max_hp=150, attack=55, defense=40, speed=90)
        pika.moves = [Move(name="Thunder Shock", type="Electric", category="Special", power=40, accuracy=100, pp=30),
                      Move(name="Growl", type="Normal", category="Status", power=0, accuracy=100, pp=40)]
        player.add_pokemon(pika)
        
        rattata = Pokemon(species_name="Rattata", types=["Normal"], level=48, max_hp=120, attack=56, defense=35, speed=72)
        rattata.moves = [Move(name="Quick Attack", type="Normal", category="Physical", power=40, accuracy=100, pp=30)]
        
        # Create and run the battle
        battle = Battle(player, rattata)
        winner = battle.run_battle()
        if winner:
            print(f"\nOverall Winner: {getattr(winner, 'nickname', None) or getattr(winner, 'species_name', 'Unknown')}")
        else:
            print("\nBattle concluded with no winner.")
            
    except NameError as e:
        print(f"\nERROR: Could not run example battle. Missing class definition? ({e})")
    except Exception as e:
         print(f"\nAn unexpected error occurred during the example battle: {e}") 