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
from .constants import STATUS_CHANGES, RECTIFICATION_PERIOD_DURATION, ITEM_EDITING_STATUSES
from .validation import validate_decision_post


class LokiLotConfigurator(LotConfigurator):
    """ Loki Tender configuration adapter """

    name = "Loki Lot configurator"
    available_statuses = STATUS_CHANGES
    item_editing_allowed_statuses = ITEM_EDITING_STATUSES


class LokiLotManagerAdapter(LotManagerAdapter):
    name = 'Loki Lot Manager'
    create_validation = (
        validate_decision_post,
    )

    def _set_rectificationPeriod(self, request):
        rectificationPeriod = type(request.context).rectificationPeriod.model_class()
        rectificationPeriod.startDate = get_now()
        rectificationPeriod.endDate = calculate_business_date(rectificationPeriod.startDate,
                                                                   RECTIFICATION_PERIOD_DURATION)
        request.context.rectificationPeriod = rectificationPeriod

    def create_lot(self, request):
        self._validate(request, self.create_validation)

    def change_lot(self, request):
        if request.validated['data'].get('status') == 'pending' and not request.context.rectificationPeriod:
            self._set_rectificationPeriod(request)