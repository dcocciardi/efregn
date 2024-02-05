from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from .decorators import *
from accounts.forms import CreateUserForm
from django.views.generic.edit import CreateView
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth.models import Group
from .forms import AggiungiPiatto
from django.db.models import Q


@utente_non_autenticato
def registrati(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Creazione dell'oggetto Utente associato
            Utente.objects.create(user=user, nome=user.username)

            # Verifica se l'indirizzo email termina con "@efregnstaff.com"
            if form.cleaned_data['email'].endswith('@efregnstaff.com'):
                # Assicurati che il gruppo "Manager" esista
                manager_group, created = Group.objects.get_or_create(name='Manager')
                # Aggiungi l'utente al gruppo "Manager"
                user.groups.add(manager_group)
                user.save()

            username = form.cleaned_data.get('username')
            messages.success(request, 'Meh ' + username + ', ora sì che siamo amici!')

            return redirect('login')

    return render(request, 'accounts/registrati.html', {'form': form})

@utente_non_autenticato
def paginaLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Per favore ricontrolla Username o Password.')


    return render(request, 'accounts/login.html')


def genera_raccomandazioni(utente):
    # Recupera tutte le categorie delle ordinazioni precedenti dell'utente
    categorie_preferite = Ordinazione.objects.filter(utente=utente, completato=True).values_list('piatto__categoria__nome', flat=True)

    # Calcola la frequenza delle categorie
    frequenza_categorie = {}
    for categoria in categorie_preferite:
        frequenza_categorie[categoria] = frequenza_categorie.get(categoria, 0) + 1

    # Ordina le categorie per frequenza decrescente
    categorie_ordinate = sorted(frequenza_categorie.items(), key=lambda x: x[1], reverse=True)

    # Ottieni la categoria più frequente
    categoria_piu_amata = None
    if categorie_ordinate:
        categoria_piu_amata = categorie_ordinate[0][0]

    # Seleziona i piatti nella categoria più amata
    raccomandazioni = Piatto.objects.filter(categoria__nome=categoria_piu_amata)

    return raccomandazioni, categoria_piu_amata




def home(request):
    ordine = request.GET.get('ordine', 'prezzo_asc')  # Ordina i piatti di default in prezzo crescente
    categoria = request.GET.get('categoria', 'Tutti')  # Filtra i piatti di default tutti

    categoria = categoria.capitalize()

    piatti = Piatto.objects.all()

    if categoria != 'Tutti':
        piatti = piatti.filter(categoria__nome=categoria)

    if ordine == 'prezzo_asc':
        piatti = piatti.order_by('prezzo')
    elif ordine == 'prezzo_desc':
        piatti = piatti.order_by('-prezzo')
    elif ordine == 'nome':
        piatti = piatti.order_by('nome')

    raccomandazioni = None
    categoria_piu_amata = None
    
    if request.user.is_authenticated:
        raccomandazioni, categoria_piu_amata = genera_raccomandazioni(request.user)


    return render(request, 'accounts/dashboard.html', {'piatti': piatti, 'raccomandazioni': raccomandazioni, 'categoria_piu_amata':categoria_piu_amata})


def logout_view(request):
    logout(request)
    return redirect('home')

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def non_autorizzato(request):
    return render(request, 'accounts/non_autorizzato.html')

@utenti_autorizzati(ruoli_autorizzati=['Manager']) 
def amministrazione(request):
    # Form per aggiungere un piatto
    if request.method == 'POST':
        aggiungi_form = AggiungiPiatto(request.POST, request.FILES)
        if aggiungi_form.is_valid():
            aggiungi_form.save()
            return redirect('home')
    else:
        aggiungi_form = AggiungiPiatto()

    return render(request, 'accounts/amministrazione.html', {'form': aggiungi_form})

def cerca_piatto(request):
    query = request.GET.get('q')
    piatti = Piatto.objects.filter(Q(nome__icontains=query) | Q(ingredienti__icontains=query))

    return render(request, 'accounts/cerca_piatto.html', {'piatti': piatti, 'query': query})


def aggiungi_al_carrello(request, piatto_id):
    if request.method == 'POST':
        piatto = get_object_or_404(Piatto, id=piatto_id)
        utente = request.user
        # Recupera le ordinazioni non completate dell'utente per il piatto selezionato
        ordinazioni = Ordinazione.objects.filter(utente=utente, piatto=piatto, completato=False)
        
        if ordinazioni.exists():
            # Se l'ordinazione esiste già, incrementa la quantità
            ordinazione = ordinazioni.first()
            ordinazione.quantita += 1
            ordinazione.save()
        else:
            # Se non esiste, crea una nuova ordinazione
            Ordinazione.objects.create(utente=utente, piatto=piatto, quantita=1)

        return redirect('home')
    else:
        return JsonResponse({'status': 'error'})

def calcola_dati_ordinazione(ordinazioni, utente):
    totale_ordine = sum(ordinazione.piatto.prezzo * ordinazione.quantita for ordinazione in ordinazioni)
    sconto = 0
    sconto_manager = False
    punti_ottenuti = 0

    if utente.groups.filter(name='Manager').exists():
        sconto = totale_ordine * 0.15
        sconto_manager = True

    else:
        if utente.utente.saldo_punti >= 5000 and totale_ordine > 5:
            sconto = 5
        punti_ottenuti = int(totale_ordine * 50)

    totale_ordine = totale_ordine - sconto

    return {
        'totale_ordine': totale_ordine,
        'sconto': sconto,
        'sconto_manager': sconto_manager,
        'punti_ottenuti': punti_ottenuti,
    }

def visualizza_ordinazione(request):
    if request.user.is_authenticated:
        ordinazioni = Ordinazione.objects.filter(utente=request.user, completato=False)
        dati_ordinazione = calcola_dati_ordinazione(ordinazioni, request.user)
        dati_ordinazione['ordinazioni'] = ordinazioni

        return render(request, 'accounts/ordinazione.html', dati_ordinazione)

    return render(request, 'home')

def invia_ordinazione(request):
    if request.user.is_authenticated:
        utente = request.user
        ordini = Ordinazione.objects.filter(utente=utente, completato=False)

        if ordini.exists():
            dati_ordinazione = calcola_dati_ordinazione(ordini, utente)

            if dati_ordinazione['sconto'] == 5:
                # Rimuovo 5000 punti solo se è stato applicato lo sconto di 5 euro
                utente.utente.saldo_punti -= 5000

            utente.utente.saldo_punti += dati_ordinazione['punti_ottenuti']
            utente.utente.save()

            ordini.update(completato=True)
            dati_ordinazione['ordine_inviato'] = True

            return render(request, 'accounts/ordinazione.html', dati_ordinazione)

    return redirect('home')

def rimuovi_piatto(request, ordinazione_id):
    if request.user.is_authenticated:
        # Recupera l'ordinazione da rimuovere
        ordinazione = get_object_or_404(Ordinazione, id=ordinazione_id, utente=request.user, completato=False)

    if ordinazione.quantita > 1:
        ordinazione.quantita -= 1
        ordinazione.save()
    else:
        # Se la quantità è 1, elimina l'ordinazione
        ordinazione.delete()
        
    return redirect('visualizza_ordinazione')