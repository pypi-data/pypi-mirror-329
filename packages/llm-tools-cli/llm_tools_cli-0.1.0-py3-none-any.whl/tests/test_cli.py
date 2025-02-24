import unittest
from click.testing import CliRunner
from llx.cli import main

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def test_argument_parsing(self):  
        result = self.runner.invoke(main, ['--model', 'gpt-3', 'Hello'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('response', result.output)

    def test_empty_prompt(self):
        result = self.runner.invoke(main, ['--model', 'gpt-3'])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn('Prompt is required', result.output)

    def test_api_call(self):
        result = self.runner.invoke(main, ['--model', 'gpt-3', 'What is AI?'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('response', result.output)

if __name__ == '__main__':
    unittest.main()