from django.urls import reverse, resolve


class TestUrls:

    def test_login_url(self):
        path = reverse('utenti:utenti-login')
        assert resolve(path).view_name == 'utenti:utenti-login'

    def test_registrazione_url(self):
        path = reverse('utenti:registrazione')
        assert resolve(path).view_name == 'utenti:registrazione'

    def test_registrazione_normale_url(self):
        path = reverse('utenti:registrazione-normale')
        assert resolve(path).view_name == 'utenti:registrazione-normale'

    def test_registrazione_petsitter_url(self):
        path = reverse('utenti:registrazione-petsitter')
        assert resolve(path).view_name == 'utenti:registrazione-petsitter'

    def test_logout_url(self):
        path = reverse('utenti:utenti-logout')
        assert resolve(path).view_name == 'utenti:utenti-logout'

    def test_view_profile_url(self):
        path = reverse('utenti:view-profile', kwargs={'oid': 1})
        assert resolve(path).view_name == 'utenti:view-profile'

    def test_edit_profile_url(self):
        path = reverse('utenti:edit-profile', kwargs={'oid': 1})
        assert resolve(path).view_name == 'utenti:edit-profile'

    def test_cassa_url(self):
        path = reverse('utenti:cassa')
        assert resolve(path).view_name == 'utenti:cassa'

    def test_classifica_url(self):
        path = reverse('utenti:classifica')
        assert resolve(path).view_name == 'utenti:classifica'

    def test_cerca_utenti_url(self):
        path = reverse('utenti:cerca_utenti')
        assert resolve(path).view_name == 'utenti:cerca_utenti'
