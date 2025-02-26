import os
import unittest
from unittest.mock import patch
from justai.agent.agent import Agent


class TestAgent(unittest.TestCase):
    def setUp(self):
        # Lijst van netwerken om te testen
        self.networks = ["gpt-4o", "gpt-4o-mini", "claude-3-opus-20240229", "claude-3-5-sonnet-20240620", 
                         "gemini-1.5-pro", "gemini-1.5-pro"]
        self.agents = [Agent(network) for network in self.networks]

    def test_chat(self):
        for i, agent in enumerate(self.agents):
            with self.subTest(network=self.networks[i]):
                with patch('justai.tools.cache.cached_llm_response') as mock_response:
                    mock_response.return_value = ("Test response", 10, 5)
                    response = agent.chat("Test prompt")
                    self.assertEqual(isinstance(response, str), True)
                    self.assertGreater(len(response), 0)

    def test_append_messages(self):
        for i, agent in enumerate(self.agents):
            with self.subTest(network=self.networks[i]):
                agent.append_messages("Test message")
                self.assertEqual(len(agent.messages), 1)
                self.assertEqual(agent.messages[0].content, "Test message")

    def test_reset(self):
        for i, agent in enumerate(self.agents):
            with self.subTest(network=self.networks[i]):
                agent.append_messages("Test message")
                agent.reset()
                self.assertEqual(len(agent.messages), 0)

if __name__ == '__main__':
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    unittest.main()