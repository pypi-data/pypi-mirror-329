from django.template import loader
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from rest_framework.filters import BaseFilterBackend
from .errors import BadRequest
from ..settings import saas_settings


class TenantIdFilter(BaseFilterBackend):
    tenant_id_field = "tenant_id"
    tenant_id_header = saas_settings.TENANT_ID_HEADER

    def filter_queryset(self, request, queryset, view):
        query_field = getattr(view, 'tenant_id_field', self.tenant_id_field)

        tenant_id = getattr(request, "tenant_id", None)
        if not tenant_id:
            raise BadRequest('Missing Tenant ID')

        kwargs = {query_field: tenant_id}
        return queryset.filter(**kwargs)

    def get_schema_operation_parameters(self, view):
        if not saas_settings.TENANT_ID_HEADER:
            return []
        return [
            {
                'name': saas_settings.TENANT_ID_HEADER,
                'required': True,
                'in': 'header',
                'schema': {
                    'type': 'string',
                },
            },
        ]


class IncludeFilter(BaseFilterBackend):
    template = 'saas/include_filter.html'
    include_title = _('Include')
    include_description = _('A include term.')

    def get_select_related_fields(self, view, request):
        return getattr(view, 'include_select_related_fields', [])

    def get_prefetch_related_fields(self, view, request):
        return getattr(view, 'include_prefetch_related_fields', [])

    def get_include_terms(self, request):
        params = request.query_params.get('include', '')
        params = params.replace('\x00', '')  # strip null characters
        params = params.replace(',', ' ')
        return params.split()

    def filter_queryset(self, request, queryset, view):
        select_related_fields = self.get_select_related_fields(view, request)
        prefetch_related_fields = self.get_prefetch_related_fields(view, request)
        if not select_related_fields and not prefetch_related_fields:
            return queryset

        include_terms = self.get_include_terms(request)
        if not include_terms:
            return queryset

        if include_terms == ['all']:
            include_terms = select_related_fields + prefetch_related_fields

        for field in include_terms:
            if field in select_related_fields:
                queryset = queryset.select_related(field)
            elif field in prefetch_related_fields:
                queryset = queryset.prefetch_related(field)

        request.include_terms = include_terms
        return queryset

    def to_html(self, request, queryset, view):
        context = {
            'term': request.query_params.get('include', '')
        }
        template = loader.get_template(self.template)
        return template.render(context)

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'include',
                'required': False,
                'in': 'query',
                'description': force_str(self.include_description),
                'schema': {
                    'type': 'string',
                },
            },
        ]
