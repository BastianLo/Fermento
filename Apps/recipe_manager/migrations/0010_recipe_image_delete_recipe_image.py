# Generated by Django 4.2 on 2023-04-05 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_manager', '0009_recipe_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default=0, upload_to='images/'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='recipe_image',
        ),
    ]
