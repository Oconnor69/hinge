from django import forms
from .models import Entreprise, Offre, Candidat, Candidature

class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ['nom', 'logo', 'description']


class OffreForm(forms.ModelForm):
    class Meta:
        model = Offre
        fields = [
            'titre',
            'entreprise',
            'description',
            'categorie',
            'exigences',
            'salaire',
            'type_contrat',
            'localisation',
            'date_expiration',
            'experience_requise',
            'niveau_etude',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'exigences': forms.Textarea(attrs={'rows': 3}),
            'date_expiration': forms.DateInput(attrs={'type': 'date'}),
        }


class CandidatForm(forms.ModelForm):
    class Meta:
        model = Candidat
        fields = '__all__'
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }


class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['candidat', 'offre', 'statut']
from django import forms
from django import forms
from .models import Entreprise
from django.contrib.auth.hashers import make_password
from .models import Candidat
from django.contrib.auth.hashers import make_password, check_password

from django import forms
from .models import Candidat
from django.contrib.auth.hashers import make_password

class RegisterForm(forms.ModelForm):
    mot_de_passe = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    confirmation = forms.CharField(widget=forms.PasswordInput, label="Confirmation")
    date_naissance = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label="Date de naissance"
    )
    class Meta:
        model = Candidat
        fields = [
            'nom', 'prenom', 'email', 'mot_de_passe', 'confirmation',
            'date_naissance', 'sexe', 'telephone', 'adresse',
            'niveau_etude', 'annee_experience', 'certificat', 'cv'
        ]

    def clean(self):
        cleaned_data = super().clean()
        mdp = cleaned_data.get("mot_de_passe")
        conf = cleaned_data.get("confirmation")

        if mdp != conf:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        cleaned_data['mot_de_passe'] = make_password(mdp)
        return cleaned_data



class LoginForm(forms.Form):
    email = forms.EmailField()
    mot_de_passe = forms.CharField(widget=forms.PasswordInput)
from django import forms
from .models import Entreprise
from django.contrib.auth.hashers import make_password

class EntrepriseRegisterForm(forms.ModelForm):
    mot_de_passe = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    confirmation = forms.CharField(widget=forms.PasswordInput, label="Confirmation du mot de passe")

    class Meta:
        model = Entreprise
        fields = ['nom', 'logo', 'description', 'email', 'mot_de_passe', 'confirmation']

    def clean(self):
        cleaned_data = super().clean()
        mot_de_passe = cleaned_data.get("mot_de_passe")
        confirmation = cleaned_data.get("confirmation")

        if mot_de_passe != confirmation:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        
        cleaned_data['mot_de_passe'] = make_password(mot_de_passe)  # Hasher le mot de passe
        return cleaned_data

class EntrepriseLoginForm(forms.Form):
    email = forms.EmailField()
    mot_de_passe = forms.CharField(widget=forms.PasswordInput)
from django import forms
from .models import Candidat

class CandidatForm(forms.ModelForm):
    class Meta:
        model = Candidat
        fields = '__all__'
from django import forms
from .models import Offre

class OffreForm(forms.ModelForm):
    class Meta:
        model = Offre
        exclude = ['entreprise', 'date_publication']
        widgets = {
            'date_expiration': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms

class LogineeeForm(forms.Form):
    email = forms.EmailField(label="Email")
    mot_de_passe = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
