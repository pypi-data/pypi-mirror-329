import unittest
import os
from justai.tools.log import Log, set_log_dir

class TestLog(unittest.TestCase):
    def setUp(self):
        set_log_dir("test_logs")
        self.log = Log()

    def tearDown(self):
        self.log.close()
        os.remove(self.log.log_path)

    def test_write_and_read(self):
        self.log.write("Test Title", "Test Content", "info")
        html_content = self.log.as_html()
        self.assertIn("Test Title", html_content)
        self.assertIn("Test Content", html_content)

    def test_clear(self):
        self.log.write("Test Title", "Test Content", "info")
        self.log.clear()
        self.assertTrue(self.log.is_empty())

if __name__ == '__main__':
    unittest.main()