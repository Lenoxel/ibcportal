from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from api.views import MyTokenObtainPairView, PostViewSet, MemberViewSet, BirthdayCelebrationViewSet, UnionCelebrationViewSet, VideoViewSet, ScheduleViewSet, GroupViewSet, EventViewSet, device, CongregationViewSet

from rest_framework import routers

from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
)

# Routers provide an easy way of automatically determining the URL conf.
api_router = routers.DefaultRouter()
api_router.register(r'posts', PostViewSet)
api_router.register(r'members', MemberViewSet, basename='Member')
api_router.register(r'birthdays', BirthdayCelebrationViewSet)
api_router.register(r'unions', UnionCelebrationViewSet)
api_router.register(r'videos', VideoViewSet)
api_router.register(r'meetings', ScheduleViewSet)
api_router.register(r'groups', GroupViewSet)
api_router.register(r'congregations', CongregationViewSet)
api_router.register(r'events', EventViewSet)

# url abaixa está depreciada, apenas mantendo-a por enquanto para não quebrar a chamada da última versão de teste do app
api_router.register(r'celebrations', BirthdayCelebrationViewSet)

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('grupos/', include('groups.urls')),
    # path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/', MyTokenObtainPairView.as_view(), name='my_token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/', token_request, name='token'),
    # path('api/token/all/', create_auth_token, name='token_all'),
    # path('api/login/', CustomAuthToken.as_view()),
    path('api/', include(api_router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('devices/', device),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
