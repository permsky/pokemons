import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        pokemon_entities = PokemonEntity.objects.filter(id=pokemon.id)
        for pokemon_entity in pokemon_entities:
            if pokemon.image:
                add_pokemon(
                    folium_map,
                    pokemon_entity.latitude,
                    pokemon_entity.longitude,
                    request.build_absolute_uri(pokemon.image.url)
                )
            else:
                add_pokemon(
                    folium_map,
                    pokemon_entity.latitude,
                    pokemon_entity.longitude,
                )

    pokemons_on_page = []
    for pokemon in pokemons:
        if pokemon.image:
            pokemons_on_page.append(
                {
                    'pokemon_id': pokemon.id,
                    'img_url': request.build_absolute_uri(pokemon.image.url),
                    'title_ru': pokemon.title,
                }
            )
        else:
            pokemons_on_page.append(
                {
                    'pokemon_id': pokemon.id,
                    'img_url': DEFAULT_IMAGE_URL,
                    'title_ru': pokemon.title,
                }
            )

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    if pokemon.image:
        pokemon = {
            'title': pokemon.title,
            'image_url': pokemon.image.url
        }
    else:
        pokemon = {
            'title': pokemon.title,
            'image_url': DEFAULT_IMAGE_URL
        }
    pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon_id)
    if not pokemon_entities:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.latitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(pokemon['image_url'])
        )

    return render(
        request,
        'pokemon.html',
        context={
            'map': folium_map._repr_html_(),
            'pokemon': pokemon
        }
    )
