from typing import List
# Import Pokemon class - handle potential ImportError if run directly
try:
    from game.classes.pokemon import Pokemon
except ImportError:
    print("Player Class: Could not import Pokemon class.")
    class Pokemon: pass # Dummy class

class Player:
    """Represents the human player."""
    
    def __init__(self, name: str):
        self.name: str = name
        self.team: List[Pokemon] = [] # List of Pokemon objects
        # TODO: Add inventory, money, badges etc. later

    def add_pokemon(self, pokemon: Pokemon):
        """Adds a Pokemon to the player's team (if space available)."""
        # Typically teams have a limit (e.g., 6)
        if len(self.team) < 6:
            if isinstance(pokemon, Pokemon):
                self.team.append(pokemon)
                print(f"{pokemon.nickname or pokemon.species_name} added to {self.name}'s team.")
            else:
                print("Error: Only Pokemon objects can be added to the team.")
        else:
            print(f"{self.name}'s team is full! Cannot add {pokemon.nickname or pokemon.species_name}.")
            # TODO: Implement sending to a PC/storage system

    def get_active_pokemon(self) -> Pokemon | None:
        """Returns the first non-fainted Pokemon from the team."""
        for pokemon in self.team:
            if not pokemon.is_fainted():
                return pokemon
        return None # No usable Pokemon left

    def __str__(self) -> str:
        team_str = ", ".join([(p.nickname or p.species_name) for p in self.team]) or "No Pokemon"
        return f"Player: {self.name}\nTeam: [{team_str}]"

# Example Usage
if __name__ == "__main__":
    # Need to define dummy Pokemon and Move if not importable
    class Move: # Dummy Move class for example
        def __init__(self, name, pp): self.name = name; self.pp = pp
        def __str__(self): return self.name
    if 'Pokemon' not in globals() or not hasattr(Pokemon, '__init__'):
        class Pokemon: # Dummy Pokemon class for example
            def __init__(self, name, lv, hp): self.species_name=name; self.nickname=None; self.level=lv; self.current_hp=hp; self.max_hp=hp; self.moves=[]; self.types=[]
            def is_fainted(self): return self.current_hp <= 0
            def __str__(self): return f"{self.nickname or self.species_name} (Lv.{self.level})"
            
    player1 = Player(name="Ash")
    print(player1)

    pika = Pokemon(name="Pikachu", lv=5, hp=35)
    pika.moves = [Move("Thunder Shock", 30)]
    bulba = Pokemon(name="Bulbasaur", lv=5, hp=45)
    bulba.moves = [Move("Vine Whip", 25)]
    
    player1.add_pokemon(pika)
    player1.add_pokemon(bulba)
    print(player1)

    active = player1.get_active_pokemon()
    if active:
        print(f"Active Pokemon: {active}")
    else:
        print("No active Pokemon!")
        
    # Test fainted scenario
    pika.current_hp = 0
    active = player1.get_active_pokemon()
    if active:
        print(f"Active Pokemon after Pika fainted: {active}") # Should be Bulbasaur
    
    bulba.current_hp = 0
    active = player1.get_active_pokemon()
    if not active:
        print("Correctly found no active Pokemon when all fainted.") 