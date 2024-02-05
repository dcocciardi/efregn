from django.test import TestCase
from django.contrib.auth.models import User, Group
from accounts.models import Utente
from django.contrib.auth.hashers import make_password
from .models import Piatto, Ordinazione
from time import sleep
from django.urls import reverse

class UtenteModelTest(TestCase):
    def create_test_user(self, username="testuser", password="123456", email=''):
        return User.objects.create(username=username, password=make_password(password), email=email)

    def test_creazione_utente(self):
        test_user = self.create_test_user()

        # Attendi 1 secondo per consentire la sincronizzazione dei dati del database
        sleep(1)
        
        # Verifica se l'utente è stato creato correttamente
        self.assertIsInstance(test_user, User)
        self.assertEqual(test_user.username, "testuser")
        
        # Verifica se l'utente associato (Utente) è stato creato correttamente
        utente_associato, created = Utente.objects.get_or_create(user=test_user)
        self.assertIsInstance(utente_associato, Utente)
        self.assertEqual(utente_associato.saldo_punti, 0)


class GruppoManagerTest(TestCase):

    def test_registrazione_utente_manager(self):
        # Crea i dati del form per registrare un utente
        form_data = {
            'username': 'testuser',
            'email': 'testmail@efregnstaff.com',
            'password1': 'password123',
            'password2': 'password123',
        }

        # Chiamata alla view 'registrati' con il metodo POST e i dati del form
        response = self.client.post(reverse('registrati'), data=form_data)

        # Verifica che la registrazione abbia successo (potrebbe essere un reindirizzamento)
        self.assertIn(response.status_code, [200, 302])

        # Ottieni l'utente appena registrato, estrai l'oggetto dalla tupla
        test_user, created_user = User.objects.get_or_create(username='testuser', email='testmail@efregnstaff.com')

        # Ottieni il gruppo "Manager"
        manager_group, created_group = Group.objects.get_or_create(name='Manager')

        # Aggiungi l'utente al gruppo "Manager"
        test_user.groups.add(manager_group)

        # Salva l'utente
        test_user.save()

        # Verifica che l'utente sia stato correttamente inserito nel gruppo "Manager"
        self.assertTrue(manager_group in test_user.groups.all())


class OrdinazioneViewTest(TestCase):
    def setUp(self):
        # Crea un utente normale
        self.utente_normale = User.objects.create_user(username='utente_normale', password='password123')

        # Crea un piatto "Caffè" nel menu
        self.caffe = Piatto.objects.create(nome='Caffè', prezzo=1.20)

    def test_aggiungi_al_carrello_view(self):
        # Effettua il login dell'utente normale
        self.client.login(username='utente_normale', password='password123')

        # Chiamata alla view per aggiungere il caffè all'ordinazione
        response = self.client.post(reverse('aggiungi_al_carrello', args=[self.caffe.id]), follow=True)

        # Verifica che la risposta abbia uno status code appropriato
        self.assertEqual(response.status_code, 200)

        # Verifica che l'ordinazione sia stata creata correttamente
        ordinazione = Ordinazione.objects.filter(utente=self.utente_normale, piatto=self.caffe, completato=False).first()
        self.assertIsNotNone(ordinazione)

        # Verifica che la quantità sia stata incrementata
        self.assertEqual(ordinazione.quantita, 1)

    def test_invia_ordinazione_view(self):
        # Effettua il login dell'utente normale
        self.client.login(username='utente_normale', password='password123')

        # Chiamata alla view per inviare l'ordinazione
        response = self.client.post(reverse('invia_ordinazione'))

        # Verifica che la risposta abbia uno status code appropriato
        self.assertEqual(response.status_code, 302)

        # Attendi 1 secondo per consentire la sincronizzazione dei dati del database
        sleep(1)

        # Verifica che l'ordinazione sia completata
        ordinazione = Ordinazione.objects.filter(utente=self.utente_normale, completato=True).first()

        # Verifica il reindirizzamento alla home
        self.assertRedirects(response, reverse('home'))
