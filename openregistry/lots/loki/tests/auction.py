# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openregistry.lots.core.tests.base import snitch

from openregistry.lots.loki.tests.base import (
    LotContentWebTest
)
from openregistry.lots.loki.tests.json_data import test_lot_auctions_data
from openregistry.lots.loki.tests.blanks.auction_blanks import (
    patch_english_auction,
    patch_half_english_auction,
    patch_insider_auction,
    rectificationPeriod_auction_workflow
)

class LotAuctionResourceTest(LotContentWebTest):
    initial_auctions_data = deepcopy(test_lot_auctions_data)

    test_patch_english_auction = snitch(patch_english_auction)
    test_patch_half_english_auction = snitch(patch_half_english_auction)
    test_patch_insider_auction = snitch(patch_insider_auction)
    test_rectificationPeriod_auction_workflow = snitch(rectificationPeriod_auction_workflow)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LotAuctionResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
