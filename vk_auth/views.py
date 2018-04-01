from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.conf import settings
import pytz
import requests

from .models import AuthModel


api_request_url = 'https://api.vk.com/method/'

auth_url = (
    'https://oauth.vk.com/authorize?client_id={}&display=page&'
    'redirect_uri={}&scope=friends&'
    'response_type=code&v={}'
).format(settings.client_id, settings.redirect_uri, settings.version)
access_url = 'https://oauth.vk.com/access_token'


def auth(request):
    return redirect(auth_url)


def index(request):
    auth_model = AuthModel.objects.first()
    if auth_model:
        if auth_model.expires_at > datetime.now().replace(tzinfo=pytz.UTC):
            return redirect('friends_list')
        auth_model.delete()
    return render(request, 'index.html', {})


def get_token(request):
    code = request.GET['code']
    params = {
        'client_id': settings.client_id,
        'client_secret': settings.client_secret,
        'redirect_uri': settings.redirect_uri,
        'code': code,
    }
    r = requests.post(access_url, params=params).json()
    expires = datetime.now() + timedelta(seconds=r.get('expires_in'))
    AuthModel.objects.create(
        token=r.get('access_token'),
        expires_at=expires,
        user_id=r.get('user_id')
    )
    return redirect('friends_list')


def get_friends_list(request):
    auth_model = AuthModel.objects.first()
    if not auth_model:
        return redirect('index')
    url = api_request_url + 'friends.get'
    params = {
        'count': 5,
        'fields': ['first_name', 'last_name', 'domain'],
        'access_token': auth_model.token,
        'v': settings.version,
    }
    r = requests.post(url, params=params).json()
    friends_list = r.get('response').get('items')
    return render(request, 'list_friends.html', {'friends_list': friends_list})
