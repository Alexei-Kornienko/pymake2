import unittest

import pymake2.pymake as pymake


class PyMakeTest(unittest.TestCase):

    def test_depency_timestamp(self):
        dep = pymake.Dependency('tests/fixtures/file_a')
        expected_tstamp = os.path.getmtime('tests/fixtures/file_a')
        tstamp = dep.get_timestamp()
        self.assertEquals(expected_tstamp, tstamp)
