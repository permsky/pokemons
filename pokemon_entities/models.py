from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=30)
    title_en = models.CharField(max_length=30, default='title_en')
    title_jp = models.CharField(max_length=30, default='title_jp')
    image = models.ImageField(blank=True, null=True)
    description = models.TextField(default='Описание покемона')
    evolution_form = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.title_ru
    
    def get_previous_evolution(self):
        return Pokemon.objects.get(evolution_form=self.id)


class PokemonEntity(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
    level = models.IntegerField(default=1)
    health = models.IntegerField(default=0)
    strength = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    endurance = models.IntegerField(default=0)
