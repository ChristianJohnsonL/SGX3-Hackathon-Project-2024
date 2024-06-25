from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import MetadataForm


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
