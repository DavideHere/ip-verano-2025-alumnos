# capa de servicio/lógica de negocio

from ..transport import transport
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de HP.
def getAllImages():
    # 1) Traer los datos desde transport.py
    raw_images = transport.getAllImages()
    
    json_collection = []

    # 2) Convertir cada imagen en una "card" (en este caso, los mismos datos pero estructurados)
    for obj in raw_images:
        json_collection.append({
            "name": obj.get("name", "Desconocido"),
            "alternate_names": ", ".join(obj.get("alternate_names", ["Sin nombres alternativos"])),
            "gender": obj.get("gender", "No especificado"),
            "house": obj.get("house", "Sin casa"),
            "actor": obj.get("actor", "No disponible"),
            "image": obj.get("image", "https://via.placeholder.com/150")  # Imagen por defecto si falta
        })

    return json_collection


# función que filtra según el nombre del personaje.
def filterByCharacter(name):
    filtered_cards = []

    for card in getAllImages():  # Obtener todas las imágenes
        if name.lower() in card['name'].lower():  # Verificar si el nombre buscado está en el nombre del personaje
            filtered_cards.append(card)

    return filtered_cards  # Eliminé la parte duplicada

# función que filtra las cards según su casa.
def filterByHouse(house_name):
    images = getAllImages() or []  # Asegura que siempre haya una lista
    filtered_cards = []

    for card in images:
        if card.get("house", "").lower() == house_name.lower():  # Convertimos ambos a minúsculas
            filtered_cards.append(card)

    return filtered_cards


# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID