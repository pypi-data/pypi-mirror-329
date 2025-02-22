from django.urls import path, include
from ..endpoints.tenant import TenantListEndpoint

urlpatterns = [
    path('tenants/', TenantListEndpoint.as_view()),
    path('user/', include('saas_base.api_urls.user')),
    path('tenant/', include('saas_base.api_urls.tenant')),
    path('members/', include('saas_base.api_urls.members')),
]
