from django.urls import path
from . import views
from core.views import PagSeguroDonateView

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('about/', views.about, name="about"),
    path('donate/', views.donate, name="donate"),
    path('donate/pagseguro', PagSeguroDonateView.as_view(), name="pagseguro_donate_view"),
    path('donate/done', views.done_payment, name="done_payment"),
    path('notificacoes/pagseguro', views.pagseguro_notification, name="pagseguro_notification")
]