# Generated by Django 4.2 on 2023-04-27 21:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('batches', '0016_alter_qrcode_jar_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcode',
            name='batch',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                       to='batches.batch'),
        ),
    ]
