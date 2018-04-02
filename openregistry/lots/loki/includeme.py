# -*- coding: utf-8 -*-
from pyramid.interfaces import IRequest
from openprocurement.api.interfaces import IContentConfigurator
from openregistry.lots.loki.models import Lot, ILokiLot
from openregistry.lots.loki.adapters import BasicLotConfigurator


def includeme(config):
    config.add_lotType(Lot)
    config.scan("openregistry.lots.loki.views")
    config.scan("openregistry.lots.loki.subscribers")
    config.registry.registerAdapter(BasicLotConfigurator,
                                    (ILokiLot, IRequest),
                                    IContentConfigurator)
