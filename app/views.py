# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages()  # Ahora sí obtiene datos reales
    favourite_list = []  # Esto se completará más adelante

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '').strip()  # Eliminamos espacios en blanco al inicio/final

    if name:
        images = services.filterByCharacter(name)  # Filtrar por nombre
    else:
        images = services.getAllImages()  # Mostrar todas las imágenes

    favourite_list = []  # Esto se completará después

    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})


# función utilizada para filtrar por casa Gryffindor o Slytherin.
def filter_by_house(request):
    house = request.POST.get('house', '')

    if house != '':
        images = services.filterByHouse(house)  # Ahora filtra por casa
        favourite_list = []  # Esto se completará más adelante

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    pass

@login_required
def saveFavourite(request):
    pass

@login_required
def deleteFavourite(request):
    pass

@login_required
def exit(request):
    logout(request)
    return redirect('home')