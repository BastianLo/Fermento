# Generated by Django 4.2 on 2023-04-14 08:40

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_manager', '0035_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=image_cropping.fields.ImageCropField(default='../../../static/img/fermentation.png', upload_to='images/'),
        ),
    ]
