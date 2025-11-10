import unittest
from chatbot import Chatbot, normalize
import pathlib

class TestChatbot(unittest.TestCase):
    def setUp(self):
        cfg = pathlib.Path(__file__).parent / "patterns.json"
        self.bot = Chatbot(str(cfg))

    def test_greeting(self):
        r = self.bot.respond("hello")
        self.assertTrue(
            any(greet in r.lower() for greet in ["hello", "hi", "hey"])
        )

    def test_unknown(self):
        r = self.bot.respond("asdfghjk")
        self.assertIn("didn't understand", r.lower())

    def test_pizza_flow(self):
        # Start the pizza dialog
        r1 = self.bot.respond("order pizza")
        self.assertIn("what size", r1.lower())

        # Choose size
        r2 = self.bot.respond("small")
        self.assertIn("what crust", r2.lower())

        # Choose crust
        r3 = self.bot.respond("thin")
        self.assertIn("pick a topping", r3.lower())

        # Choose topping
        r4 = self.bot.respond("pepperoni")
        self.assertIn("confirm", r4.lower())

        # Confirm order
        r5 = self.bot.respond("yes")
        self.assertIn("confirmed", r5.lower())

if __name__ == "__main__":
    unittest.main()
