# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openprocurement.api.tests.base import snitch


from openregistry.lots.loki.tests.base import (
    LotContentWebTest
)
from openregistry.lots.loki.tests.json_data import (
    test_loki_publication_data,
    test_loki_document_data
)
from openprocurement.api.models.registry_models.loki import LOKI_DOCUMENT_TYPES
from openregistry.lots.loki.tests.blanks.publication_documents_blanks import (
    not_found_publication_document,
    create_publication_document,
    patch_publication_document,
    put_publication_document
)

class LotPublicationResourceTest(LotContentWebTest):
    docservice = True
    document_types = LOKI_DOCUMENT_TYPES

    initial_publication_data = deepcopy(test_loki_publication_data)
    # initial_document_data = deepcopy(test_loki_document_data)

    test_not_found_publication_document = snitch(not_found_publication_document)
    test_create_publication_document = snitch(create_publication_document)
    test_patch_publication_document = snitch(patch_publication_document)
    test_put_publication_document = snitch(put_publication_document)

    def setUp(self):
        super(LotPublicationResourceTest, self).setUp()
        self.initial_document_data = deepcopy(test_loki_document_data)
        self.initial_document_data['url'] = self.generate_docservice_url()


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LotPublicationResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
