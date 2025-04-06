from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # Add Tailwind CSS classes to each field
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': (
                    'w-full '
                    'px-3 sm:px-4 md:px-6 '  # Padding adjusts on larger screens
                    'py-2 '
                    'mt-2 sm:mt-3 '  # Margin top slightly increases on larger screens
                    'border border-gray-300 '
                    'rounded-md '
                    'focus:outline-none '
                    'focus:ring-2 focus:ring-blue-500'
                ),
                'placeholder': f'Enter your {field.label.lower()}'
            })
