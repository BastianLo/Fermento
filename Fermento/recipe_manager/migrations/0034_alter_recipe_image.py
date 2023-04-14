# Generated by Django 4.2 on 2023-04-14 08:38

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_manager', '0033_process_schedule_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=image_cropping.fields.ImageCropField(default='static/img/fermentation.png', upload_to='images/'),
        ),
    ]
