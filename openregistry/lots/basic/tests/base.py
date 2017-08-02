# -*- coding: utf-8 -*-
from openregistry.lots.core.tests.base import (
    BaseLotWebTest as BaseLWT
)


test_organization = {
    "name": u"Державне управління справами",
    "identifier": {
        "scheme": u"UA-EDR",
        "id": u"00037256",
        "uri": u"http://www.dus.gov.ua/"
    },
    "address": {
        "countryName": u"Україна",
        "postalCode": u"01220",
        "region": u"м. Київ",
        "locality": u"м. Київ",
        "streetAddress": u"вул. Банкова, 11, корпус 1"
    },
    "contactPoint": {
        "name": u"Державне управління справами",
        "telephone": u"0440000000"
    }
}

test_lotCustodian = test_organization.copy()

test_lot_data = {
    "title": u"Тестовий лот",
    "description": u"Щось там тестове",
    "lotType": "basic",
    "lotCustodian": test_lotCustodian,
}


class BaseLotWebTest(BaseLWT):
    initial_data = test_lot_data
    initial_auth = ('Basic', ('broker', ''))


class LotContentWebTest(BaseLotWebTest):
    initial_data = test_lot_data

    def setUp(self):
        super(LotContentWebTest, self).setUp()
        self.create_lot()
