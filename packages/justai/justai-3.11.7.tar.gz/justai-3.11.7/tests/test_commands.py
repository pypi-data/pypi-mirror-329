
# class TestCommandHandler(unittest.TestCase):
#     def setUp(self):
#         self.agent = MagicMock(spec=Agent)
#         self.command_handler = CommandHandler(self.agent)
# 
#     def test_handle_quit(self):
#         result = self.command_handler.handle_command('quit')
#         self.assertFalse(result)
# 
#     def test_handle_load(self):
#         with patch.object(self.agent, 'load') as mock_load:
#             result = self.command_handler.handle_command('load test_file')
#             mock_load.assert_called_once_with('test_file')
#             self.assertTrue(result)
# 
#     def test_handle_save(self):
#         with patch.object(self.agent, 'save') as mock_save:
#             result = self.command_handler.handle_command('save test_file')
#             mock_save.assert_called_once_with('test_file')
#             self.assertTrue(result)
# 
#     def test_handle_system(self):
#         result = self.command_handler.handle_command('system New system message')
#         self.assertEqual(self.agent.system_message, 'New system message')
#         self.assertTrue(result)
# 
#     def test_handle_gpt_attribute(self):
#         result = self.command_handler.handle_command('temperature=0.8')
#         self.assertEqual(self.agent.temperature, 0.8)
#         self.assertTrue(result)
# 
# if __name__ == '__main__':
#     unittest.main()