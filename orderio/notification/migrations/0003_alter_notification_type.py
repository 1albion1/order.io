# Generated by Django 4.0 on 2022-01-13 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_notification_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.IntegerField(blank=True, choices=[(0, 'danger'), (1, 'success'), (2, 'warning'), (3, 'info')], default=3, null=True),
        ),
    ]
