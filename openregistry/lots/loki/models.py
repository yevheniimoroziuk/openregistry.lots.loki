# -*- coding: utf-8 -*-
from uuid import uuid4

from pyramid.security import Allow
from schematics.exceptions import ValidationError
from schematics.transforms import blacklist
from schematics.types import StringType, IntType, URLType
from schematics.types.compound import ModelType, ListType
from zope.interface import implementer

from openprocurement.api.models.auction_models.models import (
    Value
)
from openprocurement.api.models.models import (
    Guarantee,
    Period
)
from openprocurement.api.models.registry_models.loki import (
    Document,
    Item,
    Decision,
    AssetCustodian,
    AssetHolder
)
from openprocurement.api.models.registry_models.ocds import (
    Classification,
)
from openprocurement.api.models.schematics_extender import (
    Model,
    IsoDateTimeType,
    IsoDurationType,
)
from openprocurement.api.constants import IDENTIFIER_CODES
from openregistry.lots.core.models import ILot, Lot as BaseLot

from .constants import LOT_STATUSES
from .roles import (
    item_roles,
    publication_roles,
    lot_roles
)


class ILokiLot(ILot):
    """ Marker interface for basic lots """


class StartDateRequiredPeriod(Period):
    startDate = IsoDateTimeType(required=True)


class UAEDRAndMFOClassification(Classification):
    scheme = StringType(choices=['UA-EDR', 'MFO'], required=True)


class AccountDetails(Model):
    description = StringType()
    bankName = StringType()
    accountNumber = StringType()
    additionalClassifications = ListType(ModelType(UAEDRAndMFOClassification), default=list())


class Auction(Model):
    id = StringType()
    auctionID = StringType()
    procurementMethodType = StringType(choices=['Loki.english', 'Loki.insider'])
    auctionPeriod = ModelType(StartDateRequiredPeriod, required=True)
    tenderingDuration = IsoDurationType(required=True)
    documents = ListType(ModelType(Document))
    value = ModelType(Value, required=True)
    minimalStep = ModelType(Value, required=True)
    guarantee = ModelType(Guarantee, required=True)
    registrationFee = ModelType(Guarantee)
    accountDetails = ModelType(AccountDetails)
    dutchSteps = IntType(default=None, min_value=1, max_value=100)

    def validate_dutchSteps(self, data, value):
        if value and data['procurementMethodType'] != 'Loki.insider':
            raise ValidationError('Field dutchSteps is allowed only when procuremenentMethodType is Loki.insider')
        if data['procurementMethodType'] == 'Loki.insider' and not value:
            data['dutchSteps'] = 99 if data.get('dutchSteps') is None else data['dutchSteps']


class Publication(Model):
    class Options:
        roles = publication_roles

    id = StringType(required=True, min_length=1, default=lambda: uuid4().hex)
    documents = ListType(ModelType(Document), default=list())
    auctions = ListType(ModelType(Auction), max_size=3, min_size=3)
    decisions = ListType(ModelType(Decision), default=list())

    def validate_auctions(self, data, value):
        if not value:
            return
        full_price = value[0].value.amount
        price_range = (round(full_price/2), full_price/2) if round(full_price/2) < full_price/2 else (full_price/2, round(full_price/2))
        if not (value[1].value.amount >= price_range[0] and value[1].value.amount <= price_range[1]):
            raise ValidationError('In second loki.english value.amount must be a half of value.amount first loki.english')
        if value[0].value.amount != value[2].value.amount:
            raise ValidationError('Loki.english and Loki.insider must have same value.amount')
        data['auctions'][0]['procurementMethodType'] = 'Loki.english'
        data['auctions'][1]['procurementMethodType'] = 'Loki.english'
        data['auctions'][2]['procurementMethodType'] = 'Loki.insider'


@implementer(ILokiLot)
class Lot(BaseLot):
    class Options:
        roles = lot_roles

    status = StringType(choices=LOT_STATUSES, default='draft')
    description = StringType(required=True)
    lotType = StringType(default="loki")
    lotCustodian = ModelType(AssetCustodian, serialize_when_none=False)
    lotHolder = ModelType(AssetHolder, serialize_when_none=False)
    officialRegistrationID = StringType(serialize_when_none=True)
    items = ListType(ModelType(Item), default=list())
    publications = ListType(ModelType(Publication), default=list())
    documents = ListType(ModelType(Document), default=list())
    decisions = ListType(ModelType(Decision, required=True), default=list())

    def __acl__(self):
        acl = [
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_lot'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_lot_documents'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_lot_items'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_lot_publications'),
        ]
        return acl
