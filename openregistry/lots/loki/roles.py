# -*- coding: utf-8 -*-

from schematics.transforms import blacklist

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


lot_create_role = (blacklist('owner_token', 'owner', '_attachments', 'revisions',
                         'date', 'dateModified', 'lotID', 'documents', 'publications'
                         'status', 'doc_id', 'items', 'publications') + schematics_embedded_role)
lot_edit_role = (blacklist('owner_token', 'owner', '_attachments',
                       'revisions', 'date', 'dateModified', 'documents', 'publications'
                       'lotID', 'mode', 'doc_id', 'items', 'publications') + schematics_embedded_role)


lot_roles = {
    'create': lot_create_role,
    'edit': lot_edit_role,
    'edit_draft': lot_edit_role,
    'edit_pending': lot_edit_role,
}
