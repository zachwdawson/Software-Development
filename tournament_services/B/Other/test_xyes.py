import unittest
import subprocess


class XyesTest(unittest.TestCase):
    """
    Class to test the xyes program
    """

    def check_result_output(self, result_string, limit, value):
        """
        Purpose: Check that properties of the output are satisfied.
        Signature: String Bool String -> Void
        :param result_string: output string for running the program
        :param limit: Whether the limit flag was specified
        :param value: the value that all lines in the string shoudl contain
        :return: asserts properties about the program
        """
        if limit:
            self.assertEqual(20, result_string.count(value))
        else:
            self.assertTrue(result_string.count(value) > 0)
        lines = result_string.split('\n')
        for line in lines:
            if line != '':
                line = line.rstrip()
                self.assertEqual(value, line)

    @staticmethod
    def run_xyes(arg_list, should_timeout=False):
        """
        Purpose: Runs the program being tested with specific args
        Signature: List<String> Boolean -> String
        :param arg_list: list of arguments passed to function
        :param should_timeout: whether the code needs a timeout to terminate
        :return: String containing output of running the xyes program
        """
        output = ''
        if should_timeout:
            try:
                subprocess.check_output(arg_list, timeout=1)
            except subprocess.TimeoutExpired as e:
                output = e.output
        else:
            output = subprocess.check_output(arg_list)
        if output:
            output = output.decode('ascii')
        return output

    def test_blank_limit(self):
        """
        Purpose: Test what happens when you have no input with the limit flag specified
        Signature: Void -> Void
        :return: checking properties of the output of this test
        """
        output = self.run_xyes(['./../xyes', '-limit'])
        self.check_result_output(output, True, 'hello world')

    def test_not_blank_limit(self):
        """
        Purpose: Test what happnes when you have other input and limit flag specified
        Signature: Void -> Void
        :return: checking properties of the output of this test
        """
        output = self.run_xyes(['./../xyes', '-limit', 'a', 'b', 'c'])
        self.check_result_output(output, True, 'a b c')

    def test_blank_hw(self):
        """
        Purpose: Test what happens when you have no input besides the script
        Signature: Void -> Void
        :return: tests properties of the terminated infinite program
        """
        output = self.run_xyes(['./../xyes'], should_timeout=True)
        self.check_result_output(output, False, 'hello world')

    def test_not_blank(self):
        """
        Purpose: Test what happens when you have input to the program but no limit flag
        Signature: Void -> Void
        :return: tests properties of the terminated infinite program
        """
        output = self.run_xyes(['./../xyes', 'a', 'b', 'c'], should_timeout=True)
        self.check_result_output(output, False, 'a b c')

    def test_not_blank_limit_later(self):
        """
        Purpose: Test what happens when you have input to the program and limit flag but it is not the first option
        Signature: Void -> Void
        :return: tests properties of the terminated infinite program
        """
        output = self.run_xyes(['./../xyes', 'a', 'b', 'c', '-limit'], should_timeout=True)
        self.check_result_output(output, False, 'a b c -limit')

    def test_more_than_twenty(self):
        """
        Purpose: Tests that with giving enough time the program will have more than twenty lines printed when
                 limit flag is not specified
        Signature: Void -> Void
        :return: tests whether more than twenty lines printed
        """
        iter_limit = 3
        timeout_seconds = 1
        iter_times = 0
        more_than_twenty = False
        while iter_times <= iter_limit:
            output_str = ''
            try:
                subprocess.check_output(['./../xyes', 'a', 'b', 'c'], timeout=timeout_seconds)
            except subprocess.TimeoutExpired as e:
                output = e.output
                output_str = output.decode('ascii')
            # if we have read more than 20, we have read more than the limit
            if output_str.count('a b c') > 20:
                more_than_twenty = True
                break
            timeout_seconds += 1
            iter_times += 1
        self.assertTrue(more_than_twenty)


if __name__ == '__main__':
    unittest.main()
