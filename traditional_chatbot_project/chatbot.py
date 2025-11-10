#!/usr/bin/env python3
"""
Simple Traditional Chatbot (Rule-Based + Finite-State Dialog)
- No ML/LLM dependencies.
- Demonstrates intents via regex/pattern matching and a small FSM for a "pizza order" flow.
- Includes graceful handling of malformed inputs and a help/capabilities command.
"""

import re
import json
import pathlib
from dataclasses import dataclass, field
from typing import Dict, Callable, Optional

# ---------- Utilities ----------

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())

# ---------- Rule-based intent matcher ----------

@dataclass
class IntentRule:
    pattern: str
    responses: list[str]

class IntentMatcher:
    def __init__(self, rules: Dict[str, IntentRule]):
        self.rules = rules

    def match(self, text: str) -> Optional[str]:
        t = normalize(text)
        for name, rule in self.rules.items():
            if re.search(rule.pattern, t):
                return name
        return None

# ---------- Finite State Machine for a simple task (pizza order) ----------

@dataclass
class State:
    name: str
    on_enter: Callable[['Chatbot'], str]
    transitions: Dict[str, str] = field(default_factory=dict)  # intent_name -> next_state

class FSM:
    def __init__(self, states: Dict[str, State], start: str, end: str):
        self.states = states
        self.current = start
        self.end = end

    def is_done(self) -> bool:
        return self.current == self.end

    def handle(self, bot: 'Chatbot', intent: Optional[str]) -> str:
        # If we're in a dialog, follow dialog transitions
        state = self.states[self.current]
        if intent and intent in state.transitions:
            self.current = state.transitions[intent]
            return self.states[self.current].on_enter(bot)
        # If no transition applies, use state's on_enter to prompt/reprompt
        return state.on_enter(bot)

# ---------- The Chatbot ----------

class Chatbot:
    def __init__(self, patterns_path: str):
        with open(patterns_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)

        self.capabilities = cfg["capabilities"]
        self.help_text = cfg["help_text"]
        rules = {name: IntentRule(**rule) for name, rule in cfg["intents"].items()}
        self.matcher = IntentMatcher(rules)
        self.rules = rules
        self.reset_dialog()

    def reset_dialog(self):
        # Define pizza order FSM states dynamically to keep the file self-contained
        def enter_start(bot: 'Chatbot') -> str:
            return ("Let's order a pizza! What size would you like? (small/medium/large)\n"
                    "You can say 'cancel' anytime to stop.")

        def enter_size(bot: 'Chatbot') -> str:
            return "Got it. What crust do you want? (thin/regular/deep-dish)"

        def enter_crust(bot: 'Chatbot') -> str:
            return "Yum. Pick a topping: pepperoni, mushrooms, onions, or olives."

        def enter_topping(bot: 'Chatbot') -> str:
            return f"Order summary: {bot.session.get('size')} pizza, {bot.session.get('crust')} crust, {bot.session.get('topping')}.\nConfirm? (yes/no)"

        def enter_done(bot: 'Chatbot') -> str:
            return "Your pizza order is confirmed. Anything else?"

        self.session: Dict[str, str] = {}

        states = {
            "start": State("start", enter_start, transitions={
                "size_small":"size", "size_medium":"size", "size_large":"size", "cancel_dialog":"done"
            }),
            "size": State("size", enter_size, transitions={
                "crust_thin":"crust", "crust_regular":"crust", "crust_deep":"crust", "cancel_dialog":"done"
            }),
            "crust": State("crust", enter_crust, transitions={
                "topping_pepperoni":"topping", "topping_mushrooms":"topping",
                "topping_onions":"topping", "topping_olives":"topping", "cancel_dialog":"done"
            }),
            "topping": State("topping", enter_topping, transitions={
                "confirm_yes":"done", "confirm_no":"done", "cancel_dialog":"done"
            }),
            "done": State("done", enter_done, transitions={})
        }
        self.fsm = FSM(states, start="start", end="done")

    # Dialog slot filling via side-effects when intents are detected
    def track_slots(self, intent: Optional[str]):
        if intent == "size_small": self.session["size"] = "small"
        elif intent == "size_medium": self.session["size"] = "medium"
        elif intent == "size_large": self.session["size"] = "large"
        elif intent == "crust_thin": self.session["crust"] = "thin"
        elif intent == "crust_regular": self.session["crust"] = "regular"
        elif intent == "crust_deep": self.session["crust"] = "deep-dish"
        elif intent == "topping_pepperoni": self.session["topping"] = "pepperoni"
        elif intent == "topping_mushrooms": self.session["topping"] = "mushrooms"
        elif intent == "topping_onions": self.session["topping"] = "onions"
        elif intent == "topping_olives": self.session["topping"] = "olives"

    def respond(self, text: str) -> str:
        t = normalize(text)

        # system commands
        if t in ("help", "capabilities", "what can you do"):
            return self.help_text + "\n\nCapabilities:\n- " + "\n- ".join(self.capabilities)
        if t in ("reset", "restart"):
            self.reset_dialog()
            return "Dialog has been reset. Type 'order pizza' to start again."
        if t in ("exit", "quit"):
            return "Goodbye!"

        # Begin pizza dialog
        if t in ("order pizza", "pizza", "start order"):
            self.reset_dialog()
            return self.fsm.states["start"].on_enter(self)

        # Match generic intents
        intent = self.matcher.match(t)

        # Track any slots from intent
        self.track_slots(intent)

        # If we are in dialog flow, let FSM handle transitions
        if intent and intent.startswith(("size_", "crust_", "topping_", "confirm_", "cancel_")):
            return self.fsm.handle(self, intent)

        # Generic FAQ / small talk
        if intent and intent in self.rules:
            from random import choice
            return choice(self.rules[intent].responses)

        # Fallbacks for malformed or unknown input
        return ("Sorry, I didn't understand that. Try 'help' to see what I can do, "
                "or type 'order pizza' to start the pizza demo.")
        
def main():
    cfg_path = pathlib.Path(__file__).parent / "patterns.json"
    bot = Chatbot(str(cfg_path))
    print("Simple Traditional Chatbot")
    print("Type 'help' for capabilities, 'order pizza' to start a demo dialog, 'quit' to exit.\n")
    while True:
        try:
            user = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        reply = bot.respond(user)
        print(reply)
        if reply.lower().startswith("goodbye"):
            break

if __name__ == "__main__":
    main()
