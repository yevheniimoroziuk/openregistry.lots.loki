# -*- coding: utf-8 -*-

import unittest

from openregistry.lots.basic.tests import lot


def suite():
    tests = unittest.TestSuite()
    tests.addTest(lot.suite())
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
