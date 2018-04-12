# -*- coding: utf-8 -*-
from openregistry.lots.core.utils import (
    get_file,
    update_file_content_type,
    json_view,
    context_unpack,
    APIResource,
)
from openregistry.lots.core.utils import (
    save_lot, oplotsresource, apply_patch,
)
from openregistry.lots.loki.validation import validate_publication_data

@oplotsresource(name='loki:Lot Publications',
                collection_path='/lots/{lot_id}/publications',
                path='/lots/{lot_id}/publications/{publication_id}',
                lotType='loki',
                description="Lot related publications")
class LotPublicationsResource(APIResource):

    @json_view(permission='view_lot')
    def collection_get(self):
        """Lot Publications List"""
        if self.request.params.get('all', ''):
            collection_data = [i.serialize("view") for i in self.context.publications]
        else:
            collection_data = sorted(dict([
                (i.id, i.serialize("view"))
                for i in self.context.publications
            ]).values(), key=lambda i: i['dateModified'])
        return {'data': collection_data}

    @json_view(content_type="application/json", permission='upload_lot_publications', validators=(validate_publication_data, ))
    def collection_post(self):
        """Lot Publications Upload"""
        publication = self.request.validated['publication']
        self.context.publications.append(publication)
        if save_lot(self.request):
            self.LOGGER.info('Created lot publication {}'.format(publication.id),
                        extra=context_unpack(self.request, {'MESSAGE_ID': 'lot_publication_create'}, {'puublication_id': publication.id}))
            self.request.response.status = 201
            publication_route = self.request.matched_route.name.replace("collection_", "")
            self.request.response.headers['Location'] = self.request.current_route_url(_route_name=publication_route, publication_id=publication.id, _query={})
            return {'data': publication.serialize("view")}

    @json_view(permission='view_lot')
    def get(self):
        """Lot Publication Read"""
        publication = self.request.validated['publication']
        publication_data = publication.serialize("view")
        return {'data': publication_data}

    @json_view(content_type="application/json", permission='upload_lot_publications', validators=(validate_publication_data, ))
    def patch(self):
        """Lot Publications Update"""
        if apply_patch(self.request, src=self.request.context.serialize()):
            update_file_content_type(self.request)
            self.LOGGER.info('Updated lot publication {}'.format(self.request.context.id),
                        extra=context_unpack(self.request, {'MESSAGE_ID': 'lot_publication_patch'}))
            return {'data': self.request.context.serialize("view")}
