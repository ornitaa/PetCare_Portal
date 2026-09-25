from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


User = get_user_model()


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        validators=[validate_password],
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control pet-input",
                "placeholder": "Create a secure password",
                "autocomplete": "new-password",
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control pet-input",
                "placeholder": "Repeat your password",
                "autocomplete": "new-password",
            }
        ),
    )

    class Meta:
        model = User

        fields = (
            "full_name",
            "email",
            "phone",
        )

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "Your full name",
                    "autocomplete": "name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "you@example.com",
                    "autocomplete": "email",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "Phone number (optional)",
                    "autocomplete": "tel",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error(
                "password2",
                "The passwords do not match.",
            )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data["email"].strip().lower()
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control pet-input",
                "placeholder": "you@example.com",
                "autocomplete": "email",
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control pet-input password-field",
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
            }
        ),
    )

    remember_me = forms.BooleanField(
        required=False,
        label="Remember me",
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            }
        ),
    )
class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = User

        fields = (
            "full_name",
            "phone",
        )

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "Your full name",
                    "autocomplete": "name",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "Phone number (optional)",
                    "autocomplete": "tel",
                }
            ),
        }

    def clean_full_name(self):
        full_name = self.cleaned_data["full_name"].strip()

        if not full_name:
            raise forms.ValidationError(
                "Full name is required."
            )

        return full_name

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        if phone:
            phone = phone.strip()

        return phone

