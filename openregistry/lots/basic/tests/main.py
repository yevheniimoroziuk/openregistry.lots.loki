# -*- coding: utf-8 -*-

import unittest

from openregistry.lots.basic.tests import lot, document


def suite():
    tests = unittest.TestSuite()
    tests.addTest(lot.suite())
    tests.addTest(document.suite())
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
