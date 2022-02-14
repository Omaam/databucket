"""Test for databucket.
"""
import unittest

# from databucket import DataBucket
import databucket as db


class DataBcuketTest(unittest.TestCase):

    def test_acquiere_dirname(self):
        testcase = "MAXI J1820+070"
        expected = "maxi_j1820p070"
        self.assertEqual(db._acquire_dirname(testcase), expected)

    def test_load_bucketpath(self):
        expected = "~/Data/Bucket"
        self.assertEqual(db._load_bucketpath(), expected)


if __name__ == "__main__":
    unittest.main()
