# -*- coding: utf-8 -*-
from openregistry.lots.core.tests.base import (
    BaseLotWebTest as BaseLWT
)

test_lot_data = {
    "title": u"Тестовий лот",
    "description": u"Щось там тестове",
    "lotType": "basic",
}


class BaseLotWebTest(BaseLWT):
    initial_data = test_lot_data
    initial_auth = ('Basic', ('broker', ''))


class LotContentWebTest(BaseLotWebTest):
    initial_data = test_lot_data

    def setUp(self):
        super(LotContentWebTest, self).setUp()
        self.create_lot()
