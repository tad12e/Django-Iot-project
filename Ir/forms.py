from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm




class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model=User
        fields=['username','email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind CSS classes to form fields
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out',
            'placeholder': 'Choose a username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out',
            'placeholder': 'you@example.com'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out',
            'placeholder': 'Create a strong password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out',
            'placeholder': 'Re-enter password'
        })


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind CSS classes to form fields
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out',
            'placeholder': 'you@example.com'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out',
            'placeholder': '••••••••'
        })

class EmailVerificationForm(forms.Form):
    code=forms.CharField(
        max_length=6, 
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out code-input',
            'placeholder': '• • • • • •',
            'style': 'text-align: center; letter-spacing: 0.5rem; font-size: 1.5rem;'
        })
    )

        