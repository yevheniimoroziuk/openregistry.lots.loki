# -*- coding: utf-8 -*-
from uuid import uuid4

from pyramid.security import Allow

from schematics.transforms import blacklist
from schematics.types import StringType, BaseType, IntType, MD5Type
from schematics.types.compound import ModelType, ListType
from schematics.exceptions import ValidationError
from zope.interface import implementer

from openregistry.lots.core.models import ILot, Lot as BaseLot
from openprocurement.api.registry_models.schematics_extender import Model, IsoDateTimeType
from openprocurement.api.registry_models.ocds import (
    Identifier,
    Document as BaseDocument,
    Address,
    ContactPoint,
    Item as BaseItem,
    BaseUnit,
    Organization
)
from openprocurement.api.models import (
    Guarantee,
    Period,
    Value
)
from openprocurement.api.utils import get_now
from openprocurement.api.registry_models.roles import schematics_embedded_role
from openregistry.lots.ssp.constants import LOT_STATUSES, DOCUMENT_TYPES


create_role = (blacklist('owner_token', 'owner', '_attachments', 'revisions',
                         'date', 'dateModified', 'lotID', 'documents', 'publications'
                         'status', 'doc_id', 'items', 'publications') + schematics_embedded_role)
edit_role = (blacklist('owner_token', 'owner', '_attachments',
                       'revisions', 'date', 'dateModified', 'documents', 'publications'
                       'lotID', 'mode', 'doc_id', 'items', 'publications') + schematics_embedded_role)


class ISSPLot(ILot):
    """ Marker interface for basic lots """


class Document(BaseDocument):
    documentOf = StringType(choices=['lot', 'item'])
    documentType = StringType(choices=DOCUMENT_TYPES)
    dateSigned = IsoDateTimeType()
    index = IntType(required=False)
    accessDetails = StringType()

    def validate_accessDetails(self, data, value):
        if value is None and data['documentType'] == 'x_dgfAssetFamiliarization':
            raise ValidationError(u"accessDetails is required, when documentType is x_dgfAssetFamiliarization")

    def validate_dateSigned(self, data, value):
        if value is None and data['documentType'] in ['procurementPlan', 'projectPlan']:
            raise ValidationError(u"dateSigned is required, when documentType is procurementPlan or projectPlan")



class Item(BaseItem):
    unit = ModelType(BaseUnit)


class LotCustodian(Organization):
    name = StringType()
    identifier = ModelType(Identifier, serialize_when_none=False)
    additionalIdentifiers = ListType(ModelType(Identifier))
    address = ModelType(Address, serialize_when_none=False)
    contactPoint = ModelType(ContactPoint, serialize_when_none=False)
    kind = StringType(choices=['general', 'special', 'other'])


class LotHolder(Model):
    name = StringType(required=True)
    name_ru = StringType()
    name_en = StringType()
    identifier = ModelType(Identifier)
    additionalIdentifiers = ListType(ModelType(Identifier), default=list())
    address = ModelType(Address)
    contactPoint = ModelType(ContactPoint)


class Period(Period):
    startDate = startDate = IsoDateTimeType(required=True)


class AccountDetails(Model):
    description = StringType()
    bankName = StringType()
    accountNumber = StringType()
    UA_EDR = StringType()
    MFO = StringType()


class Auction(Model):
    id = StringType()
    auctionID = StringType()
    procurementMethodType = StringType(choices=['SSP.english', 'SSP.insider'])
    auctionPeriod = ModelType(Period, required=True)
    tenderingDuration = IsoDateTimeType(required=True)
    documents = ListType(ModelType(Document))
    value = ModelType(Value, required=True)
    minimalStep = ModelType(Value, required=True)
    guarantee = ModelType(Guarantee, required=True)
    registrationFee = ModelType(Guarantee)
    accountDetails = ModelType(AccountDetails)


class Publication(Model):
    id = StringType(required=True, min_length=1, default=lambda: uuid4().hex)
    date = IsoDateTimeType()
    dateModified = IsoDateTimeType(default=get_now)
    documents = ListType(ModelType(Document), min_size=1)
    auctions = ListType(ModelType(Auction), max_size=3)


@implementer(ISSPLot)
class Lot(BaseLot):
    class Options:
        roles = {
            'create': create_role,
            'edit': edit_role,
            'edit_draft': edit_role,
            'edit_pending': edit_role,

        }

    status = StringType(choices=LOT_STATUSES,
                        default='draft')
    lotType = StringType(default="ssp")
    lotCustodian = ModelType(LotCustodian, serialize_when_none=False)
    lotHolder = ModelType(LotHolder, serialize_when_none=False)
    officialRegistrationID = StringType(serialize_when_none=True)
    items = ModelType(Item)
    publications = ListType(ModelType(Publication), default=list())
    documents = ListType(ModelType(Document), default=list())

    def validate_status(self, data, value):
        is_procurement_plan = any([bool(doc.documentType == 'procurementPlan') for doc in data.get('documents', [])])
        if value == 'editing' and is_procurement_plan:
            raise ValidationError(u"Lot must have a document with type procurementPlan to be moved to editing")

    def __acl__(self):
        acl = [
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_lot'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_lot_documents'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_lot_item'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_lot_publication'),
        ]
        return acl
