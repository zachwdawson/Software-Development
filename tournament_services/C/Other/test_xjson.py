import unittest
import io
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Other.xjson as xjson


class TestXjson(unittest.TestCase):

    def parse_stdin_xjson(self, input_string):
        """
        Mocks writing to standard input for xjson
        Signature: String -> List
        :param input_string: string that should be mocked written to stdin
        :return: Result list of parsed JSON
        """
        old_stdin = sys.stdin
        sys.stdin = io.StringIO(input_string)
        sys.stdin.flush()
        json_string = xjson.read_from_stdin()
       	result_list = xjson.parse_json_objects(json_string)
        sys.stdin = old_stdin
        return result_list

    def test_parse_num(self):
        """
        Tests parsing numbers with xjson
        Signature: Void -> Void
        """
        result_list = self.parse_stdin_xjson('1 2 3 4')
        count_seq = {"count": 4, "seq": [1, 2, 3, 4]}
        self.assertEqual(count_seq, xjson.create_count_seq_object(result_list))
        json_list = [4, 4, 3, 2, 1]
        self.assertEqual(json_list, xjson.create_json_list(result_list))

    def test_parse_bool(self):
        """
        Tests parsing booleans with xjson
        Signature: Void -> Void
        """
        result_list = self.parse_stdin_xjson('true false true false')
        count_seq = {"count": 4, "seq": [True, False, True, False]}
        self.assertEqual(count_seq, xjson.create_count_seq_object(result_list))
        json_list = [4, False, True, False, True]
        self.assertEqual(json_list, xjson.create_json_list(result_list))

    def test_parse_string(self):
        """
        Tests parsing strings with xjson
        Signature: Void -> Void
        """
        result_list = self.parse_stdin_xjson('\"abc\" \"bcd\" \"cde\"')
        count_seq = {"count": 3, "seq": ["abc", "bcd", "cde"]}
        self.assertEqual(count_seq, xjson.create_count_seq_object(result_list))
        json_list = [3, "cde", "bcd", "abc"]
        self.assertEqual(json_list, xjson.create_json_list(result_list))

    def test_parse_null(self):
        """
        Tests parsing null values with xjson
        Signature: Void -> Void
        """
        result_list = self.parse_stdin_xjson("null null")
        count_seq = {"count": 2, "seq": [None, None]}
        self.assertEqual(count_seq, xjson.create_count_seq_object(result_list))
        json_list = [2, None, None]
        self.assertEqual(json_list, xjson.create_json_list(result_list))

    def test_parse_object(self):
        """
        Tests parsing object values with xjson
        Signature: Void -> Void
        """
        result_list = self.parse_stdin_xjson("""{"jason": "a"}""")
        count_seq = {"count": 1, "seq": [{"jason": "a"}]}
        self.assertEqual(count_seq, xjson.create_count_seq_object(result_list))
        json_list = [1, {"jason": "a"}]
        self.assertEqual(json_list, xjson.create_json_list(result_list))

        result_list = self.parse_stdin_xjson("""{"jason": {"vlad": "s"}}""")
        count_seq = {"count": 1, "seq": [{"jason": {"vlad": "s"}}]}
        self.assertEqual(count_seq, xjson.create_count_seq_object(result_list))
        json_list = [1, {"jason": {"vlad": "s"}}]
        self.assertEqual(json_list, xjson.create_json_list(result_list))

        result_list = self.parse_stdin_xjson("""{"jason": "a"} {"vlad": "s"}""")
        count_seq = {"count": 2, "seq": [{"jason": "a"}, {"vlad": "s"}]}
        self.assertEqual(count_seq, xjson.create_count_seq_object(result_list))
        json_list = [2, {"vlad": "s"}, {"jason": "a"}]
        self.assertEqual(json_list, xjson.create_json_list(result_list))

    def test_parse_array(self):
        """
        Tests parsing array values with xjson
        Signature: Void -> Void
        """
        result_list = self.parse_stdin_xjson("[1, 2, 3, 4 ,5]")
        count_seq = {"count": 1, "seq": [[1, 2, 3, 4, 5]]}
        self.assertEqual(count_seq, xjson.create_count_seq_object(result_list))
        json_list = [1, [1, 2, 3, 4, 5]]
        self.assertEqual(json_list, xjson.create_json_list(result_list))

        result_list = self.parse_stdin_xjson("[1, 2, 3, 4 ,5] [1, 2, 3, 4]")
        count_seq = {"count": 2, "seq": [[1, 2, 3, 4, 5], [1, 2, 3, 4]]}
        self.assertEqual(count_seq, xjson.create_count_seq_object(result_list))
        json_list = [2, [1, 2, 3, 4], [1, 2, 3, 4, 5]]
        self.assertEqual(json_list, xjson.create_json_list(result_list))

    def test_parse_complex(self):
        """
        Tests parsing complex mix of values with xjson
        Signature: Void -> Void
        """
        complex_in = """
        {"jason": [{"test": [1, 2]}]} [{"t": "y"}, [true, null]]
        """
        result_list = self.parse_stdin_xjson(complex_in)
        count_seq = {"count": 2, "seq": [{"jason": [{"test": [1, 2]}]}, [{"t": "y"}, [True, None]]]}
        self.assertEqual(count_seq, xjson.create_count_seq_object(result_list))
        json_list = [2, [{"t": "y"}, [True, None]], {"jason": [{"test": [1, 2]}]}]
        self.assertEqual(json_list, xjson.create_json_list(result_list))

    def test_parse_whitespace(self):
        """
        Tests parsing strange whitespace configurations with xjson
        Signature: Void -> Void
        """
        whitespace_in = """
        truenull "3"4       123214{"jason":   1}[1, 15]\n
        \t 1.23true
        """
        result_list = self.parse_stdin_xjson(whitespace_in)
        self.assertEqual([True, None, '3', 4, 123214, {'jason': 1}, [1, 15], 1.23, True], result_list)


if __name__ == '__main__':
    unittest.main()
