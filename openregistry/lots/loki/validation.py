# -*- coding: utf-8 -*-
from openprocurement.api.utils import raise_operation_error, update_logging_context
from openprocurement.api.validation import (
    validate_data
)

def validate_document_operation_in_not_allowed_lot_status(request, error_handler, **kwargs):
    status = request.validated['lot_status']
    if status != 'pending':
        raise_operation_error(request, error_handler,
                              'Can\'t update document in current ({}) lot status'.format(status))


def validate_item_data(request, error_handler, **kwargs):
    update_logging_context(request, {'item_id': '__new__'})
    context = request.context if 'items' in request.context else request.context.__parent__
    model = type(context).items.model_class
    validate_data(request, model)


def validate_publication_data(request, error_handler, **kwargs):
    update_logging_context(request, {'publication_id': '__new__'})
    context = request.context if 'publications' in request.context else request.context.__parent__
    model = type(context).publications.model_class
    validate_data(request, model)
