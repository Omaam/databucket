"""
"""
import unittest

import xselect_handler as xh


class TestXselectHandler(unittest.TestCase):

    def test_make_bashscript(self):
        xh._make_bashscript(".", 1.0, [1, 10])


if __name__ == "__main__":
    unittest.main()
