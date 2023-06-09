# Generated by Django 4.2 on 2023-04-08 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_manager', '0020_remove_recipe_ingredient_related_ingredient_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process_step',
            name='related_recipe',
        ),
        migrations.RemoveField(
            model_name='recipe_ingredient',
            name='related_recipe',
        ),
        migrations.CreateModel(
            name='process',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('related_recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe_manager.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='process_step',
            name='related_process',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='recipe_manager.process'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe_ingredient',
            name='related_process',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='recipe_manager.process'),
            preserve_default=False,
        ),
    ]
