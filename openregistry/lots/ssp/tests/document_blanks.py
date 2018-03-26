# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import datetime, timedelta

from openregistry.api.constants import TZ

def patch_resource_document(self):
    response = self.app.post_json('/{}/documents'.format(self.resource_id),
                                  headers=self.access_header,
                                  params={'data': self.initial_document_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    #dateModified = response.json["data"]['dateModified']
    self.assertIn(doc_id, response.headers['Location'])
    self.assertEqual(u'укр.doc', response.json["data"]["title"])
    self.assertNotIn("documentType", response.json["data"])

    response = self.app.patch_json('/{}/documents/{}'.format(self.resource_id, doc_id),
        headers=self.access_header, params={
            'data': {
                'documentOf': 'wrong_document_of',
                'relatedItem': '0' * 32
            }}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u"Value must be one of ['lot', 'item']."], u'location': u'body', u'name': u'documentOf'}
    ])

    response = self.app.patch_json('/{}/documents/{}'.format(self.resource_id, doc_id),
        headers=self.access_header, params={
            "data": {
                "description": "document description",
                "documentType": 'tenderNotice'
            }}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u"Value must be one of {}.".format(str(self.document_types))], u'location': u'body', u'name': u'documentType'}
    ])
    response = self.app.patch_json('/{}/documents/{}'.format(self.resource_id, doc_id),
        headers=self.access_header, params={
            "data": {
                "description": "document description"
            }})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    self.assertNotIn("documentType", response.json["data"])

    response = self.app.get('/{}/documents/{}'.format(self.resource_id, doc_id),
                            headers=self.access_header)
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    self.assertEqual('document description', response.json["data"]["description"])
    #self.assertTrue(dateModified < response.json["data"]["dateModified"])

    self.set_status(self.forbidden_document_modification_actions_status)

    response = self.app.patch_json('/{}/documents/{}'.format(self.resource_id, doc_id),
        headers=self.access_header, params={
            "data": {
                "description": "document description"
            }}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"],
                     "Can't update document in current ({}) {} status".format(self.forbidden_document_modification_actions_status, self.resource_name[:-1]))


def model_validation(self):
    initial_document_data = deepcopy(self.initial_document_data)
    initial_document_data['documentType'] = 'x_dgfAssetFamiliarization'
    response = self.app.post_json('/{}/documents'.format(self.resource_id),
                                  headers=self.access_header,
                                  params={'data': initial_document_data},
                                  status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'][0]['description'][0], u"accessDetails is required, when documentType is x_dgfAssetFamiliarization")

    initial_document_data['accessDetails'] = u'Some access details'
    response = self.app.post_json('/{}/documents'.format(self.resource_id),
                                  headers=self.access_header,
                                  params={'data': initial_document_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['accessDetails'], initial_document_data['accessDetails'])


    initial_document_data['documentType'] = 'procurementPlan'
    del initial_document_data['accessDetails']
    response = self.app.post_json('/{}/documents'.format(self.resource_id),
                                  headers=self.access_header,
                                  params={'data': initial_document_data},
                                  status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'][0]['description'][0], u"dateSigned is required, when documentType is procurementPlan or projectPlan")

    initial_document_data['documentType'] = 'projectPlan'
    response = self.app.post_json('/{}/documents'.format(self.resource_id),
                                  headers=self.access_header,
                                  params={'data': initial_document_data},
                                  status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'][0]['description'][0], u"dateSigned is required, when documentType is procurementPlan or projectPlan")

    initial_document_data['dateSigned'] = TZ.localize(datetime.now() + timedelta(10)).isoformat()
    response = self.app.post_json('/{}/documents'.format(self.resource_id),
                                  headers=self.access_header,
                                  params={'data': initial_document_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['dateSigned'], initial_document_data['dateSigned'])

    response = self.app.post_json('/{}/documents'.format(self.resource_id),
                                  headers=self.access_header,
                                  params={'data': initial_document_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['dateSigned'], initial_document_data['dateSigned'])
