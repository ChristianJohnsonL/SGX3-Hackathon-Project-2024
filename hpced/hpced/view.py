from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import transaction

from .forms import MetadataForm, SearchForm
from .globus_api import queryHPC_ED
import json
from django.core.serializers.json import DjangoJSONEncoder

from json import dumps
from django.utils import timezone
from datetime import timedelta
import datetime


from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from functools import wraps
import globus_sdk
import os
from pprint import pp

from allauth.socialaccount.providers.globus.views import GlobusOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView, OAuth2LoginView

from copy import copy


def calculate_expiration(expires_in):
    return timezone.now() + timedelta(seconds=expires_in)


class CustomGlobusOauth2Adapter(GlobusOAuth2Adapter):
   def complete_login(self, request, app, token, response):
        login = super().complete_login(request, app, token, response)
        user = login.user
        for res in response['other_tokens']:
                if res['resource_server'] == 'search.api.globus.org':
                    user.search_resource_server = res['resource_server']
                    user.search_access_token = res['access_token']
                    user.search_refresh_token = res['refresh_token']
                    user.search_expires_at = calculate_expiration(res['expires_in'])
                    user.search_scope = res['scope']


        return login



globus_login = OAuth2LoginView.adapter_view(CustomGlobusOauth2Adapter)
globus_callback = OAuth2CallbackView.adapter_view(CustomGlobusOauth2Adapter)




def get_valid_globus_token(user):
    print("getting globus token")
    token = refresh_globus_token(user)
    return token


def refresh_globus_token(user):
    print("refreshing globus token")

    client = globus_sdk.ConfidentialAppAuthClient(
        os.getenv('GLOBUS_OAUTH2_CLIENT_ID'),
        os.getenv('GLOBUS_OAUTH2_CLIENT_SECRET')
    )


    token_response = client.oauth2_refresh_token(user.search_refresh_token)
    token_data = token_response.by_resource_server['search.api.globus.org']
    user.search_access_token = token_data['access_token']
    print(token_data)
    user.search_refresh_token = token_data['refresh_token']  # Update refresh token if provided
    user.search_expires_at = datetime.datetime.utcfromtimestamp(token_data['expires_at_seconds'])
    user.save()
    return user.search_access_token



def globus_token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        access_token = get_valid_globus_token(request.user)
        if access_token:
            # Add the access token to the request object for use in the view
            request.access_token = access_token
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("No valid Globus token found for this user.", status=500)

    return _wrapped_view


def index(request):
    return render(request, "hpced/index.html")


def thanks(request):
    return render(request, "hpced/thanks.html")


@login_required
@globus_token_required
def metadata_form_view(request):
    form_data = {}
    if request.method == "POST":
        form = MetadataForm(request.POST)
        if form.is_valid():
            ## API ACCESS HERE
            form_data = form.cleaned_data
            print(dumps(form_data, cls=DjangoJSONEncoder))
            return render(request, "hpced/thanks.html", {"data": form_data})
            #return render(request, "hpced/metadata.html", {"form": form, "data": form_data})
        
    else:
        form = MetadataForm()
    return render(request, "hpced/metadata.html", {"form": form, "data": form_data})

@login_required
@globus_token_required
def search_form_view(request):
    results = []
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            ## API ACCESS HERE
            form_data = form.cleaned_data
            #print(json.dumps(form_data, indent=4))

            query_str = form_data.pop('Search_Query')

            results = queryHPC_ED(query_str, 20, form_data, access_token=request.access_token)
            pp(results)

            return render(request, "hpced/search.html", {"form": form, "result_list": results})
        
    else:
        form = SearchForm()
    return render(request, "hpced/search.html", {"form": form, "result_list": results})
