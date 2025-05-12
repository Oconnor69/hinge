# Dans urls.py de votre application
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('entreprise/register/', views.entreprise_register, name='entreprise_register'),
    path('entreprise/login/', views.entreprise_login, name='entreprise_login'),
    path('entreprise/logout/', views.entreprise_logout, name='entreprise_logout'),
    path('entreprise/dashboard/', views.entreprise_dashboard, name='entreprise_dashboard'),
    path('entreprises/', views.entreprise_list, name='entreprise_list'),
    path('entreprise/<int:pk>/', views.entreprise_detail, name='entreprise_detail'),
    path('entreprise/new/', views.entreprise_create, name='entreprise_create'),
    path('entreprise/<int:pk>/edit/', views.entreprise_update, name='entreprise_update'),
    path('entreprise/<int:pk>/delete/', views.entreprise_delete, name='entreprise_delete'),
    path('offres/', views.offre_list, name='offre_list'),
    path('offres/<int:pk>/', views.offre_detail, name='offre_detail'),
    path('offres/nouveau/', views.offre_create, name='offre_create'),
    path('offres/<int:pk>/modifier/', views.update_offre, name='offre_update'),
    path('offres/<int:pk>/supprimer/', views.offre_delete, name='offre_delete'),
    path('dash', views.dashboard, name='dashboard'),
    path('candidats/', views.candidat_list, name='candidat_list'),
    path('candidats/create/', views.candidat_create, name='candidat_create'),
    path('candidats/<int:pk>/', views.candidat_detail, name='candidat_detail'),
    path('candidats/<int:pk>/edit/', views.candidat_update, name='candidat_update'),
    path('candidats/<int:pk>/delete/', views.candidat_delete, name='candidat_delete'),
    path('', views.home, name='home'),
    path('candidatures/', CandidatureListView.as_view(), name='candidature_list'),
    path('candidature/<int:pk>/', CandidatureDetailView.as_view(), name='candidature_detail'),
    path('candidature/ajouter/', CandidatureCreateView.as_view(), name='candidature_create'),
    path('candidature/<int:pk>/modifier/', CandidatureUpdateView.as_view(), name='candidature_update'),
    path('candidature/<int:pk>/supprimer/', CandidatureDeleteView.as_view(), name='candidature_delete'),
    path('listeoffres/', views.liste_offres, name='liste_offres'),
    path('listeoffres/<int:offre_id>/', views.detail_offre, name='detail_offre'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('postuler/', views.postuler_offre, name='postuler_offre'),
    path('modifier-candidature/<int:pk>/', modifier_candidature, name='modifier_candidature'),
    path('supprimer-candidature/<int:pk>/', supprimer_candidature, name='supprimer_candidature'),
    path('mes-candidatures/', lister_candidatures, name='mes_candidatures'),
    path('profil/', views.profil_candidat, name='profil'),
    path('entreprise/offres/', views.entreprise_offres, name='entreprise_offres'),
    path('entreprise/offres/nouvelle/', views.entreprise_creer_offre, name='entreprise_creer_offre'),
    path('entreprise/offres/<int:offre_id>/modifier/', views.entreprise_modifier_offre, name='entreprise_modifier_offre'),
    path('entreprise/offres/<int:offre_id>/supprimer/', views.entreprise_supprimer_offre, name='entreprise_supprimer_offre'),
    path('entreprise/mescandidaturesss/', views.entreprise_liste_candidatures, name='entreprise_liste_candidaturesss'),
    path('entreprise/telecharger-cv/<int:candidature_id>/', views.entreprise_telecharger_cv, name='entreprise_telecharger_cv'),
    path('modifier-statut/', modifier_statut_candidature, name='modifier_statut_candidature'),
    path('candidats_postules/', views.candidats_postules_view, name='candidats_postules'),
    path('candidatees/<int:candidat_id>/', views.detail_candidat_view, name='detail_candidatess'),
    path('export-candidats/', views.export_candidats_csv, name='export_candidats'),
    path('admine/', views.logineee_view, name='logineee'),
    path('choix/', views.choix_login_view, name='choix_login'),
]


   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
