import os
from inventory import Inventory
from order_agent import OrderAgent


def main() -> None:
    key = os.getenv("OPENAI_API_KEY")
    inv = Inventory()
    agent = OrderAgent(inv, openai_api_key=key)
    # Example initial stock
    inv.set_stock("coffee beans", 20, threshold=5)
    inv.set_stock("milk", 15, threshold=5)
    agent.chat()


if __name__ == "__main__":
    main()
