from .models import *

from django import forms


class GroupForm(forms.ModelForm):
    
   class Meta:
       model = User
       fields = "__all__"
       
