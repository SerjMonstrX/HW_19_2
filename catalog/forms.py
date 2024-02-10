from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product, Version


from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'user']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Извлекаем атрибут request
        super().__init__(*args, **kwargs)
        # self.fields['user'].widget = forms.HiddenInput()  # Скрываем поле user, пока добавил отображение, т.к. не работает авто привязка
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.request:
            instance.user = self.request.user  # Устанавливаем текущего пользователя в качестве автора
        if commit:
            instance.save()
        return instance

    def clean_name(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        name = self.cleaned_data.get('name', '').lower()
        for word in forbidden_words:
            if word in name:
                raise ValidationError(f"Недопустимое слово в названии продукта: {word}")
        return name

    def clean_description(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        description = self.cleaned_data.get('description', '').lower()
        for word in forbidden_words:
            if word in description:
                raise ValidationError(f"Недопустимое слово в описании продукта: {word}")
        return description


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['version_number', 'version_name', 'is_current_version']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
