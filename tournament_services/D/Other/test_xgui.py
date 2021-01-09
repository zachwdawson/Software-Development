import unittest
import subprocess

USAGE_STRING = 'usage: ./xgui positive-integer'


class TestXgui(unittest.TestCase):

    def run_xgui(self, size):
        """
        Purpose: Run the xgui program and grab the output
        Signature: Int -> String
        :return: a string representing the output of running the program
        """
        output = subprocess.check_output(['./../xgui', str(size)])
        if output:
            output = output.decode('ascii')
        return output

    def test_string(self):
        """
        Purpose: Test passing a string to xgui
        Signature: Void -> Void
        """
        output = self.run_xgui('hello world')
        self.assertEqual(USAGE_STRING, output.strip())

    def test_negative_int(self):
        """
         Purpose: Test passing a negative integer
         Signature: Void -> Void
         """
        output = self.run_xgui(-10)
        self.assertEqual(USAGE_STRING, output.strip())

    def test_multiple_args(self):
        """
         Purpose: Test passing multiple args to xgui
         Signature: Void -> Void
         """
        output = subprocess.check_output(['./../xgui', '10', '10'])
        if output:
            output = output.decode('ascii')
        self.assertEqual(USAGE_STRING, output.strip())


if __name__ == '__main__':
    unittest.main()
