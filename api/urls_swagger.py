from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Movie Review API",
        default_version='v1',
        description="API documentation for the Movie Review and Recommendation API",
        terms_of_service="#",
        contact=openapi.Contact(email="rajverma.developer@gmail.com"),
        license=openapi.License(name="License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)