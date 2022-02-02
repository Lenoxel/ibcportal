from django.urls import path
from . import views

urlpatterns = [
    path('ebd/classes/<int:class_id>/presences/', views.EBDClassPresencesView.as_view(), name="ebd_class_presences"),
    path('ebd/users/<str:user_id>/presences/', views.EBDUserPresencesView.as_view(), name="ebd_user_presences"),
    path('ebd/presences/analytics/', views.EBDPresencesAnalyticsView.as_view(), name="ebd_presences_analytics"),
]