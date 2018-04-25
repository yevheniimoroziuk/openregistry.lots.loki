# -*- coding: utf-8 -*-
from openregistry.lots.core.adapters import (
    LotConfigurator,
    LotManagerAdapter
)
from openregistry.lots.core.validation import (
    validate_lot_data,
    validate_post_lot_role,

)
from openregistry.lots.core.utils import (
    get_now,
    calculate_business_date
)
from .constants import STATUS_CHANGES, RECTIFICATION_PERIOD_DURATION
from .validation import validate_decision_post


class BasicLotConfigurator(LotConfigurator):
    """ Loki Tender configuration adapter """

    name = "Loki Lot configurator"
    available_statuses = STATUS_CHANGES


class LokiLotManagerAdapter(LotManagerAdapter):
    name = 'Loki Lot Manager'
    create_validation = (
        validate_decision_post,
    )

    def _set_rectificationPeriod(self, request):
        if request.validated['data'].get('status') == 'pending' and not request.context.rectificationPeriod:
            request.context.rectificationPeriod = type(request.context).rectificationPeriod.model_class()
            request.context.rectificationPeriod.startDate = get_now()
            request.context.rectificationPeriod.endDate = calculate_business_date(request.context.rectificationPeriod.startDate,
                                                                       RECTIFICATION_PERIOD_DURATION)

    def create_lot(self, request):
        self._validate(request, self.create_validation)

    def change_lot(self, request):
        self._set_rectificationPeriod(request)