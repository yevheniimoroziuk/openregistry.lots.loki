# -*- coding: utf-8 -*-

from schematics.transforms import blacklist
from openprocurement.api.registry_models.roles import schematics_default_role


item_create_role = blacklist('id')
item_edit_role = blacklist('id')
item_view_role = (schematics_default_role)

publication_create_role = blacklist('id', 'date', 'dateModified', 'documents')
publication_edit_role = blacklist('id', 'date', 'dateModified', 'documents')
publication_view_role = (schematics_default_role)

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
