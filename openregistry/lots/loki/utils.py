# -*- coding: utf-8 -*-
from openregistry.lots.core.utils import get_now


def check_status(request):
    lot = request.validated['lot']
    now = get_now()
    check_lot_status(lot, now)


def check_lot_status(lot, now=None):
    if not now:
        now = get_now()
    if lot.status == 'pending' and lot.next_check <= now:
        lot.status = 'active.salable'
