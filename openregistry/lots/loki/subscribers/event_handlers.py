# -*- coding: utf-8 -*-
from pyramid.events import subscriber
from openregistry.lots.core.events import LotInitializeEvent
from openprocurement.api.utils import get_now

from openregistry.lots.loki.constants import DEFAULT_DUTCH_STEPS

@subscriber(LotInitializeEvent, lotType="loki")
def tender_init_handler(event):
    """ initialization handler for basic lots """
    event.lot.date = get_now()
    event.lot.serialize()
    for auction in event.lot.auctions:
        auctionParameters_class = event.lot.__class__.auctions.model_class.auctionParameters.model_class
        auction.auctionParameters = auction.auctionParameters if auction.auctionParameters else auctionParameters_class()
        if auction.procurementMethodType == 'Loki.english':
            auction.auctionParameters.type = 'english'
        if auction.procurementMethodType == 'Loki.insider':
            auction.auctionParameters.type = 'insider'
            auction.auctionParameters.dutchSteps = DEFAULT_DUTCH_STEPS if auction.auctionParameters.dutchSteps is None else auction.auctionParameters.dutchSteps
