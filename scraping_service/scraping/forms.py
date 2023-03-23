from django import forms

from scraping.models import City, Language, Vacancy


class FindForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=False,
        to_field_name='slug',
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='City'
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        required=False,
        to_field_name='slug',
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Language'
    )


class VForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='City'
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        required=False,
        to_field_name='slug',
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Language'
    )
    url = forms.CharField(
        label='URL',
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    company = forms.CharField(
        label='Company',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Vacancy
        fields = '__all__'
