# -*- coding: utf-8 -*-
from openregistry.lots.loki.tests.json_data import (
    publication_auction_english_data,
    publication_auction_english_half_data,
    publication_auction_insider_data
)
from copy import deepcopy


def create_publication(self):
    response = self.app.post_json('/{}/publications'.format(self.resource_id),
                                  headers=self.access_header,
                                  params={'data': self.initial_publication_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    publication_id = response.json["data"]['id']
    self.assertIn(publication_id, response.headers['Location'])
    self.assertEqual(
        response.json['data']['auctions'][0]['procurementMethodType'],
        'Loki.english'
    )
    self.assertEqual(
        response.json['data']['auctions'][1]['procurementMethodType'],
        'Loki.english'
    )
    self.assertEqual(
        response.json['data']['auctions'][2]['procurementMethodType'],
        'Loki.insider'
    )

    response = self.app.get('/{}/publications/{}'.format(self.resource_id, publication_id))
    self.assertEqual(
        response.json['data']['auctions'][0]['procurementMethodType'],
        'Loki.english'
    )
    self.assertEqual(
        response.json['data']['auctions'][1]['procurementMethodType'],
        'Loki.english'
    )
    self.assertEqual(
        response.json['data']['auctions'][2]['procurementMethodType'],
        'Loki.insider'
    )


def patch_publication(self):
    pub_eng = deepcopy(publication_auction_english_data)
    pub_eng_half = deepcopy(publication_auction_english_half_data)
    pub_insider = deepcopy(publication_auction_insider_data)
    response = self.app.post_json('/{}/publications'.format(self.resource_id),
                                  headers=self.access_header,
                                  params={'data': self.initial_publication_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    publication_id = response.json["data"]['id']
    self.assertIn(publication_id, response.headers['Location'])
    pub_eng['tenderingDuration'] = 'P15DT12H'
    pub_eng_half['tenderingDuration'] = 'P15DT12H'

    response = self.app.patch_json('/{}/publications/{}'.format(self.resource_id, publication_id),
        headers=self.access_header, params={
            "data": {
                "auctions": [
                    pub_eng,
                    pub_eng_half,
                    pub_insider
                ],
                "decisionDetails": self.initial_publication_data['decisionDetails']
            }})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(publication_id, response.json["data"]["id"])
    self.assertEqual(
        pub_eng['tenderingDuration'],
        response.json['data']['auctions'][0]['tenderingDuration']
    )
    self.assertEqual(
        pub_eng['tenderingDuration'],
        response.json['data']['auctions'][1]['tenderingDuration']
    )