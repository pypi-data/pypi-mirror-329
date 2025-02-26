from django.db import models


class DynamicFileField(models.FileField):
    def clean(self, value, model_instance):
        cleaned_value = super().clean(value, model_instance)

        if validators := getattr(model_instance, "get_validators", None):
            assert callable(validators)
            for validator in validators():
                validator(cleaned_value)

        return cleaned_value
