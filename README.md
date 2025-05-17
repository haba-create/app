# Coffee Shop Order Agent

This project provides a simple example of using the OpenAI agents framework to manage a coffee shop inventory. Users can interact with the agent via a chatbot or by calling functions directly.

## Requirements

- Python 3.11+
- The `openai` package (optional if you want actual OpenAI responses)

Install dependencies:

```bash
pip install openai
```

## Usage

1. Export your OpenAI API key:

```bash
export OPENAI_API_KEY=your-key
```

2. Run the agent script:

```bash
python run_order_agent.py
```

The agent starts a chat session. Type messages such as `set stock of espresso to 5` or `order 2 lattes`. Type `exit` to quit.

If the `openai` package is not installed, the script will run but replies will be placeholders.
