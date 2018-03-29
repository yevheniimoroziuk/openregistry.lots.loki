# -*- coding: utf-8 -*-

def not_found_publication_document(self):
    response = self.app.post_json('/{}/publications'.format(self.resource_id),
                                  headers=self.access_header,
                                  params={'data': self.initial_publication_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    publication_id = response.json["data"]['id']


    response = self.app.post_json(
        '/some_id/publications/some_id/documents', status=404,
        params={'data': self.initial_document_data}
    )
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'lot_id'}
    ])

    response = self.app.post_json(
        '/{}/publications/some_id/documents'.format(self.resource_id),
        status=404,
        params={'data': self.initial_document_data}
    )
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'publication_id'}
    ])

    response = self.app.get('/some_id/publications/some_id/documents', status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'lot_id'}
    ])

    response = self.app.get('/{}/publications/some_id/documents'.format(self.resource_id), status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'publication_id'}
    ])

    response = self.app.get('/some_id/publications/some_id/documents/some_id', status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'lot_id'}
    ])

    response = self.app.get('/{}/publications/some_id/documents/some_id'.format(self.resource_id), status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'publication_id'}
    ])

    response = self.app.get('/{}/publications/{}/documents/some_id'.format(self.resource_id, publication_id), status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'document_id'}
    ])


    response = self.app.put_json('/some_id/publications/some_id/documents/some_id', status=404,
                            upload_files=[('file', 'name.doc', 'content2')])
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'lot_id'}
    ])


    response = self.app.put_json('/{}/publications/some_id/documents/some_id'.format(self.resource_id), status=404, upload_files=[
                            ('file', 'name.doc', 'content2')])
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'publication_id'}
    ])

    response = self.app.put_json(
        '/{}/publications/{}/documents/some_id'.format(self.resource_id, publication_id),
        status=404,
        params={'data': self.initial_document_data},
    )
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location': u'url', u'name': u'document_id'}
    ])

def create_publication_document(self):
    response = self.app.post_json('/{}/publications'.format(self.resource_id),
                                  headers=self.access_header,
                                  params={'data': self.initial_publication_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    publication_id = response.json["data"]['id']

    response = self.app.post_json('/{}/publications/{}/documents'.format(
        self.resource_id, publication_id),
        params={'data': self.initial_document_data},
        content_type='application/json',
        headers=self.access_header,
    )
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    self.assertIn(doc_id, response.headers['Location'])
    self.assertEqual(self.initial_document_data['title'], response.json["data"]["title"])
    key = response.json["data"]["url"].split('?')[-1]

    response = self.app.get('/{}/publications/{}/documents'.format(self.resource_id, publication_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"][0]["id"])
    self.assertEqual(self.initial_document_data['title'], response.json["data"][0]["title"])

    response = self.app.get('/{}/publications/{}/documents?all=true'.format(self.resource_id, publication_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"][0]["id"])
    self.assertEqual(self.initial_document_data['title'], response.json["data"][0]["title"])

    response = self.app.get('/{}/publications/{}/documents/{}?download=some_id'.format(
        self.resource_id, publication_id, doc_id), status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location': u'url', u'name': u'download'}
    ])

    # response = self.app.get('/{}/publications/{}/documents/{}?{}'.format(
    #     self.resource_id, publication_id, doc_id, key))
    # self.assertEqual(response.status, '200 OK')
    # self.assertIn('http://localhost/get/', response.location)
    # self.assertIn('Signature=', response.location)
    # self.assertIn('KeyID=', response.location)
    # self.assertNotIn('Expires=', response.location)


    response = self.app.get('/{}/publications/{}/documents/{}'.format(
        self.resource_id, publication_id, doc_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    self.assertEqual(self.initial_document_data['title'], response.json["data"]["title"])


def put_publication_document(self):
    response = self.app.post_json('/{}/publications'.format(self.resource_id),
                                  headers=self.access_header,
                                  params={'data': self.initial_publication_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    publication_id = response.json["data"]['id']


    response = self.app.post_json('/{}/publications/{}/documents'.format(
        self.resource_id, publication_id),
        params={'data': self.initial_document_data},
        headers=self.access_header,
    )
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    self.assertIn(doc_id, response.headers['Location'])


    response = self.app.put_json(
        '/{}/publications/{}/documents/{}'.format(self.resource_id, publication_id, doc_id),
        params={'data': self.initial_document_data},
        headers=self.access_header
    )
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    key = response.json["data"]["url"].split('?')[-1]

    # response = self.app.get('/{}/publications/{}/documents/{}?{}'.format(
    #     self.resource_id, publication_id, doc_id, key))
    # self.assertEqual(response.status, '200 OK')
    # self.assertEqual(response.content_type, 'application/msword')
    # self.assertEqual(response.content_length, 8)
    # self.assertEqual(response.body, 'content2')

    response = self.app.get('/{}/publications/{}/documents/{}'.format(
        self.resource_id, publication_id, doc_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    self.assertEqual(self.initial_document_data['title'], response.json["data"]["title"])

    # response = self.app.put_json('/{}/publications/{}/documents/{}'.format(
    #     self.resource_id, publication_id, doc_id),
    #     'content3',
    #     headers=self.access_header,
    #     content_type='application/msword'
    # )
    # self.assertEqual(response.status, '200 OK')
    # self.assertEqual(response.content_type, 'application/json')
    # self.assertEqual(doc_id, response.json["data"]["id"])
    # key = response.json["data"]["url"].split('?')[-1]
    #
    # response = self.app.get('/{}/publications/{}/documents/{}?{}'.format(
    #     self.resource_id, publication_id, doc_id, key))
    # self.assertEqual(response.status, '200 OK')
    # self.assertEqual(response.content_type, 'application/msword')
    # self.assertEqual(response.content_length, 8)
    # self.assertEqual(response.body, 'content3')


def patch_publication_document(self):
    response = self.app.post_json('/{}/publications'.format(self.resource_id),
                                  headers=self.access_header,
                                  params={'data': self.initial_publication_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    publication_id = response.json["data"]['id']


    response = self.app.post_json('/{}/publications/{}/documents'.format(
        self.resource_id, publication_id),
        headers=self.access_header,
        params={'data': self.initial_document_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    self.assertIn(doc_id, response.headers['Location'])

    response = self.app.patch_json('/{}/publications/{}/documents/{}'.format(
        self.resource_id, publication_id, doc_id),
        {"data": {"description": "document description"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Forbidden")

    response = self.app.patch_json(
        '/{}/publications/{}/documents/{}'.format(self.resource_id, publication_id, doc_id),
        {"data": {"description": "document description"}},
        headers=self.access_header
    )
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])

    response = self.app.get('/{}/publications/{}/documents/{}'.format(
        self.resource_id, publication_id, doc_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    self.assertEqual('document description', response.json["data"]["description"])


