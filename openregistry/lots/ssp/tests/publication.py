# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openregistry.api.tests.base import snitch
from openregistry.api.tests.blanks.mixins import ResourceDocumentTestMixin
from openregistry.api.tests.blanks.document import (
    not_found,
    create_document_in_forbidden_resource_status,
    put_resource_document_invalid,
    create_resource_document_error,
    create_resource_document_json_invalid,
    create_resource_document_json,
    put_resource_document_json
)

from openregistry.lots.ssp.tests.base import (
    LotContentWebTest
)
from openregistry.api.tests.blanks.json_data import test_ssp_document_data
from openregistry.api.constants import DOCUMENT_TYPES
from openregistry.lots.ssp.tests.document_blanks import (
    patch_resource_document
)

class LotPublicationResourceTest(LotContentWebTest):
    initial_publication_data = deepcopy(test_ssp_document_data)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LotPublicationResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
