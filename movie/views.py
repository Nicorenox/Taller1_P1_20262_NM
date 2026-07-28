from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie
# Create your views here.

def home(request):
    #return ('<h1> Welcome to Home Page </h1>')
    #return render(request, 'home.html')
    movies = Movie.objects.all()
    
    searchTerm = request.GET.get('searchMovie')

    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
        
    return render(request, "home.html", {'searchTerm':searchTerm, 'movies': movies})


def about(request):
    #return HttpResponse("This is the About Page")
    return render(request, "about.html")