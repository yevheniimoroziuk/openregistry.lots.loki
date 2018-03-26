# -*- coding: utf-8 -*-
from pyramid.events import subscriber
from openregistry.lots.ssp.events import PublicationInitializeEvent, ItemInitializeEvent
from openregistry.api.utils import get_now


@subscriber(PublicationInitializeEvent, lotType="ssp")
def publication_init_handler(event):
    """ initialization handler for publications of lots """
    event.publication.date = get_now()


@subscriber(ItemInitializeEvent, lotType="ssp")
def item_init_handler(event):
    """ initialization handler for publications of lots """
    event.item.date = get_now()
