from django import forms


# Create your forms here.

class ContactUsForm(forms.Form):
    name =  forms.CharField(max_length = 100, widget = forms.TextInput(attrs={'placeholder':'100 characters max.'}))
    phone = forms.RegexField(required = False, regex= "^[6-9]\d{9}$", widget = forms.TextInput(attrs={'placeholder':'Max 10 digits'}))
    subject = forms.CharField(max_length = 100, widget = forms.TextInput(attrs={'placeholder':'Enter Subject.'}), required = False)
    email = forms.EmailField(required = False, widget = forms.EmailInput(attrs={'placeholder':'Enter your email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'If you have any message for us, please type it here' }), required = False)

    # Only email or phone_number must be entered.
    def clean(self):
        cleaned_data = super().clean()
        if not (cleaned_data.get('email') or cleaned_data.get('phone_number')):
            raise forms.ValidationError("Please enter either Email or Phone Number Correctly", code="invalid")

    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     if ("edyoda" not in data) and (data != ''):
    #         raise forms.ValidationError("Invalid domain", code="invalid")
    #     return data 


from django.forms import ModelForm 
from care_all.models import Reviews

class WriteReviewForm(ModelForm):
    class Meta:
        model = Reviews
        fields = ['review_subject', 'review_message', 'review_rating']
        
    # name =  forms.CharField(max_length = 50, widget = forms.TextInput(attrs={'placeholder':'Your Name'}))
    # subject = forms.CharField(max_length = 100, widget = forms.TextInput(attrs={'placeholder':'Enter Subject.'}))
    # review = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Your Review' }))