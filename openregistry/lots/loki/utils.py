# -*- coding: utf-8 -*-
from pkg_resources import get_distribution
from logging import getLogger

from openregistry.lots.core.utils import get_now, context_unpack


PKG = get_distribution(__package__)
LOGGER = getLogger(PKG.project_name)


def check_status(request):
    lot = request.validated['lot']
    now = get_now()
    check_lot_status(request, lot, now)


def check_lot_status(request, lot, now=None):
    if not now:
        now = get_now()
    if lot.status == 'pending' and lot.next_check <= now:
        LOGGER.info('Switched lot {} to {}'.format(lot.id, 'active.salable'),
                    extra=context_unpack(request, {'MESSAGE_ID': 'switched_lot_active.salable'}))
        lot.status = 'active.salable'
