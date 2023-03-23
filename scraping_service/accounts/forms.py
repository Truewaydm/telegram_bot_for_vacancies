from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from scraping.models import City, Language

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()
        if email and password:
            query_set = User.objects.filter(email=email)
            if not query_set.exists():
                raise forms.ValidationError('This user not found!')
            if not check_password(password, query_set[0].password):
                raise forms.ValidationError('Invalid password!')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('This user is inactive')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.CharField(label='Input email',
                            widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Input password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Enter your password again',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Passwords do not match!')
        return data['password2']


class UserUpdateForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=True,
        to_field_name='slug',
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='City'
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        required=True,
        to_field_name='slug',
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Language'
    )
    send_email = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput,
        label='Receive a mailing list?'
    )

    class Meta:
        model = User
        fields = ('city', 'language', 'send_email')


class ContactForm(forms.Form):
    city = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='City'
    )
    language = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Language'
    )
    email = forms.CharField(
        label='Input email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
