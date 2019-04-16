import requests

from django.shortcuts import render

from .forms import SearchForm

# Create your views here.


def search_movie(request, page_num=1):
    search_form = SearchForm()
    query = None
    found_results = False
    results = []
    has_next_page = False

    if query in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            omdb_endpoint = f'http://www.omdbapi.com/?apikey=225ea357&type=movie&page={page_num}&s='
            omdb_call = omdb_endpoint + query
            omdb_resp = requests.get(omdb_endpoint + query)
            if omdb_resp['Response'] == 'True':
                found_results = True
                results = omdb_resp['Search']
                if int(omdb_resp['totalResults']) > 10:
                    has_next_page = True
    return render(request, 'ratings/search-movie', {
        'search_form': search_form,
        'query': query,
        'found_results': found_results,
        'results': results,
        'has_next_page': has_next_page
    })
