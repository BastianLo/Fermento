# Generated by Django 4.2 on 2023-04-19 09:29

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_manager', '0039_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=image_cropping.fields.ImageCropField(upload_to='images'),
        ),
    ]
