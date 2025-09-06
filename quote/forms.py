from django import forms
from .models import Quote


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'source', 'weight']
        validate_unique = False
        labels = {
            'text': 'Текст цитаты',
            'source': 'Источник',
            'weight': 'Вес',
        }
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Введите текст цитаты'}),
            'source': forms.TextInput(attrs={'placeholder': 'Введите источник'}),
            'weight': forms.NumberInput(attrs={'placeholder': 'Введите вес'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        source = cleaned_data.get('source')
        weight = cleaned_data.get('weight')

        errors = []

        if text:
            if not (2 <= len(text) <= 70):
                errors.append("Длина цитаты должна быть от 2 до 70 символов.")
            qs = Quote.objects.filter(text__iexact=text)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                errors.append("Цитата с таким текстом уже существует.")

        # Проверка длины источника
        if source:
            if not (2 <= len(source) <= 50):
                errors.append("Длина источника должна быть от 2 до 50 символов.")
            qs_source = Quote.objects.filter(source__iexact=source)
            if self.instance.pk:
                qs_source = qs_source.exclude(pk=self.instance.pk)
            if qs_source.count() >= 3:
                errors.append(f"У источника '{source}' уже есть 3 цитаты.")

        if weight is not None:
            if not (1 <= weight <= 100):
                errors.append("Вес должен быть числом от 1 до 100.")

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data
