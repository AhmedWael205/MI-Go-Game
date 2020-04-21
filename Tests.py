from unittest.mock import patch
import unittest

from Go import go

class GoTestCase(unittest.TestCase):

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
            '2', '1', '1',
            '1',                # White Pass
            '2', '1', '0',
            '1',                # White Pass
            '2', '0', '1',
            '2', '0', '0',      # White Try Suicide should fail and plays again
            '2', '2',           # White plays again
            '1',
            '1'
        ]
        expected_output = [7.5, 4]
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
            '2', '1', '1',
            '2', '2', '1',   # Super KO
            '0', '0',
            '1',
            '1'
        ]
        expected_output = [11.5, 6]
        with patch('builtins.input', side_effect=user_input):
            stacks = go()
        self.assertEqual(stacks, expected_output)

    #################################################################################


if __name__ == "__main__":
    unittest.main()

