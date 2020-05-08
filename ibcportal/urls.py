"""ibcportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.views import PostViewSet, MemberViewSet, BirthdayCelebrationViewSet, UnionCelebrationViewSet, VideoViewSet, ScheduleViewSet, GroupViewSet, EventViewSet, token_request
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'members', MemberViewSet)
router.register(r'birthdays', BirthdayCelebrationViewSet)
router.register(r'unions', UnionCelebrationViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'meetings', ScheduleViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'events', EventViewSet)

# url abaixa está depreciada, apenas mantendo-a por enquanto para não quebrar a chamada da última versão de teste do app
router.register(r'celebrations', BirthdayCelebrationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('grupos/', include('groups.urls')),
    path('token/', token_request, name='token'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
