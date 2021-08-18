# Generated by Django 3.2.5 on 2021-08-18 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_dossier_paiement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date_arrivee',
            field=models.DateField(default='12-09-2020', null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='nom',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='num_client',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='prenom',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='telephone',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='article',
            name='frais_montage',
            field=models.FloatField(default=60000),
        ),
        migrations.AlterField(
            model_name='article',
            name='num_stock',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='article',
            name='statut',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='campagne',
            name='objet',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='client',
            name='nom',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='pays_naissance',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone_1',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone_2',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='prenom',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='statut',
            field=models.CharField(default='P1', max_length=60),
        ),
        migrations.AlterField(
            model_name='client',
            name='type_piece_id',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='ville_naissance',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='compteendettement',
            name='nom_compte',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='compteendettement',
            name='type_compte',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='cosignataire',
            name='nom',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='cosignataire',
            name='numero_piece_id',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='cosignataire',
            name='pays_naissance',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='cosignataire',
            name='phone_1',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='cosignataire',
            name='phone_2',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='cosignataire',
            name='prenom',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='cosignataire',
            name='type_piece_id',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='cosignataire',
            name='ville_naissance',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='dadsr',
            name='num_courrier',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='dossier',
            name='statut',
            field=models.CharField(default='A', max_length=60),
        ),
        migrations.AlterField(
            model_name='emploi',
            name='ancien_code_postal',
            field=models.CharField(max_length=65, null=True),
        ),
        migrations.AlterField(
            model_name='emploi',
            name='ancien_pays',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='emploi',
            name='ancien_ville',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='emploi',
            name='code_postal',
            field=models.CharField(max_length=65, null=True),
        ),
        migrations.AlterField(
            model_name='emploi',
            name='pays',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='emploi',
            name='ville',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='endettement',
            name='nom_responsable',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='endettement',
            name='phone_emploi',
            field=models.CharField(max_length=65),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='num_transaction',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='penalite',
            name='User_encaisseur',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='place',
            name='ancienne_code_postal',
            field=models.CharField(max_length=65, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='ancienne_pays',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='ancienne_ville',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='code_postal',
            field=models.CharField(max_length=65, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='pays',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='ville',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='societe',
            name='address',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='societe',
            name='code_postal',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='societe',
            name='pays',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='societe',
            name='telephone',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='societe',
            name='ville',
            field=models.CharField(max_length=60, null=True),
        ),
    ]