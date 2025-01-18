from django.urls import path

from core.views import DonateViewPagseguro

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("posts/", views.posts, name="posts"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path(
        "donate/pagseguro", DonateViewPagseguro.as_view(), name="pagseguro_donate_view"
    ),
    path("donate/paypal", views.donateViewPayPal, name="paypal_donate_view"),
    path("donate/done", views.done_payment, name="done_payment"),
    path(
        "notificacoes/pagseguro",
        views.pagseguro_notification,
        name="pagseguro_notification",
    ),
    path(
        "notificacoes/paypal", views.paypal_notification, name="pagseguro_notification"
    ),
]
