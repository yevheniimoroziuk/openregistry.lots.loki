# -*- coding: utf-8 -*-
from openregistry.lots.core.utils import get_now, context_unpack, LOGGER


def check_status(request):
    lot = request.validated['lot']
    now = get_now()
    check_lot_status(request, lot, now)


def check_lot_status(request, lot, now=None):
    if not now:
        now = get_now()
    if lot.status == 'pending' and lot.next_check <= now:
        LOGGER.info('Switched lot %s to %s', lot.id, 'active.salable',
                    extra=context_unpack(request, {'MESSAGE_ID': 'switched_lot_active.salable'}))
        lot.status = 'active.salable'


def update_auctions(lot):
    auctions = sorted(lot.auctions, key=lambda a: a.tenderAttempts)
    english = auctions[0]
    second_english = auctions[1]
    insider = auctions[2]

    auto_calculated_fields = ['value', 'minimalStep', 'registrationFee', 'guarantee']
    auto_calculated_fields = filter(
        lambda f: getattr(english, f, None), auto_calculated_fields
    )

    for auction in (second_english, insider):
        for key in auto_calculated_fields:
            object_class = getattr(lot.__class__.auctions.model_class, key)
            auction[key] = object_class(english[key].serialize())
            auction[key]['amount'] = (
                0 if key == 'minimalStep' and auction.procurementMethodType == 'sellout.insider'
                else english[key]['amount'] / 2
            )

    insider.tenderingDuration = second_english.tenderingDuration
    auctions[2] = insider
    return auctions
