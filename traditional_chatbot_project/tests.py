import unittest
from chatbot import Chatbot, normalize
import pathlib

class TestChatbot(unittest.TestCase):
    def setUp(self):
        cfg = pathlib.Path(__file__).parent / "patterns.json"
        self.bot = Chatbot(str(cfg))

    def test_greeting(self):
        r = self.bot.respond("hello")
        self.assertTrue(any(greet in r.lower() for greet in ["hello", "hi", "hey"]))

    def test_unknown(self):
        r = self.bot.respond("asdfghjk")
        self.assertIn("didn't understand", r.lower())

    def test_pizza_flow(self):
        self.bot.respond("order pizza")
        self.assertIn("what size", self.bot.respond("small").lower())
        self.assertIn("what crust", self.bot.respond("thin").lower())
        self.assertIn("pick a topping", self.bot.respond("pepperoni").lower())
        self.assertIn("confirm", self.bot.respond("yes").lower())

if __name__ == "__main__":
    unittest.main()
