# -*- coding: utf-8 -*-
from openregistry.lots.core.adapters import (
    LotConfigurator,
    LotManagerAdapter
)
from openregistry.lots.core.validation import (
    validate_post_lot_role,

)
from openregistry.lots.core.utils import (
    get_now,
    calculate_business_date
)
from .constants import (
    STATUS_CHANGES,
    RECTIFICATION_PERIOD_DURATION,
    ITEM_EDITING_STATUSES,
    DEFAULT_DUTCH_STEPS
)
from .validation import (
    validate_decision_post,
    validate_verification_status,
)


class LokiLotConfigurator(LotConfigurator):
    """ Loki Tender configuration adapter """

    name = "Loki Lot configurator"
    available_statuses = STATUS_CHANGES
    item_editing_allowed_statuses = ITEM_EDITING_STATUSES


class LokiLotManagerAdapter(LotManagerAdapter):
    name = 'Loki Lot Manager'
    create_validation = (
        validate_post_lot_role,
        validate_decision_post,
    )
    change_validation = (
        validate_verification_status,
    )

    def _set_rectificationPeriod(self, request):
        rectificationPeriod = type(request.context).rectificationPeriod.model_class()
        rectificationPeriod.startDate = get_now()
        rectificationPeriod.endDate = calculate_business_date(rectificationPeriod.startDate,
                                                                   RECTIFICATION_PERIOD_DURATION)
        request.context.rectificationPeriod = rectificationPeriod

    def _create_auctions(self, request):
        lot = request.validated['lot']
        lot.date = get_now()
        auction_types = ['sellout.english', 'sellout.english', 'sellout.insider']
        auction_class = lot.__class__.auctions.model_class
        auctionParameters_class = lot.__class__.auctions.model_class.auctionParameters.model_class
        for tenderAttempts, auction_type in enumerate(auction_types, 1):
            auction = auction_class()
            auction.procurementMethodType = auction_type
            auction.tenderAttempts = tenderAttempts
            auction.auctionParameters = auctionParameters_class()
            if auction_type == 'sellout.english':
                auction.auctionParameters.type = 'english'
            if auction_type == 'sellout.insider':
                auction.auctionParameters.type = 'insider'
                auction.auctionParameters.dutchSteps = DEFAULT_DUTCH_STEPS
            lot.auctions.append(auction)

    def create_lot(self, request):
        self._validate(request, self.create_validation)
        self._create_auctions(request)

    def change_lot(self, request):
        self._validate(request, self.change_validation)
        if request.validated['data'].get('status') == 'pending' and not request.context.rectificationPeriod:
            self._set_rectificationPeriod(request)