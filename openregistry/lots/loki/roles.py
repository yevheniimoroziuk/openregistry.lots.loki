# -*- coding: utf-8 -*-

from schematics.transforms import blacklist, whitelist
from openregistry.lots.core.models import (
    plain_role,
    listing_role
)
from openregistry.lots.core.models import (
    schematics_default_role,
    schematics_embedded_role
)


item_create_role = blacklist('id')
item_edit_role = blacklist('id')
item_view_role = (schematics_default_role + blacklist())

publication_create_role = blacklist('id', 'date', 'dateModified', 'documents')
publication_edit_role = blacklist('id', 'date', 'dateModified', 'documents')
publication_view_role = (schematics_default_role + blacklist())

item_roles = {
    'create': item_create_role,
    'edit': item_edit_role,
    'view': item_view_role,
}

publication_roles = {
    'create': publication_create_role,
    'edit': publication_edit_role,
    'view': publication_view_role,
}


# lot_create_role = (blacklist('owner_token', 'owner', '_attachments', 'revisions',
#                          'date', 'dateModified', 'lotID', 'documents', 'publications'
#                          'status', 'doc_id', 'items') + schematics_embedded_role)
lot_create_role = (whitelist('status', 'auctions', 'assets', 'decisions', 'lotType', 'lotIdentifier', 'mode'))
lot_edit_role = (blacklist('owner_token', 'owner', '_attachments',
                       'revisions', 'date', 'dateModified', 'documents', 'decisions',
                       'lotID', 'mode', 'doc_id', 'items', 'rectificationPeriod') + schematics_embedded_role)
view_role = (blacklist('owner_token',
                       '_attachments', 'revisions') + schematics_embedded_role)

Administrator_role = whitelist('status', 'mode')
concierge_role = (blacklist(
    'owner_token', 'owner', '_attachments', 'revisions', 'date', 'dateModified',
    'lotID', 'mode', 'doc_id') + schematics_embedded_role)

lot_roles = {
    'create': lot_create_role,
    'plain': plain_role,
    'edit': lot_edit_role,
    'view': view_role,
    'listing': listing_role,
    'default': schematics_default_role,
    'Administrator': Administrator_role,
    # Draft role
    'draft': view_role,
    'edit_draft': whitelist('status'),
    # Composing role
    'composing': view_role,
    'edit_composing': whitelist(),
    # Pending role
    'pending': view_role,
    'edit_pending': lot_edit_role,
    'edit_pendingAfterRectificationPeriod': whitelist('status'),
    # Deleted role
    'deleted': view_role,
    'edit_deleted': whitelist(),
    # Active.salable role
    'active.salable': view_role,
    'edit_active.salable': whitelist(),
    # pending.dissolution role
    'pending.dissolution': view_role,
    'edit_pending.dissolution': whitelist(),
    # Dissolved role
    'dissolved': view_role,
    'edit_dissolved': whitelist(),
    # Active.awaiting role
    'active.awaiting': view_role,
    'edit_active.awaiting': whitelist(),
    # Active.auction role
    'active.auction': view_role,
    'edit_active.auction': whitelist(),
    # Active.contracting role
    'active.contracting': view_role,
    'edit_active.contracting': whitelist(),
    # pending.sold role
    'pending.sold': view_role,
    'edit.pending.sold': whitelist(),
    # Sold role
    'sold': view_role,
    'edit.sold': whitelist(),
    'invalid': view_role,
    'edit.invalid': whitelist(),
    'concierge': whitelist('status', 'decisions', 'title_ru'),
    'convoy': whitelist('status', 'auctions')
}
