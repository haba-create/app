from __future__ import annotations

import os
from flask import Flask, render_template, request, jsonify

from inventory import Inventory
from order_agent import OrderAgent

app = Flask(__name__)

# Initialize order agent with optional OpenAI key
def create_agent() -> OrderAgent:
    key = os.getenv("OPENAI_API_KEY")
    inventory = Inventory()
    # Example stock items
    inventory.set_stock("coffee beans", 20, threshold=5)
    inventory.set_stock("milk", 15, threshold=5)
    return OrderAgent(inventory, openai_api_key=key)

agent: OrderAgent = create_agent()

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/chat")
def chat():
    if agent is None:
        return jsonify({"reply": "Agent not initialized"})
    data = request.get_json() or {}
    msg = data.get("message", "")
    if not msg:
        return jsonify({"reply": "No message provided"})

    # Build conversation messages
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful coffee shop agent. Use the functions provided "
                "to manage orders and stock."
            ),
        },
        {"role": "user", "content": msg},
    ]

    if os.getenv("OPENAI_API_KEY") and agent:
        try:
            response = agent._openai_chat(messages)
            reply = response["choices"][0]["message"].get("content", "")
        except Exception as exc:  # pragma: no cover - runtime safety
            reply = f"Error: {exc}"
    else:
        reply = "(OpenAI not configured)"
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
