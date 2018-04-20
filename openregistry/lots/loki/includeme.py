# -*- coding: utf-8 -*-
from pyramid.interfaces import IRequest

from openregistry.lots.core.interfaces import IContentConfigurator, ILotManager
from .models import Lot, ILokiLot
from .adapters import BasicLotConfigurator, LokiLotManagerAdapter


def includeme(config):
    config.add_lotType(Lot)
    config.scan("openregistry.lots.loki.views")
    config.scan("openregistry.lots.loki.subscribers")
    config.registry.registerAdapter(BasicLotConfigurator,
                                    (ILokiLot, IRequest),
                                    IContentConfigurator)
    config.registry.registerAdapter(LokiLotManagerAdapter,
                                    (ILokiLot,),
                                    ILotManager)