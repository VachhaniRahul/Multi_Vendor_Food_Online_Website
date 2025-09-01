from django.urls import path

from . import views

urlpatterns = [
    path("", views.my_account),
    path("registerUser/", views.register_user, name="register_user"),
    path("registerVendor/", views.register_vendor, name="register_vendor"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("myAccount/", views.my_account, name="my_account"),
    path("customerDashboard/", views.customer_dashboard, name="customer_dashboard"),
    path("vendorDashboard/", views.vendor_dashboard, name="vendor_dashboard"),
    path("activate/<uuid64>/<token>/", views.activate, name="activate"),
    path("forgotPassword/", views.forgot_password, name="forgot_password"),
    path(
        "reset_password_validate/<uuid64>/<token>/",
        views.reset_password_validate,
        name="reset_password_validate",
    ),
    path("resetPassword/", views.reset_password, name="reset_password"),
]
