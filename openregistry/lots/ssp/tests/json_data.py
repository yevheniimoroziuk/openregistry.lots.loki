# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import timedelta

from openprocurement.api.utils import get_now
from openprocurement.api.tests.blanks.json_data import (
    test_document_data,
    test_item_data,
    test_organization
)


test_ssp_document_data = deepcopy(test_document_data)
test_ssp_lot_data = {
    "title": u"Тестовий лот",
    "description": u"Щось там тестове",
    "lotIdentifier": u"Q81318b19827",
    "lotType": "ssp",
    "lotCustodian": deepcopy(test_organization),
    "assets": [],
    "lotHolder": {"name": "name"}
}

now = get_now()
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
publication_auction_english_data.update({'procurementMethodType': 'SSP.english'})

publication_auction_insider_data = deepcopy(publication_auction_common)
publication_auction_insider_data.update({'procurementMethodType': 'SSP.insider'})

test_ssp_publication_data = {
    'auctions': [
        publication_auction_english_data,
        publication_auction_english_data,
        publication_auction_insider_data
    ],
}

test_ssp_item_data = deepcopy(test_item_data)
