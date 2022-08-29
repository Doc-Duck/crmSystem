from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(label='Login', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg mb-2 shadow', 'placeholder': 'Enter your crm'}))
    passwd = forms.CharField(label='Password', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg mb-2 shadow', 'placeholder': 'Password', "type": "password"}))


class RegistrationForm(forms.Form):
    login = forms.CharField(label='Login', max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg mb-2 shadow', 'placeholder': 'Enter your crm'}))
    passwd = forms.CharField(label='Password', max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg mb-2 shadow', 'placeholder': 'Password', "type": "password"}))
    passwd_repeat = forms.CharField(label='Password', max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg mb-2 shadow', 'placeholder': 'Confirm assword', "type": "password"}))
    first_name = forms.CharField(label='Password', max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg mb-2 shadow', 'placeholder': 'Enter your name'}))
    last_name = forms.CharField(label='Password', max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg mb-2 shadow', 'placeholder': 'Enter your lastname'}))