from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import MetadataForm, SearchForm
from .globus_api import queryHPC_ED
import json


def index(request):
    return render(request, "hpced/index.html")


def metadata_form_view(request):
    if request.method == "POST":
        form = MetadataForm(request.POST)
        if form.is_valid():
            ## API ACCESS HERE
            return HttpResponseRedirect("/thanks/")
        
    else:
        form = MetadataForm()
    return render(request, "hpced/metadata.html", {"form": form})


def search_form_view(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            ## API ACCESS HERE
            form_data = form.cleaned_data

            query_str = form_data['search_query']

            results = queryHPC_ED(query_str, 2, {})
            results = json.dumps(results, indent=4)
            print(results)

            return HttpResponseRedirect("/thanks/")
        
    else:
        form = SearchForm()
    return render(request, "hpced/search.html", {"form": form})
