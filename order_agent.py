import json
import os
from typing import Any

try:
    import openai
except ImportError:  # pragma: no cover - openai may not be installed in this env
    openai = None

from inventory import Inventory


class OrderAgent:
    """Coffee shop order agent using the OpenAI agents framework."""

    def __init__(self, inventory: Inventory, openai_api_key: str | None = None) -> None:
        self.inventory = inventory
        self.model = "gpt-4o"  # default model
        if openai and openai_api_key:
            openai.api_key = openai_api_key
        self._tools = [
            {
                "type": "function",
                "function": {
                    "name": "set_stock",
                    "description": "Set stock for an item",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "item": {"type": "string"},
                            "qty": {"type": "integer"},
                            "threshold": {"type": "integer"},
                        },
                        "required": ["item", "qty"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "place_order",
                    "description": "Order an item by decreasing stock",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "item": {"type": "string"},
                            "qty": {"type": "integer"},
                        },
                        "required": ["item", "qty"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_stock",
                    "description": "Return current stock level",
                    "parameters": {
                        "type": "object",
                        "properties": {"item": {"type": "string"}},
                        "required": ["item"],
                    },
                },
            },
        ]

    def _openai_chat(self, messages: list[dict[str, str]]) -> dict[str, Any]:
        if not openai.api_key:
            return {"choices": [{"message": {"content": "(OpenAI API key not set in agent)"}}]}
        if openai is None:
            raise RuntimeError("openai package is not installed")
        return openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            tools=self._tools,
            tool_choice="auto",
        )

    # Functions exposed to the agent
    def set_stock(self, item: str, qty: int, threshold: int = 10) -> str:
        self.inventory.set_stock(item, qty, threshold)
        return f"Stock for {item} set to {qty} with threshold {threshold}."

    def place_order(self, item: str, qty: int) -> str:
        self.inventory.decrease_stock(item, qty)
        return f"Ordered {qty} x {item}."

    def get_stock(self, item: str) -> str:
        qty = self.inventory.get_stock(item)
        return f"{item} stock level: {qty}."

    # Chat interface
    def chat(self) -> None:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful coffee shop agent. Use the functions provided "
                    "to manage orders and stock."
                ),
            }
        ]
        print("Type 'exit' to stop chatting.")
        while True:
            user = input("User: ")
            if user.lower() == "exit":
                break
            messages.append({"role": "user", "content": user})
            if openai is None:
                print("openai not available: responding with placeholder message")
                print("Agent: (OpenAI responses would appear here)")
                continue
            response = self._openai_chat(messages)
            message = response["choices"][0]["message"]
            messages.append(message)
            if "tool_calls" in message:
                for call in message["tool_calls"]:
                    name = call["function"]["name"]
                    args = json.loads(call["function"]["arguments"])
                    result = getattr(self, name)(**args)
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": call["id"],
                            "content": result,
                        }
                    )
            else:
                print("Agent:", message.get("content"))

    def auto_reorder(self) -> list[str]:
        """Return items that need reordering."""
        return self.inventory.check_reorder()
