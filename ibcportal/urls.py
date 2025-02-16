from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from api.views import (
    BirthdayCelebrationViewSet,
    CongregationViewSet,
    CustomEBDTokenObtainPairView,
    CustomTokenObtainPairView,
    EBDAnalyticsPresenceClassesViewSet,
    EBDAnalyticsPresenceCountsViewSet,
    EBDAnalyticsPresenceHistoryViewSet,
    EBDAnalyticsPresenceUsersViewSet,
    EBDAnalyticsUsersInteractivityViewSet,
    EBDAnalyticsUsersPunctualityViewSet,
    EBDClassViewSet,
    EBDLabelOptionsViewSet,
    EBDLessonViewSet,
    EBDPresenceRecordLabelsViewSet,
    EBDPresenceViewSet,
    EventViewSet,
    GroupViewSet,
    MemberViewSet,
    PeopleViewSet,
    PostViewSet,
    ScheduleViewSet,
    UnionCelebrationViewSet,
    VideoViewSet,
    device,
    UpdateUserDetailsView,
)

api_router = routers.DefaultRouter()
api_router.register(r"posts", PostViewSet)
api_router.register(r"members", MemberViewSet, basename="Member")
api_router.register(r"birthdays", BirthdayCelebrationViewSet, basename="Birthdays")
api_router.register(r"unions", UnionCelebrationViewSet)
api_router.register(r"videos", VideoViewSet)
api_router.register(r"meetings", ScheduleViewSet)
api_router.register(r"groups", GroupViewSet)
api_router.register(r"congregations", CongregationViewSet)
api_router.register(r"events", EventViewSet)
api_router.register(r"ebd/classes", EBDClassViewSet, basename="EBDClass")
api_router.register(r"ebd/lessons", EBDLessonViewSet, basename="EBDLesson")
api_router.register(r"ebd/people", PeopleViewSet, basename="People")
api_router.register(r"ebd/presences", EBDPresenceViewSet, basename="EBDPresence")
api_router.register(r"ebd/labels", EBDLabelOptionsViewSet, basename="EBDLabelOptions")
api_router.register(
    r"ebd/presence-record-labels",
    EBDPresenceRecordLabelsViewSet,
    basename="EBDPresenceRecordLabels",
)
api_router.register(
    r"ebd/analytics/presences/counts",
    EBDAnalyticsPresenceCountsViewSet,
    basename="EBDAnalyticsPresenceCounts",
)
api_router.register(
    r"ebd/analytics/presences/history",
    EBDAnalyticsPresenceHistoryViewSet,
    basename="EBDAnalyticsPresenceHistory",
)
api_router.register(
    r"ebd/analytics/presences/classes",
    EBDAnalyticsPresenceClassesViewSet,
    basename="EBDAnalyticsPresenceClasses",
)
api_router.register(
    r"ebd/analytics/presences/users",
    EBDAnalyticsPresenceUsersViewSet,
    basename="EBDAnalyticsPresenceUsers",
)
api_router.register(
    r"ebd/analytics/presences/users/punctuality",
    EBDAnalyticsUsersPunctualityViewSet,
    basename="EBDAnalyticsPresenceUsersPunctuality",
)
api_router.register(
    r"ebd/analytics/presences/users/interactivity",
    EBDAnalyticsUsersInteractivityViewSet,
    basename="EBDAnalyticsPresenceUsersInteractivity",
)

# url abaixa está depreciada, apenas mantendo-a por enquanto para não
# quebrar a chamada da última versão de teste do app
api_router.register(
    r"celebrations", BirthdayCelebrationViewSet, basename="deprecated-birthdays"
)

urlpatterns = [
    path("", include("core.urls")),
    path("jet/", include("jet.urls", "jet")),
    path("admin/", admin.site.urls),
    path("groups/", include("groups.urls")),
    path("api/", include(api_router.urls)),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path(
        "api/login/", CustomTokenObtainPairView.as_view(), name="my_token_obtain_pair"
    ),
    path(
        "api/ebd/login/",
        CustomEBDTokenObtainPairView.as_view(),
        name="my_ebd_token_obtain_pair",
    ),
    path(
        "api/ebd/user/<int:user_id>/",
        UpdateUserDetailsView.as_view(),
        name="update-user-details",
    ),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("paypal/", include("paypal.standard.ipn.urls")),
    path("devices/", device),
    path("accounts/", include("django.contrib.auth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
