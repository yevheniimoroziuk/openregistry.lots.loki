# -*- coding: utf-8 -*-
from schematics.types import StringType
from zope.interface import implementer

from openregistry.lots.core.models import ILot, Lot as BaseLot


class IBasicLot(ILot):
    """ Marker interface for basic lotss """


@implementer(IBasicLot)
class Lot(BaseLot):
    lotType = StringType(default="basic")
