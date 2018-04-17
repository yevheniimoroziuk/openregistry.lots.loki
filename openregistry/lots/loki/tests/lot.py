# -*- coding: utf-8 -*-
import os
import unittest

from openprocurement.api.tests.base import BaseWebTest, snitch
from openprocurement.api.tests.blanks.mixins import ResourceTestMixin
from openregistry.lots.loki.tests.base import (
    BaseLotWebTest
)
from openregistry.lots.loki.tests.json_data import test_loki_lot_data
from openregistry.lots.loki.tests.blanks.lot_blanks import (
    dateModified_resource,
    # LotResourceTest
    change_draft_lot,
    change_dissolved_lot,
    check_lot_assets,
    check_lotIdentifier,
    check_decisions,
    change_pending_lot,
    change_composing_lot,
    change_active_salable_lot,
    change_deleted_lot,
    change_pending_dissolution_lot,
    change_active_salable_lot,
    change_active_awaiting_lot,
    change_active_auction_lot,
    change_active_contracting_lot,
    change_sold_lot,
    change_pending_sold_lot,
    # LotTest
    simple_add_lot,
    simple_patch
)
from openregistry.lots.loki.models import Lot


class LotTest(BaseWebTest):
    initial_data = test_loki_lot_data
    relative_to = os.path.dirname(__file__)
    test_simple_add_lot = snitch(simple_add_lot)


class LotResourceTest(BaseLotWebTest, ResourceTestMixin):
    initial_status = 'pending'
    lot_model = Lot

    test_05_dateModified_resource = snitch(dateModified_resource)
    test_08_change_draft_lot = snitch(change_draft_lot)
    test_09_change_pending_lot = snitch(change_pending_lot)
    test_10_change_active_salable_lot = snitch(change_active_salable_lot)
    test_11_check_deleted_lot = snitch(change_deleted_lot)
    test_12_check_pending_dissolution_lot = snitch(change_pending_dissolution_lot)
    test_13_check_active_salable_lot = snitch(change_active_salable_lot)
    test_14_check_active_awaiting_lot = snitch(change_active_awaiting_lot)
    test_15_check_active_auction_lot = snitch(change_active_auction_lot)
    test_16_check_active_contracting_lot = snitch(change_active_contracting_lot)
    test_17_change_dissolved_lot = snitch(change_dissolved_lot)
    test_18_check_sold_lot = snitch(change_sold_lot)
    test_19_check_lot_assets = snitch(check_lot_assets)
    test_20_check_lot_lotIdentifier = snitch(check_lotIdentifier)
    test_21_check_pending_sold_lot = snitch(change_pending_sold_lot)
    test_22_simple_patch = snitch(simple_patch)
    test_change_composing_lot = snitch(change_composing_lot)
    test_check_decisions = snitch(check_decisions)

def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(LotResourceTest))
    tests.addTest(unittest.makeSuite(LotTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
