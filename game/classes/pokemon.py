import uuid
import random

class Pokemon:
    """Represents a Pokémon in the game."""
    XP_PER_LEVEL = 100 # XP needed to gain a level (can be adjusted later)

    def __init__(self, species_name: str, types: list[str], level: int, max_hp: int, attack: int, defense: int, speed: int):
        self.id: uuid.UUID = uuid.uuid4() # Unique ID for this specific instance
        self.species_name: str = species_name
        self.nickname: str | None = None # Can be set later
        self.types: list[str] = types # e.g., ['Fire'], ['Water', 'Flying']
        self.level: int = level
        # Store initial stats potentially as base stats for recalculation
        self._base_max_hp: int = max_hp
        self._base_attack: int = attack
        self._base_defense: int = defense
        self._base_speed: int = speed

        self.xp: int = 0
        self.max_hp: int = max_hp
        self.current_hp: int = max_hp # Start with full health
        self.attack: int = attack
        self.defense: int = defense
        self.speed: int = speed
        self.moves: list = [] # Will hold Move objects later (type hint needs Move class)
        self.status: str | None = None # e.g., 'Poisoned', 'Paralyzed' (optional for later)

    def __str__(self) -> str:
        display_name = self.nickname if self.nickname else self.species_name
        return f"{display_name} (Lv.{self.level} Type: {', '.join(self.types)}, HP: {self.current_hp}/{self.max_hp})"

    def is_fainted(self) -> bool:
        """Check if the Pokémon has fainted."""
        return self.current_hp <= 0
    
    def _recalculate_stats(self):
        """Recalculates stats upon level up. Simple placeholder version."""
        # Placeholder: Increase stats by a small fixed amount + tiny random bonus
        print(f"{self.nickname or self.species_name}'s stats are increasing! (Level {self.level})")
        hp_increase = random.randint(1, 2) + 2 # e.g., +3 or +4 HP
        stat_increase = random.randint(0, 1) + 1 # e.g., +1 or +2 for others
        self.max_hp += hp_increase
        self.attack += stat_increase
        self.defense += stat_increase
        self.speed += stat_increase
        # Heal the amount gained in max_hp as well
        self.current_hp += hp_increase
        # Ensure current_hp doesn't exceed new max_hp (e.g., if healed by item before level up)
        if self.current_hp > self.max_hp:
             self.current_hp = self.max_hp
        print(f"New Stats -> MaxHP: {self.max_hp}, Atk: {self.attack}, Def: {self.defense}, Spd: {self.speed}")

    def level_up(self):
        """Handles the process of leveling up."""
        self.level += 1
        print(f"\n*** {self.nickname or self.species_name} grew to Level {self.level}! ***")
        self._recalculate_stats() # Recalculate and increase stats
        # Fully heal is common, but let's just heal the HP gained for now
        # self.current_hp = self.max_hp
        # self.status = None # Clear status conditions
        print(f"{self.nickname or self.species_name} feels stronger!")
        # We can add move learning logic here later

    def gain_xp(self, amount: int):
        """Gains XP and checks for level up."""
        if self.is_fainted() or self.level >= 100: # Fainted or max level Pokemon shouldn't gain XP
            return
        if amount <= 0:
            return

        print(f"{self.nickname or self.species_name} gained {amount} XP.")
        self.xp += amount
        xp_needed = self.XP_PER_LEVEL # In future, this could depend on level

        # Check for level up (potentially multiple times)
        while self.xp >= xp_needed and self.level < 100:
            level_up_xp = xp_needed
            self.xp -= level_up_xp
            self.level_up()
            # Update xp_needed for the *next* potential level up in the same gain_xp call
            xp_needed = self.XP_PER_LEVEL # Stays constant for now

        if self.level < 100:
             print(f"Current XP: {self.xp}/{xp_needed}")
        else:
             print(f"{self.nickname or self.species_name} reached Max Level!")
             self.xp = 0 # Reset XP at max level