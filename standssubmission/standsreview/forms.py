from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    next_url = forms.CharField(widget=forms.HiddenInput, required=False)


class ReviewForm(forms.Form):
    comments = forms.CharField(label='Comments', widget=forms.Textarea, required=False)
    score = forms.CharField(label='Score', widget=forms.NumberInput, empty_value=0)
