# -*- coding: utf-8 -*-
import logging

from pyramid.interfaces import IRequest

from openregistry.lots.core.interfaces import IContentConfigurator, ILotManager
from .models import Lot, ILokiLot
from .adapters import LokiLotConfigurator, LokiLotManagerAdapter

LOGGER = logging.getLogger(__name__)


def includeme(config, plugin_config=None):
    config.scan("openregistry.lots.loki.views")
    config.scan("openregistry.lots.loki.subscribers")
    configurator = (LokiLotConfigurator, (ILokiLot, IRequest), IContentConfigurator)
    manager = (LokiLotManagerAdapter, (ILokiLot,), ILotManager)
    for adapter in (configurator, manager):
        config.registry.registerAdapter(*adapter)

    lot_types = plugin_config.get('aliases', [])
    if plugin_config.get('use_default', False):
        lot_types.append('loki')
    for lt in lot_types:
        config.add_lotType(Lot, lt)

    LOGGER.info("Included openregistry.lots.loki plugin", extra={'MESSAGE_ID': 'included_plugin'})
