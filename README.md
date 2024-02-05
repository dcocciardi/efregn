# Efregn



## Descrizione generale
**Efregn** è il sito web, interamente sviluppato con Django, del fittizio ristorante di specialità pugliesi con lo stesso nome. 
Consente agli utenti di visualizzare i piatti presenti nel menù e, previa registrazione, di creare delle vere e proprie ordinazioni, accumulando anche punti e sconti. 
Il personale può, inoltre, modificare il menù aggiungendo nuovi piatti.
## Requisiti
- Python 3.11
- pipenv
- git

## Installazione
1. Clonazione repo:
```bash
git clone https://github.com/dcocciardi/efregn.git
```
2. Preparazione ambiente virtuale:
```bash
cd efregn/
pipenv install
```
3. Avvio del server di sviluppo (il parametro indicato tra [] è facoltativo):
```bash
pipenv shell
cd efregn/
python manage.py runserver [0.0.0.0:8000]
```
