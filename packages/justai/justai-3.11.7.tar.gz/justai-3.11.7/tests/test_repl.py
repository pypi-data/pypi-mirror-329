
# class TestRepl(unittest.TestCase):
#     def setUp(self):
#         self.agent = MagicMock(spec=Agent)
#         self.command_handler = MagicMock()
#         self.repl = Repl(self.agent, self.command_handler)
# 
#     @patch('builtins.input', side_effect=[':quit'])
#     def test_run_quit(self, mock_input):
#         self.repl.run()
#         self.command_handler.assert_called_once_with('quit')
# 
#     @patch('builtins.input', side_effect=['Test prompt', ':quit'])
#     def test_run_chat(self, mock_input):
#         self.agent.chat.return_value = "Test response"
#         self.repl.run()
#         self.agent.chat.assert_called_once_with('Test prompt')
# 
# if __name__ == '__main__':
#     unittest.main()