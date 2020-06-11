import unittest
from assignment import CourseWareB


class AssignmentTest(unittest.TestCase):
    """
    这两个测试必写，你也可以增加其他你认为重要的测试
    """

    def test_load_state(self):
        CourseWareB.load_raw_state("")

    def test_right_ans(self):
        CourseWareB.is_user_right(())


if __name__ == "__main__":
    unittest.main()
