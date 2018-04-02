# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import timedelta

from openprocurement.api.utils import get_now
from openprocurement.api.tests.blanks.json_data import (
    test_document_data,
    test_item_data,
    test_organization
)

now = get_now()
test_loki_document_data = deepcopy(test_document_data)
test_loki_document_data['documentOf'] = 'lot'
test_loki_lot_data = {
    "title": u"Тестовий лот",
    "description": u"Щось там тестове",
    "lotIdentifier": u"Q81318b19827",
    "lotType": "loki",
    "lotCustodian": deepcopy(test_organization).update(
        {
            'identifier': {
              "legalNama": "Legal Name",
              "id": "identifier-id",
              "uri": "https://localhost"
            }
        }),
    "assets": [],
    "lotHolder": {
        "name": "name",
        "identifier": {
            "legalName": "Legal Name",
            "id": "identifier-id",
            "uri": "https://localhost"
        }
    },
    "decisionDetails": {
        "title": "Some Title",
        "decisionDate": (now + timedelta(days=5)).isoformat(),
        "decisionID": "ID-DECISION"
    },
}
publication_auction_common = {
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
publication_auction_english_data = deepcopy(publication_auction_common)
publication_auction_english_data.update({'procurementMethodType': 'Loki.english'})

publication_auction_insider_data = deepcopy(publication_auction_common)
publication_auction_insider_data.update({'procurementMethodType': 'Loki.insider'})

test_loki_publication_data = {
    'auctions': [
        publication_auction_english_data,
        publication_auction_english_data,
        publication_auction_insider_data
    ],
    "decisionDetails": {
        "title": "Some Title",
        "decisionDate": (now + timedelta(days=5)).isoformat(),
        "decisionID": "ID-DECISION"
    }
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
        "quantity": 5.0001
    }
)
