# -*- coding: utf-8 -*-
from pyramid.events import subscriber
from openregistry.lots.core.events import lotInitializeEvent
from openregistry.api.utils import get_now


@subscriber(lotInitializeEvent, lotType="basic")
def tender_init_handler(event):
    """ initialization handler for basic lots """
    event.lot.date = get_now()
