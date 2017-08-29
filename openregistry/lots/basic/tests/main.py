# -*- coding: utf-8 -*-

import unittest

from openregistry.lots.basic.tests import lot, document


def suite():
    tests = unittest.TestSuite()
    tests.addTest(document.suite())  # TODO: find out where tests interfere between each other
    tests.addTest(lot.suite())
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
