# -*- coding: utf-8 -*-
import unittest
import mock

from copy import deepcopy
from datetime import timedelta

from schematics.exceptions import ConversionError, ValidationError, ModelValidationError

from openprocurement.api.utils import get_now
from openregistry.lots.ssp.tests.json_data import (
    test_ssp_item_data
)
from openregistry.lots.ssp.models import (
    StartDateRequiredPeriod,
    Document,
    RegistrationDetails,
    Item,
    LotCustodian,
    LotHolder,
    AccountDetails,
    Auction,
    DecisionDetails,
    Publication
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

    def test_Document(self):
        data = {
            'title': u'укр.doc',
            'url': 'http://localhost/get',  # self.generate_docservice_url(),
            'hash': 'md5:' + '0' * 32,
            'format': 'application/msword',
        }

        document = Document()

        self.assertEqual(document.serialize('create'), None)
        self.assertEqual(document.serialize('edit'), None)
        with self.assertRaisesRegexp(ValueError, 'Document Model has no role "test"'):
            document.serialize('test')

        self.assertEqual(document.serialize().keys(),
                         ['url', 'dateModified', 'id', 'datePublished'])

        with self.assertRaises(ModelValidationError) as ex:
            document.validate()
        self.assertEqual(
            ex.exception.messages,
            {"url": ["This field is required."],
            "format": ["This field is required."],
            "title": ["This field is required."]}
        )

        document.import_data(data)
        document.validate()
        self.assertEqual(document.serialize('create'), data)
        self.assertEqual(document.serialize('edit'),
                         {'format': u'application/msword',
                          'title': u'\u0443\u043a\u0440.doc'})

        document.url = data['url'] = u'http://localhost/get/docs?download={}'.format(document.id)
        document.__parent__ = mock.MagicMock(**{
            '__parent__': mock.MagicMock(**{
                '__parent__': None,
                'request.registry.docservice_url': None})})
        document.validate()

        serialized_by_create = document.serialize('create')
        self.assertEqual(serialized_by_create.keys(),
                         ['url', 'format', 'hash', '__parent__', 'title'])
        serialized_by_create.pop('__parent__')
        self.assertEqual(serialized_by_create, data)

        data.update({'documentType': 'x_dgfAssetFamiliarization'})
        document.import_data(data)
        with self.assertRaises(ModelValidationError) as ex:
            document.validate()
        self.assertEqual(
            ex.exception.messages,
            {"accessDetails": [u"accessDetails is required, when documentType is x_dgfAssetFamiliarization"]}
        )

        data.update({'accessDetails': 'Details'})
        document.import_data(data)
        document.validate()
        data['accessDetails'] = None

        data.update({'documentType': 'procurementPlan'})
        document.import_data(data)
        with self.assertRaises(ModelValidationError) as ex:
            document.validate()
        self.assertEqual(
            ex.exception.messages,
            {"dateSigned": [u"dateSigned is required, when documentType is procurementPlan or projectPlan"]}
        )

        data.update({'documentType': 'projectPlan'})
        document.import_data(data)
        with self.assertRaises(ModelValidationError) as ex:
            document.validate()
        self.assertEqual(
            ex.exception.messages,
            {"dateSigned": [u"dateSigned is required, when documentType is procurementPlan or projectPlan"]}
        )

    def test_RegistrationDetails(self):
        registration_details = RegistrationDetails()

        self.assertEqual(registration_details.serialize(), None)
        with self.assertRaisesRegexp(ValueError, 'RegistrationDetails Model has no role "test"'):
            registration_details.serialize('test')

        data = {
            'status': 'unknown'
        }
        registration_details.import_data(data)
        registration_details.validate()

        data.update({
            'registrationID': 'REG-ID',
            'registrationDate': now.isoformat()
        })
        registration_details.import_data(data)

        with self.assertRaises(ModelValidationError) as ex:
            registration_details.validate()
        self.assertEqual(
            ex.exception.messages,
            {'registrationID': [u'You can fill registrationID only when status is complete'],
            'registrationDate': [u'You can fill registrationDate only when status is complete']}
        )

        data['status'] = 'proceed'
        registration_details.import_data(data)

        with self.assertRaises(ModelValidationError) as ex:
            registration_details.validate()
        self.assertEqual(
            ex.exception.messages,
            {'registrationID': [u'You can fill registrationID only when status is complete'],
            'registrationDate': [u'You can fill registrationDate only when status is complete']}
        )

        data['status'] = 'complete'
        registration_details.import_data(data)
        registration_details.validate()

    def test_Item(self):
        item = Item()

        self.assertEqual(item.serialize('create'), None)
        self.assertEqual(item.serialize('edit'), None)

        with self.assertRaises(ModelValidationError) as ex:
            item.validate()
        self.assertEqual(
            ex.exception.messages,
            {
                'registrationDetails': [u'This field is required.'],
                'description': [u'This field is required.'],
                'unit': [u'This field is required.'],
                'quantity': [u'This field is required.'],
                'classification': [u'This field is required.'],
                'address': [u'This field is required.'],
            }
        )

        ssp_item_data = deepcopy(test_ssp_item_data)
        item = Item(ssp_item_data)
        item.validate()
        self.assertEqual(item.serialize()['description'], ssp_item_data['description'])
        self.assertEqual(item.serialize()['classification'], ssp_item_data['classification'])
        self.assertEqual(item.serialize()['additionalClassifications'], ssp_item_data['additionalClassifications'])
        self.assertEqual(item.serialize()['address'], ssp_item_data['address'])
        self.assertEqual(item.serialize()['id'], ssp_item_data['id'])
        self.assertEqual(item.serialize()['unit'], ssp_item_data['unit'])
        self.assertEqual(float(item.serialize()['quantity']), ssp_item_data['quantity'])
        self.assertEqual(item.serialize()['registrationDetails'], ssp_item_data['registrationDetails'])

        with self.assertRaisesRegexp(ValueError, 'Item Model has no role "test"'):
            item.serialize('test')

        ssp_item_data['location'] = {'latitude': '123', 'longitude': '567'}
        item2 = Item(ssp_item_data)
        item2.validate()

        self.assertNotEqual(item, item2)
        item2.location = None
        self.assertEqual(item, item2)

    def test_LotCustodian(self):
        data = {
            'name': 'Name'
        }

        lot_custodian = LotCustodian()
        self.assertEqual(lot_custodian.serialize(), None)
        with self.assertRaisesRegexp(ValueError, 'LotCustodian Model has no role "test"'):
            lot_custodian.serialize('test')

        lot_custodian.import_data(data)
        lot_custodian.validate()

    def test_LotHolder(self):
        data = {
            'name': 'Name',
            'identifier': {
                'legalName_ru': "Some name"
            }
        }

        lot_holder = LotHolder()
        self.assertEqual(lot_holder.serialize(), None)
        with self.assertRaisesRegexp(ValueError, 'LotHolder Model has no role "test"'):
            lot_holder.serialize('test')

        with self.assertRaises(ModelValidationError) as ex:
            lot_holder.validate()
        self.assertEqual(
            ex.exception.messages,
            {'name': [u'This field is required.'],
            'identifier': [u'This field is required.']}
        )

        lot_holder.import_data(data)
        with self.assertRaises(ModelValidationError) as ex:
            lot_holder.validate()
        self.assertEqual(
            ex.exception.messages,
            {
                'identifier': {
                    'uri': [u'This field is required.'],
                    'legalName': [u'This field is required.'],
                    'id': [u'This field is required.']
                }
            }
        )
        data.update({
            'identifier': {
                'legalName': 'Legal Name',
                'uri': 'https://localhost/someuri',
                'id': 'justID'
            }})
        lot_holder.import_data(data)
        lot_holder.validate()

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
            "procurementMethodType": "SSP.english",
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
        with self.assertRaises(ModelValidationError) as ex:
            auction.validate()
        self.assertEqual(
            ex.exception.messages,
            {'auctionPeriod': [u'This field is required.'],
            'value': [u'This field is required.'],
            'minimalStep': [u'This field is required.'],
            'guarantee': [u'This field is required.'],
            'tenderingDuration': [u'This field is required.'],
             }
        )
        auction.import_data(data)
        auction.validate()

        data['dutchSteps'] = 69
        auction.import_data(data)
        with self.assertRaises(ModelValidationError) as ex:
            auction.validate()
        self.assertEqual(
            ex.exception.messages,
            {'dutchSteps': [u'Field dutchSteps is allowed only when procuremenentMethodType is SSP.insider']}
        )

        auction = Auction()
        del data['dutchSteps']
        data['procurementMethodType'] = 'SSP.insider'
        auction.import_data(data)
        auction.validate()
        self.assertEqual(auction.dutchSteps, 99)

        data['dutchSteps'] = -3
        auction.import_data(data)
        with self.assertRaises(ModelValidationError) as ex:
            auction.validate()
        self.assertEqual(
            ex.exception.messages,
            {'dutchSteps': [u'Int value should be greater than 1.']}
        )

        data['dutchSteps'] = 132
        auction.import_data(data)
        with self.assertRaises(ModelValidationError) as ex:
            auction.validate()
        self.assertEqual(
            ex.exception.messages,
            {'dutchSteps': [u'Int value should be less than 100.']}
        )

        auction = Auction()
        data['dutchSteps'] = 55
        data['procurementMethodType'] = 'SSP.insider'
        auction.import_data(data)
        auction.validate()
        self.assertEqual(auction.dutchSteps, data['dutchSteps'])

    def test_DecisionDetails(self):
        data = {
            'decisionDate': now.isoformat(),
            'decisionID': 'decisionID'
        }

        decision_details = DecisionDetails()
        self.assertEqual(decision_details.serialize(), None)
        with self.assertRaisesRegexp(ValueError, 'DecisionDetails Model has no role "test"'):
            decision_details.serialize('test')

        with self.assertRaises(ModelValidationError) as ex:
            decision_details.validate()
        self.assertEqual(
            ex.exception.messages,
            {'decisionDate': [u'This field is required.'],
            'decisionID': [u'This field is required.']}
        )

        decision_details.import_data(data)
        decision_details.validate()

    def test_Publication(self):
        pass

def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(DummyModelsTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')


