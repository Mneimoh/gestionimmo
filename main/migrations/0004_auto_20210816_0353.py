# Generated by Django 3.2.5 on 2021-08-16 02:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210816_0053'),
    ]

    operations = [
        migrations.AddField(
            model_name='dossier',
            name='facture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.facture'),
        ),
        migrations.AlterField(
            model_name='dossier',
            name='User',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='dossier',
            name='article_interet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.article'),
        ),
        migrations.AlterField(
            model_name='dossier',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.client'),
        ),
        migrations.AlterField(
            model_name='dossier',
            name='societe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.societe'),
        ),
    ]