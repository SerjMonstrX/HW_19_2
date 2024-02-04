from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']

    def clean_name(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        name = self.cleaned_data.get('name', '').lower()
        for word in forbidden_words:
            if word in name:
                raise ValidationError(f"Недопустимое слово в названии продукта: {word}")
        return name

    def clean_description(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        description = self.cleaned_data.get('description', '').lower()
        for word in forbidden_words:
            if word in description:
                raise ValidationError(f"Недопустимое слово в описании продукта: {word}")
        return description