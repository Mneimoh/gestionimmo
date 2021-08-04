from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models.fields import PositiveIntegerField
from django.db.models.query import QuerySet
# Create your models here.

USER_POSTES = (
    ("accueuil", "accueuil"),
    ("transac", "transac"),
    ("caisse", "caisse"),
    ("recouvrement", "recouvrement"),
    ("N/A","N/A")
)


# Societe Models
class Societe(models.Model):
    nom             = models.CharField(max_length=60,default="N/A")
    localisation    = models.CharField(max_length=200,null=True)
    active          = models.BooleanField(default=False)
    date_created    = models.DateTimeField(verbose_name="Date Created",auto_now_add=True)

    def __str__(self):
        return self.nom


class UserManager(BaseUserManager):
    def create_user(self,email,username,password = None):
        print('------------------------------------')
        print('creating new user here')
        print('------------------------------------')

        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Users should have a username')
        user = self.model(
            email =self.normalize_email(email),
            username = username,
            )

        user.set_password(password)
        user.save(using = self._db)
        return user
 
    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        print('------------------------------------')
        print('creating staff user here')
        print('------------------------------------')
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password):
        print('*****   creating the supter user   ******')
        user = self.create_user(
            email =self.normalize_email(email),
            username = username,
            password = password
        )

        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using = self._db)
        return user

    

class User(AbstractBaseUser):
    username            = models.CharField(verbose_name="Name",max_length=255,unique=True)
    email               = models.EmailField(verbose_name="Email Address",max_length=60,unique=True,null=True)
    date_joined         = models.DateTimeField(verbose_name="Date joined",auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    last_login          = models.DateTimeField(verbose_name="Last login",auto_now=True)    
    is_admin            = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)
    is_staff            = models.BooleanField(default=True)
    is_superuser        = models.BooleanField(default=False)
    # societe             = models.IntegerField(default=0)
    societe             = models.ForeignKey(Societe, on_delete=models.CASCADE,null=True,blank=True)
    poste               = models.CharField(max_length=255,
                        choices=USER_POSTES,
                        default="N/A"
                        )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self,perm, obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True




class Place(models.Model):
    adresse = models.CharField(max_length=60)
    ville = models.CharField(max_length=30)
    code_postal = models.CharField(max_length=15)
    pays = models.CharField(max_length=20)
    anciennete = models.IntegerField()
    loyer = models.FloatField()
    residence = models.TextField()
    residence_actu = models.BooleanField(default=False)

    def __str__(self):
        return self.adresse


class Emploi(models.Model):
    denomination = models.CharField(max_length=60)
    nom_societe = models.CharField(max_length=60)
    adresse = models.CharField(max_length=60)
    ville = models.CharField(max_length=30)
    code_postal = models.CharField(max_length=15)
    pays = models.CharField(max_length=20)
    salaire_m = models.FloatField()
    anciennete = models.IntegerField()
    poste_actu = models.TextField()
    autre_revenu = models.BooleanField(default=False)
    autre_rev_sum = models.FloatField()

    def __str__(self):
        return self.denomination



class Endettement(models.Model):
    phone_emploi = models.CharField(max_length=15)
    nom_responsable = models.CharField(max_length=30)
    saisi = models.BooleanField(default=False)
    faillite = models.BooleanField(default=False)
    charge = models.BooleanField(default=False)
    charge_sum = models.FloatField()

    def __str__(self):
        return self.charge_sum


class CompteEndettement(models.Model):
    endettement = models.ForeignKey(Endettement, on_delete=models.CASCADE)
    nom_banque = models.CharField(max_length=60)
    type_compte = models.CharField(max_length=30)
    carte = models.BooleanField(default=False)
    nom_carte = models.CharField(max_length=40)

    def __str__(self):
        return self.nom_banque


class PretEndettement(models.Model):
    endettement = models.ForeignKey(Endettement, on_delete=models.CASCADE)
    nom_banque = models.CharField(max_length=60)
    type_pret = models.CharField(max_length=60)
    reste = models.FloatField()
    mensualite = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return self.nom_banque


class Client(models.Model):
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    num_client = models.CharField(max_length=10)
    statut = models.CharField(max_length=20)
    phone_1 = models.CharField(max_length=15)
    phone_2 = models.CharField(max_length=15)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    date_naissance = models.DateField()
    ville_naissance = models.CharField(max_length=20)
    pays_naissance = models.CharField(max_length=20)
    type_piece_id = models.CharField(max_length=30)
    numero_piece_id = models.CharField(max_length=10)
    date_delivrance_id = models.DateField()
    num_client_2 = models.CharField(max_length=10)
    proprietaire = models.BooleanField(default=False)
    how_connu = models.TextField()
    nom_boutique = models.CharField(max_length=40)
    num_ref = models.CharField(max_length=10)
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    emploi = models.OneToOneField(
        Emploi,
        on_delete=models.CASCADE,
        primary_key=False,
    )
    endettement = models.OneToOneField(
        Endettement,
        on_delete=models.CASCADE,
        primary_key=False,
    )

    def __str__(self):
        return self.nom


class Dossier(models.Model):
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20)
    article_interet = models.CharField(max_length=40)
    frais_dossier = models.FloatField()
    frais_montage = models.FloatField()
    frais_immat = models.FloatField()
    autres_tax = models.FloatField()
    frais_livraison = models.FloatField()
    frais_desendet = models.FloatField()
    frais_autres = models.FloatField()
    coeff_recouv = models.FloatField()
    appele_recouvre = models.BooleanField(default=False)
    pin = models.IntegerField()
    dernier_appel = models.DateTimeField()
    verifie = models.BooleanField(default=False)

    def __str__(self):
        return self.pin


class Article(models.Model):
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    type_article = models.CharField(max_length=60)
    num_type = models.IntegerField()
    nom = models.CharField(max_length=60)
    denomination = models.CharField(max_length=60)
    num_stock = models.CharField(max_length=10)
    valeur = models.FloatField()
    date_achat = models.DateField()
    date_dernier_paiement = models.DateField()
    accompte = models.FloatField()
    statut = models.CharField(max_length=20)
    #statut_final = models.CharField(max_length=20)

    def __str__(self):
        return self.nom

class Facture(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    User_editeur = models.ForeignKey(User, on_delete=models.CASCADE)
    statut = models.CharField(max_length=60)
    num_facture = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.num_facture


class Paiement(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    User_encaisseur = models.ForeignKey(User, on_delete=models.CASCADE)
    somme = models.FloatField()
    num_transaction = models.CharField(max_length=10)
    date_paiement = models.DateField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.num_transaction


class TypeArticleImmobilier(models.Model):
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE)
    site = models.CharField(max_length=60)
    dimension = models.IntegerField()
    situation = models.TextField()
    doc_1 = models.ImageField(upload_to="static/menu/images")
    doc_2 = models.ImageField(upload_to="static/menu/images")
    doc_3 = models.ImageField(upload_to="static/menu/images")
    nom_cite = models.CharField(max_length=60)
    batiment = models.CharField(max_length=60)
    inexistant = models.BooleanField(default=False)
    etage = models.IntegerField()
    porte = models.CharField(max_length=5)
    plan_masse_local = models.ImageField(upload_to="static/menu/images")

    def __str__(self):
        return self.site


class TypeArticleMoto(models.Model):
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE)
    modele = models.CharField(max_length=60)
    marque = models.CharField(max_length=60)
    code = models.CharField(max_length=60)
    couleur = models.CharField(max_length=60)

    def __str__(self):
        return self.modele


class Penalite(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    emetteur = models.ForeignKey(User, on_delete=models.CASCADE)
    somme_attendue = models.FloatField()
    num_penal = models.IntegerField()
    User_encaisseur = models.CharField(max_length=10)
    statut = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.num_penal


class Credit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    emetteur = models.ForeignKey(User, on_delete=models.CASCADE)
    montant = models.FloatField()
    taux = models.FloatField()
    apport = models.FloatField()
    date_emission = models.DateField()
    date_fin = models.DateField()
    frais_dossier = models.FloatField()
    autre_frais = models.FloatField()
    subvention = models.FloatField()
    accompte = models.FloatField()
    date_signature = models.DateField()
    somme_payee = models.FloatField()
    pre_qual = models.BooleanField(default=False)
    struct_pret = models.BooleanField(default=False)
    application_credit = models.BooleanField(default=False)
    autorisation_etude = models.BooleanField(default=False)
    notification_cosign = models.BooleanField(default=False)
    ref_acheteur = models.BooleanField(default=False)
    verif_pro = models.BooleanField(default=False)
    aut_paiement_source = models.BooleanField(default=False)
    aut_prel_bk = models.BooleanField(default=False)
    aut_prel_cb = models.BooleanField(default=False)
    lettre_eng = models.BooleanField(default=False)
    plan_dom = models.BooleanField(default=False)
    certif_res = models.BooleanField(default=False)
    phot_fact = models.BooleanField(default=False)
    att_heberg = models.BooleanField(default=False)
    photo_id = models.BooleanField(default=False)
    photoc_piece_id = models.BooleanField(default=False)
    fdp = models.BooleanField(default=False)
    photoc_crt_pro = models.BooleanField(default=False)
    reg_comm = models.BooleanField(default=False)
    rdb = models.BooleanField(default=False)
    attest_rev = models.BooleanField(default=False)
    carte_ret = models.BooleanField(default=False)
    facture = models.BooleanField(default=False)
    protect_vie = models.BooleanField(default=False)
    protect_empl = models.BooleanField(default=False)
    protoc_accord = models.BooleanField(default=False)
    cond_resp_financ = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.article


class Assurance(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    emetteur = models.ForeignKey(User, on_delete=models.CASCADE)
    statut = models.CharField(max_length=60)
    nom = models.CharField(max_length=60)
    adresse = models.CharField(max_length=60)
    ville = models.CharField(max_length=60)
    cp = models.CharField(max_length=60)
    pays = models.CharField(max_length=60)
    phone = models.CharField(max_length=60)
    num_police = models.CharField(max_length=60)
    somme = models.FloatField()
    date_emission = models.DateField()
    date_fin = models.DateField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


class Recouvrement(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date = models.DateField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.article


class ProcedureContact(models.Model):
    recouvrement = models.ForeignKey(Recouvrement, on_delete=models.CASCADE)
    emetteur = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=60)
    annotation = models.TextField()
    message = models.TextField()
    date_emission = models.DateField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.recouvrement


class Campagne(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    objet = models.CharField(max_length=200)
    type = models.CharField(max_length=60)
    periodicite = models.CharField(max_length=60)
    date_lancement = models.DateTimeField()
    Cible = models.TextField()
    Contenu = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.objet


class ClientAppel(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_ap = models.DateTimeField()
    obtention = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client


class ClientAnnotation(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    statut = models.CharField(max_length=60)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client


class ClientAnnotationContenu(models.Model):
    client_annotation = models.ForeignKey(ClientAnnotation, on_delete=models.CASCADE)
    date_ap = models.DateTimeField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client_annotation


class ClientAnnotationContenuMessage(models.Model):
    client_annotation_contenu = models.ForeignKey(ClientAnnotationContenu, on_delete=models.CASCADE)
    Message = models.TextField()
    date_ap = models.DateTimeField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client_annotation_contenu


class Dadsr(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    info = models.TextField()
    statut_1 = models.BooleanField(default=False)
    num_courrier = models.CharField(max_length=10)
    date_courrier = models.DateField()
    contenu = models.TextField()
    statut_trait_cour = models.CharField(max_length=60)
    statut_2 = models.CharField(max_length=60)
    statut_3 = models.CharField(max_length=60)
    date_enr = models.DateTimeField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.article
