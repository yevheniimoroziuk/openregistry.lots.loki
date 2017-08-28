# -*- coding: utf-8 -*-
import os
import unittest

from openregistry.api.tests.base import BaseWebTest, snitch
from openregistry.api.tests.blanks.mixins import ResourceTestMixin
from openregistry.lots.basic.tests.base import (
    test_lot_data, BaseLotWebTest
)
from openregistry.lots.basic.tests.lot_blanks import (
    # LotResourceTest
    change_draft_lot,
    change_waiting_lot,
    change_dissolved_lot,
    check_lot_assets,
    # LotTest
    simple_add_lot
)


class LotTest(BaseWebTest):
    initial_data = test_lot_data
    relative_to = os.path.dirname(__file__)
    test_simple_add_lot = snitch(simple_add_lot)


class LotResourceTest(BaseLotWebTest, ResourceTestMixin):
    initial_status = 'pending'

    test_08_change_draft_lot = snitch(change_draft_lot)
    test_09_change_waiting_lot = snitch(change_waiting_lot)
    test_10_change_dissolved_lot = snitch(change_dissolved_lot)
    test_11_check_lot_assets = snitch(check_lot_assets)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LotResourceTest))
    suite.addTest(unittest.makeSuite(LotTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
