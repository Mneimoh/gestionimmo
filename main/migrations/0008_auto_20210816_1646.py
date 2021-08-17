# Generated by Django 3.2.5 on 2021-08-16 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_facture_date_dernier_paiement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facture',
            name='date_dernier_paiement',
        ),
        migrations.AddField(
            model_name='dossier',
            name='date_dernier_paiement',
            field=models.DateField(blank=True, null=True),
        ),
    ]
