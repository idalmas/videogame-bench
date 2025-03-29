#implement the move class
class Move:
    """Represents a move a Pokemon can use."""
    def __init__(self, name: str, type: str, category: str, power: int, accuracy: int, pp: int):
        self.name: str = name
        self.type: str = type        # e.g., "Normal", "Fire", "Water"
        self.category: str = category  # e.g., "Physical", "Special", "Status"
        self.power: int = power      # Base power (0 for Status moves)
        self.accuracy: int = accuracy  # Accuracy percentage (e.g., 95, 100). Can be > 100 for always-hit.
        self.pp: int = pp          # Maximum Power Points (uses)
        # Note: Current PP needs to be tracked separately, perhaps when assigned to a Pokemon

    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return f"{self.name} ({self.type}) Cat:{self.category} Pow:{self.power} Acc:{self.accuracy} PP:{self.pp}"

# Example Usage (for testing, can be removed later)
if __name__ == "__main__":
    tackle = Move(name="Tackle", type="Normal", category="Physical", power=40, accuracy=100, pp=35)
    growl = Move(name="Growl", type="Normal", category="Status", power=0, accuracy=100, pp=40)
    water_gun = Move(name="Water Gun", type="Water", category="Special", power=40, accuracy=100, pp=25)

    print(tackle)
    print(growl)
    print(water_gun)