# -*- coding: utf-8 -*-

import unittest

from openregistry.lots.basic.tests import lot, document


def suite():
    suite = unittest.TestSuite()
    suite.addTest(lot.suite())
    suite.addTest(document.suite())
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
