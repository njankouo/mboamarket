# Generated by Django 4.2.17 on 2025-04-16 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctn_bpf', '0003_institution_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='numero_whatsapp',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
