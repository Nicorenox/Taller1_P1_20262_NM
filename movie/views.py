from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

import matplotlib.pyplot as plt
import matplotlib
import io
import base64
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

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request):
    matplotlib.use('Agg')

    all_movies = Movie.objects.all()

    # --- Gráfica: películas por año ---
    movie_counts_by_year = {}
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        movie_counts_by_year[year] = movie_counts_by_year.get(year, 0) + 1

    bar_positions = range(len(movie_counts_by_year))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=0.5, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    graphic_year = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # --- Gráfica: películas por género (solo el primer género) ---
    genre_counts = {}
    for movie in all_movies:
        if movie.genre:
            first_genre = movie.genre.split(',')[0].strip()
        else:
            first_genre = "None"
        genre_counts[first_genre] = genre_counts.get(first_genre, 0) + 1

    bar_positions_genre = range(len(genre_counts))
    plt.bar(bar_positions_genre, genre_counts.values(), width=0.5, align='center', color='green')
    plt.title('Movies per genre (first only)')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_genre, genre_counts.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    plt.close()
    graphic_genre = base64.b64encode(buffer2.getvalue()).decode('utf-8')
    buffer2.close()

    return render(request, 'statistics.html', {
        'graphic': graphic_year,
        'graphic_genre': graphic_genre,
    })
    
    