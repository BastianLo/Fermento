# Generated by Django 4.2 on 2023-04-15 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('batches', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcode',
            name='batch',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='batches.batch'),
        ),
    ]