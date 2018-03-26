# -*- coding: utf-8 -*-
from openregistry.lots.core.adapters import LotConfigurator
from openregistry.lots.ssp.constants import STATUS_CHANGES


class BasicLotConfigurator(LotConfigurator):
    """ SSP Tender configuration adapter """

    name = "SSP Lot configurator"
    available_statuses = STATUS_CHANGES
