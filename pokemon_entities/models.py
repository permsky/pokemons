from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=30)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
