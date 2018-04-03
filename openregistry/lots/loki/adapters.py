# -*- coding: utf-8 -*-
from openregistry.lots.core.adapters import LotConfigurator
from .constants import STATUS_CHANGES


class BasicLotConfigurator(LotConfigurator):
    """ Loki Tender configuration adapter """

    name = "Loki Lot configurator"
    available_statuses = STATUS_CHANGES
