# -*- coding: utf-8 -*-
from openregistry.lots.core.adapters import LotConfigurator
from .constants import STATUS_CHANGES
from openregistry.lots.core.adapters import LotManagerAdapter
from openregistry.lots.core.validation import (
    validate_lot_data,
    validate_post_lot_role,

)
from openregistry.lots.loki.validation import validate_decision_post


class BasicLotConfigurator(LotConfigurator):
    """ Loki Tender configuration adapter """

    name = "Loki Lot configurator"
    available_statuses = STATUS_CHANGES



class LokiLotManagerAdapter(LotManagerAdapter):
    name = 'Loki Lot Manager'
    create_validation = (
        validate_decision_post,
    )

    def create_lot(self, request):
        self._validate(request, self.create_validation)