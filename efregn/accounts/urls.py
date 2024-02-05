from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('registrati/', views.registrati, name='registrati'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.paginaLogin, name='login'),
    path('amministrazione/', views.amministrazione, name='amministrazione'),
    path('non_autorizzato/', views.non_autorizzato, name='non_autorizzato'),
    path('cerca_piatto/', views.cerca_piatto, name='cerca_piatto'),
    path('aggiungi_al_carrello/<int:piatto_id>/', views.aggiungi_al_carrello, name='aggiungi_al_carrello'),
    path('ordinazione/', views.visualizza_ordinazione, name='visualizza_ordinazione'),
    path('invia_ordinazione/', views.invia_ordinazione,name='invia_ordinazione'),
    path('rimuovi_piatto/<int:ordinazione_id>/', views.rimuovi_piatto, name='rimuovi_piatto'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
