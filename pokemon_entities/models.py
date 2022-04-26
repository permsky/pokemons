from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField('название покемона по-русски', max_length=255)
    title_en = models.CharField(
        'название покемона по-английски',
        max_length=255,
        blank=True
    )
    title_jp = models.CharField(
        'название покемона по-японски',
        max_length=255,
        blank=True
    )
    image = models.ImageField('изображение покемона', blank=True, null=True)
    description = models.TextField(
        'описание покемона',
        default='описание покемона',
        blank=True
    )
    evolution_form = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='в кого эволюционирует'
    )

    def __str__(self):
        return self.title_ru
    
    def get_previous_evolution(self):
        return Pokemon.objects.get(evolution_form=self.id)


class PokemonEntity(models.Model):
    latitude = models.FloatField('широта')
    longitude = models.FloatField('долгота')
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='покемон'
    )
    appeared_at = models.DateTimeField('появляется в', blank=True, null=True)
    disappeared_at = models.DateTimeField('исчезает в', blank=True, null=True)
    level = models.IntegerField('уровень', default=1)
    health = models.IntegerField('здоровье', default=0)
    strength = models.IntegerField('сила', default=0)
    defense = models.IntegerField('защита', default=0)
    endurance = models.IntegerField('выносливость', default=0)
