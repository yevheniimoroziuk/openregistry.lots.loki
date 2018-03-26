def create_item_resource(self):
    response = self.app.post_json('/{}/items'.format(self.resource_id),
                                  headers=self.access_header,
                                  params={'data': self.initial_item_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    item_id = response.json["data"]['id']
    #dateModified = response.json["data"]['dateModified']
    self.assertIn(item_id, response.headers['Location'])
    self.assertEqual(self.initial_item_data['data']['description'], response.json["data"]["description"])
    self.assertEqual(self.initial_item_data['data']['quantity'], response.json["data"]["quantity"])
    self.assertEqual(self.initial_item_data['data']['address'], response.json["data"]["address"])
    self.assertEqual(self.initial_item_data['data']['location'], response.json["data"]["location"])




def patch_item(self):
    pass


def create_item_resource_invalid(self):
    pass


def patch_item_resource_invalid(self):
    pass


def list_item_resource(self):
    pass
