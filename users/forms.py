from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class RegisterForm(UserCreationForm):

    first_name = forms.CharField(
        required=True,
        error_messages={"required": "Вкажіть ім’я"}
    )

    last_name = forms.CharField(
        required=True,
        error_messages={"required": "Вкажіть прізвище"}
    )

    email = forms.EmailField(
        required=True,
        error_messages={
            "required": "Email обов’язковий",
            "invalid": "Введіть коректний email"
        }
    )

    phone = forms.CharField(
        required=True,
        error_messages={"required": "Вкажіть номер телефону"}
    )

    password1 = forms.CharField(
        error_messages={"required": "Введіть пароль"}
    )

    password2 = forms.CharField(
        error_messages={"required": "Підтвердіть пароль"}
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "password1",
            "password2",
        ]

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        digits = "".join(filter(str.isdigit, phone))

        if digits.startswith("0") and len(digits) == 10:
            digits = "38" + digits
        elif len(digits) == 9:
            digits = "380" + digits
        elif digits.startswith("380") and len(digits) == 12:
            pass
        else:
            raise forms.ValidationError("Введіть номер у форматі +380XXXXXXXXX")

        return f"+{digits}"

class EmailLoginForm(AuthenticationForm):

    username = forms.EmailField(
        label="Email",
        error_messages={
            "required": "Введіть email"
        }
    )


class ProfileUpdateForm(forms.ModelForm):

    first_name = forms.CharField(
        required=True,
        error_messages={
            "required": "Вкажіть ім'я"
        },
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ім'я"
        })
    )
    last_name = forms.CharField(
        required=True,
        error_messages={
            "required": "Вкажіть прізвище"
        },
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Прізвище"
        })
    )
    phone = forms.CharField(
        required=True,
        error_messages={
            "required": "Вкажіть номер телефону"
        },
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "+380XXXXXXXXX"
        })
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "phone",
            "address"
        ]

        widgets = {

            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Прізвище"
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Адреса доставки"
            }),
        }

    def clean_phone(self):

        phone = self.cleaned_data["phone"]

        digits = "".join(filter(str.isdigit, phone))

        if digits.startswith("0") and len(digits) == 10:
            digits = "38" + digits

        elif len(digits) == 9:
            digits = "380" + digits

        elif digits.startswith("380") and len(digits) == 12:
            pass

        else:
            raise forms.ValidationError(
                "Введіть коректний номер телефону"
            )

        return f"+{digits}"
