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
        if not pokemon.image:
            pokemons_on_page.append(
                {
                    'pokemon_id': pokemon.id,
                    'img_url': DEFAULT_IMAGE_URL,
                    'title_ru': pokemon.title_ru,
                }
            )
            continue
        pokemons_on_page.append(
            {
                'pokemon_id': pokemon.id,
                'img_url': request.build_absolute_uri(pokemon.image.url),
                'title_ru': pokemon.title_ru,
            }
        )
            

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    try:
        previous_evolution = pokemon.get_previous_evolution()
        previous_evolution = {
            'title_ru': previous_evolution.title_ru,
            'pokemon_id': previous_evolution.id,
            'img_url': request.build_absolute_uri(
                previous_evolution.image.url
            )
        }
    except Pokemon.DoesNotExist:
        previous_evolution = None
    next_evolution = pokemon.evolution_form
    if next_evolution:
        next_evolution = {
            'title_ru': next_evolution.title_ru,
            'pokemon_id': next_evolution.id,
            'img_url': request.build_absolute_uri(next_evolution.image.url)
        }
    if pokemon.image:
        pokemon = {
            'title_ru': pokemon.title_ru,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
            'img_url': pokemon.image.url,
            'description': pokemon.description,
            'previous_evolution': previous_evolution,
            'next_evolution': next_evolution
        }
    else:
        pokemon = {
            'title_ru': pokemon.title_ru,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
            'img_url': DEFAULT_IMAGE_URL,
            'description': pokemon.description,
            'previous_evolution': previous_evolution,
            'next_evolution': next_evolution
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
            request.build_absolute_uri(pokemon['img_url'])
        )

    return render(
        request,
        'pokemon.html',
        context={
            'map': folium_map._repr_html_(),
            'pokemon': pokemon
        }
    )
