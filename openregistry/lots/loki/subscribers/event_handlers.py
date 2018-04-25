# -*- coding: utf-8 -*-
from pyramid.events import subscriber
from openregistry.lots.core.events import LotInitializeEvent
from openregistry.lots.core.constants import SANDBOX_MODE
from openprocurement.api.utils import get_now

from openregistry.lots.loki.constants import DEFAULT_DUTCH_STEPS

@subscriber(LotInitializeEvent, lotType="loki")
def tender_init_handler(event):
    """ initialization handler for basic lots """
    event.lot.date = get_now()
    auction_types = ['sellout.english', 'sellout.english', 'sellout.insider']
    auction_class = event.lot.__class__.auctions.model_class
    auctionParameters_class = event.lot.__class__.auctions.model_class.auctionParameters.model_class

    for auction_type, tenderAttempts in zip(auction_types, list(range(1, len(auction_types) + 1))):
        auction = auction_class()
        auction.procurementMethodType = auction_type
        auction.tenderAttempts = tenderAttempts
        auction.auctionParameters = auctionParameters_class()
        if auction_type == 'sellout.english':
            auction.auctionParameters.type = 'english'
        if auction_type == 'sellout.insider':
            auction.auctionParameters.type = 'insider'
            auction.auctionParameters.dutchSteps = DEFAULT_DUTCH_STEPS
        event.lot.auctions.append(auction)

    # To serialize_auction
    # if SANDBOX_MODE:
    #     for auction in event.lot.auctions[1:]:
    #         auction.auctionParameters.procurementMethodDetails = event.lot.auctions[0].auctionParameters.procurementMethodDetails
