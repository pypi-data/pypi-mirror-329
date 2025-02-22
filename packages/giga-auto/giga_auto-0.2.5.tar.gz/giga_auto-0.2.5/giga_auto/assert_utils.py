class AssertUtils:

    @staticmethod
    def assert_equal(actual, expected, msg=None):
        """
        断言两个值相等
        """
        assert actual == expected, f"{msg or ''} \nAssert Equal Failed: Expected:{expected},Actual:{actual}"

    @staticmethod
    def assert_not_equal(actual, expected, msg=None):
        """
        断言两个值不相等
        """
        assert actual != expected, f"{msg or ''} \nAssert Not Equal Failed: Expected:{expected},Actual:{actual}"

    @staticmethod
    def assert_in(expect_text, actual_text, msg=None):
        """
        断言actual在expected中
        """
        assert expect_text in actual_text, f"{msg or ''} \nAssert In Failed: Expected:{expect_text}"

    @staticmethod
    def assert_not_in(expect_text, actual_text, msg=None):
        """
        断言actual不在expected中
        """
        assert expect_text not in actual_text, f"{msg or ''} \nAssert Not In Failed"

    @staticmethod
    def assert_not_none(actual, msg=None):
        assert actual is not None, f"{msg or ''} \nAssert Not None Failed: Actual:{actual}"

    @staticmethod
    def assert_is_none(actual, msg=None):
        assert actual is None, f"{msg or ''} \nAssert Not None Failed: Actual:{actual}"

    @staticmethod
    def assert_true(actual, msg=None):
        assert actual == True, f"{msg or ''} \nAssert True Failed: Actual:{actual}"

    @staticmethod
    def assert_false(actual, msg=None):
        assert actual == False, f"{msg or ''} \nAssert False Failed: Actual:{actual}"
