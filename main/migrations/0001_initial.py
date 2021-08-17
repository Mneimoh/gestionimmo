# Generated by Django 3.2.5 on 2021-08-12 22:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('email', models.EmailField(max_length=60, null=True, unique=True, verbose_name='Email Address')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date joined')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('poste', models.CharField(choices=[('accueuil', 'accueuil'), ('transac', 'transac'), ('caisse', 'caisse'), ('recouvrement', 'recouvrement'), ('N/A', 'N/A')], default='N/A', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_article', models.CharField(blank=True, max_length=60, null=True)),
                ('num_type', models.IntegerField(blank=True, null=True)),
                ('nom', models.CharField(blank=True, max_length=60, null=True)),
                ('denomination', models.CharField(blank=True, max_length=60, null=True)),
                ('num_stock', models.CharField(max_length=10)),
                ('valeur', models.FloatField(blank=True, null=True)),
                ('date_achat', models.DateField(blank=True, null=True)),
                ('date_dernier_paiement', models.DateField(blank=True, null=True)),
                ('accompte', models.FloatField(blank=True, null=True)),
                ('statut', models.CharField(max_length=20, null=True)),
                ('frais_dossier', models.FloatField(blank=True, null=True)),
                ('frais_montage', models.FloatField(blank=True, null=True)),
                ('frais_immat', models.FloatField(blank=True, null=True)),
                ('autres_tax', models.FloatField(blank=True, null=True)),
                ('frais_livraison', models.FloatField(blank=True, null=True)),
                ('frais_desendet', models.FloatField(blank=True, null=True)),
                ('frais_autres', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClientAnnotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statut', models.CharField(max_length=60)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ClientAnnotationContenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ap', models.DateTimeField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('client_annotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.clientannotation')),
            ],
        ),
        migrations.CreateModel(
            name='Emploi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denomination', models.CharField(max_length=60, null=True)),
                ('nom_societe', models.CharField(max_length=60, null=True)),
                ('adresse', models.CharField(max_length=60, null=True)),
                ('ville', models.CharField(max_length=30, null=True)),
                ('code_postal', models.CharField(max_length=15, null=True)),
                ('pays', models.CharField(max_length=20, null=True)),
                ('salaire_m', models.FloatField(null=True)),
                ('anciennete', models.IntegerField(null=True)),
                ('poste_actu', models.TextField(null=True)),
                ('autre_revenu', models.BooleanField(default=False, null=True)),
                ('autre_rev_sum', models.FloatField(null=True)),
                ('ancien_denomination', models.CharField(max_length=60, null=True)),
                ('ancien_nom_societe', models.CharField(max_length=60, null=True)),
                ('ancien_adresse', models.CharField(max_length=60, null=True)),
                ('ancien_ville', models.CharField(max_length=30, null=True)),
                ('ancien_code_postal', models.CharField(max_length=15, null=True)),
                ('ancien_pays', models.CharField(max_length=20, null=True)),
                ('ancien_salaire_m', models.FloatField(null=True)),
                ('ancien_anciennete', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Endettement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_emploi', models.CharField(max_length=15)),
                ('nom_responsable', models.CharField(max_length=30)),
                ('saisi', models.BooleanField(default=False)),
                ('faillite', models.BooleanField(default=False)),
                ('charge', models.BooleanField(default=False)),
                ('charge_sum', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statut', models.CharField(max_length=60)),
                ('num_facture', models.CharField(max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('User_editeur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.article')),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresse', models.CharField(max_length=60, null=True)),
                ('ville', models.CharField(max_length=30, null=True)),
                ('code_postal', models.CharField(max_length=15, null=True)),
                ('pays', models.CharField(max_length=20, null=True)),
                ('anciennete', models.IntegerField(null=True)),
                ('loyer', models.FloatField(null=True)),
                ('residence', models.TextField(null=True)),
                ('residence_actu', models.BooleanField(default=False, null=True)),
                ('ancienne_address', models.BooleanField(default=False, null=True)),
                ('ancienne_ville', models.CharField(max_length=30, null=True)),
                ('ancienne_code_postal', models.CharField(max_length=15, null=True)),
                ('ancienne_pays', models.CharField(max_length=20, null=True)),
                ('ancienne_anciennete', models.IntegerField(null=True)),
                ('ancienne_loyer', models.FloatField(null=True)),
                ('ancienne_residence', models.TextField(null=True)),
                ('ancienne_residence_actu', models.BooleanField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Societe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(default='N/A', max_length=60)),
                ('localisation', models.CharField(max_length=200, null=True)),
                ('active', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('address', models.CharField(max_length=20, null=True)),
                ('code_postal', models.CharField(max_length=20, null=True)),
                ('pays', models.CharField(max_length=20, null=True)),
                ('ville', models.CharField(max_length=20, null=True)),
                ('telephone', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('email', models.EmailField(blank=True, max_length=60, null=True, verbose_name='Email Address')),
                ('phone_1', models.CharField(blank=True, max_length=15, null=True)),
                ('phone_2', models.CharField(blank=True, max_length=15, null=True)),
                ('nom', models.CharField(blank=True, max_length=30, null=True)),
                ('prenom', models.CharField(blank=True, max_length=30, null=True)),
                ('date_naissance', models.DateField(null=True)),
                ('ville_naissance', models.CharField(blank=True, max_length=20, null=True)),
                ('pays_naissance', models.CharField(blank=True, max_length=20, null=True)),
                ('type_piece_id', models.CharField(blank=True, max_length=30, null=True)),
                ('numero_piece_id', models.CharField(blank=True, max_length=10, null=True)),
                ('proprietaire', models.BooleanField(default=False)),
                ('parents', models.BooleanField(default=False)),
                ('how_connu', models.TextField()),
                ('statut', models.CharField(default='P1', max_length=20)),
                ('uid', models.IntegerField(default=0, unique=True)),
                ('place', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='main.place')),
            ],
        ),
        migrations.CreateModel(
            name='TypeArticleMoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modele', models.CharField(max_length=60)),
                ('marque', models.CharField(max_length=60)),
                ('code', models.CharField(max_length=60)),
                ('couleur', models.CharField(max_length=60)),
                ('societe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.societe')),
            ],
        ),
        migrations.CreateModel(
            name='TypeArticleImmobilier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.CharField(max_length=60)),
                ('dimension', models.IntegerField()),
                ('situation', models.TextField()),
                ('doc_1', models.ImageField(upload_to='static/menu/images')),
                ('doc_2', models.ImageField(upload_to='static/menu/images')),
                ('doc_3', models.ImageField(upload_to='static/menu/images')),
                ('nom_cite', models.CharField(max_length=60)),
                ('batiment', models.CharField(max_length=60)),
                ('inexistant', models.BooleanField(default=False)),
                ('etage', models.IntegerField()),
                ('porte', models.CharField(max_length=5)),
                ('plan_masse_local', models.ImageField(upload_to='static/menu/images')),
                ('societe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.societe')),
            ],
        ),
        migrations.CreateModel(
            name='Recouvrement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.article')),
            ],
        ),
        migrations.CreateModel(
            name='ProcedureContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=60)),
                ('annotation', models.TextField()),
                ('message', models.TextField()),
                ('date_emission', models.DateField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('emetteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recouvrement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.recouvrement')),
            ],
        ),
        migrations.CreateModel(
            name='PretEndettement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_banque', models.CharField(max_length=60)),
                ('type_pret', models.CharField(max_length=60)),
                ('reste', models.FloatField()),
                ('mensualite', models.FloatField()),
                ('nom_banque_1', models.CharField(max_length=60, null=True)),
                ('type_pret_1', models.CharField(max_length=60, null=True)),
                ('reste_1', models.FloatField(null=True)),
                ('mensualite_1', models.FloatField(null=True)),
                ('nom_banque_2', models.CharField(max_length=60, null=True)),
                ('type_pret_2', models.CharField(max_length=60, null=True)),
                ('reste_2', models.FloatField(null=True)),
                ('mensualite_2', models.FloatField(null=True)),
                ('date', models.DateField(null=True)),
                ('endettement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.endettement')),
            ],
        ),
        migrations.CreateModel(
            name='Penalite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('somme_attendue', models.FloatField()),
                ('num_penal', models.IntegerField()),
                ('User_encaisseur', models.CharField(max_length=10)),
                ('statut', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('emetteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.facture')),
            ],
        ),
        migrations.CreateModel(
            name='Paiement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('somme', models.FloatField()),
                ('num_transaction', models.CharField(max_length=10)),
                ('date_paiement', models.DateField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('User_encaisseur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.facture')),
            ],
        ),
        migrations.CreateModel(
            name='Dadsr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField()),
                ('statut_1', models.BooleanField(default=False)),
                ('num_courrier', models.CharField(max_length=10)),
                ('date_courrier', models.DateField()),
                ('contenu', models.TextField()),
                ('statut_trait_cour', models.CharField(max_length=60)),
                ('statut_2', models.CharField(max_length=60)),
                ('statut_3', models.CharField(max_length=60)),
                ('date_enr', models.DateTimeField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.article')),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.facture')),
            ],
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.FloatField()),
                ('taux', models.FloatField()),
                ('apport', models.FloatField()),
                ('date_emission', models.DateField()),
                ('date_fin', models.DateField()),
                ('frais_dossier', models.FloatField()),
                ('autre_frais', models.FloatField()),
                ('subvention', models.FloatField()),
                ('accompte', models.FloatField()),
                ('date_signature', models.DateField()),
                ('somme_payee', models.FloatField()),
                ('pre_qual', models.BooleanField(default=False)),
                ('struct_pret', models.BooleanField(default=False)),
                ('application_credit', models.BooleanField(default=False)),
                ('autorisation_etude', models.BooleanField(default=False)),
                ('notification_cosign', models.BooleanField(default=False)),
                ('ref_acheteur', models.BooleanField(default=False)),
                ('verif_pro', models.BooleanField(default=False)),
                ('aut_paiement_source', models.BooleanField(default=False)),
                ('aut_prel_bk', models.BooleanField(default=False)),
                ('aut_prel_cb', models.BooleanField(default=False)),
                ('lettre_eng', models.BooleanField(default=False)),
                ('plan_dom', models.BooleanField(default=False)),
                ('certif_res', models.BooleanField(default=False)),
                ('phot_fact', models.BooleanField(default=False)),
                ('att_heberg', models.BooleanField(default=False)),
                ('photo_id', models.BooleanField(default=False)),
                ('photoc_piece_id', models.BooleanField(default=False)),
                ('fdp', models.BooleanField(default=False)),
                ('photoc_crt_pro', models.BooleanField(default=False)),
                ('reg_comm', models.BooleanField(default=False)),
                ('rdb', models.BooleanField(default=False)),
                ('attest_rev', models.BooleanField(default=False)),
                ('carte_ret', models.BooleanField(default=False)),
                ('facture', models.BooleanField(default=False)),
                ('protect_vie', models.BooleanField(default=False)),
                ('protect_empl', models.BooleanField(default=False)),
                ('protoc_accord', models.BooleanField(default=False)),
                ('cond_resp_financ', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.article')),
                ('emetteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CompteEndettement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_banque', models.CharField(max_length=60)),
                ('type_compte', models.CharField(max_length=30)),
                ('compte', models.BooleanField(default=False)),
                ('nom_compte', models.CharField(max_length=40, null=True)),
                ('endettement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.endettement')),
            ],
        ),
        migrations.CreateModel(
            name='ClientAnnotationContenuMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Message', models.TextField()),
                ('date_ap', models.DateTimeField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('client_annotation_contenu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.clientannotationcontenu')),
            ],
        ),
        migrations.CreateModel(
            name='Campagne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objet', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=60)),
                ('periodicite', models.CharField(max_length=60)),
                ('date_lancement', models.DateTimeField()),
                ('Cible', models.TextField()),
                ('Contenu', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Assurance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statut', models.CharField(max_length=60)),
                ('nom', models.CharField(max_length=60)),
                ('adresse', models.CharField(max_length=60)),
                ('ville', models.CharField(max_length=60)),
                ('cp', models.CharField(max_length=60)),
                ('pays', models.CharField(max_length=60)),
                ('phone', models.CharField(max_length=60)),
                ('num_police', models.CharField(max_length=60)),
                ('somme', models.FloatField()),
                ('date_emission', models.DateField()),
                ('date_fin', models.DateField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.article')),
                ('emetteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='societe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.societe'),
        ),
        migrations.CreateModel(
            name='Dossier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statut', models.CharField(default='A', max_length=20)),
                ('coeff_recouv', models.FloatField(default=0)),
                ('appele_recouvre', models.BooleanField(default=False)),
                ('pin', models.IntegerField(default=0)),
                ('dernier_appel', models.DateTimeField(auto_now_add=True, null=True)),
                ('verifie', models.BooleanField(default=False)),
                ('uid', models.IntegerField(null=True, unique=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('article_interet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.article')),
                ('societe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.societe')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.client')),
            ],
        ),
        migrations.CreateModel(
            name='Cosignataire',
            fields=[
                ('email', models.EmailField(blank=True, max_length=60, null=True, verbose_name='Email Address')),
                ('phone_1', models.CharField(blank=True, max_length=15, null=True)),
                ('phone_2', models.CharField(blank=True, max_length=15, null=True)),
                ('nom', models.CharField(blank=True, max_length=30, null=True)),
                ('prenom', models.CharField(blank=True, max_length=30, null=True)),
                ('date_naissance', models.DateField(null=True)),
                ('ville_naissance', models.CharField(blank=True, max_length=20, null=True)),
                ('pays_naissance', models.CharField(blank=True, max_length=20, null=True)),
                ('type_piece_id', models.CharField(blank=True, max_length=30, null=True)),
                ('numero_piece_id', models.CharField(blank=True, max_length=10, null=True)),
                ('proprietaire', models.BooleanField(default=False)),
                ('parents', models.BooleanField(default=False)),
                ('how_connu', models.TextField()),
                ('place', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='main.place')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('emploi', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.emploi')),
                ('endettement', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.endettement')),
                ('societe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.societe')),
            ],
        ),
        migrations.CreateModel(
            name='ClientAppel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ap', models.DateTimeField()),
                ('obtention', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.client')),
            ],
        ),
        migrations.AddField(
            model_name='clientannotation',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.client'),
        ),
        migrations.AddField(
            model_name='client',
            name='User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='client',
            name='cosigner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.cosignataire'),
        ),
        migrations.AddField(
            model_name='client',
            name='emploi',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.emploi'),
        ),
        migrations.AddField(
            model_name='client',
            name='endettement',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.endettement'),
        ),
        migrations.AddField(
            model_name='client',
            name='societe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.societe'),
        ),
    ]