from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django import forms
from . models import Profile, Review
from django.core.validators import MaxValueValidator, MinValueValidator

class UserInfoForm(forms.ModelForm):
	GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
	gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDER_CHOICES)
	birthdate = forms.DateField(required=False)
	LANGUAGE_CHOICES = (('E', 'English'), ('A', 'Arabic'), ('K', 'Korean'), ('G', 'German'))
	language = forms.ChoiceField(widget=forms.RadioSelect, choices=LANGUAGE_CHOICES)

	class Meta:
		model = Profile
		fields = ('gender', 'birthdate', 'language')

class UserReviewForm(forms.ModelForm):
	rating = forms.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)])
	fullreview = forms.CharField()
	class Meta:
		model = Review
		fields = ['rating', 'fullreview']


class ChangePasswordForm(SetPasswordForm):
	class Meta:
		model = User
		fields = ['new_password1', 'new_password2']
	
	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)
		
		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['new_password1'].label = ''
		self.fields['new_password1'].help_text = None
		
		self.fields['new_password2'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['new_password2'].label = ''
		self.fields['new_password2'].help_text = None

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(required=True)
	
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

	def __init__(self, *args, **kwargs):
		super(UserRegisterForm, self).__init__(*args, **kwargs)
		
		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = ' User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = None
		
		self.fields['email'].widget.attrs['class'] = 'form-control'
		self.fields['email'].widget.attrs['placeholder'] = ' Email'
		self.fields['email'].label = ''
		self.fields['email'].help_text = None

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = ' Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = None
		
		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = ' Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = None


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField(required=False)

	class Meta:
		model = User
		fields = ['email', 'first_name', 'last_name']

	def __init__(self, *args, **kwargs):
		super(UserUpdateForm, self).__init__(*args, **kwargs)

		self.fields['username'].required = False
		self.fields['email'].required = False
		self.fields['first_name'].required = False
		self.fields['last_name'].required = False


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['gender', 'birthdate', 'language']

	def __init__(self, *args, **kwargs):
		super(ProfileUpdateForm, self).__init__(*args, **kwargs)

		self.fields['gender'].required = False
		self.fields['birthdate'].required = False
		self.fields['language'].required = False

'''
class ProfileSkillForm(forms.ModelForm):
	class Meta:
		model = Profile_Skill
		fields = ['skills']

	def __init__(self, *args, **kwargs):
		super(ProfileSkillForm, self).__init__(*args, **kwargs)

		self.fields['skills'].required = True
'''