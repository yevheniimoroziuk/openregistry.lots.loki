# -*- coding: utf-8 -*-
from pyramid.events import subscriber
from openregistry.lots.loki.events import PublicationInitializeEvent, ItemInitializeEvent
from openprocurement.api.utils import get_now


@subscriber(PublicationInitializeEvent, lotType="loki")
def publication_init_handler(event):
    """ initialization handler for publications of lots """
    event.publication.date = get_now()


@subscriber(ItemInitializeEvent, lotType="loki")
def item_init_handler(event):
    """ initialization handler for publications of lots """
    event.item.date = get_now()
