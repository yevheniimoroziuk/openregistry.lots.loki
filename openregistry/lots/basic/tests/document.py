# -*- coding: utf-8 -*-
import unittest

from openregistry.api.tests.blanks.mixins import ResourceDocumentTestMixin
from openregistry.lots.basic.tests.base import (
    LotContentWebTest
)


class LotDocumentWithDSResourceTest(LotContentWebTest, ResourceDocumentTestMixin):
    docservice = True

    # status, in which operations with lot documents (adding, updating) are forbidden
    forbidden_document_modification_actions_status = 'active.salable'


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LotDocumentWithDSResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
