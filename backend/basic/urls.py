# myapi/urls.py
from django.urls import include, path
from . import views
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register(r'test', views.TestViewSet, basename="test")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('basic/', include(router.urls)),
]
