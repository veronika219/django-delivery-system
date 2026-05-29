from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):

    phone = forms.CharField(
        required=True,
        error_messages={
            "required": "Вкажіть номер телефону"

        }
    )

    email = forms.EmailField(
        required=True,
        error_messages={
            "required": "Вкажіть email для отримання квитанції",
            "invalid": "Введіть коректний email"
        }
    )

    class Meta:
        model = Order

        fields = [
            "name",
            "phone",
            "email",
            "address",
            "comment",
            "delivery_type",
            "payment_method",
        ]

        widgets = {

            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ваше ім’я"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+380 XX XXX XX XX",
                "inputmode": "tel",
                "autocomplete": "tel"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control email-input",
                "placeholder": "example@gmail.com"
            }),

            "address": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Адреса доставки"
            }),

            "comment": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Коментар до замовлення"
            }),

            "delivery_type": forms.Select(attrs={
                "class": "form-select"
            }),

            "payment_method": forms.Select(attrs={
                "class": "form-select"
            }),
        }

    def clean_phone(self):

        phone = self.cleaned_data["phone"]

        digits = "".join(filter(str.isdigit, phone))

        # 0671234567
        if digits.startswith("0") and len(digits) == 10:
            digits = "38" + digits

        # 671234567
        elif len(digits) == 9:
            digits = "380" + digits

        # 380671234567
        elif digits.startswith("380") and len(digits) == 12:
            pass

        else:
            raise forms.ValidationError(
                "Введіть коректний номер телефону"
            )

        return f"+{digits}"

    def clean(self):

        data = super().clean()

        if (
            data.get("delivery_type") == "DELIVERY"
            and not data.get("address")
        ):
            self.add_error(
                "address",
                "Вкажіть адресу доставки"
            )

        return data
