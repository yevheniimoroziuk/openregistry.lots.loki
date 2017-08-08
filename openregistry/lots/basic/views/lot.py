# -*- coding: utf-8 -*-
from openregistry.api.utils import (
    json_view,
    context_unpack,
    APIResource
)

from openregistry.lots.core.utils import (
    save_lot, oplotsresource, apply_patch
)

from openregistry.lots.core.validation import (
    validate_patch_lot_data,
    validate_lot_status_update_in_terminated_status,
)

from openregistry.lots.basic.validation import (
    validate_change_lot_status,
)


patch_lot_validators = (
    validate_patch_lot_data,
    validate_lot_status_update_in_terminated_status,
    validate_change_lot_status,
)


@oplotsresource(name='basic:Lot',
                path='/lots/{lot_id}',
                lotType='basic',
                description="Open Contracting compatible data exchange format.")

class LotResource(APIResource):

    @json_view(permission='view_lot')
    def get(self):
        lot_data = self.context.serialize(self.context.status)
        return {'data': lot_data}

    @json_view(content_type="application/json", validators=patch_lot_validators, permission='edit_lot')
    def patch(self):
        lot = self.context
        apply_patch(self.request, src=self.request.validated['lot_src'])
        self.LOGGER.info(
            'Updated lot {}'.format(lot.id),
            extra=context_unpack(self.request, {'MESSAGE_ID': 'lot_patch'})
        )
        return {'data': lot.serialize(lot.status)}
