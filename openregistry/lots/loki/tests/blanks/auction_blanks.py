# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy
from datetime import timedelta

from openregistry.lots.core.utils import (
    get_now,
    calculate_business_date
)
from openregistry.lots.core.models import Period
from openregistry.lots.loki.models import Lot
from openregistry.lots.core.constants import SANDBOX_MODE
from openregistry.lots.loki.constants import DEFAULT_DUTCH_STEPS


def patch_english_auction(self):
    data = deepcopy(self.initial_auctions_data)
    response = self.app.get('/{}/auctions'.format(self.resource_id))
    auctions = sorted(response.json['data'], key=lambda a: a['tenderAttempts'])
    english = auctions[0]

    response = self.app.patch_json('/{}/auctions/{}'.format(self.resource_id, english['id']),
        headers=self.access_header, params={
            "data": data['english']
            })
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json["data"]["id"], english['id'])
    self.assertEqual(response.json["data"]["tenderAttempts"], 1)
    self.assertEqual(response.json["data"]["value"], data['english']['value'])
    self.assertEqual(response.json["data"]["minimalStep"], data['english']['minimalStep'])
    self.assertEqual(response.json["data"]["auctionPeriod"], data['english']['auctionPeriod'])
    self.assertEqual(response.json["data"]["guarantee"], data['english']['guarantee'])
    self.assertEqual(response.json["data"]["registrationFee"], data['english']['registrationFee'])
    self.assertNotIn('dutchSteps', response.json["data"]["auctionParameters"])

    data_with_tenderingDuration = {'tenderingDuration': 'P2YT3H'}
    response = self.app.patch_json('/{}/auctions/{}'.format(self.resource_id, english['id']),
        headers=self.access_header, params={
            "data": data_with_tenderingDuration
            })
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json["data"]["tenderAttempts"], 1)
    self.assertNotIn('tenderingDuration', response.json['data'])

    response = self.app.get('/{}/auctions'.format(self.resource_id))
    auctions = sorted(response.json['data'], key=lambda a: a['tenderAttempts'])
    english = auctions[0]
    half_english = auctions[1]
    insider = auctions[2]

    # Test first sellout.english
    self.assertEqual(english['procurementMethodType'], 'sellout.english')
    self.assertEqual(english['value']['amount'], data['english']['value']['amount'])
    self.assertEqual(english['registrationFee']['amount'], data['english']['registrationFee']['amount'])
    self.assertEqual(english['minimalStep']['amount'], data['english']['minimalStep']['amount'])
    self.assertEqual(english['guarantee']['amount'], data['english']['guarantee']['amount'])
    self.assertEqual(english['auctionParameters']['type'], 'english')
    self.assertNotIn('dutchSteps', english['auctionParameters'])
    self.assertNotIn('tenderingDuration', english)

    # Test second sellout.english(half values)
    self.assertEqual(half_english['procurementMethodType'], 'sellout.english')
    self.assertEqual(half_english['value']['amount'], english['value']['amount'] / 2)
    self.assertEqual(half_english['registrationFee']['amount'], english['registrationFee']['amount'] / 2)
    self.assertEqual(half_english['minimalStep']['amount'], english['minimalStep']['amount'] / 2)
    self.assertEqual(half_english['guarantee']['amount'], english['guarantee']['amount'] / 2)
    self.assertEqual(half_english['auctionParameters']['type'], 'english')
    self.assertNotIn('dutchSteps', half_english['auctionParameters'])

    # Test second sellout.insider(half values)
    self.assertEqual(insider['procurementMethodType'], 'sellout.insider')
    self.assertEqual(insider['value']['amount'], english['value']['amount'] / 2)
    self.assertEqual(insider['registrationFee']['amount'], english['registrationFee']['amount'] / 2)
    self.assertEqual(insider['minimalStep']['amount'], english['minimalStep']['amount'] / 2)
    self.assertEqual(insider['guarantee']['amount'], english['guarantee']['amount'] / 2)
    self.assertEqual(insider['auctionParameters']['type'], 'insider')
    self.assertEqual(insider['auctionParameters']['dutchSteps'], DEFAULT_DUTCH_STEPS)

    # Test dutch steps validation
    data = deepcopy(self.initial_auctions_data)
    data['english']['auctionParameters'] = {'dutchSteps': 66}
    response = self.app.patch_json(
        '/{}/auctions/{}'.format(self.resource_id, english['id']),
        headers=self.access_header, params={
            "data": data['english']
            },
        status=422
    )
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(
        response.json['errors'][0]['description']['dutchSteps'],
        ["dutchSteps can be filled only when type is insider."]
    )


def patch_half_english_auction(self):
    data = deepcopy(self.initial_auctions_data)
    response = self.app.get('/{}/auctions'.format(self.resource_id))
    auctions = sorted(response.json['data'], key=lambda a: a['tenderAttempts'])
    half_english = auctions[1]

    response = self.app.patch_json('/{}/auctions/{}'.format(self.resource_id, half_english['id']),
        headers=self.access_header, params={
            "data": data['half.english']
            })
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['tenderingDuration'], data['half.english']['tenderingDuration'])
    self.assertEqual(response.json["data"]["tenderAttempts"], 2)
    self.assertNotIn('dutchSteps', response.json["data"]["auctionParameters"])

    response = self.app.get('/{}/auctions'.format(self.resource_id))
    auctions = sorted(response.json['data'], key=lambda a: a['tenderAttempts'])
    half_english = auctions[1]
    insider = auctions[2]

    # Test second sellout.english(half values)
    self.assertEqual(half_english['auctionParameters']['type'], 'english')
    self.assertEqual(half_english['tenderingDuration'], data['half.english']['tenderingDuration'])
    self.assertNotIn('dutchSteps', half_english['auctionParameters'])

    # Test second sellout.insider(half values)
    self.assertEqual(insider['procurementMethodType'], 'sellout.insider')
    self.assertEqual(insider['tenderingDuration'], half_english['tenderingDuration'])
    self.assertEqual(insider['auctionParameters']['dutchSteps'], DEFAULT_DUTCH_STEPS)

    # Test dutch steps validation
    data = deepcopy(self.initial_auctions_data)
    data['english']['auctionParameters'] = {'dutchSteps': 66}
    response = self.app.patch_json(
        '/{}/auctions/{}'.format(self.resource_id, half_english['id']),
        headers=self.access_header, params={
            "data": data['english']
            },
        status=422
    )
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(
        response.json['errors'][0]['description']['dutchSteps'],
        ["dutchSteps can be filled only when type is insider."]
    )


def patch_insider_auction(self):
    data = deepcopy(self.initial_auctions_data)
    response = self.app.get('/{}/auctions'.format(self.resource_id))
    auctions = sorted(response.json['data'], key=lambda a: a['tenderAttempts'])
    insider = auctions[2]
    data_dutch_steps = {'auctionParameters': {'dutchSteps': 77}}

    response = self.app.patch_json('/{}/auctions/{}'.format(self.resource_id, insider['id']),
        headers=self.access_header, params={
            "data": data_dutch_steps
            })
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['auctionParameters']['dutchSteps'], data_dutch_steps['auctionParameters']['dutchSteps'])
    self.assertNotIn('tenderingDuration', response.json['data'])
    self.assertEqual(response.json["data"]["tenderAttempts"], 3)

    data_with_tenderingDuration = {'tenderingDuration': 'P2YT3H'}
    response = self.app.patch_json('/{}/auctions/{}'.format(self.resource_id, insider['id']),
        headers=self.access_header, params={
            "data": data_with_tenderingDuration
            })
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertNotIn('tenderingDuration', response.json['data'])
    self.assertEqual(response.json["data"]["tenderAttempts"], 3)


def rectificationPeriod_auction_workflow(self):
    rectificationPeriod = Period()
    rectificationPeriod.startDate = get_now() - timedelta(3)
    rectificationPeriod.endDate = calculate_business_date(rectificationPeriod.startDate, timedelta(1))
    data = deepcopy(self.initial_auctions_data)

    lot = self.create_resource()

    # Change rectification period in db
    fromdb = self.db.get(lot['id'])
    fromdb = Lot(fromdb)

    fromdb.status = 'pending'
    fromdb.rectificationPeriod = rectificationPeriod
    fromdb = fromdb.store(self.db)

    self.assertEqual(fromdb.id, lot['id'])

    response = self.app.get('/{}'.format(lot['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['id'], lot['id'])

    response = self.app.get('/{}/auctions'.format(self.resource_id))
    auctions = sorted(response.json['data'], key=lambda a: a['tenderAttempts'])
    english = auctions[0]


    response = self.app.patch_json('/{}/auctions/{}'.format(lot['id'], english['id']),
                                   headers=self.access_header,
                                   params={'data': data['english']},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.json['errors'][0]['description'], 'You can\'t change auctions after rectification period')


@unittest.skipIf(not SANDBOX_MODE, 'If sandbox mode is enabled auctionParameters has additional field procurementMethodDetails')
def procurementMethodDetails_check_with_sandbox(self):
    data = deepcopy(self.initial_data)

    # Test procurementMethodDetails after creating lot
    response = self.app.get('/{}'.format(self.resource_id))
    lot = response.json['data']
    english = response.json['data']['auctions'][0]
    half_english = response.json['data']['auctions'][1]
    insider = response.json['data']['auctions'][2]

    self.assertNotIn(
        'procurementMethodDetails',
        english['auctionParameters']
    )
    self.assertNotIn(
        'procurementMethodDetails',
         half_english['auctionParameters']
    )
    self.assertNotIn(
        'procurementMethodDetails',
        insider['auctionParameters']
    )

    auction_param_with_procurementMethodDetails = {
        'auctionParameters': {'procurementMethodDetails': 'quick'}
    }

    # Test procurementMethodDetails after update half english
    response = self.app.patch_json(
        '/{}/auctions/{}'.format(lot['id'], half_english['id']),
        {"data": auction_param_with_procurementMethodDetails},
        headers=self.access_header
    )
    self.assertNotIn(
        'procurementMethodDetails',
        response.json['data']['auctionParameters']
    )

    response = self.app.get('/{}'.format(lot['id']))
    english = response.json['data']['auctions'][0]
    half_english = response.json['data']['auctions'][1]
    insider = response.json['data']['auctions'][2]
    self.assertNotIn(
        'procurementMethodDetails',
        english['auctionParameters']
    )
    self.assertNotIn(
        'procurementMethodDetails',
         half_english['auctionParameters']
    )
    self.assertNotIn(
        'procurementMethodDetails',
        insider['auctionParameters']
    )

    # Test procurementMethodDetails after update insider
    response = self.app.patch_json(
        '/{}/auctions/{}'.format(lot['id'], insider['id']),
        {"data": auction_param_with_procurementMethodDetails},
        headers=self.access_header
    )
    self.assertNotIn(
        'procurementMethodDetails',
        response.json['data']['auctionParameters']
    )

    response = self.app.get('/{}'.format(lot['id']))
    english = response.json['data']['auctions'][0]
    half_english = response.json['data']['auctions'][1]
    insider = response.json['data']['auctions'][2]
    self.assertNotIn(
        'procurementMethodDetails',
        english['auctionParameters']
    )
    self.assertNotIn(
        'procurementMethodDetails',
         half_english['auctionParameters']
    )
    self.assertNotIn(
        'procurementMethodDetails',
        insider['auctionParameters']
    )

    # Test procurementMethodDetails after update english
    response = self.app.patch_json(
        '/{}/auctions/{}'.format(lot['id'], english['id']),
        {"data": auction_param_with_procurementMethodDetails},
        headers=self.access_header
    )
    self.assertEqual(
        response.json['data']['auctionParameters']['procurementMethodDetails'],
        auction_param_with_procurementMethodDetails['auctionParameters']['procurementMethodDetails']
    )

    response = self.app.get('/{}'.format(lot['id']))
    english = response.json['data']['auctions'][0]
    half_english = response.json['data']['auctions'][1]
    insider = response.json['data']['auctions'][2]

    self.assertEqual(
        english['auctionParameters']['procurementMethodDetails'],
        auction_param_with_procurementMethodDetails['auctionParameters']['procurementMethodDetails']
    )
    self.assertEqual(
        half_english['auctionParameters']['procurementMethodDetails'],
        auction_param_with_procurementMethodDetails['auctionParameters']['procurementMethodDetails']
    )
    self.assertEqual(
        insider['auctionParameters']['procurementMethodDetails'],
        auction_param_with_procurementMethodDetails['auctionParameters']['procurementMethodDetails']
    )


@unittest.skipIf(SANDBOX_MODE, 'If sandbox mode is disabled auctionParameters has not procurementMethodDetails field')
def procurementMethodDetails_check_without_sandbox(self):

    # Test procurementMethodDetails after creating lot
    data = deepcopy(self.initial_data)
    response = self.app.get('/{}'.format(self.resource_id))
    lot = response.json['data']
    english = response.json['data']['auctions'][0]
    half_english = response.json['data']['auctions'][1]
    insider = response.json['data']['auctions'][2]

    self.assertNotIn(
        'procurementMethodDetails',
        response.json['data']['auctions'][0]['auctionParameters'],
    )
    self.assertNotIn(
        'procurementMethodDetails',
        response.json['data']['auctions'][1]['auctionParameters'],
    )
    self.assertNotIn(
        'procurementMethodDetails',
        response.json['data']['auctions'][2]['auctionParameters'],
    )


    auction_param_with_procurementMethodDetails = {
        'auctionParameters': {'procurementMethodDetails': 'quick'}
    }

    # Test procurementMethodDetails error while updating english
    response = self.app.patch_json(
        '/{}/auctions/{}'.format(lot['id'], english['id']),
        {"data": auction_param_with_procurementMethodDetails},
        headers=self.access_header,
        status=422
    )
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['description']['procurementMethodDetails'], u'Rogue field')

    # Test procurementMethodDetails error while updating english
    response = self.app.patch_json(
        '/{}/auctions/{}'.format(lot['id'], half_english['id']),
        {"data": auction_param_with_procurementMethodDetails},
        headers=self.access_header,
        status=422
    )
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['description']['procurementMethodDetails'], u'Rogue field')

    # Test procurementMethodDetails error while updating english
    response = self.app.patch_json(
        '/{}/auctions/{}'.format(lot['id'], insider['id']),
        {"data": auction_param_with_procurementMethodDetails},
        headers=self.access_header,
        status=422
    )
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['description']['procurementMethodDetails'], u'Rogue field')
