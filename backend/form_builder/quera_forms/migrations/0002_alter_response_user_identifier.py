# Generated by Django 5.0.10 on 2024-12-12 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quera_forms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='user_identifier',
            field=models.EmailField(max_length=254, verbose_name='User Email'),
        ),
    ]