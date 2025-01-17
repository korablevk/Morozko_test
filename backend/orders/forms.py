import re
from django import forms


class CreateOrderForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    zip_code = forms.CharField(required=False)
    requires_delivery = forms.ChoiceField(
        choices=[
            ("0", False),
            ("1", True),
        ],
    )
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(
        choices=[
            ("0", 'False'),
            ("1", 'True'),
        ],
    )

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        pattern = re.compile(r'^\+7\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}$')

        # Check if the phone number matches the expected format
        if not pattern.match(data):
            raise forms.ValidationError(
                "Неверный формат номера. Используйте формат: +7 999 999 99 99 или +7 9999999999"
            )

        # Optionally normalize the phone number (remove spaces)
        normalized_number = re.sub(r'\s+', '', data)
        return normalized_number
