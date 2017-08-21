# -*- coding: utf-8 -*-
import os
from copy import deepcopy
from uuid import uuid4

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
    "assets": [uuid4().hex]
}


class BaseLotWebTest(BaseLWT):
    initial_data = deepcopy(test_lot_data)
    initial_auth = ('Basic', ('broker', ''))
    relative_to = os.path.dirname(__file__)


class LotContentWebTest(BaseLotWebTest):
    init = True
    initial_status = 'pending'
