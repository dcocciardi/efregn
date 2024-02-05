from django.db import models
from django.contrib.auth.models import User, Group



class Utente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=25, null=True)
    cognome = models.CharField(max_length=25, null=True)
    email = models.CharField(max_length=30, null=True)
    data_creazione = models.DateTimeField(auto_now_add=True)
    saldo_punti = models.IntegerField(default=0)

    # Mostra il nome dell'Utente anziché Utente object (N)' nella tabella
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'Utenti'


class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    # Mostra il nome della categoria anziché 'Categoria object (N)' nella tabella
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'Categorie'

class Piatto(models.Model):
    nome = models.CharField(max_length=50)
    ingredienti = models.CharField(max_length=500, null=True, blank=True)
    prezzo = models.FloatField(null=True)
    categoria = models.ManyToManyField(Categoria)
    immagine = models.ImageField(upload_to='piatti/', null=True, blank=True)


    # Mostra il nome del piatto anziché 'Piatto object (N)' nella tabella
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'Piatti'


class Ordinazione(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=1)
    piatto = models.ForeignKey(Piatto, on_delete=models.CASCADE, default=None) 
    quantita = models.PositiveIntegerField(default=1)
    completato = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Ordinazioni'