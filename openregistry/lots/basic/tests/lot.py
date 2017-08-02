# -*- coding: utf-8 -*-
import os
import unittest

from openregistry.api.tests.base import BaseWebTest, snitch

from openregistry.lots.basic.tests.base import (
    test_lot_data, BaseLotWebTest
)
from openregistry.lots.basic.tests.lot_blanks import (
    # TenderResourceTest
    # listing,
    # get_lot,
    # lot_not_found,
    # dateModified_lot,
    # listing_draft,
    # listing_changes,
    # create_lot,
    # patch_lot,
    # TenderTest
    simple_add_lot,
)


# class TenderResourceTestMixin(object):
#     test_listing_changes = snitch(listing_changes)
#     test_listing_draft = snitch(listing_draft)
#     test_listing = snitch(listing)
#     test_create_lot = snitch(create_lot)
#     test_get_lot = snitch(get_lot)
#     test_dateModified_lot = snitch(dateModified_lot)
#     test_lot_not_found = snitch(lot_not_found)


class TenderTest(BaseWebTest):
    initial_data = test_lot_data
    relative_to = os.path.dirname(__file__)

    test_simple_add_lot = snitch(simple_add_lot)


# class TenderResourceTest(BaseLotWebTest, TenderResourceTestMixin):
#     initial_data = test_lot_data
#     initial_auth = ('Basic', ('broker', ''))
#     relative_to = os.path.dirname(__file__)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TenderResourceTest))
    suite.addTest(unittest.makeSuite(TenderTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
