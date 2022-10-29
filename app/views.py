from django.shortcuts import render, redirect

from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import login

from .models import Tip, User, UserTipped, JoinUs
from .forms import DashboardEditForm, RegistrationForm, JoinUsApplicationForm, EditProfileForm


# Create your views here.

class CustomLoginView(LoginView):
	"""
	Login Page
	"""
	template_name = "login.html"
	fields = "__all__"
	redirect_authenticated_user = True

	def get_success_url(self):
		return reverse_lazy("user-dashboard")


class RegisterPage(generic.FormView):
	"""
	Create account page
	"""
	template_name = "register.html"
	form_class = RegistrationForm
	redirect_authenticated_user = True
	success_url = reverse_lazy("user-dashboard")

	def form_valid(self, form):
		user = form.save()
		if user is not None:
			login(self.request, user)

		return super(RegisterPage, self).form_valid(form)

	def get(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect("user-dashboard")
		return super(RegisterPage, self).get(*args, **kwargs)


class UserEditView(LoginRequiredMixin, generic.UpdateView):
	model = User
	form_class = EditProfileForm
	template_name = "edit-profile.html"
	success_url = reverse_lazy("user-dashboard")

	def get_object(self):
		return self.request.user


class LandingPage(generic.TemplateView):
	template_name = "home.html"


class JoinUsView(generic.FormView):
	model = JoinUs
	form_class = JoinUsApplicationForm
	template_name = "join-us.html"
	success_url = reverse_lazy("landing-page")

	def form_valid(self, form):
		model_instance = JoinUs(first_name = form.cleaned_data["first_name"],
			last_name = form.cleaned_data["last_name"],
			email = form.cleaned_data["email"])
		model_instance.save()
		model_instance.betting_accounts.add(*form.cleaned_data["betting_accounts"])
		return super().form_valid(form)


class UserDashboard(LoginRequiredMixin, generic.ListView):
	"""
	Displays a table of the tips that have been given to the user 
	"""
	model = Tip
	template_name = "user-dashboard.html"
	context_object_name = "user_tips"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["user_tips"] = self.model.objects.filter(user=self.request.user)
		context["user_tips_unsubmitted"] = self.model.objects.filter(Q(user=self.request.user) & Q(usertipped__user_entered_detail=False))
		context["user_tips_submitted"] = self.model.objects.filter(Q(user=self.request.user) & Q(usertipped__user_entered_detail=True))

		return context


class UserDashboardInput(LoginRequiredMixin, generic.UpdateView):
	"""
	Displays single tip instance from the UserTipped model allowing user to input information
	"""
	model = UserTipped
	form_class = DashboardEditForm
	template_name = "user-dashboard-input.html"
	success_url = reverse_lazy("user-dashboard")

	def get_object(self):
		user = self.request.user
		tip_id = self.kwargs.get("tip_id")
		return self.model.objects.filter(Q(user=user) & Q(tip__id=tip_id))[0]

	def form_valid(self, form):
		self.object.user_entered_detail = True
		return super().form_valid(form)




