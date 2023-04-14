# Generated by Django 4.2 on 2023-04-14 09:00

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_manager', '0037_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=image_cropping.fields.ImageCropField(blank=True, upload_to='images/dynamic'),
        ),
    ]
