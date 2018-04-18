# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import timedelta

from openregistry.lots.core.utils import get_now
from openregistry.lots.core.tests.blanks.json_data import (
    test_document_data,
    test_item_data,
    test_organization
)

now = get_now()
test_loki_document_data = deepcopy(test_document_data)
test_loki_document_data['documentOf'] = 'lot'

auction_common = {
    'auctionPeriod': {
        'startDate': (now + timedelta(days=5)).isoformat(),
        'endDate': (now + timedelta(days=10)).isoformat()
    },
    'tenderingDuration': 'P25DT12H',
    'value': {
        'amount': 3000,
        'currency': 'UAH',
        'valueAddedTaxIncluded': True
    },
    'minimalStep': {
        'amount': 300,
        'currency': 'UAH',
        'valueAddedTaxIncluded': True
    },
    'guarantee': {
        'amount': 700,
        'currency': 'UAH'
    },
    'registrationFee': {
        'amount': 700,
        'currency': 'UAH'
    }
}
auction_english_data = deepcopy(auction_common)
auction_english_data.update({'procurementMethodType': 'Loki.english'})

auction_half_english_data = deepcopy(auction_common)
auction_half_english_data['value']['amount'] = auction_english_data['value']['amount'] / 2
auction_half_english_data['minimalStep']['amount'] = auction_english_data['minimalStep']['amount'] / 2
auction_half_english_data.update({'procurementMethodType': 'Loki.english'})

auction_insider_data = deepcopy(auction_common)
auction_insider_data.update({'procurementMethodType': 'Loki.insider'})

test_loki_lot_data = {
    "title": u"Тестовий лот",
    "description": u"Щось там тестове",
    "lotIdentifier": u"Q81318b19827",
    "lotType": "loki",
    "assets": [],
    "auctions": [
        auction_english_data,
        auction_half_english_data,
        auction_insider_data
    ]
}

test_loki_item_data = deepcopy(test_item_data)
test_loki_item_data['registrationDetails'] = {
    'status': 'unknown'
}
test_loki_item_data.update(
    {
        "unit": {"code": "code"},
        "classification": {
            "scheme": "CAV",
            "id": "42111000-7",
            "description": "Description"
        },
        "address": {"countryName": "Ukraine"},
        "quantity": 5.0001,
        "additionalClassifications": [
            {
                "scheme": u"UA-EDR",
                "id": u"111111-4",
                "description": u"папір і картон гофровані, паперова й картонна тара"
            }
        ]
    }
)
