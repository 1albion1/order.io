# Generated by Django 4.0 on 2022-01-12 22:13

from django.db import migrations, models
import main.images_rename


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0005_alter_meal_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='meal_img',
            field=models.ImageField(default='meal-default.png', null=True, upload_to=main.images_rename.path_and_rename('')),
        ),
    ]
