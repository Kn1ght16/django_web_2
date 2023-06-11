from django import forms
from django.forms import formset_factory
from .models import Version, Product, Category


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['version_number', 'version_name', 'is_current_version']


VersionFormSet = formset_factory(VersionForm, extra=1)


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')

        if name is not None and description is not None:
            prohibited_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
            for word in prohibited_words:
                if word.lower() in name.lower() or word.lower() in description.lower():
                    raise forms.ValidationError(
                        f"Запрещенное слово '{word}' не может быть использовано в названии или описании продукта.")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.category = self.cleaned_data['category']  # Сохраняем выбранную категорию
        if commit:
            instance.save()
        return instance
