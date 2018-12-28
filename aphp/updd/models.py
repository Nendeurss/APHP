from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _



class Structure(models.Model):
	nom = models.CharField(max_length=100)

class Hopital(models.Model):
	structure = models.OneToOneField("Structure", on_delete=models.CASCADE, primary_key=True)

class Pole(models.Model):
	structure = models.OneToOneField("Structure", on_delete=models.CASCADE, primary_key=True)
	hopital = models.ForeignKey("Hopital", on_delete=models.CASCADE)


class Service(models.Model):
	structure = models.OneToOneField("Structure", on_delete=models.CASCADE, primary_key=True)
	pole = models.ForeignKey("Pole", on_delete=models.CASCADE)

class UH(models.Model):
	structure = models.OneToOneField("Structure", on_delete=models.CASCADE, primary_key=True)
	service = models.ForeignKey("Service", on_delete=models.CASCADE)

class US(models.Model):
	structure = models.OneToOneField("Structure", on_delete=models.CASCADE, primary_key=True)
	uh = models.ForeignKey("UH", on_delete=models.CASCADE)

class Personnel(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	adresse = models.CharField(max_length=150)
	telephone = models.CharField(max_length=15)

class Medecin(models.Model):
	user = models.OneToOneField("Personnel", primary_key=True, on_delete=models.CASCADE)
	dirigep = models.OneToOneField("Pole",related_name=_("dirige_pole"), on_delete=models.CASCADE)
	diriges = models.OneToOneField("Service", related_name=_("dirige_service"), on_delete=models.CASCADE)
	dossiermedical = models.ForeignKey("DossierMedical", on_delete=models.CASCADE, verbose_name=_("Dossier medical"))

class Infirmier(models.Model):
	user = models.OneToOneField("Personnel", on_delete=models.CASCADE, primary_key=True)

class Secretaire(models.Model):
	user = models.OneToOneField("Personnel", on_delete=models.CASCADE, primary_key=True)

class Patient(models.Model):
	user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
	date_naissance = models.DateField(auto_now=True)
	telephone = models.CharField(max_length=15)
	adresse = models.CharField(max_length=150)
	numsecu = models.CharField(max_length=15)
	hospitalisation = models.ForeignKey("US", on_delete=models.CASCADE)


class DossierMedical(models.Model):
	patient = models.ForeignKey("Patient", on_delete=models.CASCADE )


class Document(models.Model):
	author = models.ForeignKey("Personnel", on_delete=models.CASCADE, verbose_name=_("Auteur"))
	dossier = models.ForeignKey("DossierMedical", on_delete=models.CASCADE)
	complet = models.BooleanField(default=False, verbose_name=_("Terminé"))
	date_creations = models.DateTimeField(auto_now=True)

class Diagnostic(models.Model):
	document = models.OneToOneField("Document", on_delete=models.CASCADE, primary_key=True)
	fichier = models.FileField()
	observation = models.TextField()

class Ordonnance(models.Model):
	document = models.OneToOneField("Document", on_delete=models.CASCADE, primary_key=True)
	texte = models.TextField(verbose_name=_("Contenu ordonnace"))

class Operation(models.Model):
	chir = _("Chirurgie")
	anest = _("Anesthésie")
	obst = _("Obstétrique")
	CHOICES = (
		(chir, chir),
		(anest, anest),
		(obst, obst),
		)
	document = models.OneToOneField("Document", on_delete=models.CASCADE, primary_key=True)
	types = models.CharField(max_length=20, verbose_name=_("Type de l'opération"))
	libelle = models.CharField(max_length=100, verbose_name=_("Libelle de l'opération"))

class Soin(models.Model):
	document = models.OneToOneField("Document", on_delete=models.CASCADE, primary_key=True)
	texte = models.TextField(verbose_name=_("Contenu fiche de soin"))
