
# Simple Traditional Chatbot (Rule-Based + FSM)

This project implements a **non-LLM** chatbot using:
- Regex-based intent matching
- A small **finite-state machine** (FSM) for a pizza-order dialog
- Fallback handling for malformed inputs
- A simple CLI runner (no cloud dependencies)

## Quick Start

```bash
python3 chatbot.py
```

Try:
- `help`
- `order pizza`
- `small` → `thin` → `pepperoni` → `yes`
- `reset` to restart the dialog
- `quit` to exit

## Tests

```bash
python3 -m unittest tests.py
```

## Extending

- Add new intents to `patterns.json` with regex and responses.
- Add new dialog flows by creating additional FSMs or states/editing `reset_dialog()`.

## Notes

This is intentionally framework-free so it can run anywhere. If you want to wrap this in a web service, you can add a thin Flask/FastAPI layer that calls `Chatbot.respond(...)`.
