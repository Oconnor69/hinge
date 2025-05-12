# models.py
from django.db import models

class Entreprise(models.Model):
    nom = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', blank=True)
    description = models.TextField(blank=True)
    email = models.EmailField(max_length=191, unique=True,  default="default")
    mot_de_passe = models.CharField(max_length=128, default="default")

    def __str__(self):
        return self.nom
class Admin(models.Model):
    email = models.EmailField(max_length=191, unique=True,  default="default")
    mot_de_passe = models.CharField(max_length=128, default="default")
    def __str__(self):
        return self.email 
from django.db import models

class Offre(models.Model):
    titre = models.CharField(max_length=100)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    description = models.TextField()
    categorie = models.CharField(
        max_length=50,
        choices=[
            ('INFORMATIQUE', 'Informatique'),
            ('MARKETING', 'Marketing'),
            ('RESSOURCES_HUMAINES', 'Ressources Humaines'),
            ('FINANCE', 'Finance'),
            ('AUTRE', 'Autre'),
        ],
        default='AUTRE'
    )
    exigences = models.TextField(blank=True, null=True)  # Champs pour les requirements
    salaire= models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    type_contrat = models.CharField(
        max_length=50,
        choices=[
            ('CDI', 'CDI'),
            ('CDD', 'CDD'),
            ('Stage', 'Stage'),
            ('Freelance', 'Freelance'),
            ('Alternance', 'Alternance'),
        ],
        blank=True,
        null=True
    )
    localisation = models.CharField(max_length=100, blank=True, null=True)
    date_publication = models.DateField(auto_now_add=True)
    date_expiration = models.DateField()
    experience_requise = models.CharField(max_length=100, blank=True, null=True)  # Ex: "2 ans", "Débutant accepté"
    niveau_etude = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Ex : Bac+3, Bac+5, Master, Doctorat, etc."
    )


    def __str__(self):
        return self.titre

class Candidat(models.Model):
    
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(max_length=191, unique=True)
    mot_de_passe = models.CharField(max_length=128, default="default")
    date_naissance = models.DateField(null=True, blank=True)
    sexe = models.CharField(
        max_length=10,
        choices=[
            ('HOMME', 'Homme'),
            ('FEMME', 'Femme'),
            ('AUTRE', 'Autre'),
        ],
        default='AUTRE'
    )
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    niveau_etude = models.CharField(
        max_length=100,
        choices=[
            ('BAC', 'Baccalauréat'),
            ('BAC+2', 'Bac +2'),
            ('BAC+3', 'Bac +3'),
            ('BAC+5', 'Bac +5'),
            ('DOCTORAT', 'Doctorat'),
            ('AUTRE', 'Autre'),
        ],
        default='BAC'
    )
    annee_experience = models.PositiveIntegerField(default=0)
    certificat = models.FileField(upload_to='certificats/', blank=True, null=True)
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
  
  
    
    # Méthodes pour simuler l'interface User
    def is_authenticated(self):
        return True
    
    class Meta:
        verbose_name = "Candidat"
        verbose_name_plural = "Candidats"

    def __str__(self):
        return f"{self.prenom} {self.nom}"
class Candidature(models.Model):
    STATUTS = [
        ('EN_ATTENTE', 'En attente'),
        ('ACCEPTEE', 'Acceptée'),
        ('REFUSEE', 'Refusée'),
    ]
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    date_postulation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='EN_ATTENTE')

    def __str__(self):
        return f"{self.candidat} → {self.offre}"