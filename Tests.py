from unittest.mock import patch
import unittest
import io
import sys

from Go import go

class GoTestCase1(unittest.TestCase):

    def test_go_White_Resign(self):
        user_input = [
            '2', '0', '0',
            '0'
        ]
        expected_output = "Black"
        with patch('builtins.input', side_effect=user_input):
            stacks = go()
        self.assertEqual(stacks, expected_output)



    #################################################################################
class GoTestCase2(unittest.TestCase):
    def test_go_Black_Resign(self):
        user_input = [
            '0'
        ]
        expected_output = "White"
        with patch('builtins.input', side_effect=user_input):
            stacks = go()
        self.assertEqual(stacks, expected_output)
        stacks = None

    ################################################################################
class GoTestCase3(unittest.TestCase):
    def test_go_1_move(self):
        user_input = [
            '2', '0', '0',
            '1',
            '1',
        ]
        expected_output = [6.5, 361]
        with patch('builtins.input', side_effect=user_input):
            stacks = go()
        self.assertEqual(stacks, expected_output)
        patch('builtins.input', 'original_input')

    #################################################################################
class GoTestCase4(unittest.TestCase):
    def test_go_suicide(self):
        user_input = [
            '2','7','7',
            '2', '1', '0',
            '2', '1', '2',
            '2', '2', '0',
            '2', '2', '1',
            '2', '0', '2',
            '2', '2', '2',
            '2', '0', '1',
            '1',
            '2', '3', '1',
            '1',
            '2', '3', '2',
            '1',
            '2', '2', '3',
            '1',
            '2', '1', '3',
            '2', '1', '1',
            '8','8',
            '1',
            '1'
        ]
        expected_output = [15.5, 5]
        with patch('builtins.input', side_effect=user_input):
            stacks = go()
        self.assertEqual(stacks, expected_output)
        patch('builtins.input', 'original_input')
    #################################################################################
class GoTestCase5(unittest.TestCase):
    def test_go_Eatgroup(self):
        user_input = [
            '2', '1', '1',
            '2', '1', '0',
            '2', '1', '2',
            '2', '2', '0',
            '2', '2', '1',
            '2', '0', '2',
            '2', '2', '2',
            '2', '0', '1',
            '1',
            '2', '3', '1',
            '1',
            '2', '3', '2',
            '1',
            '2', '2', '3',
            '1',
            '2', '1', '3',
            '1',
            '1'
        ]
        expected_output = [371.5, 0]
        with patch('builtins.input', side_effect=user_input):
            stacks = go()
        self.assertEqual(stacks, expected_output)

    #################################################################################
class GoTestCase6(unittest.TestCase):
    def test_go_SuperKo(self):
        user_input = [
            '2', '2', '0',
            '2', '1', '0',
            '2', '3', '1',
            '2', '0', '1',
            '2', '2', '2',
            '2', '1', '2',
            '2', '1', '1',
            '2', '2', '1',
            '2', '1', '1',   # Super KO
            '8', '8',
            '1',
            '1'
        ]
        expected_output = [13.5, 4]
        with patch('builtins.input', side_effect=user_input):
            stacks = go()
        self.assertEqual(stacks, expected_output)

    #################################################################################
"""
class GoTestCase7(unittest.TestCase):
    def getJSONscore(self):
        expected_output = "[191.5, 834]"
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        exec(open('ServerConfig.py').read())
        sys.stdout = sys.__stdout__
        x = capturedOutput.getvalue()[3500:3512][:]
        if x == expected_output:
            return True
        else:
            return False
"""

if __name__ == "__main__":
    unittest.main()

