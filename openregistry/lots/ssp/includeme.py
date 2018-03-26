# -*- coding: utf-8 -*-
from pyramid.interfaces import IRequest
from openprocurement.api.interfaces import IContentConfigurator
from openregistry.lots.ssp.models import Lot, ISSPLot
from openregistry.lots.ssp.adapters import BasicLotConfigurator


def includeme(config):
    config.add_lotType(Lot)
    config.scan("openregistry.lots.ssp.views")
    config.scan("openregistry.lots.ssp.subscribers")
    config.registry.registerAdapter(BasicLotConfigurator,
                                    (ISSPLot, IRequest),
                                    IContentConfigurator)
