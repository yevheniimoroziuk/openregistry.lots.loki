# -*- coding: utf-8 -*-
from uuid import uuid4

from openprocurement.api.models.auction_models.models import (
    Value
)
from openprocurement.api.models.models import (
    Guarantee,
    Period
)
from openprocurement.api.models.registry_models.roles import schematics_embedded_role
from openprocurement.api.models.registry_models.ocds import (
    Identifier as BaseIdentifier,
    Document as BaseDocument,
    Address,
    ContactPoint,
    Item as BaseItem,
    BaseUnit,
    Organization,
    ItemClassification,
    Classification
)
from openprocurement.api.models.schematics_extender import (
    Model,
    IsoDateTimeType,
    IsoDurationType,
    DecimalType
)
from openprocurement.api.constants import IDENTIFIER_CODES
from openregistry.lots.core.models import ILot, Lot as BaseLot
from openregistry.lots.loki.constants import LOT_STATUSES, DOCUMENT_TYPES
from openregistry.lots.loki.roles import (
    item_roles,
    publication_roles
)
from pyramid.security import Allow
from schematics.exceptions import ValidationError
from schematics.transforms import blacklist
from schematics.types import StringType, IntType, URLType
from schematics.types.compound import ModelType, ListType
from zope.interface import implementer

create_role = (blacklist('owner_token', 'owner', '_attachments', 'revisions',
                         'date', 'dateModified', 'lotID', 'documents', 'publications'
                         'status', 'doc_id', 'items', 'publications') + schematics_embedded_role)
edit_role = (blacklist('owner_token', 'owner', '_attachments',
                       'revisions', 'date', 'dateModified', 'documents', 'publications'
                       'lotID', 'mode', 'doc_id', 'items', 'publications') + schematics_embedded_role)


class ILokiLot(ILot):
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


class RegistrationDetails(Model):
    status = StringType(choices=['unknown', 'proceed', 'complete'], required=True)
    registrationID = StringType()
    registrationDate = IsoDateTimeType()

    def validate_registrationID(self, data, value):
        if value and data['status'] != 'complete':
            raise ValidationError(u"You can fill registrationID only when status is complete")

    def validate_registrationDate(self, data, value):
        if value and data['status'] != 'complete':
            raise ValidationError(u"You can fill registrationDate only when status is complete")


class Item(BaseItem):
    class Options:
        roles = item_roles

    unit = ModelType(BaseUnit, required=True)
    quantity = DecimalType(precision=-4, required=True)
    address = ModelType(Address, required=True)
    classification = ModelType(ItemClassification, required=True)
    registrationDetails = ModelType(RegistrationDetails, required=True)


class Identifier(BaseIdentifier):
    scheme = StringType(choices=IDENTIFIER_CODES)
    legalName = StringType(required=True)
    uri = URLType(required=True)


class LotCustodian(Organization):
    name = StringType()
    identifier = ModelType(Identifier, serialize_when_none=False)
    additionalIdentifiers = ListType(ModelType(Identifier), default=list())
    address = ModelType(Address, serialize_when_none=False)
    contactPoint = ModelType(ContactPoint, serialize_when_none=False)
    kind = StringType(choices=['general', 'special', 'other'])


class LotHolder(Model):
    name = StringType(required=True)
    name_ru = StringType()
    name_en = StringType()
    identifier = ModelType(Identifier, required=True)
    additionalIdentifiers = ListType(ModelType(Identifier), default=list())
    address = ModelType(Address)
    contactPoint = ModelType(ContactPoint)


class StartDateRequiredPeriod(Period):
    startDate = IsoDateTimeType(required=True)


class AccountDetails(Model):
    description = StringType()
    bankName = StringType()
    accountNumber = StringType()
    additionalClassifications = ListType(ModelType(Classification), default=list())

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


class DecisionDetails(Model):
    title = StringType()
    decisionDate = IsoDateTimeType(required=True)
    decisionID = StringType(required=True)


class Publication(Model):
    class Options:
        roles = publication_roles

    id = StringType(required=True, min_length=1, default=lambda: uuid4().hex)
    documents = ListType(ModelType(Document), default=list())
    auctions = ListType(ModelType(Auction), max_size=3, min_size=3)
    decisionDetails = ModelType(DecisionDetails, required=True)

    def validate_auctions(self, data, value):
        pass


@implementer(ILokiLot)
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
    description = StringType(required=True)
    lotType = StringType(default="loki")
    lotCustodian = ModelType(LotCustodian, serialize_when_none=False)
    lotHolder = ModelType(LotHolder, serialize_when_none=False)
    officialRegistrationID = StringType(serialize_when_none=True)
    items = ListType(ModelType(Item), default=list())
    publications = ListType(ModelType(Publication), default=list())
    documents = ListType(ModelType(Document), default=list())
    decisionDetails = ModelType(DecisionDetails, required=True)

    def __acl__(self):
        acl = [
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_lot'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_lot_documents'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_lot_items'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_lot_publications'),
        ]
        return acl
