from django.db import models


class Language(models.Model):
    language_data = models.TextField(verbose_name="content of language file in base64")
    dt_created = models.DateTimeField(verbose_name="datetime of language file upload", auto_now_add=True)
