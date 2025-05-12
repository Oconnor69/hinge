# Dans views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Entreprise, Offre
from .forms import EntrepriseForm, OffreForm
from django.utils import timezone

def entreprise_list(request):
    entreprises = Entreprise.objects.all()
    return render(request, 'entreprise_list.html', {'entreprises': entreprises})

def entreprise_detail(request, pk):
    entreprise = get_object_or_404(Entreprise, pk=pk)
    return render(request, 'entreprise_detail.html', {'entreprise': entreprise})

def entreprise_create(request):
    if request.method == 'POST':
        form = EntrepriseForm(request.POST, request.FILES)
        if form.is_valid():
            entreprise = form.save()
            return redirect('entreprise_detail', pk=entreprise.pk)
    else:
        form = EntrepriseForm()
    return render(request, 'entreprise_form.html', {'form': form})

def entreprise_update(request, pk):
    entreprise = get_object_or_404(Entreprise, pk=pk)
    if request.method == 'POST':
        form = EntrepriseForm(request.POST, request.FILES, instance=entreprise)
        if form.is_valid():
            entreprise = form.save()
            return redirect('entreprise_detail', pk=entreprise.pk)
    else:
        form = EntrepriseForm(instance=entreprise)
    return render(request, 'entreprise_form.html', {'form': form})

def entreprise_delete(request, pk):
    entreprise = get_object_or_404(Entreprise, pk=pk)
    if request.method == 'POST':
        entreprise.delete()
        return redirect('entreprise_list')
    return render(request, 'entreprise_confirm_delete.html', {'entreprise': entreprise})


def offre_list(request):
    offres = Offre.objects.all().order_by('-date_publication')
    today = timezone.now().date()
    days7 = today + timezone.timedelta(days=7)
    context = {
        'offres': offres,
        'today': today,
        'days7': days7,
    }
    return render(request, 'offres/offre_list.html', context)

def offre_detail(request, pk):
    offre = get_object_or_404(Offre, pk=pk)
    return render(request, 'offres/offre_detail.html', {'offre': offre})

def offre_create(request):
    if request.method == 'POST':
        form = OffreForm(request.POST)
        if form.is_valid():
            offre = form.save()
            return redirect('offre_detail', pk=offre.pk)
    else:
        form = OffreForm()
    return render(request, 'offres/offre_form.html', {'form': form})

def update_offre(request, pk):
    offre = Offre.objects.get(id=pk)
    if request.method == 'POST':
        form = OffreForm(request.POST, instance=offre)
        if form.is_valid():
            form.save()
            return redirect('offre_list')
    else:
        form = OffreForm(instance=offre)
    return render(request, 'offres/offre_form.html', {'form': form})

def offre_delete(request, pk):
    offre = get_object_or_404(Offre, pk=pk)
    if request.method == 'POST':
        offre.delete()
        return redirect('offre_list')
    return render(request, 'offres/offre_confirm_delete.html', {'offre': offre})

from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from .models import Entreprise, Offre, Candidat, Candidature

def dashboard(request):
    
    stats = {
        'total_entreprises': Entreprise.objects.count(),
        'total_offres': Offre.objects.count(),
        'total_candidats': Candidat.objects.count(),
        'total_candidatures': Candidature.objects.count(),
    }
    
   
    offres_recentes = Offre.objects.select_related('entreprise').order_by('-date_publication')[:5]
   
    candidatures_recentes = Candidature.objects.select_related(
        'candidat', 'offre', 'offre__entreprise'
    ).order_by('-date_postulation')[:5]
    
  
    offres_expirant = Offre.objects.filter(
        date_expiration__gte=timezone.now(),
        date_expiration__lte=timezone.now() + timezone.timedelta(days=7)
    ).order_by('date_expiration')
    
   
    stats_candidatures = Candidature.objects.values('statut').annotate(
        total=Count('id')
    ).order_by('statut')
    
    context = {
        **stats,
        'offres_recentes': offres_recentes,
        'candidatures_recentes': candidatures_recentes,
        'offres_expirant': offres_expirant,
        'stats_candidatures': stats_candidatures,
    }
    
    return render(request, 'dashboard.html', context)


from .models import Candidat
from .forms import CandidatForm

def candidat_list(request):
    candidats = Candidat.objects.all()
    return render(request, 'candidat/candidat_list.html', {'candidats': candidats})

def candidat_detail(request, pk):
    candidat = get_object_or_404(Candidat, pk=pk)
    return render(request, 'candidat/candidat_detail.html', {'candidat': candidat})

def candidat_create(request):
    if request.method == 'POST':
        form = CandidatForm(request.POST, request.FILES)
        if form.is_valid():
            candidat = form.save()
            return redirect('candidat_detail', pk=candidat.pk)
    else:
        form = CandidatForm()
    return render(request, 'candidat/candidat_form.html', {'form': form})

def candidat_update(request, pk):
    candidat = get_object_or_404(Candidat, pk=pk)
    if request.method == 'POST':
        form = CandidatForm(request.POST, request.FILES, instance=candidat)
        if form.is_valid():
            candidat = form.save()
            return redirect('candidat_detail', pk=candidat.pk)
    else:
        form = CandidatForm(instance=candidat)
    return render(request, 'candidat/candidat_form.html', {'form': form})

def candidat_delete(request, pk):
    candidat = get_object_or_404(Candidat, pk=pk)
    if request.method == 'POST':
        candidat.delete()
        return redirect('candidat_list')
    return render(request, 'candidat/candidat_confirm_delete.html', {'candidat': candidat})
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
# views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Candidature
from .forms import CandidatureForm

class CandidatureListView(ListView):
    model = Candidature
    template_name = 'candidature/candidature_list.html'

class CandidatureDetailView(DetailView):
    model = Candidature
    template_name = 'candidature/candidature_detail.html'

class CandidatureCreateView(CreateView):
    model = Candidature
    form_class = CandidatureForm
    template_name = 'candidature/candidature_form.html'
    success_url = reverse_lazy('candidature_list')

class CandidatureUpdateView(UpdateView):
    model = Candidature
    form_class = CandidatureForm
    template_name = 'candidature/candidature_form.html'
    success_url = reverse_lazy('candidature_list')

class CandidatureDeleteView(DeleteView):
    model = Candidature
    template_name = 'candidature/candidature_confirm_delete.html'
    success_url = reverse_lazy('candidature_list')
from django.shortcuts import render, get_object_or_404
from .models import Offre

def liste_offres(request):
    today = timezone.now().date()
    offres = Offre.objects.filter(date_expiration__gte=today)

    # Filtres
    entreprise_id = request.GET.get('entreprise')
    if entreprise_id:
        offres = offres.filter(entreprise_id=entreprise_id)

    date_pub = request.GET.get('date_pub')
    if date_pub:
        offres = offres.filter(date_publication=date_pub)

    salaire_min = request.GET.get('salaire_min')
    if salaire_min:
        offres = offres.filter(salaire__gte=salaire_min)

    salaire_max = request.GET.get('salaire_max')
    if salaire_max:
        offres = offres.filter(salaire__lte=salaire_max)

    type_contrat = request.GET.get('type_contrat')
    if type_contrat:
        offres = offres.filter(type_contrat=type_contrat)

    categorie = request.GET.get('categorie')
    if categorie:
        offres = offres.filter(categorie=categorie)

    localisation = request.GET.get('localisation')
    if localisation:
        offres = offres.filter(localisation__icontains=localisation)

    niveau_etude = request.GET.get('niveau_etude')
    if niveau_etude:
        offres = offres.filter(niveau_etude__icontains=niveau_etude)

    experience = request.GET.get('experience')
    if experience:
        offres = offres.filter(experience_requise__icontains=experience)

    offres = offres.order_by('-date_publication')

    # Récupération des choix et valeurs distinctes
    entreprises = Entreprise.objects.all()
    
    # Correction ici: accès aux choix via get_field()
    categorie_field = Offre._meta.get_field('categorie')
    categories = categorie_field.choices
    
    type_contrat_field = Offre._meta.get_field('type_contrat')
    types_contrat = type_contrat_field.choices
    
    localisations = Offre.objects.exclude(localisation__isnull=True).exclude(localisation__exact='')\
                       .values_list('localisation', flat=True).distinct()
    
    niveaux_etude = Offre.objects.exclude(niveau_etude__isnull=True).exclude(niveau_etude__exact='')\
                       .values_list('niveau_etude', flat=True).distinct()

    return render(request, 'listecandidature/offres.html', {
        'offres': offres,
        'entreprises': entreprises,
        'categories': categories,
        'types_contrat': types_contrat,
        'localisations': localisations,
        'niveaux_etude': niveaux_etude,
        'selected_entreprise': entreprise_id,
        'selected_categorie': categorie,
        'selected_type_contrat': type_contrat,
        'selected_localisation': localisation,
        'selected_niveau_etude': niveau_etude,
        'selected_experience': experience,
        'selected_salaire_min': salaire_min,
        'selected_salaire_max': salaire_max,
    })

from django.contrib.auth.models import Group

def detail_offre(request, offre_id):
    offre = get_object_or_404(Offre, pk=offre_id)

    # Détection via la session personnalisée
    is_candidat = 'candidat_id' in request.session

    return render(request, 'listecandidature/detail_offre.html', {
        'offre': offre,
        'is_candidat': is_candidat
    })
from django.views.decorators.http import require_POST
from .models import Candidature, Candidat

@require_POST
def postuler_offre(request):
    if 'candidat_id' not in request.session:
        messages.error(request, "Veuillez vous connecter pour postuler.")
        return redirect('detail_offre', offre_id=offre.id)


    candidat = Candidat.objects.get(id=request.session['candidat_id'])
    offre_id = request.POST.get('offre_id')

    # Vérifier que l'offre existe
    try:
        offre = Offre.objects.get(pk=offre_id)
    except Offre.DoesNotExist:
        messages.error(request, "Offre introuvable.")
        return redirect('liste_offres')

    # Vérifier que le candidat n'a pas déjà postulé
    if Candidature.objects.filter(candidat=candidat, offre=offre).exists():
        messages.warning(request, "Vous avez déjà postulé à cette offre.")
    else:
        Candidature.objects.create(candidat=candidat, offre=offre)
        messages.success(request, "Candidature envoyée avec succès.")

    return redirect('detail_offre', offre_id=offre.id)

from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .models import Candidat
from django.contrib import messages
from django.contrib.auth.hashers import check_password

from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Candidat
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.cleaned_data.pop('confirmation')  # Enlève le champ non présent dans le modèle
            Candidat.objects.create(**form.cleaned_data)
            messages.success(request, "Inscription réussie.")
            return redirect('login')  # ou autre page
        else:
            messages.error(request, "Erreur dans le formulaire.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
from django.shortcuts import render

from django.shortcuts import redirect

def dashboard(request):

    if 'candidat_id' not in request.session:
        messages.error(request, "Session expirée. Veuillez vous reconnecter.")
        return redirect('login')
    
    candidat_id = request.session['candidat_id']
    candidat = Candidat.objects.get(id=candidat_id)
    return render(request, 'dashboard.html', {'candidat': candidat})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            mot_de_passe = form.cleaned_data['mot_de_passe']
            try:
                candidat = Candidat.objects.get(email=email)
                if check_password(mot_de_passe, candidat.mot_de_passe):
                    request.session['candidat_id'] = candidat.id
                    messages.success(request, "Connexion réussie.")
                    return redirect('/listeoffres/')  # Redirection après succès
                else:
                    messages.error(request, "Mot de passe incorrect.")
            except Candidat.DoesNotExist:
                messages.error(request, "Email non reconnu.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    request.session.flush()
    messages.info(request, "Déconnecté avec succès.")
    return redirect('login')
from django.shortcuts import render, redirect
from .models import Entreprise
from .forms import EntrepriseRegisterForm, EntrepriseLoginForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password

def entreprise_register(request):
    if request.method == "POST":
        form = EntrepriseRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.cleaned_data.pop('confirmation')
            Entreprise.objects.create(**form.cleaned_data)
            messages.success(request, "Inscription réussie. Connectez-vous.")
            return redirect('entreprise_login')
        else:
            messages.error(request, "Erreur dans le formulaire.")
    else:
        form = EntrepriseRegisterForm()
    return render(request, 'entreprise/register.html', {'form': form})

def entreprise_login(request):
    if request.method == "POST":
        form = EntrepriseLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            mot_de_passe = form.cleaned_data['mot_de_passe']
            try:
                entreprise = Entreprise.objects.get(email=email)
                if check_password(mot_de_passe, entreprise.mot_de_passe):
                    request.session['entreprise_id'] = entreprise.id
                    messages.success(request, "Connexion réussie.")
                    return redirect('entreprise_dashboard')
                else:
                    messages.error(request, "Mot de passe incorrect.")
            except Entreprise.DoesNotExist:
                messages.error(request, "Email non reconnu.")
    else:
        form = EntrepriseLoginForm()
    return render(request, 'entreprise/login.html', {'form': form})

def entreprise_logout(request):
    request.session.flush()
    messages.info(request, "Déconnecté avec succès.")
    return redirect('entreprise_login')

def entreprise_dashboard(request):
    if 'entreprise_id' not in request.session:
        messages.error(request, "Session expirée. Veuillez vous reconnecter.")
        return redirect('entreprise_login')
    
    entreprise_id = request.session['entreprise_id']
    entreprise = Entreprise.objects.get(id=entreprise_id)
    
    # Calcul des statistiques pour le tableau de bord
    offres_count = Offre.objects.filter(entreprise=entreprise).count()
    
    # Récupération des candidatures liées aux offres de cette entreprise
    candidatures = Candidature.objects.filter(offre__entreprise=entreprise)
    candidatures_count = candidatures.count()
    
    # Candidatures en attente
    candidatures_pending = candidatures.filter(statut="EN_ATTENTE").count()
    
    context = {
        'entreprise': entreprise,
        'offres_count': offres_count,
        'candidatures_count': candidatures_count,
        'candidatures_pending': candidatures_pending,
    }
    
    return render(request, 'entreprise/dashboard.html', context)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Candidature
from .forms import CandidatureForm

def modifier_candidature(request, pk):
    candidature = get_object_or_404(Candidature, pk=pk)

    # Vérifie si la session candidat correspond à la candidature
    if candidature.candidat.id != request.session.get('candidat_id'):
        messages.error(request, "Accès refusé.")
        return redirect('mes_candidatures')

    # Vérifie si le statut est encore modifiable
    if candidature.statut != "EN_ATTENTE":
        messages.error(request, "Vous ne pouvez pas modifier cette candidature.")
        return redirect('mes_candidatures')

    if request.method == 'POST':
        form = CandidatureForm(request.POST, instance=candidature)
        if form.is_valid():
            form.save()
            messages.success(request, "Candidature modifiée avec succès.")
            return redirect('mes_candidatures')
    else:
        form = CandidatureForm(instance=candidature)

    return render(request, 'candidature/modifier_candidature.html', {'form': form})
def supprimer_candidature(request, pk):
    candidature = get_object_or_404(Candidature, pk=pk)

    if candidature.candidat.id != request.session.get('candidat_id'):
        messages.error(request, "Accès refusé.")
        return redirect('mes_candidatures')

    if candidature.statut != "EN_ATTENTE":
        messages.error(request, "Vous ne pouvez pas supprimer cette candidature.")
        return redirect('mes_candidatures')

    if request.method == 'POST':
        candidature.delete()
        messages.success(request, "Candidature supprimée avec succès.")
        return redirect('mes_candidatures')

    return render(request, 'candidature/supprimer_candidature.html', {'candidature': candidature})
from django.shortcuts import render
from django.contrib import messages
from .models import Candidature

def lister_candidatures(request):
    # Récupère les candidatures du candidat authentifié
    candidat_id = request.session.get('candidat_id')
    if not candidat_id:
        messages.error(request, "Accès non autorisé.")
        return redirect('login')  # Ou rediriger vers une page d'erreur, selon ton système

    candidatures = Candidature.objects.filter(candidat_id=candidat_id)

    # Filtrer les candidatures avec le statut "EN_ATTENTE"
    candidatures_en_attente = candidatures.filter(statut="EN_ATTENTE")

    return render(request, 'candidature/lister_candidatures.html', {'candidatures': candidatures_en_attente})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Candidat
from .forms import CandidatForm

def profil_candidat(request):
    candidat_id = request.session.get('candidat_id')
    if not candidat_id:
        return redirect('login')  # Ou autre vue de connexion

    candidat = get_object_or_404(Candidat, id=candidat_id)

    if request.method == 'POST':
        form = CandidatForm(request.POST, request.FILES, instance=candidat)
        if form.is_valid():
            form.save()
            return redirect('profil')  # Redirige vers le profil après modification
    else:
        form = CandidatForm(instance=candidat)

    return render(request, 'candidat/profil.html', {'form': form})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Candidat, Offre
from .forms import CandidatForm, OffreForm

# Vue profil du candidat (inchangée)
def profil_candidat(request):
    candidat_id = request.session.get('candidat_id')
    if not candidat_id:
        return redirect('login')

    candidat = get_object_or_404(Candidat, id=candidat_id)

    if request.method == 'POST':
        form = CandidatForm(request.POST, request.FILES, instance=candidat)
        if form.is_valid():
            form.save()
            return redirect('profil')
    else:
        form = CandidatForm(instance=candidat)

    return render(request, 'candidat/profil.html', {'form': form})


# Vue pour afficher les offres de l'entreprise connectée
def entreprise_offres(request):
    entreprise_id = request.session.get('entreprise_id')
    if not entreprise_id:
        return redirect('entreprise_login')

    offres = Offre.objects.filter(entreprise_id=entreprise_id)
    return render(request, 'entrepriseoffres/liste.html', {'offres': offres})


# Vue pour créer une nouvelle offre
def entreprise_creer_offre(request):
    entreprise_id = request.session.get('entreprise_id')
    if not entreprise_id:
        return redirect('entreprise_login')

    if request.method == 'POST':
        form = OffreForm(request.POST)
        if form.is_valid():
            offre = form.save(commit=False)
            offre.entreprise_id = entreprise_id
            offre.save()
            return redirect('entreprise_offres')
    else:
        form = OffreForm()

    return render(request, 'entrepriseoffres/form.html', {'form': form})


# Vue pour modifier une offre existante
def entreprise_modifier_offre(request, offre_id):
    entreprise_id = request.session.get('entreprise_id')
    offre = get_object_or_404(Offre, pk=offre_id, entreprise_id=entreprise_id)

    if request.method == 'POST':
        form = OffreForm(request.POST, instance=offre)
        if form.is_valid():
            form.save()
            return redirect('entreprise_offres')
    else:
        form = OffreForm(instance=offre)

    return render(request, 'entrepriseoffres/form.html', {'form': form})


# Vue pour supprimer une offre
def entreprise_supprimer_offre(request, offre_id):
    entreprise_id = request.session.get('entreprise_id')
    offre = get_object_or_404(Offre, pk=offre_id, entreprise_id=entreprise_id)

    if request.method == 'POST':
        offre.delete()
        return redirect('entreprise_offres')

    return render(request, 'entrepriseoffres/confirm_suppression.html', {'offre': offre})
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404
from .models import Offre, Candidature

def entreprise_liste_candidatures(request):
    """
    Affiche toutes les candidatures reçues par l'entreprise connectée.
    """
    entreprise_id = request.session.get('entreprise_id')
    if not entreprise_id:
        return redirect('entreprise_login')  # Redirection si l'entreprise n'est pas connectée

    # Récupérer les offres appartenant à l'entreprise
    offres = Offre.objects.filter(entreprise_id=entreprise_id)

    # Récupérer toutes les candidatures liées à ces offres
    candidatures = Candidature.objects.filter(offre__in=offres).select_related('candidat', 'offre')

    return render(request, 'entrepriseoffres/candidatures.html', {
        'candidatures': candidatures
    })


def entreprise_telecharger_cv(request, candidature_id):
    """
    Permet à l'entreprise de télécharger le CV du candidat s’il existe.
    """
    entreprise_id = request.session.get('entreprise_id')
    if not entreprise_id:
        return redirect('entreprise_login')

    candidature = get_object_or_404(
        Candidature,
        pk=candidature_id,
        offre__entreprise_id=entreprise_id
    )

    candidat = candidature.candidat
    if not candidat.cv:
        raise Http404("Ce candidat n'a pas de CV.")

    return FileResponse(candidat.cv.open('rb'), as_attachment=True, filename=candidat.cv.name)
# views.py
# Dans views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Entreprise, Offre
from .forms import EntrepriseForm, OffreForm
from django.utils import timezone

def entreprise_list(request):
    entreprises = Entreprise.objects.all()
    return render(request, 'entreprise_list.html', {'entreprises': entreprises})

def entreprise_detail(request, pk):
    entreprise = get_object_or_404(Entreprise, pk=pk)
    return render(request, 'entreprise_detail.html', {'entreprise': entreprise})

def entreprise_create(request):
    if request.method == 'POST':
        form = EntrepriseForm(request.POST, request.FILES)
        if form.is_valid():
            entreprise = form.save()
            return redirect('entreprise_detail', pk=entreprise.pk)
    else:
        form = EntrepriseForm()
    return render(request, 'entreprise_form.html', {'form': form})

def entreprise_update(request, pk):
    entreprise = get_object_or_404(Entreprise, pk=pk)
    if request.method == 'POST':
        form = EntrepriseForm(request.POST, request.FILES, instance=entreprise)
        if form.is_valid():
            entreprise = form.save()
            return redirect('entreprise_detail', pk=entreprise.pk)
    else:
        form = EntrepriseForm(instance=entreprise)
    return render(request, 'entreprise_form.html', {'form': form})

def entreprise_delete(request, pk):
    entreprise = get_object_or_404(Entreprise, pk=pk)
    if request.method == 'POST':
        entreprise.delete()
        return redirect('entreprise_list')
    return render(request, 'entreprise_confirm_delete.html', {'entreprise': entreprise})


def offre_list(request):
    offres = Offre.objects.all().order_by('-date_publication')
    today = timezone.now().date()
    days7 = today + timezone.timedelta(days=7)
    context = {
        'offres': offres,
        'today': today,
        'days7': days7,
    }
    return render(request, 'offres/offre_list.html', context)

def offre_detail(request, pk):
    offre = get_object_or_404(Offre, pk=pk)
    return render(request, 'offres/offre_detail.html', {'offre': offre})

def offre_create(request):
    if request.method == 'POST':
        form = OffreForm(request.POST)
        if form.is_valid():
            offre = form.save()
            return redirect('offre_detail', pk=offre.pk)
    else:
        form = OffreForm()
    return render(request, 'offres/offre_form.html', {'form': form})

def update_offre(request, pk):
    offre = Offre.objects.get(id=pk)
    if request.method == 'POST':
        form = OffreForm(request.POST, instance=offre)
        if form.is_valid():
            form.save()
            return redirect('offre_list')
    else:
        form = OffreForm(instance=offre)
    return render(request, 'offres/offre_form.html', {'form': form})

def offre_delete(request, pk):
    offre = get_object_or_404(Offre, pk=pk)
    if request.method == 'POST':
        offre.delete()
        return redirect('offre_list')
    return render(request, 'offres/offre_confirm_delete.html', {'offre': offre})

from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from .models import Entreprise, Offre, Candidat, Candidature

def dashboard(request):
    
    stats = {
        'total_entreprises': Entreprise.objects.count(),
        'total_offres': Offre.objects.count(),
        'total_candidats': Candidat.objects.count(),
        'total_candidatures': Candidature.objects.count(),
    }
    
   
    offres_recentes = Offre.objects.select_related('entreprise').order_by('-date_publication')[:5]
   
    candidatures_recentes = Candidature.objects.select_related(
        'candidat', 'offre', 'offre__entreprise'
    ).order_by('-date_postulation')[:5]
    
  
    offres_expirant = Offre.objects.filter(
        date_expiration__gte=timezone.now(),
        date_expiration__lte=timezone.now() + timezone.timedelta(days=7)
    ).order_by('date_expiration')
    
   
    stats_candidatures = Candidature.objects.values('statut').annotate(
        total=Count('id')
    ).order_by('statut')
    
    context = {
        **stats,
        'offres_recentes': offres_recentes,
        'candidatures_recentes': candidatures_recentes,
        'offres_expirant': offres_expirant,
        'stats_candidatures': stats_candidatures,
    }
    
    return render(request, 'dashboard.html', context)


from .models import Candidat
from .forms import CandidatForm

def candidat_list(request):
    candidats = Candidat.objects.all()
    return render(request, 'candidat/candidat_list.html', {'candidats': candidats})

def candidat_detail(request, pk):
    candidat = get_object_or_404(Candidat, pk=pk)
    return render(request, 'candidat/candidat_detail.html', {'candidat': candidat})

def candidat_create(request):
    if request.method == 'POST':
        form = CandidatForm(request.POST, request.FILES)
        if form.is_valid():
            candidat = form.save()
            return redirect('candidat_detail', pk=candidat.pk)
    else:
        form = CandidatForm()
    return render(request, 'candidat/candidat_form.html', {'form': form})

def candidat_update(request, pk):
    candidat = get_object_or_404(Candidat, pk=pk)
    if request.method == 'POST':
        form = CandidatForm(request.POST, request.FILES, instance=candidat)
        if form.is_valid():
            candidat = form.save()
            return redirect('candidat_detail', pk=candidat.pk)
    else:
        form = CandidatForm(instance=candidat)
    return render(request, 'candidat/candidat_form.html', {'form': form})

def candidat_delete(request, pk):
    candidat = get_object_or_404(Candidat, pk=pk)
    if request.method == 'POST':
        candidat.delete()
        return redirect('candidat_list')
    return render(request, 'candidat/candidat_confirm_delete.html', {'candidat': candidat})
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
# views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Candidature
from .forms import CandidatureForm

class CandidatureListView(ListView):
    model = Candidature
    template_name = 'candidature/candidature_list.html'

class CandidatureDetailView(DetailView):
    model = Candidature
    template_name = 'candidature/candidature_detail.html'

class CandidatureCreateView(CreateView):
    model = Candidature
    form_class = CandidatureForm
    template_name = 'candidature/candidature_form.html'
    success_url = reverse_lazy('candidature_list')

class CandidatureUpdateView(UpdateView):
    model = Candidature
    form_class = CandidatureForm
    template_name = 'candidature/candidature_form.html'
    success_url = reverse_lazy('candidature_list')

class CandidatureDeleteView(DeleteView):
    model = Candidature
    template_name = 'candidature/candidature_confirm_delete.html'
    success_url = reverse_lazy('candidature_list')
from django.shortcuts import render, get_object_or_404
from .models import Offre

def liste_offres(request):
    today = timezone.now().date()
    offres = Offre.objects.filter(date_expiration__gte=today)

    # Filtres
    entreprise_id = request.GET.get('entreprise')
    if entreprise_id:
        offres = offres.filter(entreprise_id=entreprise_id)

    date_pub = request.GET.get('date_pub')
    if date_pub:
        offres = offres.filter(date_publication=date_pub)

    salaire_min = request.GET.get('salaire_min')
    if salaire_min:
        offres = offres.filter(salaire__gte=salaire_min)

    salaire_max = request.GET.get('salaire_max')
    if salaire_max:
        offres = offres.filter(salaire__lte=salaire_max)

    type_contrat = request.GET.get('type_contrat')
    if type_contrat:
        offres = offres.filter(type_contrat=type_contrat)

    categorie = request.GET.get('categorie')
    if categorie:
        offres = offres.filter(categorie=categorie)

    localisation = request.GET.get('localisation')
    if localisation:
        offres = offres.filter(localisation__icontains=localisation)

    niveau_etude = request.GET.get('niveau_etude')
    if niveau_etude:
        offres = offres.filter(niveau_etude__icontains=niveau_etude)

    experience = request.GET.get('experience')
    if experience:
        offres = offres.filter(experience_requise__icontains=experience)

    offres = offres.order_by('-date_publication')

    # Récupération des choix et valeurs distinctes
    entreprises = Entreprise.objects.all()
    
    # Correction ici: accès aux choix via get_field()
    categorie_field = Offre._meta.get_field('categorie')
    categories = categorie_field.choices
    
    type_contrat_field = Offre._meta.get_field('type_contrat')
    types_contrat = type_contrat_field.choices
    
    localisations = Offre.objects.exclude(localisation__isnull=True).exclude(localisation__exact='')\
                       .values_list('localisation', flat=True).distinct()
    
    niveaux_etude = Offre.objects.exclude(niveau_etude__isnull=True).exclude(niveau_etude__exact='')\
                       .values_list('niveau_etude', flat=True).distinct()

    return render(request, 'listecandidature/offres.html', {
        'offres': offres,
        'entreprises': entreprises,
        'categories': categories,
        'types_contrat': types_contrat,
        'localisations': localisations,
        'niveaux_etude': niveaux_etude,
        'selected_entreprise': entreprise_id,
        'selected_categorie': categorie,
        'selected_type_contrat': type_contrat,
        'selected_localisation': localisation,
        'selected_niveau_etude': niveau_etude,
        'selected_experience': experience,
        'selected_salaire_min': salaire_min,
        'selected_salaire_max': salaire_max,
    })

from django.contrib.auth.models import Group

def detail_offre(request, offre_id):
    offre = get_object_or_404(Offre, pk=offre_id)

    # Détection via la session personnalisée
    is_candidat = 'candidat_id' in request.session

    return render(request, 'listecandidature/detail_offre.html', {
        'offre': offre,
        'is_candidat': is_candidat
    })
from django.views.decorators.http import require_POST
from .models import Candidature, Candidat

@require_POST
def postuler_offre(request):
    if 'candidat_id' not in request.session:
        messages.error(request, "Veuillez vous connecter pour postuler.")
        return redirect('detail_offre', offre_id=offre.id)


    candidat = Candidat.objects.get(id=request.session['candidat_id'])
    offre_id = request.POST.get('offre_id')

    # Vérifier que l'offre existe
    try:
        offre = Offre.objects.get(pk=offre_id)
    except Offre.DoesNotExist:
        messages.error(request, "Offre introuvable.")
        return redirect('liste_offres')

    # Vérifier que le candidat n'a pas déjà postulé
    if Candidature.objects.filter(candidat=candidat, offre=offre).exists():
        messages.warning(request, "Vous avez déjà postulé à cette offre.")
    else:
        Candidature.objects.create(candidat=candidat, offre=offre)
        messages.success(request, "Candidature envoyée avec succès.")

    return redirect('detail_offre', offre_id=offre.id)

from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .models import Candidat
from django.contrib import messages
from django.contrib.auth.hashers import check_password

from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Candidat
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.cleaned_data.pop('confirmation')  # Enlève le champ non présent dans le modèle
            Candidat.objects.create(**form.cleaned_data)
            messages.success(request, "Inscription réussie.")
            return redirect('login')  # ou autre page
        else:
            messages.error(request, "Erreur dans le formulaire.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
from django.shortcuts import render

from django.shortcuts import redirect

def dashboard(request):

    if 'candidat_id' not in request.session:
        messages.error(request, "Session expirée. Veuillez vous reconnecter.")
        return redirect('login')
    
    candidat_id = request.session['candidat_id']
    candidat = Candidat.objects.get(id=candidat_id)
    return render(request, 'dashboard.html', {'candidat': candidat})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            mot_de_passe = form.cleaned_data['mot_de_passe']
            try:
                candidat = Candidat.objects.get(email=email)
                if check_password(mot_de_passe, candidat.mot_de_passe):
                    request.session['candidat_id'] = candidat.id
                    messages.success(request, "Connexion réussie.")
                    return redirect('/listeoffres/')  # Redirection après succès
                else:
                    messages.error(request, "Mot de passe incorrect.")
            except Candidat.DoesNotExist:
                messages.error(request, "Email non reconnu.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    request.session.flush()
    messages.info(request, "Déconnecté avec succès.")
    return redirect('login')
from django.shortcuts import render, redirect
from .models import Entreprise
from .forms import EntrepriseRegisterForm, EntrepriseLoginForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password

def entreprise_register(request):
    if request.method == "POST":
        form = EntrepriseRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.cleaned_data.pop('confirmation')
            Entreprise.objects.create(**form.cleaned_data)
            messages.success(request, "Inscription réussie. Connectez-vous.")
            return redirect('entreprise_login')
        else:
            messages.error(request, "Erreur dans le formulaire.")
    else:
        form = EntrepriseRegisterForm()
    return render(request, 'entreprise/register.html', {'form': form})

def entreprise_login(request):
    if request.method == "POST":
        form = EntrepriseLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            mot_de_passe = form.cleaned_data['mot_de_passe']
            try:
                entreprise = Entreprise.objects.get(email=email)
                if check_password(mot_de_passe, entreprise.mot_de_passe):
                    request.session['entreprise_id'] = entreprise.id
                    messages.success(request, "Connexion réussie.")
                    return redirect('entreprise_dashboard')
                else:
                    messages.error(request, "Mot de passe incorrect.")
            except Entreprise.DoesNotExist:
                messages.error(request, "Email non reconnu.")
    else:
        form = EntrepriseLoginForm()
    return render(request, 'entreprise/login.html', {'form': form})

def entreprise_logout(request):
    request.session.flush()
    messages.info(request, "Déconnecté avec succès.")
    return redirect('entreprise_login')

def entreprise_dashboard(request):
    if 'entreprise_id' not in request.session:
        messages.error(request, "Session expirée. Veuillez vous reconnecter.")
        return redirect('entreprise_login')
    
    entreprise_id = request.session['entreprise_id']
    entreprise = Entreprise.objects.get(id=entreprise_id)
    
    # Calcul des statistiques pour le tableau de bord
    offres_count = Offre.objects.filter(entreprise=entreprise).count()
    
    # Récupération des candidatures liées aux offres de cette entreprise
    candidatures = Candidature.objects.filter(offre__entreprise=entreprise)
    candidatures_count = candidatures.count()
    
    # Candidatures en attente
    candidatures_pending = candidatures.filter(statut="EN_ATTENTE").count()
    
    context = {
        'entreprise': entreprise,
        'offres_count': offres_count,
        'candidatures_count': candidatures_count,
        'candidatures_pending': candidatures_pending,
    }
    
    return render(request, 'entreprise/dashboard.html', context)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Candidature
from .forms import CandidatureForm

def modifier_candidature(request, pk):
    candidature = get_object_or_404(Candidature, pk=pk)

    # Vérifie si la session candidat correspond à la candidature
    if candidature.candidat.id != request.session.get('candidat_id'):
        messages.error(request, "Accès refusé.")
        return redirect('mes_candidatures')

    # Vérifie si le statut est encore modifiable
    if candidature.statut != "EN_ATTENTE":
        messages.error(request, "Vous ne pouvez pas modifier cette candidature.")
        return redirect('mes_candidatures')

    if request.method == 'POST':
        form = CandidatureForm(request.POST, instance=candidature)
        if form.is_valid():
            form.save()
            messages.success(request, "Candidature modifiée avec succès.")
            return redirect('mes_candidatures')
    else:
        form = CandidatureForm(instance=candidature)

    return render(request, 'candidature/modifier_candidature.html', {'form': form})
def supprimer_candidature(request, pk):
    candidature = get_object_or_404(Candidature, pk=pk)

    if candidature.candidat.id != request.session.get('candidat_id'):
        messages.error(request, "Accès refusé.")
        return redirect('mes_candidatures')

    if candidature.statut != "EN_ATTENTE":
        messages.error(request, "Vous ne pouvez pas supprimer cette candidature.")
        return redirect('mes_candidatures')

    if request.method == 'POST':
        candidature.delete()
        messages.success(request, "Candidature supprimée avec succès.")
        return redirect('mes_candidatures')

    return render(request, 'candidature/supprimer_candidature.html', {'candidature': candidature})
from django.shortcuts import render
from django.contrib import messages
from .models import Candidature

def lister_candidatures(request):
    # Récupère les candidatures du candidat authentifié
    candidat_id = request.session.get('candidat_id')
    if not candidat_id:
        messages.error(request, "Accès non autorisé.")
        return redirect('login')  # Ou rediriger vers une page d'erreur, selon ton système

    candidatures = Candidature.objects.filter(candidat_id=candidat_id)

    # Filtrer les candidatures avec le statut "EN_ATTENTE"
    candidatures_en_attente = candidatures.filter(statut="EN_ATTENTE")

    return render(request, 'candidature/lister_candidatures.html', {'candidatures': candidatures_en_attente})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Candidat
from .forms import CandidatForm

def profil_candidat(request):
    candidat_id = request.session.get('candidat_id')
    if not candidat_id:
        return redirect('login')  # Ou autre vue de connexion

    candidat = get_object_or_404(Candidat, id=candidat_id)

    if request.method == 'POST':
        form = CandidatForm(request.POST, request.FILES, instance=candidat)
        if form.is_valid():
            form.save()
            return redirect('profil')  # Redirige vers le profil après modification
    else:
        form = CandidatForm(instance=candidat)

    return render(request, 'candidat/profil.html', {'form': form})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Candidat, Offre
from .forms import CandidatForm, OffreForm

# Vue profil du candidat (inchangée)
def profil_candidat(request):
    candidat_id = request.session.get('candidat_id')
    if not candidat_id:
        return redirect('login')

    candidat = get_object_or_404(Candidat, id=candidat_id)

    if request.method == 'POST':
        form = CandidatForm(request.POST, request.FILES, instance=candidat)
        if form.is_valid():
            form.save()
            return redirect('profil')
    else:
        form = CandidatForm(instance=candidat)

    return render(request, 'candidat/profil.html', {'form': form})


# Vue pour afficher les offres de l'entreprise connectée
def entreprise_offres(request):
    entreprise_id = request.session.get('entreprise_id')
    if not entreprise_id:
        return redirect('entreprise_login')

    offres = Offre.objects.filter(entreprise_id=entreprise_id)
    return render(request, 'entrepriseoffres/liste.html', {'offres': offres})


# Vue pour créer une nouvelle offre
def entreprise_creer_offre(request):
    entreprise_id = request.session.get('entreprise_id')
    if not entreprise_id:
        return redirect('entreprise_login')

    if request.method == 'POST':
        form = OffreForm(request.POST)
        if form.is_valid():
            offre = form.save(commit=False)
            offre.entreprise_id = entreprise_id
            offre.save()
            return redirect('entreprise_offres')
    else:
        form = OffreForm()

    return render(request, 'entrepriseoffres/form.html', {'form': form})


# Vue pour modifier une offre existante
def entreprise_modifier_offre(request, offre_id):
    entreprise_id = request.session.get('entreprise_id')
    offre = get_object_or_404(Offre, pk=offre_id, entreprise_id=entreprise_id)

    if request.method == 'POST':
        form = OffreForm(request.POST, instance=offre)
        if form.is_valid():
            form.save()
            return redirect('entreprise_offres')
    else:
        form = OffreForm(instance=offre)

    return render(request, 'entrepriseoffres/form.html', {'form': form})


# Vue pour supprimer une offre
def entreprise_supprimer_offre(request, offre_id):
    entreprise_id = request.session.get('entreprise_id')
    offre = get_object_or_404(Offre, pk=offre_id, entreprise_id=entreprise_id)

    if request.method == 'POST':
        offre.delete()
        return redirect('entreprise_offres')

    return render(request, 'entrepriseoffres/confirm_suppression.html', {'offre': offre})
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404
from .models import Offre, Candidature

def entreprise_liste_candidatures(request):
    """
    Affiche toutes les candidatures reçues par l'entreprise connectée.
    """
    entreprise_id = request.session.get('entreprise_id')
    if not entreprise_id:
        return redirect('entreprise_login')  # Redirection si l'entreprise n'est pas connectée

    # Récupérer les offres appartenant à l'entreprise
    offres = Offre.objects.filter(entreprise_id=entreprise_id)

    # Récupérer toutes les candidatures liées à ces offres
    candidatures = Candidature.objects.filter(offre__in=offres).select_related('candidat', 'offre')

    return render(request, 'entrepriseoffres/candidatures.html', {
        'candidatures': candidatures
    })


def entreprise_telecharger_cv(request, candidature_id):
    """
    Permet à l'entreprise de télécharger le CV du candidat s’il existe.
    """
    entreprise_id = request.session.get('entreprise_id')
    if not entreprise_id:
        return redirect('entreprise_login')

    candidature = get_object_or_404(
        Candidature,
        pk=candidature_id,
        offre__entreprise_id=entreprise_id
    )

    candidat = candidature.candidat
    if not candidat.cv:
        raise Http404("Ce candidat n'a pas de CV.")

    return FileResponse(candidat.cv.open('rb'), as_attachment=True, filename=candidat.cv.name)
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404
from django.contrib import messages
from .models import Offre, Candidature

def entreprise_liste_candidatures(request):
    """
    Affiche toutes les candidatures reçues par l'entreprise connectée.
    """
    entreprise_id = request.session.get('entreprise_id')
    if not entreprise_id:
        return redirect('entreprise_login')

    offres = Offre.objects.filter(entreprise_id=entreprise_id)
    candidatures = Candidature.objects.filter(offre__in=offres).select_related('candidat', 'offre')

    return render(request, 'entrepriseoffres/candidatures.html', {
        'candidatures': candidatures,
         'statuts_choices': Candidature.STATUTS  # Ajoutez cette ligne
    })

def modifier_statut_candidature(request):
    """
    Modifie le statut d'une candidature via formulaire POST
    """
    if request.method == 'POST':
        entreprise_id = request.session.get('entreprise_id')
        if not entreprise_id:
            return redirect('entreprise_login')

        candidature_id = request.POST.get('candidature_id')
        nouveau_statut = request.POST.get('nouveau_statut')

        candidature = get_object_or_404(
            Candidature,
            pk=candidature_id,
            offre__entreprise_id=entreprise_id
        )

        # Vérifie que le nouveau statut est valide
        if nouveau_statut in dict(Candidature.STATUTS).keys():
            candidature.statut = nouveau_statut
            candidature.save()
            messages.success(request, "Statut mis à jour avec succès")
        else:
            messages.error(request, "Statut invalide")

    return redirect('entreprise_liste_candidaturesss')
from django.shortcuts import render, get_object_or_404
from .models import Candidat, Candidature
from django.shortcuts import render, get_object_or_404
from .models import Candidat, Candidature

def candidats_postules_view(request):
    niveau_etude = request.GET.get('niveau_etude')
    min_experience = request.GET.get('experience')

    candidats = Candidat.objects.filter(candidature__isnull=False).distinct()

    if niveau_etude:
        candidats = candidats.filter(niveau_etude=niveau_etude)

    if min_experience:
        try:
            min_experience = int(min_experience)
            candidats = candidats.filter(annee_experience__gte=min_experience)
        except ValueError:
            pass  # Ignore invalid input

    return render(request, 'candidats_postules.html', {
        'candidats': candidats,
        'niveau_etude': niveau_etude,
        'experience': min_experience,
    })


def detail_candidat_view(request, candidat_id):
    candidat = get_object_or_404(Candidat, id=candidat_id)
    candidatures = Candidature.objects.filter(candidat=candidat).select_related('offre')
    return render(request, 'detail_candidat.html', {'candidat': candidat, 'candidatures': candidatures})
import csv
from django.http import HttpResponse
from .models import Candidature

def export_candidats_csv(request):
    entreprise = request.session.get('entreprise_id')  # ou via request.user si auth
    if not entreprise:
        return HttpResponse("Non autorisé", status=401)

    # Filtrer les candidatures sur les offres de l'entreprise connectée
    candidatures = Candidature.objects.filter(offre__entreprise_id=entreprise).select_related('candidat', 'offre')

    # Créer une réponse CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="candidats_postules.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Nom', 'Prénom', 'Email', 'Téléphone', 'Adresse', 'Niveau d\'étude',
        'Année d\'expérience', 'Offre', 'Date de postulation', 'Statut'
    ])

    for c in candidatures:
        candidat = c.candidat
        writer.writerow([
            candidat.nom,
            candidat.prenom,
            candidat.email,
            candidat.telephone,
            candidat.adresse,
            candidat.niveau_etude,
            candidat.annee_experience,
            c.offre.titre,
            c.date_postulation.strftime("%Y-%m-%d %H:%M"),
            c.statut,
        ])

    return response
from django.shortcuts import render, redirect


from django.shortcuts import render, redirect
from .models import Admin
from .forms import LogineeeForm

def logineee_view(request):
    message = ''
    if request.method == 'POST':
        form = LogineeeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            mot_de_passe = form.cleaned_data['mot_de_passe']
            try:
                admin = Admin.objects.get(email=email, mot_de_passe=mot_de_passe)
                request.session['admin_id'] = admin.id  # Auth simple via session
                return redirect('dashboard')  # Redirige vers une page après connexion
            except Admin.DoesNotExist:
                message = "Identifiants invalides."
    else:
        form = LogineeeForm()
    return render(request, 'logine.html', {'form': form, 'message': message})
from django.shortcuts import render

def choix_login_view(request):
    return render(request, 'choix_login.html')
