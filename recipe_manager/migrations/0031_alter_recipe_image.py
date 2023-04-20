# Generated by Django 4.2 on 2023-04-10 11:20

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_manager', '0030_recipe_cropping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=image_cropping.fields.ImageCropField(upload_to='images/'),
        ),
    ]