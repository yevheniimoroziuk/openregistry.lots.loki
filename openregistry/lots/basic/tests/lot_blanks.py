# -*- coding: utf-8 -*-
from copy import deepcopy
from uuid import uuid4

from openregistry.api.utils import get_now
from openregistry.api.constants import ROUTE_PREFIX

from openregistry.lots.basic.models import Lot


# LotTest

def simple_add_lot(self):
    u = Lot(self.initial_data)
    u.lotID = "UA-X"
    u.assets = [uuid4().hex]

    assert u.id is None
    assert u.rev is None

    u.store(self.db)

    assert u.id is not None
    assert u.rev is not None

    fromdb = self.db.get(u.id)

    assert u.lotID == fromdb['lotID']
    assert u.doc_type == "Lot"

    u.delete_instance(self.db)


def check_patch_status_successful(self, path, lot_status, headers=None):
    response = self.app.patch_json(path,
                                   headers=headers,
                                   params={'data': {'status': lot_status}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], lot_status)


def check_patch_status_forbidden(self, path, lot_status, headers=None):

    # Check if response.status is forbidden, when you try to change status to incorrect
    # 'data' should be {'data': {'status': allowed_status}}
    response = self.app.patch_json(path,
                                   params={'data': {'status': lot_status}},
                                   headers=headers,
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')


def create_single_lot(self, data):
    response = self.app.post_json('/', {"data": data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'draft')
    return response


def check_lot_assets(self):

    # lot with a single assets
    self.initial_data["assets"] = [uuid4().hex]
    lot = create_single_lot(self, self.initial_data).json['data']
    response = self.app.get('/{}'.format(lot['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(set(response.json['data']), set(lot))
    self.assertEqual(response.json['data'], lot)

    # lot with different assets
    self.initial_data["assets"] = [uuid4().hex, uuid4().hex]
    lot = create_single_lot(self, self.initial_data).json['data']
    response = self.app.get('/{}'.format(lot['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(set(response.json['data']), set(lot))
    self.assertEqual(response.json['data'], lot)

    # # lot with no assets
    self.initial_data["assets"] = []
    response = self.app.post_json('/', {"data": self.initial_data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u"Please provide at least 1 item."], u'location': u'body', u'name': u'assets'}
    ])
    # # lot with equal assets
    id_ex = uuid4().hex
    self.initial_data["assets"] = [id_ex, id_ex]
    response = self.app.post_json('/', {"data": self.initial_data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u"Assets should be unique"], u'location': u'body', u'name': u'assets'}
    ])


def change_draft_lot(self):
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    self.app.authorization = ('Basic', ('broker', ''))

    # Create lot in 'draft' status
    draft_lot = deepcopy(self.initial_data)
    draft_lot['assets'] = [uuid4().hex]
    response = create_single_lot(self, draft_lot)
    lot = response.json['data']
    token = response.json['access']['token']
    access_header = {'X-Access-Token': str(token)}
    self.assertEqual(lot.get('status', ''), 'draft')

    response = self.app.get('/{}'.format(lot['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], lot)

    # Move from 'draft' to 'draft' status
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'draft', access_header)

    # Move from 'draft' to 'pending' status
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending', access_header)

    # Create lot in draft status
    draft_lot = deepcopy(draft_lot)
    draft_lot['status'] = 'draft'
    lot = create_single_lot(self, draft_lot).json['data']

    # Move from 'draft' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution', access_header)
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold', access_header)

    self.app.authorization = ('Basic', ('concierge', ''))

    # Create lot in 'draft' status
    draft_lot = deepcopy(self.initial_data)
    draft_lot['status'] = 'draft'
    response = self.app.post_json('/', {'data': draft_lot}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')

    # Move from 'draft' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')


    self.app.authorization = ('Basic', ('convoy', ''))

    # Create lot in 'draft' status
    draft_lot = deepcopy(self.initial_data)
    draft_lot['status'] = 'draft'
    response = self.app.post_json('/', {'data': draft_lot}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')

    # Move from 'draft' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')


    self.app.authorization = ('Basic', ('administrator', ''))

    # Create lot in 'draft' status
    draft_lot = deepcopy(draft_lot)
    draft_lot['status'] = 'draft'
    response = self.app.post_json('/', {'data': draft_lot}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')

    # Move from 'draft' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')

    # Move from 'draft' to 'draft' status
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'draft')

    # Move from 'draft' to 'pending' status
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending')


def change_pending_lot(self):

    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)


    self.app.authorization = ('Basic', ('broker', ''))

    lot_info = deepcopy(self.initial_data)
    lot_info['status'] = 'draft'

    # Create lot in 'draft' status and move it to 'pending'
    response = create_single_lot(self, lot_info)
    lot = response.json['data']
    token = response.json['access']['token']
    access_header = {'X-Access-Token': str(token)}

    response = self.app.get('/{}'.format(lot['id']), headers=access_header)
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], lot)

    # Move from 'draft' to 'pending' status
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending', access_header)

    # Move from 'pending' to 'pending' status
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending', access_header)

    # Move from 'pending' to 'deleted' status
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'deleted', access_header)

    # Create lot in 'draft' status and move it to 'pending'
    response = create_single_lot(self, deepcopy(lot_info))
    token = response.json['access']['token']
    access_header = {'X-Access-Token': str(token)}
    lot = response.json['data']

    # Move from 'draft' to 'pending' status
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending', access_header)

    # Move from 'pending' to 'verification' status
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'verification', access_header)

    # Create lot in 'draft' status and move it to 'pending'
    response = create_single_lot(self, deepcopy(lot_info))
    token = response.json['access']['token']
    access_header = {'X-Access-Token': str(token)}
    lot = response.json['data']

    # Move from 'draft' to 'pending' status
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending', access_header)

    # Move from 'pending' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft', headers=access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable', headers=access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution', headers=access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'dissolved', headers=access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting', headers=access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction', headers=access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold', headers=access_header)


    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'pending' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'pending' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')


    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'pending' to 'pending' status
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending')

    # Move from 'pending' to 'verification'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'verification')

    # Move from 'verification' to 'pending'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending')

    # Move from 'pending' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')

    # Move from 'pending' to 'deleted'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'deleted')


def change_verification_lot(self):
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)


    self.app.authorization = ('Basic', ('broker', ''))

    lot_info = self.initial_data
    lot_info['status'] = 'draft'

    # Create new lot in 'draft' status
    response = create_single_lot(self, lot_info)
    lot = response.json['data']
    token = response.json['access']['token']
    access_header = {'X-Access-Token': str(token)}
    self.assertEqual(lot.get('status', ''), 'draft')

    response = self.app.get('/{}'.format(lot['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], lot)

    # Move status from 'draft' to 'pending'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending', access_header)

    # Move status from 'pending' to 'verification'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'verification', access_header)

    # Move from 'verification' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution', access_header)
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold', access_header)


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'verification' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')


    self.app.authorization = ('Basic', ('concierge', ''))

    # Move status from 'verification' to 'verification'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'verification')

    # Move from 'verification' to 'pending' status
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending')

    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'pending' to 'verification' status
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'verification')

    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'verification' to 'active.salable' status
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')

    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'pending' to 'verification' status
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'verification')

    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'verification' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')


    self.app.authorization = ('Basic', ('administrator', ''))

    # Move status from 'verification' to 'verification'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'verification')

    # Move from 'verification' to 'pending' status
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending')

    # Move from 'pending' to 'verification' status
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'verification')

    # Move from 'verification' to 'active.salable' status
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')

    # Move from 'active.salable' to 'verification' status
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'verification')

    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')


def change_deleted_lot(self):

    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)


    self.app.authorization = ('Basic', ('broker', ''))

    lot_info = self.initial_data
    lot_info['status'] = 'draft'

    # Create new lot in 'draft' status
    response = create_single_lot(self, lot_info)
    lot = response.json['data']
    token = response.json['access']['token']
    access_header = {'X-Access-Token': str(token)}
    self.assertEqual(lot.get('status', ''), 'draft')

    response = self.app.get('/{}'.format(lot['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], lot)

    # Move from 'draft' to 'pending'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending', access_header)

    # Move from 'pending' to 'deleted'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'deleted', access_header)

    # Move from 'deleted' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution', access_header)
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold', access_header)


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'deleted' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')


    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'deleted' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')

    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'deleted' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')


def change_pending_dissolution_lot(self):

    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)


    self.app.authorization = ('Basic', ('broker', ''))

    lot_info = self.initial_data
    lot_info['status'] = 'draft'

    # Create new lot in 'draft' status
    response = create_single_lot(self, lot_info)
    lot = response.json['data']
    token = response.json['access']['token']
    access_header = {'X-Access-Token': str(token)}
    self.assertEqual(lot.get('status', ''), 'draft')

    # Move status from 'draft' to 'pending'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending', access_header)

    # Move status from 'pending' to 'verification'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'verification', access_header)

    self.app.authorization = ('Basic', ('administrator', ''))

    # Move status from 'verification' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')

    self.app.authorization = ('Basic', ('broker', ''))

    # Move status from 'active.salable' to 'pending.dissolution'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending.dissolution', access_header)

    # Move from 'pending.dissolution' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution', access_header)
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold', access_header)


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'pending.dissolution' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')


    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'pending.dissolution' to 'pending.dissolution'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending.dissolution')

    # Move from 'pending.dissolution' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')

    # Move from 'active.salable' to 'pending.dissolution'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending.dissolution')

    # Move from 'pending.dissolution' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')

    # Move from 'pending.dissolution' to 'dissolved'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'dissolved')


    self.app.authorization = ('Basic', ('broker', ''))

    # Create new lot in 'draft' status
    response = create_single_lot(self, lot_info)
    lot = response.json['data']


    self.app.authorization = ('Basic', ('administrator', ''))

    # Move status from 'draft' to 'pending'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending')

    # Move status from 'pending' to 'verification'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'verification')

    # Move status from 'verification' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')

    # Move status from 'active.salable' to 'pending.dissolution'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending.dissolution')


    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'pending.dissolution' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')

    # Move from 'pending.dissolution' to 'pending.dissolution'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending.dissolution')

    # Move from 'pending.dissolution' to 'dissolved'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'dissolved')


def change_active_salable_lot(self):

    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)


    self.app.authorization = ('Basic', ('broker', ''))

    lot_info = self.initial_data
    lot_info['status'] = 'draft'

    # Create new lot in 'draft' status
    response = create_single_lot(self, lot_info)
    lot = response.json['data']
    token = response.json['access']['token']
    access_header = {'X-Access-Token': str(token)}
    self.assertEqual(lot.get('status', ''), 'draft')

    response = self.app.get('/{}'.format(lot['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], lot)

    # Move from 'draft' to 'pending'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending', access_header)

    # Move from 'pending' to 'verification'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'verification', access_header)

    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'verification' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')

    self.app.authorization = ('Basic', ('broker', ''))

    # Move from 'active.salable' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification', access_header)
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold', access_header)

    # Move from 'active.salable' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable', access_header)

    # Move from 'active.salable' to 'pending.dissolution'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending.dissolution', access_header)

    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'pending.dissolution' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')


    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'active.salable' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')


    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'active.salable' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')

    # Move from 'active.salable' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')

    # Move from 'active.salable' to 'pending.dissolution'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending.dissolution')

    # Move from 'pending.dissolution' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')

    # Move from 'active.salable' to 'verification'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'verification')

    # Move from 'verification' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')

    # Move from 'active.salable' to 'active.awaiting'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.awaiting')


    self.app.authorization = ('Basic', ('broker', ''))

    # Create new lot in 'draft' status
    response = create_single_lot(self, lot_info)
    lot = response.json['data']

    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'draft' to 'pending'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending')

    # Move from 'pending' to 'verification'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'verification')

    # Move from 'verification' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'active.salable' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')

    # Move from 'active.salable' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable', access_header)

    # Move from 'active.salable' to 'active.awaiting'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.awaiting', access_header)

    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'verification' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')


def change_active_awaiting_lot(self):
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    self.app.authorization = ('Basic', ('broker', ''))

    lot_info = self.initial_data
    lot_info['status'] = 'draft'

    # Create new lot in 'draft' status
    response = create_single_lot(self, lot_info)
    lot = response.json['data']
    token = response.json['access']['token']
    access_header = {'X-Access-Token': str(token)}
    self.assertEqual(lot.get('status', ''), 'draft')

    response = self.app.get('/{}'.format(lot['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], lot)

    # Move from 'draft' to 'pending'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending', access_header)

    # Move from 'pending' to 'verification'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'verification', access_header)

    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'verification' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')

    # Move from 'active.salable' to 'active.awaiting'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.awaiting')


    self.app.authorization = ('Basic', ('broker', ''))

    # Move from 'active.awaiting' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution', access_header)
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold', access_header)


    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'active.awaiting' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')


    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'active.awaiting' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')

    # Move from 'active.awaiting' to 'active.awaiting'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.awaiting')

    # Move from 'active.awaiting' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')

    # Move from 'active.salable' to 'active.awaiting'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.awaiting')

    # Move from 'active.awaiting' to 'active.auction'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.auction')

    # Move from 'active.auction' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')

    # Move from 'active.salable' to 'active.awaiting'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.awaiting')


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'active.awaiting' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')

    # Move from 'active.awaiting' to 'active.awaiting'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.awaiting')

    # Move from 'active.awaiting' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')

    # Move from 'active.salable' to 'active.awaiting'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.awaiting')

    # Move from 'active.awaiting' to 'active.auction'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.auction')


def change_active_auction_lot(self):
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    self.app.authorization = ('Basic', ('broker', ''))

    lot_info = self.initial_data
    lot_info['status'] = 'draft'

    # Create new lot in 'draft' status
    response = create_single_lot(self, lot_info)
    lot = response.json['data']
    token = response.json['access']['token']
    access_header = {'X-Access-Token': str(token)}
    self.assertEqual(lot.get('status', ''), 'draft')

    response = self.app.get('/{}'.format(lot['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], lot)

    # Move from 'draft' to 'pending'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending', access_header)

    # Move from 'pending' to 'verification'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'verification', access_header)

    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'verification' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')

    # Move from 'active.salable' to 'active.awaiting'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.awaiting')

    # Move from 'active.awaiting' to 'active.auction'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.auction')

    self.app.authorization = ('Basic', ('broker', ''))

    # Move from 'active.auction' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution', access_header)
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold', access_header)


    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'active.auction' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'active.auction' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')

    # Move from 'active.auction' to 'active.auction'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.auction')

    # Move from 'active.auction' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')

    # Move from 'active.salable' to 'active.awaiting'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.awaiting')

    # Move from 'active.awaiting' to 'active.auction'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.auction')

    # Move from 'active.auction' to 'sold'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'sold')

    self.app.authorization = ('Basic', ('broker', ''))

    lot_info = self.initial_data
    lot_info['status'] = 'draft'

    # Create new lot in 'draft' status
    response = create_single_lot(self, lot_info)
    lot = response.json['data']
    self.assertEqual(lot.get('status', ''), 'draft')

    response = self.app.get('/{}'.format(lot['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], lot)

    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'draft' to 'pending'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending')

    # Move from 'pending' to 'verification'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'verification')

    # Move from 'verification' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')

    # Move from 'active.salable' to 'active.awaiting'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.awaiting')

    # Move from 'active.awaiting' to 'active.auction'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.auction')

    # Move from 'active.auction' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')

    # Move from 'active.auction' to 'active.auction'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.auction')

    # Move from 'active.auction' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')

    # Move from 'active.salable' to 'active.awaiting'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.awaiting')

    # Move from 'active.awaiting' to 'active.auction'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.auction')

    # Move from 'active.auction' to 'sold'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'sold')


def change_dissolved_lot(self):

    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)


    self.app.authorization = ('Basic', ('broker', ''))

    lot_info = self.initial_data
    lot_info['status'] = 'draft'

    # Create new lot in 'draft' status
    response = create_single_lot(self, lot_info)
    lot = response.json['data']
    token = response.json['access']['token']
    access_header = {'X-Access-Token': str(token)}
    self.assertEqual(lot.get('status', ''), 'draft')

    response = self.app.get('/{}'.format(lot['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], lot)

    # Move from 'draft' to 'pending'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending', access_header)

    # Move from 'pending' to 'verification'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'verification', access_header)

    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'verification' to 'active.salable'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'active.salable')

    # Move from 'active.salable' to 'pending.dissolution'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'pending.dissolution')

    # Move from 'pending.dissolution' to 'dissolved'
    check_patch_status_successful(self, '/{}'.format(lot['id']), 'dissolved')

    self.app.authorization = ('Basic', ('broker', ''))

    # Move from 'dissolved' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution', access_header)
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction', access_header)
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold', access_header)


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'dissolved' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')


    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'dissolved' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')

    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'dissolved' to one of 'blacklist' status
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'draft')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'deleted')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'verification')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.salable')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'pending.dissolution')
    check_patch_status_forbidden(self,'/{}'.format(lot['id']), 'dissolved')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.awaiting')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'active.auction')
    check_patch_status_forbidden(self, '/{}'.format(lot['id']), 'sold')