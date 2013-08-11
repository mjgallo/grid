from django import forms

class InvitationKeyForm(forms.Form):
    email = forms.EmailField()
    grid = forms.IntegerField(required=False)