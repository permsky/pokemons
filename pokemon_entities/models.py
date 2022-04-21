from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=30)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title
