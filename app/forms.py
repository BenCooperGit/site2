from django import forms
from .models import UserTipped, User, JoinUs, BettingAccount
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserChangeForm


class DashboardEditForm(forms.ModelForm):
	
	class Meta:
		model = UserTipped
		fields = ("odds_bet", "stake_bet", )

		labels = {
		"odds_bet": _("Odds you bet at"),
		"stake_bet": _("Stake you bet"),
		}


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=60, help_text="Required. Add a valid email address")

	class Meta:
		model = User
		fields = ("email", "username", "password1", "password2")

class EditProfileForm(UserChangeForm):
	email = forms.EmailField(widget=forms.EmailInput(), max_length=60)
	username = forms.CharField(max_length=60)
	class Meta:
		model = User
		fields = ("email", "username", "first_name", "last_name")

class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, betting_account):
        return "    " + str(betting_account.name)


class JoinUsApplicationForm(forms.ModelForm):

	class Meta:
		model = JoinUs
		fields = ("first_name", "last_name", "email", "betting_accounts", "why_want_to_join")

		labels = {
		"first_name": _("First name"),
		"last_name": _("Surname"),
		"email": _("Email address"),
		"betting_accounts": _("Select all betting accounts that you currently have open"),
		"why_want_to_join": _("Detail why you want to join us"),
		}

		widgets ={
		"why_want_to_join": forms.Textarea(attrs={"rows":8, "placeholder": "(max 800 characters)"}),
		}

	betting_accounts = CustomMMCF(
        queryset=BettingAccount.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


