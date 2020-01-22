from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from utenti.models import Profile
from utenti.views import cassa, edit_profile, logout_user
from mixer.backend.django import mixer
import pytest
import unittest


@pytest.mark.django_db
class TestViews(unittest.TestCase):
    def test_cassa_authenticated(self):
        path = reverse('utenti:cassa')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = cassa(request)
        assert response.status_code == 200

    def test_cassa_unauthenticated(self):
        path = reverse('utenti:cassa')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = cassa(request)
        assert 'utenti/login' in response.url

    def test_edit_profile_authenticated(self):
        path = reverse('utenti:edit-profile', kwargs={'oid': 1})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        mixer.blend(Profile, user=request.user)

        response = edit_profile(request, oid=1)
        print(response.status_code)
        assert response.status_code == 200

    def test_edit_profile_unauthenticated(self):
        path = reverse('utenti:edit-profile', kwargs={'oid': 1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = edit_profile(request, oid=1)
        assert 'utenti/login' in response.url

    def test_logout_user_unauthenticated(self):
        path = reverse('utenti:utenti-logout')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = logout_user(request)
        assert 'utenti/login' in response.url

    # test acquista pet coins
    def test_cassa_acquista(self):
        path = reverse('utenti:cassa')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        value = request.POST.copy()
        value['value'] = 100

        response = cassa(request)
        assert response.status_code == 200

    # test vendi pet coins (pet_coins_attuali < pet_coins_vendi)
    def test_cassa_vendi(self):
        path = reverse('utenti:cassa')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        value = request.POST.copy()
        value['value'] = -100

        response = cassa(request)
        assert response.status_code == 200
