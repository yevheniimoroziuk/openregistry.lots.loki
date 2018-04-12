# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openregistry.lots.core.tests.base import snitch

from openregistry.lots.loki.tests.base import (
    LotContentWebTest
)
from openregistry.lots.loki.tests.json_data import test_loki_publication_data
from openregistry.lots.loki.tests.blanks.publication_blanks import (
    create_publication,
    patch_publication
)

class LotPublicationResourceTest(LotContentWebTest):
    initial_publication_data = deepcopy(test_loki_publication_data)
    test_create_publication_resource = snitch(create_publication)
    test_patch_publication_resource = snitch(patch_publication)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LotPublicationResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
