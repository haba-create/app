class Inventory:
    """Simple in-memory inventory for coffee shop items."""

    def __init__(self):
        self.items = {}

    def set_stock(self, item: str, qty: int, threshold: int = 10) -> None:
        """Set stock level and restock threshold for an item."""
        self.items[item] = {"qty": qty, "threshold": threshold}

    def get_stock(self, item: str) -> int:
        """Return current stock level for an item."""
        return self.items.get(item, {}).get("qty", 0)

    def decrease_stock(self, item: str, qty: int) -> None:
        """Remove quantity from stock when an order is placed."""
        if item not in self.items:
            self.items[item] = {"qty": 0, "threshold": 10}
        self.items[item]["qty"] = max(0, self.items[item]["qty"] - qty)

    def check_reorder(self) -> list[str]:
        """Return list of items that are at or below their threshold."""
        low = []
        for name, data in self.items.items():
            if data["qty"] <= data["threshold"]:
                low.append(name)
        return low
