# -*- coding: utf-8 -*-
import unittest
import mock

from datetime import timedelta

from schematics.exceptions import ModelValidationError

from openregistry.lots.core.utils import get_now

from openregistry.lots.loki.models import (
    StartDateRequiredPeriod,
    AccountDetails,
    Auction,
)

now = get_now()


class DummyModelsTest(unittest.TestCase):

    def test_StartDateRequiredPeriod(self):
        period = StartDateRequiredPeriod()

        self.assertEqual(period.serialize(), None)
        with self.assertRaisesRegexp(ValueError, 'Period Model has no role "test"'):
            period.serialize('test')
        with self.assertRaisesRegexp(ModelValidationError, u'This field is required.'):
            period.validate()
        data = {'startDate': now.isoformat()}
        period.import_data(data)
        period.validate()
        self.assertEqual(period.serialize(), data)
        data['endDate'] = now.isoformat()
        period.import_data(data)
        period.validate()
        self.assertEqual(period.serialize(), data)
        period.startDate += timedelta(3)
        with self.assertRaises(ModelValidationError) as ex:
            period.validate()
        self.assertEqual(ex.exception.messages,
                         {"startDate": ["period should begin before its end"]})

    def test_AccountDetails(self):
        data = {
            'name': 'Name'
        }

        account_details = AccountDetails()
        self.assertEqual(account_details.serialize(), None)
        with self.assertRaisesRegexp(ValueError, 'AccountDetails Model has no role "test"'):
            account_details.serialize('test')

        account_details.import_data(data)
        account_details.validate()

    def test_Auction(self):
        data = {
            "procurementMethodType": "sellout.english",
            "auctionPeriod": {
                "startDate": now.isoformat(),
                "endDate": (now + timedelta(days=5)).isoformat()
            },
            "tenderingDuration": 'P4DT5H',
            "guarantee": {
                "amount": 30.54,
                "currency": "UAH"
            },
            "minimalStep": {
                "amount": 60.54,
                "currency": "UAH"
            },
            "value": {
                "amount": 1500.54,
                "currency": "UAH"
            },
        }
        auction = Auction()
        auction.import_data(data)
        auction.validate()

        data['auctionParameters'] = {'dutchSteps': -3}
        auction.import_data(data)
        with self.assertRaises(ModelValidationError) as ex:
            auction.validate()
        self.assertEqual(
            ex.exception.messages,
            {'auctionParameters':
                 {'dutchSteps': [u'Int value should be greater than 1.']}
            }
        )

        data['auctionParameters'] = {'dutchSteps': 132}
        auction.import_data(data)
        with self.assertRaises(ModelValidationError) as ex:
            auction.validate()
        self.assertEqual(
            ex.exception.messages,
            {'auctionParameters':
                 {'dutchSteps': [u'Int value should be less than 100.']}
            }
        )

        auction = Auction()
        data['auctionParameters'] = {'dutchSteps': 55}
        data['procurementMethodType'] = 'sellout.insider'
        auction.import_data(data)
        auction.validate()
        self.assertEqual(auction.auctionParameters.dutchSteps, data['auctionParameters']['dutchSteps'])


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(DummyModelsTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')


