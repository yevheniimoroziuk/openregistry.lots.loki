# -*- coding: utf-8 -*-
import os
import unittest

from openregistry.api.tests.base import BaseWebTest, snitch

from openregistry.lots.basic.tests.base import (
    test_lot_data, BaseLotWebTest
)
from openregistry.lots.basic.tests.lot_blanks import (
    listing,
    get_lot,
    lot_not_found,
    dateModified_lot,
    change_draft_lot,
    change_waiting_lot,
    change_dissolved_lot,
    listing_draft,
    listing_changes,
    create_lot,
    simple_add_lot,
    check_lot_assets,
)


class LotTest(BaseWebTest):
    initial_data = test_lot_data
    relative_to = os.path.dirname(__file__)
    test_simple_add_lot = snitch(simple_add_lot)


class LotResourceTest(BaseLotWebTest):
    initial_data = test_lot_data
    initial_auth = ('Basic', ('broker', ''))
    initial_status = 'pending'
    relative_to = os.path.dirname(__file__)
    test_01_listing = snitch(listing)
    test_02_listing_draft = snitch(listing_draft)
    test_03_listing_changes = snitch(listing_changes)
    test_04_lot_not_found = snitch(lot_not_found)
    test_05_get_lot = snitch(get_lot)
    test_06_dateModified_lot = snitch(dateModified_lot)
    test_07_create_lot = snitch(create_lot)
    test_08_change_draft_lot = snitch(change_draft_lot)
    test_09_change_waiting_lot = snitch(change_waiting_lot)
    test_10_change_dissolved_lot = snitch(change_dissolved_lot)
    test_11_check_lot_assets = snitch(check_lot_assets)


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(LotResourceTest))
    tests.addTest(unittest.makeSuite(LotTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
