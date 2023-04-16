# Generated by Django 4.2 on 2023-04-15 13:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batch_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QrCode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=2000)),
                ('batch', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='batches.batch')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qrcode_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
