from django.db import models

# Create your models here.

class Societe(models.Model):
    nom = models.CharField(max_length=60)
    localisation = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    date_creation = models.DateField()

    def __str__(self):
        return self.nom



class BasicUser(models.Model):
    societe = models.IntegerField(default=0)
    login = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    email = models.EmailField(max_length=60)
    active = models.BooleanField(default=False)

    class Meta:
        abstract = True


class User(BasicUser):
    poste = models.CharField(max_length=15)
    date_creation = models.DateField()

    def __str__(self):
        return self.login


class Agent(BasicUser):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    statut = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


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
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
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
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
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
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
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
    agent_editeur = models.ForeignKey(Agent, on_delete=models.CASCADE)
    statut = models.CharField(max_length=60)
    num_facture = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.num_facture


class Paiement(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    agent_encaisseur = models.ForeignKey(Agent, on_delete=models.CASCADE)
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
    emetteur = models.ForeignKey(Agent, on_delete=models.CASCADE)
    somme_attendue = models.FloatField()
    num_penal = models.IntegerField()
    agent_encaisseur = models.CharField(max_length=10)
    statut = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.num_penal


class Credit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    emetteur = models.ForeignKey(Agent, on_delete=models.CASCADE)
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
    emetteur = models.ForeignKey(Agent, on_delete=models.CASCADE)
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
    emetteur = models.ForeignKey(Agent, on_delete=models.CASCADE)
    type = models.CharField(max_length=60)
    annotation = models.TextField()
    message = models.TextField()
    date_emission = models.DateField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.recouvrement


class Campagne(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
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
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_ap = models.DateTimeField()
    article_interet = models.CharField(max_length=60, default='maison')
    date_rendezvous = models.DateField( default= None)
    obtention = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client


class ClientAnnotation(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
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
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
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
