from django.urls import path
from . import views 
from django.contrib.auth.views import LogoutView

urlpatterns = [
	path("login/", views.CustomLoginView.as_view(), name="login"),
	path("logout/", LogoutView.as_view(next_page="landing-page"), name="logout"),
	path("register/", views.RegisterPage.as_view(), name="register"),
	path("edit-profile/", views.UserEditView.as_view(), name="edit-profile"),

	path("join-us/", views.JoinUsView.as_view(), name="join-us"),

	path("", views.LandingPage.as_view(), name="landing-page"),
	path("dashboard/", views.UserDashboard.as_view(), name="user-dashboard"),
	path("dashboard/<int:tip_id>/", views.UserDashboardInput.as_view(), name="user-dashboard-input"),
]