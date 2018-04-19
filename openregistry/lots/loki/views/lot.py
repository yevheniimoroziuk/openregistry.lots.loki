# -*- coding: utf-8 -*-
from openregistry.lots.core.utils import (
    json_view,
    context_unpack,
    APIResource
)
from openregistry.lots.core.validation import (
    validate_change_status,
)

from openregistry.lots.core.utils import (
    oplotsresource, apply_patch
)

from openregistry.lots.core.validation import (
    validate_patch_lot_data,
    validate_lot_data,
    validate_post_lot_role,

)
from openregistry.lots.loki.validation import validate_decision_post, validate_decision_patch, validate_deleted_status

patch_lot_validators = (
    validate_patch_lot_data,
    validate_change_status,
    validate_decision_patch,
    validate_deleted_status

)
post_lot_validators = (
    validate_lot_data,
    validate_post_lot_role,
    validate_decision_post
)


@oplotsresource(name='loki:Lot',
                path='/lots/{lot_id}',
                lotType='loki',
                description="Open Contracting compatible data exchange format.")
class LotResource(APIResource):


    @json_view(permission='view_lot')
    def get(self):
        lot_data = self.context.serialize(self.context.status)
        return {'data': lot_data}

    @json_view(content_type="application/json", permission='create_lot', validators=post_lot_validators)
    def post(self):
        return super(LotResource, self).post()

    @json_view(content_type="application/json", validators=patch_lot_validators,
               permission='edit_lot')
    def patch(self):
        lot = self.context
        apply_patch(self.request, src=self.request.validated['lot_src'])
        self.LOGGER.info(
            'Updated lot {}'.format(lot.id),
            extra=context_unpack(self.request, {'MESSAGE_ID': 'lot_patch'})
        )
        return {'data': lot.serialize(lot.status)}
